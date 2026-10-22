from datetime import datetime, timedelta

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QProgressBar, QSlider

from vbc_player.common.widgets.design_panel import DesignPanel


def timecode(ms):
    ms = max(0, ms)
    return f"{ms//60000:02d}:{ms//1000%60:02d}.{ms//100%10}"


class RoundedProgressBar(QProgressBar):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bounds = QRectF(self.rect())
        radius = bounds.height() / 2

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#26344a"))
        painter.drawRoundedRect(bounds, radius, radius)

        span = self.maximum() - self.minimum()
        ratio = (self.value() - self.minimum()) / span if span else 0
        fill_width = bounds.width() * max(0.0, min(1.0, ratio))
        if fill_width > 0:
            fill = QRectF(bounds.left(), bounds.top(), fill_width, bounds.height())
            fill_radius = min(radius, fill_width / 2)
            painter.setBrush(QColor("#f97316"))
            painter.drawRoundedRect(fill, fill_radius, fill_radius)


class DeckWidget(DesignPanel):
    def __init__(self, service, on_air=True, parent=None):
        super().__init__("24:4" if on_air else "24:5", parent)
        self.service = service
        self.on_air = on_air
        service.track_changed.connect(self._track_changed)
        service.queue_changed.connect(self._queue_changed)
        if on_air:
            self.nodes["17:421"]["b"][2] = self.design_width - self.local_rect("17:421").x() - 18
            service.player.positionChanged.connect(self._position_changed)
            service.player.playbackStateChanged.connect(self._state_changed)
            self.progress = RoundedProgressBar(self)
            self.progress.setRange(0, 1000)
            self.progress.setTextVisible(False)
            self.add_control(self.progress, self.local_rect("17:428"))
            self.progress.hide()
            self.seek = QSlider(Qt.Orientation.Horizontal)
            self.seek.setRange(0, 1000)
            self.seek.setAccessibleName("Posição do áudio")
            self.seek.setStyleSheet("""
                QSlider { background: transparent; }
                QSlider::groove:horizontal {
                    height: 8px;
                    background: transparent;
                }
                QSlider::sub-page:horizontal,
                QSlider::add-page:horizontal {
                    background: transparent;
                    border: 0;
                }
                QSlider::handle:horizontal {
                    width: 0;
                    background: transparent;
                    border: 0;
                }
            """)
            self.seek.sliderReleased.connect(lambda: service.player.setPosition(round(service.player.duration()*self.seek.value()/1000)))
            self.add_control(self.seek, self.local_rect("17:428").adjusted(0, -8, 0, 8))
        self._queue_changed()

    def _track_changed(self, track):
        if self.on_air:
            self.set_text("17:422", track.title)
            self.nodes["17:422"]["b"][2] = 356
            self.set_text("17:423", f"{track.kind} • Arquivo local")
        self._queue_changed()

    def _queue_changed(self):
        if self.on_air:
            if self.service.index < 0:
                self.set_text("17:422", "Nenhum áudio selecionado")
                self.nodes["17:422"]["b"][2] = 356
                self.set_text("17:423", "Adicione arquivos à lista de reprodução")
                self.set_text("17:427", "—")
                self.set_text("17:421", "PLAYER — PRONTO")
                self._position_changed(0)
        else:
            i = self.service.index + 1
            next_track = self.service.tracks[i] if i < len(self.service.tracks) else None
            self.set_text("17:436", next_track.title if next_track else "Fim da lista")
            self.nodes["17:436"]["b"][2] = 356
            self.set_text("17:437", f"{next_track.kind} • Arquivo local" if next_track else "Adicione mais arquivos")
            self.set_text("29:39", timecode(next_track.duration_ms) if next_track else "00:00.0")
            self.set_text("17:441", "—")
            self.set_text("17:443", "PRONTO" if next_track else "FIM")

    def _position_changed(self, position):
        duration = self.service.player.duration()
        remaining = max(0, duration-position)
        for node in ("17:425", "29:25", "29:35"):
            self.set_text(node, timecode(remaining))
        self.set_text("17:427", (datetime.now()+timedelta(milliseconds=remaining)).strftime("%H:%M:%S") if duration else "—")
        percent = position/duration if duration else 0
        self.set_text("17:430", f"Progresso {percent:.0%}")
        self.hidden.update({"17:428", "17:429"})
        self.progress.show()
        self.progress.setValue(round(percent*1000))

    def _state_changed(self, state):
        text = {
            QMediaPlayer.PlaybackState.PlayingState: "NO AR — TOCANDO AGORA",
            QMediaPlayer.PlaybackState.PausedState: "PLAYER — PAUSADO",
            QMediaPlayer.PlaybackState.StoppedState: "PLAYER — PARADO",
        }[state]
        self.set_text("17:421", text)
