from pathlib import Path

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from vbc_player.models import Track, demo_tracks
import random


class PlaybackService(QObject):
    """Uma saída de áudio compartilhada pelas páginas."""

    track_changed = Signal(object)
    queue_changed = Signal()
    played = Signal(str)
    mode_changed = Signal()
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.output = QAudioOutput(self)
        self.output.setVolume(0.714)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.output)
        self.tracks = demo_tracks()
        self.demo = True
        self.index = -1
        self.automatic = True
        self.loop = False
        self.shuffle = False
        self.player.mediaStatusChanged.connect(self._media_status)
        self.player.durationChanged.connect(self._duration_changed)
        self.player.errorOccurred.connect(
            lambda _error, message: self.error.emit(message)
        )

    def add_tracks(self, paths):
        valid = [str(Path(path).resolve()) for path in paths if Path(path).is_file()]
        if not valid:
            return
        if self.demo:
            self.tracks = []
            self.demo = False
        existing = {track.path for track in self.tracks}
        for path in valid:
            if path not in existing:
                self.tracks.append(Track.from_path(path))
                existing.add(path)
        self.queue_changed.emit()

    def play_index(self, index):
        if not 0 <= index < len(self.tracks):
            return
        track = self.tracks[index]
        if not track.path:
            self.error.emit("A lista de referência não inclui áudio. Use Adicionar para escolher seus arquivos.")
            return
        if not Path(track.path).is_file():
            self.error.emit(f"Arquivo não encontrado: {track.path}")
            return
        self.player.stop()
        self.index = index
        for i, item in enumerate(self.tracks):
            item.status = "NO AR" if i == index else "PRÓXIMO" if i == index+1 else "AGUARDA"
        self.player.setSource(QUrl.fromLocalFile(track.path))
        self.track_changed.emit(track)
        self.queue_changed.emit()
        self.player.play()
        self.played.emit(track.title)

    def play(self):
        if self.player.source().isEmpty():
            self.play_index(0)
        else:
            self.player.play()

    def toggle(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.play()

    def next(self):
        if not self.tracks or self.demo:
            return
        if self.shuffle and len(self.tracks) > 1:
            index = random.choice([i for i in range(len(self.tracks)) if i != self.index])
        else:
            index = self.index + 1
            if index >= len(self.tracks):
                if not self.loop:
                    self.player.stop()
                    return
                index = 0
        self.play_index(index)

    def remove(self, index):
        if not 0 <= index < len(self.tracks):
            return
        if index == self.index:
            self.player.stop()
            self.player.setSource(QUrl())
            self.index = -1
        elif index < self.index:
            self.index -= 1
        del self.tracks[index]
        self.queue_changed.emit()

    def clear(self):
        self.player.stop()
        self.player.setSource(QUrl())
        self.index = -1
        self.demo = False
        self.tracks.clear()
        self.queue_changed.emit()

    def _duration_changed(self, duration):
        if 0 <= self.index < len(self.tracks) and duration:
            self.tracks[self.index].duration_ms = duration
            self.queue_changed.emit()

    def _media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self.automatic:
            self.next()
