import math

from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QSlider

from vbc_player.common.widgets.design_panel import DesignPanel
from vbc_player.pages.player.widgets.agc import AGCButton


class TransportWidget(DesignPanel):
    def __init__(self, service, parent=None):
        super().__init__("24:10", parent)
        self.service = service
        self.play = self.button("Play", self.local_rect("52:228"), service.play)
        self.stop = self.button("Stop", self.local_rect("52:234"), service.player.stop)
        self.pause = self.button("Pausa", self.local_rect("52:239"), service.player.pause)
        self.next_button = self.button("Próximo", self.local_rect("52:245"), service.next)
        self.transport_buttons = (
            (self.play, "52:228"), (self.stop, "52:234"),
            (self.pause, "52:239"), (self.next_button, "52:245"),
        )
        service.queue_changed.connect(self._update_transport)
        self._update_transport()
        self.hidden.add("47:829")
        self.agc = self.add_control(AGCButton(service.audio), self.local_rect("47:829"))
        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(71)
        self.volume.setAccessibleName("Volume master")
        self.volume.setStyleSheet("QSlider {background:transparent;}")
        self.hidden.update({"17:604", "17:605", "17:606"})
        self.add_control(self.volume, QRectF(642, 36, 300, 38))
        self.volume.valueChanged.connect(self._volume_changed)

    def _update_transport(self):
        enabled = bool(self.service.tracks)
        for button, node_id in self.transport_buttons:
            button.setEnabled(enabled)
            button.setCursor(Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor)
            self.nodes[node_id]["o"] = 1.0 if enabled else .35
        self.update()

    def _volume_changed(self, value):
        self.service.output.setVolume(value/100)
        db = 20*math.log10(value/100) if value else None
        self.set_text("17:607", f"{db:.1f} dB" if db is not None else "Mudo")
