from datetime import datetime
import math
from time import monotonic

from PySide6.QtCore import QRectF, QTimer
from PySide6.QtGui import QColor, QPainter
from vbc_player.common.widgets.design_panel import DesignPanel


class StudioClockWidget(DesignPanel):
    def __init__(self, service, parent=None):
        super().__init__("24:6", parent)
        self.service = service
        # Mantém os trilhos do Figma e substitui as barras demonstrativas.
        self.hidden.update({"17:452", "17:453", "17:456", "17:457"})
        self.meter_levels = [-60.0, -60.0]
        self._targets = [-60.0, -60.0]
        self._last_sample_time = self._last_animation_time = monotonic()
        self.meter_timer = QTimer(self)
        self.meter_timer.setInterval(33)
        self.meter_timer.timeout.connect(self._animate_meters)
        self.meter_timer.start()
        service.audio.stereo_levels_changed.connect(self._set_levels)
        service.output.volumeChanged.connect(self._set_master_volume)
        self.nodes["17:458"]["b"][2] = 196
        self._set_master_volume(service.output.volume())
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

    def _set_master_volume(self, volume):
        value = f"{20 * math.log10(volume):.1f} dB" if volume > 0 else "MUDO"
        self.set_text("17:458", f"MASTER {value}")

    def _set_levels(self, left, right):
        self._targets = [max(-60.0, min(0.0, level)) for level in (left, right)]
        self._last_sample_time = monotonic()

    def _animate_meters(self):
        now = monotonic()
        elapsed = max(0.0, now - self._last_animation_time)
        self._last_animation_time = now
        # Evita leituras congeladas se o decodificador parar de entregar áudio.
        if now - self._last_sample_time > .25:
            self._targets = [-60.0, -60.0]
        for channel, target in enumerate(self._targets):
            current = self.meter_levels[channel]
            time_constant = .035 if target > current else .18
            value = target + (current - target) * math.exp(-elapsed / time_constant)
            self.meter_levels[channel] = target if abs(value - target) < .05 else value
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.scale(self.width() / self.design_width, self.height() / self.design_height)
        for node_id, level in zip(("17:451", "17:455"), self.meter_levels):
            track = self.local_rect(node_id)
            # Verde até −12 dBFS, amarelo até −3 dBFS, vermelho até 0.
            for low, high, color in ((-60, -12, "#22c55e"), (-12, -3, "#f59e0b"), (-3, 0, "#ef4444")):
                end = min(level, high)
                if end > low:
                    left = track.x() + track.width() * (low + 60) / 60
                    width = track.width() * (end - low) / 60
                    painter.fillRect(QRectF(left, track.y(), width, track.height()), QColor(color))
        painter.end()

    def _tick(self):
        now = datetime.now()
        weekdays = ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo")
        months = ("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")
        self.set_text("17:447", now.strftime("%H:%M:%S"))
        self.set_text("17:448", f"{weekdays[now.weekday()]}, {now.day} de {months[now.month-1]}")
        self.nodes["17:448"]["b"][2] = 200
