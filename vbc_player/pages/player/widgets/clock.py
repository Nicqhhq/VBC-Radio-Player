from datetime import datetime

from PySide6.QtCore import QTimer
from vbc_player.common.widgets.design_panel import DesignPanel


class StudioClockWidget(DesignPanel):
    def __init__(self, parent=None):
        super().__init__("24:6", parent)
        # Arial has different metrics on Windows and the original 177 px box
        # elides the final digits. Use the bundled font and all available card
        # width so HH:MM:SS is rendered consistently on every platform.
        clock = self.nodes["17:447"]
        clock["f"] = "Inter"
        clock["b"][2] = self.design_width - (clock["b"][0] - self.origin_x) - 12
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)
        self._tick()
        self.setToolTip("Relógio local do computador. Medidores de referência do design.")

    def _tick(self):
        now = datetime.now()
        weekdays = ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo")
        months = ("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")
        self.set_text("17:447", now.strftime("%H:%M:%S"))
        self.set_text("17:448", f"{weekdays[now.weekday()]}, {now.day} de {months[now.month-1]}")
        self.nodes["17:448"]["b"][2] = 200
