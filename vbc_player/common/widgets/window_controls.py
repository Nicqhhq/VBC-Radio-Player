"""Controles da janela: semáforo macOS e botões Windows/Linux."""
import sys

from PySide6.QtCore import QEvent, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QAbstractButton, QHBoxLayout, QWidget


class WindowControlButton(QAbstractButton):
    def __init__(self, action, controls):
        super().__init__(controls)
        self.action = action
        self.controls = controls
        self._keyboard_focus = False
        self.setFixedSize(28 if controls.mac_style else 46, 48)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

    def enterEvent(self, event):
        self.controls.update_buttons()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.controls.update_buttons()
        super().leaveEvent(event)

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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.controls.mac_style:
            self._paint_mac(painter)
        else:
            self._paint_windows(painter)

    def _paint_mac(self, painter):
        color = {"close": "#ff5f57", "minimize": "#febc2e", "maximize": "#28c840"}[self.action]
        painter.setPen(QPen(QColor(color).darker(115), .6))
        painter.setBrush(QColor(color).darker(120) if self.isDown() else QColor(color))
        center = QPointF(self.width() / 2, self.height() / 2)
        painter.drawEllipse(center, 6, 6)
        if self.controls.underMouse() or self.underMouse() or (self.hasFocus() and self._keyboard_focus):
            painter.save()
            painter.translate(center)
            painter.setPen(QPen(QColor("#55201d" if self.action == "close" else "#4b421c" if self.action == "minimize" else "#155624"), 1.15))
            if self.action == "close":
                painter.drawLine(QPointF(-2.5, -2.5), QPointF(2.5, 2.5))
                painter.drawLine(QPointF(-2.5, 2.5), QPointF(2.5, -2.5))
            elif self.action == "minimize":
                painter.drawLine(QPointF(-3, 0), QPointF(3, 0))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor("#155624"))
                # Duas setas diagonais, como o controle de tela cheia do Mac.
                for points in (((-3, -3), (1, -3), (-3, 1)), ((3, 3), (-1, 3), (3, -1))):
                    painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in points]))
            painter.restore()
        if self.hasFocus() and self._keyboard_focus:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor("#70b8ff"), 1))
            painter.drawEllipse(center, 9, 9)

    def _paint_windows(self, painter):
        if self.underMouse() or self.isDown():
            color = "#c42b1c" if self.action == "close" else "#ffffff"
            background = QColor(color)
            if self.action != "close":
                background.setAlpha(40 if self.isDown() else 22)
            elif self.isDown():
                background = background.darker(120)
            painter.fillRect(self.rect(), background)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(QPen(QColor("#f4f7fc"), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if self.action == "minimize":
            painter.drawLine(QPointF(-5, .5), QPointF(5, .5))
        elif self.action == "close":
            painter.drawLine(QPointF(-5, -5), QPointF(5, 5))
            painter.drawLine(QPointF(-5, 5), QPointF(5, -5))
        elif self.controls.window.isMaximized() or self.controls.window.isFullScreen():
            painter.drawPolyline(QPolygonF([QPointF(-2.5, -3.5), QPointF(-2.5, -5.5), QPointF(5.5, -5.5), QPointF(5.5, 2.5), QPointF(3.5, 2.5)]))
            painter.drawRect(QRectF(-5.5, -2.5, 8, 8))
        else:
            painter.drawRect(QRectF(-4.5, -4.5, 9, 9))
        if self.hasFocus() and self._keyboard_focus:
            painter.setPen(QPen(QColor("#70b8ff"), 1))
            painter.drawRect(QRectF(-self.width() / 2 + 3, -self.height() / 2 + 3, self.width() - 6, self.height() - 6))


class WindowControls(QWidget):
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.window = window
        self.mac_style = sys.platform == "darwin"
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4 if self.mac_style else 0, 0, 12 if self.mac_style else 0, 0)
        layout.setSpacing(0)
        self.buttons = {}
        for action in (("close", "minimize", "maximize") if self.mac_style else ("minimize", "maximize", "close")):
            button = WindowControlButton(action, self)
            layout.addWidget(button)
            self.buttons[action] = button
        self.buttons["close"].clicked.connect(window.close)
        self.buttons["minimize"].clicked.connect(window.showMinimized)
        self.buttons["maximize"].clicked.connect(self._maximize)
        self.setFixedSize(100 if self.mac_style else 138, 48)
        window.installEventFilter(self)
        self.update_buttons()

    def _maximize(self):
        if self.window.isFullScreen() or self.window.isMaximized():
            self.window.showNormal()
        elif self.mac_style:
            self.window.showFullScreen()
        else:
            self.window.showMaximized()

    def update_buttons(self):
        expanded = self.window.isMaximized() or self.window.isFullScreen()
        labels = {"close": "Fechar", "minimize": "Minimizar", "maximize": "Restaurar" if expanded else "Tela cheia" if self.mac_style else "Maximizar"}
        for action, button in self.buttons.items():
            button.setAccessibleName(labels[action])
            button.setToolTip(labels[action])
            button.update()

    def eventFilter(self, watched, event):
        if event.type() in (QEvent.Type.WindowStateChange, QEvent.Type.ActivationChange):
            self.update_buttons()
        return super().eventFilter(watched, event)

    def enterEvent(self, event):
        self.update_buttons()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_buttons()
        super().leaveEvent(event)
