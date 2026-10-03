import math

from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QMessageBox, QSlider

from vbc_player.common.widgets.design_panel import DesignPanel


class TransportWidget(DesignPanel):
    def __init__(self, service, parent=None):
        super().__init__("24:10", parent)
        self.service = service
        self.play = self.button("Play", self.local_rect("52:228"), service.play)
        self.stop = self.button("Stop", self.local_rect("52:234"), service.player.stop)
        self.pause = self.button("Pausa", self.local_rect("52:239"), service.player.pause)
        self.next_button = self.button("Próximo", self.local_rect("52:245"), service.next)
        self.agc = self.button("Abrir monitoramento AGC", self.local_rect("47:829"), self._agc_info)
        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(71)
        self.volume.setAccessibleName("Volume master")
        self.volume.setStyleSheet("QSlider {background:transparent;}")
        self.hidden.update({"17:604", "17:605", "17:606"})
        self.add_control(self.volume, QRectF(642, 36, 300, 38))
        self.volume.valueChanged.connect(self._volume_changed)

    def _volume_changed(self, value):
        self.service.output.setVolume(value/100)
        db = 20*math.log10(value/100) if value else None
        self.set_text("17:607", f"{db:.1f} dB" if db is not None else "Mudo")

    def _agc_info(self):
        QMessageBox.information(self, "Controle automático de ganho",
            "O botão AGC e as leituras dos medidores reproduzem a referência visual do Figma. "
            "O processamento de ganho automático ainda não está implementado.")
