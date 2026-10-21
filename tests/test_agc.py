import math
import os
from pathlib import Path
import tempfile
import wave
from array import array
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QByteArray, QEventLoop, QTimer
from PySide6.QtMultimedia import QAudioBuffer, QMediaPlayer, QtAudio
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from vbc_player.services.agc import BIAS, CEILING, DECAY, NUMERATOR, ZaraAGC, rms_dbfs
from vbc_player.services.processed_audio import ProcessedAudio
from vbc_player.pages.player.widgets.agc import AGCButton


class AGCTests(unittest.TestCase):
    def test_validation_and_silence(self):
        agc = ZaraAGC()
        for invalid in ([1], [0, 32768], [-32769, 0], [1.5, 0]):
            with self.assertRaises(ValueError):
                agc.process(invalid)
        self.assertEqual(agc.process([]), [])
        self.assertEqual(agc.process([0, 0] * 1025), [0, 0] * 1025)
        self.assertEqual(rms_dbfs([0, 0]), -math.inf)

    def test_independent_channel_energy_decay_and_truncation(self):
        agc = ZaraAGC()
        samples = [100, -300] * 1024
        gain_l = NUMERATOR / math.sqrt(1024 * 100 ** 2 + BIAS)
        gain_r = NUMERATOR / math.sqrt(1024 * 300 ** 2 + BIAS)
        self.assertEqual(agc.process(samples), [int(100 * gain_l), int(-300 * gain_r)] * 1024)
        agc.process([0, 0])
        self.assertEqual(agc.energy_left, DECAY * 1024 * 100 ** 2)
        self.assertEqual(agc.energy_right, DECAY * 1024 * 300 ** 2)
        self.assertEqual(samples, [100, -300] * 1024)
        agc.reset()
        self.assertEqual((agc.energy_left, agc.energy_right), (0, 0))

    def test_clipping_updates_memory_before_following_sample(self):
        agc = ZaraAGC()
        result = agc.process([32767, -32768, 1000, -1000])
        self.assertEqual(result[:2], [CEILING, -CEILING])
        self.assertEqual(agc.energy_left, 12000 * 32767 ** 2 - BIAS)
        self.assertEqual(agc.energy_right, 12000 * 32768 ** 2 - BIAS)
        self.assertEqual(result[2:], [int(1000 * NUMERATOR / math.sqrt(12000 * 32767 ** 2)),
                                      int(-1000 * NUMERATOR / math.sqrt(12000 * 32768 ** 2))])

    def test_block_boundaries_and_state_across_calls(self):
        samples = [1000, -7000] * 2400
        whole, split = ZaraAGC(), ZaraAGC()
        result = whole.process(samples)
        self.assertEqual(result, split.process(samples[:2048]) + split.process(samples[2048:4096]) + split.process(samples[4096:]))
        self.assertLessEqual(max(abs(x) for x in result), CEILING)
        # Fronteiras diferentes são deliberadamente diferentes no callback.
        other = ZaraAGC()
        self.assertNotEqual(result, other.process(samples[:100]) + other.process(samples[100:]))


class FakeSink:
    def __init__(self):
        self.written = bytearray()
        self.capacity = 65536

    def bytesFree(self):
        return self.capacity

    def setBufferSize(self, size):
        pass

    def setVolume(self, volume):
        pass

    def start(self):
        return self

    def error(self):
        return QtAudio.Error.NoError

    def state(self):
        return QtAudio.State.IdleState

    def write(self, data):
        # Escritas parciais também precisam preservar a sequência PCM.
        size = min(516, len(data))
        self.written.extend(data[:size])
        return size

    def reset(self):
        pass

    def deleteLater(self):
        pass


class AudioPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        from vbc_player.theme import ASSETS
        QFontDatabase.addApplicationFont(str(ASSETS / "fonts/Inter.ttf"))

    def setUp(self):
        self.player, self.output = MagicMock(), MagicMock()
        self.output.volume.return_value = 1.0
        self.player.playbackState.return_value = QMediaPlayer.PlaybackState.PlayingState
        self.output.device.return_value.isNull.return_value = False
        self.audio = ProcessedAudio(self.player, self.output)
        self.sink = FakeSink()
        self.audio.sink = self.audio.device = self.sink

    def tearDown(self):
        self.audio.reset()

    def feed(self, samples):
        self.audio.receive(QAudioBuffer(QByteArray(array("h", samples).tobytes()), self.audio.format))

    def flush(self):
        self.audio.receive(QAudioBuffer())
        while self.audio.pending:
            self.audio._write()

    def test_reblocking_tail_and_actual_sink_bytes(self):
        source = [1000, -2500] * 2301
        levels = []
        self.audio.levels_changed.connect(lambda *args: levels.append(args))
        offset = 0
        for frames in (128, 960, 200, 1013):
            self.feed(source[offset:offset + frames * 2])
            offset += frames * 2
        self.flush()
        expected = array("h", ZaraAGC().process(source)).tobytes()
        self.assertEqual(bytes(self.sink.written), expected)
        self.assertEqual(len(levels), 3)
        self.assertAlmostEqual(levels[0][0], rms_dbfs(source[:2048]))
        self.assertNotEqual(expected, array("h", source).tobytes())
        self.output.setMuted.assert_called_once_with(True)

    def test_bypass_is_bit_exact_and_reset_discards_pending_audio(self):
        self.audio.set_enabled(False)
        source = [-32768, 32767, 1, -1] * 1000
        self.feed(source)
        self.flush()
        self.assertEqual(bytes(self.sink.written), array("h", source).tobytes())
        self.feed([123, -456] * 128)
        self.audio.pending.extend(b"old audio")
        self.audio.reset()
        self.assertEqual(len(self.audio.samples), 0)
        self.assertEqual(self.audio.pending, b"")
        self.assertIsNone(self.audio.sink)

    def test_pause_does_not_write_and_master_volume_controls_sink(self):
        self.sink.setVolume = MagicMock()
        self.audio._volume_changed(.35)
        self.sink.setVolume.assert_called_once_with(.35)
        self.player.playbackState.return_value = QMediaPlayer.PlaybackState.PausedState
        self.audio.pending.extend(b"queued")
        self.audio._write()
        self.assertEqual(self.sink.written, b"")
        self.assertEqual(self.audio.pending, b"queued")

    def test_stereo_meters_measure_channels_after_processing_and_master(self):
        readings = []
        self.audio.stereo_levels_changed.connect(lambda *levels: readings.append(levels))
        self.audio.set_enabled(False)
        self.feed([16384, 8192] * 1024)
        left, right = readings[-1]
        self.assertAlmostEqual(left, -6.020599913)
        self.assertAlmostEqual(right, -12.041199826)
        self.audio._volume_changed(.5)
        self.assertAlmostEqual(readings[-1][0], left - 6.020599913)
        self.assertAlmostEqual(readings[-1][1], right - 6.020599913)
        self.audio._volume_changed(0)
        self.assertEqual(readings[-1], (-math.inf, -math.inf))
        self.audio.set_enabled(True)
        source = [100, 300] * 1024
        expected = ZaraAGC().process(source)
        self.feed(source)
        self.assertAlmostEqual(readings[-1][0], rms_dbfs(expected[::2]))
        self.assertAlmostEqual(readings[-1][1], rms_dbfs(expected[1::2]))
        self.sink.suspend = MagicMock()
        self.audio._state_changed(QMediaPlayer.PlaybackState.PausedState)
        self.assertEqual(readings[-1], (-math.inf, -math.inf))
        self.audio._volume_changed(1)
        self.assertEqual(readings[-1], (-math.inf, -math.inf))
        self.audio.reset()
        self.assertEqual(readings[-1], (-math.inf, -math.inf))

    def test_figma_panel_toggle_close_and_svg_assets(self):
        button = AGCButton(self.audio)
        button.resize(178, 60)
        button.open_panel()
        self.app.processEvents()
        self.assertTrue(button.panel.isVisible())
        self.assertEqual(button.panel.size().toTuple(), (364, 437))
        button.panel.toggle.click()
        self.assertFalse(self.audio.enabled)
        self.assertEqual(button.panel.toggle.accessibleName(), "Ligar AGC")
        button.panel.toggle.click()
        self.assertTrue(self.audio.enabled)
        from PySide6.QtSvg import QSvgRenderer
        from vbc_player.theme import ASSETS
        for path in (ASSETS / "figma/agc").glob("*.svg"):
            self.assertGreater(path.stat().st_size, 0)
            self.assertTrue(QSvgRenderer(str(path)).isValid(), str(path))
        button.panel.close_button.click()
        self.assertFalse(button.panel.isVisible())
        button.deleteLater()

    def test_real_decoder_routes_processed_pcm_to_sink(self):
        from vbc_player.services.playback import PlaybackService
        service = PlaybackService()
        service.automatic = False
        decoded = array("h")
        errors = []
        service.error.connect(errors.append)
        service.audio.buffer_output.audioBufferReceived.connect(
            lambda buffer: decoded.frombytes(bytes(buffer.constData())) if buffer.isValid() else None)
        sink = FakeSink()
        device = MagicMock()
        device.isNull.return_value = False
        device.isFormatSupported.return_value = True
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tone.wav"
            with wave.open(str(path), "wb") as file:
                file.setnchannels(1)
                file.setsampwidth(2)
                file.setframerate(8000)
                file.writeframes(array("h", [int(1200 * math.sin(i * .2)) for i in range(2400)]).tobytes())
            with patch.object(service.output, "device", return_value=device), patch(
                    "vbc_player.services.processed_audio.QAudioSink", return_value=sink):
                service.add_tracks([str(path)])
                service.play_index(0)
                for _ in range(150):
                    loop = QEventLoop()
                    QTimer.singleShot(10, loop.quit)
                    loop.exec()
                    if service.player.mediaStatus() == QMediaPlayer.MediaStatus.EndOfMedia and service.audio.sink is None:
                        break
                self.assertEqual(errors, [])
                self.assertGreater(len(decoded), 2000)
                self.assertEqual(bytes(sink.written), array("h", ZaraAGC().process(decoded.tolist())).tobytes())
                self.assertNotEqual(sink.written, decoded.tobytes())
                service.player.stop()
        service.deleteLater()

    def test_transport_stop_and_seek_flush_dsp_and_pending_output(self):
        from vbc_player.services.playback import PlaybackService
        service = PlaybackService()
        for action in (service.player.stop, lambda: service.player.setPosition(1000)):
            service.audio.samples.extend([100, -100])
            service.audio.pending.extend(b"queued")
            service.audio.agc.process([500, -500])
            action()
            self.assertEqual(service.audio.pending, b"")
            self.assertEqual(len(service.audio.samples), 0)
            self.assertEqual(service.audio.agc.energy_left, 0)
        service.deleteLater()


if __name__ == "__main__":
    unittest.main()
