"""PCM16 estéreo → AGC → saída real; QMediaPlayer mantém transporte/codecs.

O buffer do Qt é reagrupado em 1024 frames, com bloco curto só no fim.
O áudio nativo fica mudo para não duplicar o sinal processado.
"""
from array import array
import math

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtMultimedia import QAudioBufferOutput, QAudioFormat, QAudioSink, QMediaPlayer, QtAudio

from vbc_player.services.agc import BLOCK_FRAMES, ZaraAGC, rms_dbfs


class ProcessingPlayer(QMediaPlayer):
    discontinuity = Signal()

    def stop(self):
        super().stop()
        self.discontinuity.emit()

    def setPosition(self, position):
        self.discontinuity.emit()
        super().setPosition(position)


class ProcessedAudio(QObject):
    levels_changed = Signal(float, float, float)
    stereo_levels_changed = Signal(float, float)
    enabled_changed = Signal(bool)
    error = Signal(str)

    def __init__(self, player, output, parent=None):
        super().__init__(parent)
        self.player, self.output = player, output
        self.enabled = True
        self._channel_levels = (-math.inf, -math.inf)
        self.agc = ZaraAGC()
        self.samples = array("h")
        self.pending = bytearray()
        self.sink = None
        self.device = None
        self.format = QAudioFormat()
        self.format.setSampleRate(44100)
        self.format.setChannelCount(2)
        self.format.setSampleFormat(QAudioFormat.SampleFormat.Int16)
        self.buffer_output = QAudioBufferOutput(self.format, self)
        player.setAudioBufferOutput(self.buffer_output)
        output.setMuted(True)
        self.buffer_output.audioBufferReceived.connect(self.receive)
        player.discontinuity.connect(self.reset)
        player.sourceChanged.connect(self.reset)
        player.playbackStateChanged.connect(self._state_changed)
        output.volumeChanged.connect(self._volume_changed)
        output.deviceChanged.connect(self.reset)
        self.timer = QTimer(self)
        self.timer.setInterval(5)
        self.timer.timeout.connect(self._write)

    def set_enabled(self, enabled):
        enabled = bool(enabled)
        if enabled != self.enabled:
            self.enabled = enabled
            self.agc.reset()
            self.enabled_changed.emit(enabled)

    def reset(self, *_):
        self.timer.stop()
        if self.sink:
            self.sink.reset()
            self.sink.deleteLater()
        self.sink = self.device = None
        self.samples = array("h")
        self.pending.clear()
        self.agc.reset()
        self.levels_changed.emit(-math.inf, -math.inf, 0.0)
        self._clear_stereo_levels()

    def _start_sink(self):
        device = self.output.device()
        if not device.isFormatSupported(self.format):
            self.error.emit("A saída de áudio não aceita PCM16 estéreo a 44,1 kHz.")
            self.player.stop()
            return False
        self.sink = QAudioSink(device, self.format, self)
        self.sink.setBufferSize(32768)
        self.sink.setVolume(self.output.volume())
        self.device = self.sink.start()
        if self.device is None:
            self.error.emit("Não foi possível abrir a saída de áudio do AGC.")
            self.player.stop()
            return False
        self.timer.start()
        return True

    def receive(self, buffer):
        if buffer.isValid():
            if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
                return
            if buffer.format() != self.format:
                self.error.emit("O decodificador não entregou o formato PCM16 estéreo solicitado.")
                self.player.stop()
                return
            self.samples.frombytes(bytes(buffer.constData()))
        count = BLOCK_FRAMES * 2
        while len(self.samples) >= count or (not buffer.isValid() and self.samples):
            block = self.samples[:count].tolist()
            del self.samples[:count]
            result = self.agc.process(block) if self.enabled else block
            # Sem dispositivo (inclui CI/headless), mantém DSP/medição sem
            # acumular áudio que nunca poderia ser reproduzido.
            if not self.output.device().isNull():
                self.pending.extend(array("h", result).tobytes())
            before, after = rms_dbfs(block), rms_dbfs(result)
            gain = after - before if math.isfinite(before) and math.isfinite(after) else 0.0
            self.levels_changed.emit(before, after, gain)
            self._channel_levels = (rms_dbfs(result[::2]), rms_dbfs(result[1::2]))
            self._emit_stereo_levels()
        if self.pending and (self.sink or self._start_sink()):
            self._write()

    def _write(self):
        if not self.sink or self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState:
            return
        if self.sink.error() != QtAudio.Error.NoError and self.sink.error() != QtAudio.Error.UnderrunError:
            self.error.emit("A saída de áudio foi interrompida.")
            self.player.stop()
            return
        size = min(self.sink.bytesFree(), len(self.pending))
        if size:
            written = self.device.write(bytes(self.pending[:size]))
            if written > 0:
                del self.pending[:written]

    def drained(self):
        return not self.pending and (not self.sink or self.sink.state() == QtAudio.State.IdleState)

    def _volume_changed(self, volume):
        if self.sink:
            self.sink.setVolume(volume)
        self._emit_stereo_levels(volume)

    def _emit_stereo_levels(self, volume=None):
        volume = self.output.volume() if volume is None else volume
        attenuation = 20 * math.log10(volume) if volume > 0 else -math.inf
        self.stereo_levels_changed.emit(*(level + attenuation for level in self._channel_levels))

    def _clear_stereo_levels(self):
        self._channel_levels = (-math.inf, -math.inf)
        self.stereo_levels_changed.emit(*self._channel_levels)

    def _state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PausedState:
            self._clear_stereo_levels()
        if self.sink:
            if state == QMediaPlayer.PlaybackState.PausedState:
                self.sink.suspend()
            elif state == QMediaPlayer.PlaybackState.PlayingState:
                self.sink.resume()
