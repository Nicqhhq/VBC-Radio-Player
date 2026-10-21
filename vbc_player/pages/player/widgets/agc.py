import math

from PySide6.QtCore import QPoint, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QDialog, QPushButton

from vbc_player.theme import ASSETS

GREEN, MUTED, TEXT = "#4ce0ae", "#91a2b9", "#f4f7fc"


def text(painter, value, x, y, width, height, size=12, color=TEXT, weight=400, right=False):
    font = QFont("Inter")
    font.setPixelSize(size)
    font.setWeight(QFont.Weight(weight))
    painter.setFont(font)
    painter.setPen(QColor(color))
    painter.drawText(QRectF(x, y, width, height), Qt.AlignmentFlag.AlignVCenter |
                     (Qt.AlignmentFlag.AlignRight if right else Qt.AlignmentFlag.AlignLeft), value)


class SvgButton(QPushButton):
    def __init__(self, label, parent, rect, asset, callback):
        super().__init__(parent)
        self.setGeometry(*rect)
        self.setAccessibleName(label)
        self.setToolTip(label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setStyleSheet("QPushButton {background:transparent;border:none;padding:0;}")
        self._keyboard_focus = False
        self.asset = asset
        self.clicked.connect(callback)

    def paintEvent(self, event):
        painter = QPainter(self)
        QSvgRenderer(str(ASSETS / "figma" / "agc" / self.asset)).render(painter)
        if self.hasFocus() and self._keyboard_focus:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor("#5aa5ff"), 1.5))
            radius = self.height() / 2 if self.isCheckable() else 4
            painter.drawRoundedRect(QRectF(self.rect()).adjusted(.75, .75, -.75, -.75), radius, radius)

    def focusInEvent(self, event):
        self._keyboard_focus = event.reason() in (
            Qt.FocusReason.TabFocusReason, Qt.FocusReason.BacktabFocusReason,
            Qt.FocusReason.ShortcutFocusReason,
        )
        super().focusInEvent(event)
        self.update()

    def mousePressEvent(self, event):
        self._keyboard_focus = False
        super().mousePressEvent(event)
        self.update()


class AGCPanel(QDialog):
    def __init__(self, audio, parent=None):
        super().__init__(parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.audio = audio
        self.setWindowTitle("Controle automático de ganho")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(364, 437)
        self.levels = (-math.inf, -math.inf, 0.0)
        self.close_button = SvgButton("Fechar painel", self, (319, 33, 18, 18), "close.svg", self.close)
        self.toggle = SvgButton("Desligar AGC", self, (303, 79, 40, 24), "switch-on.svg",
                                lambda: audio.set_enabled(not audio.enabled))
        self.toggle.setCheckable(True)
        audio.enabled_changed.connect(self._state_changed)
        audio.levels_changed.connect(self._levels_changed)
        # Repinta no máximo 20 vezes/s, mesmo que o DSP emita mais blocos.
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update)
        self._state_changed(audio.enabled)

    def showEvent(self, event):
        self.timer.start()
        super().showEvent(event)

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)

    def _state_changed(self, enabled):
        self.toggle.asset = "switch-on.svg" if enabled else "switch-off.svg"
        self.toggle.setChecked(enabled)
        label = "Desligar AGC" if enabled else "Ligar AGC"
        self.toggle.setAccessibleName(label)
        self.toggle.setToolTip(label)
        self.toggle.update()
        self.update()

    def _levels_changed(self, before, after, gain):
        self.levels = (before, after, gain)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor("#101827"))
        p.setPen(QPen(QColor("#2b3b52"), 1))
        p.drawRoundedRect(QRectF(.5, .5, 363, 436), 12, 12)
        text(p, "Controle automático de ganho", 21, 20, 294, 23, 16, weight=600)
        text(p, "Volume consistente, faixa a faixa.", 21, 45, 294, 17, color=MUTED)
        enabled = self.audio.enabled
        accent = GREEN if enabled else MUTED
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#113a32" if enabled else "#182335"))
        p.drawRoundedRect(QRectF(21, 78, 94 if enabled else 113, 27), 6, 6)
        QSvgRenderer(str(ASSETS / "figma/agc" / ("dot-on.svg" if enabled else "dot-off.svg"))).render(p, QRectF(31, 88, 6, 6))
        text(p, "AGC ligado" if enabled else "AGC desligado", 45, 84, 83, 15, 11, accent, 600)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#182335"))
        p.drawRoundedRect(QRectF(21, 121, 322, 164), 10, 10)
        text(p, "NÍVEIS DE ÁUDIO", 35, 135, 145, 16, 11, MUTED, 500)
        text(p, "● Monitorando" if enabled else "● Bypass", 210, 135, 119, 16, 11, accent, 500, True)
        before, after, gain = self.levels
        for label, level, y, color in [("Entrada", before, 165, "#5aa5ff"), ("Saída", after, 211, GREEN if enabled else "#5aa5ff")]:
            text(p, label, 35, y, 100, 17)
            text(p, f"{level:.1f} dBFS" if math.isfinite(level) else "−∞ dBFS", 204, y, 125, 17, 11, MUTED, 500, True)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor("#273449"))
            p.drawRoundedRect(QRectF(35, y + 23, 294, 8), 4, 4)
            width = 294 * max(0, min(1, (level + 60) / 60))
            if width > 0:
                p.setBrush(QColor(color))
                p.drawRoundedRect(QRectF(35, y + 23, width, 8), 4, 4)
        for value, x, width in [("−60",35,30),("−30",101,30),("−18",168,30),("−6",235,25),("0 dBFS",289,40)]:
            text(p, value, x, 257, width, 16, 11, MUTED, 500)
        text(p, "Ajuste de ganho", 21, 301, 180, 17)
        text(p, "Compensando o volume de entrada" if enabled else "Sinal original, sem ajuste", 21, 320, 228, 16, 11, MUTED, 500)
        text(p, f"{gain:+.1f} dB" if enabled else "0.0 dB", 247, 302, 96, 31, 22, accent, 600, True)
        text(p, "Teto de saída", 21, 351, 160, 17, color=MUTED)
        text(p, "−1.3 dBFS", 230, 351, 113, 17, 11, weight=600, right=True)
        p.setPen(QPen(QColor("#2b3b52"), 1))
        p.drawLine(21, 384, 343, 384)
        text(p, "Áudio real • níveis antes do volume master", 21, 401, 322, 17, 11, MUTED, 500)


class AGCButton(QPushButton):
    def __init__(self, audio, parent=None):
        super().__init__(parent)
        self.audio = audio
        self.panel = AGCPanel(audio, self)
        self.setAccessibleName("Abrir monitoramento AGC")
        self.setToolTip("Abrir monitoramento AGC")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.open_panel)
        audio.enabled_changed.connect(lambda _: self.update())

    def open_panel(self):
        point = self.mapToGlobal(QPoint(self.width() - 364, -445))
        screen = self.screen().availableGeometry()
        point.setX(max(screen.left(), min(point.x(), screen.right() - 363)))
        point.setY(max(screen.top(), min(point.y(), screen.bottom() - 436)))
        self.panel.move(point)
        self.panel.show()
        self.panel.toggle.setFocus()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.scale(self.width() / 178, self.height() / 60)
        enabled = self.audio.enabled
        p.setBrush(QColor("#113a32" if enabled else "#182335"))
        p.setPen(QPen(QColor(GREEN if enabled else "#2b3b52"), 1))
        p.drawRoundedRect(QRectF(.5, .5, 177, 59), 12, 12)
        left = 32.5 if enabled else 23.5
        path = ASSETS / "figma/191cb.svg" if enabled else ASSETS / "figma/agc/levels-off.svg"
        QSvgRenderer(str(path)).render(p, QRectF(left, 18, 24, 24))
        text(p, "AGC", left + 43, 11, 40, 22, 16, weight=600)
        dot = ASSETS / "figma/61d97.svg" if enabled else ASSETS / "figma/agc/button-dot-off.svg"
        QSvgRenderer(str(dot)).render(p, QRectF(left + 36, 39, 5, 5))
        text(p, "Ligado" if enabled else "Desligado", left + 49, 34, 60, 15, 11, GREEN if enabled else MUTED, 600)
        QSvgRenderer(str(ASSETS / "figma/0b259.svg")).render(p, QRectF(129.5 if enabled else 138.5, 22, 16, 16))
        if self.hasFocus() or self.underMouse():
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor("#5aa5ff"), 1))
            p.drawRoundedRect(QRectF(1, 1, 176, 58), 12, 12)
