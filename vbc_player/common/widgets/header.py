from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter
from vbc_player.common.widgets.design_panel import DesignPanel
from vbc_player.common.widgets.window_controls import WindowControls


class HeaderWidget(DesignPanel):
    def __init__(self, window):
        super().__init__("24:2", window)
        self.window = window
        self.hidden.update({"56:292", "56:304"})
        for component in ("29:6",):
            node = self._components[component]
            self.design.setdefault("c", []).append(node)
            from vbc_player.common.widgets.design_panel import descendants
            self.nodes.update({n["id"]: n for n in descendants(node)})
        self.controls = WindowControls(window, self)
        self._place_window_controls()

    def _place_window_controls(self):
        self.controls.move(self.width() - self.controls.width(), 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._place_window_controls()

    def _maximize(self):
        self.window.showNormal() if self.window.isMaximized() or self.window.isFullScreen() else self.window.showMaximized()

    def paintEvent(self, event):
        if self.window.isMaximized() or self.window.isFullScreen():
            # Completa o gradiente nos cantos arredondados do SVG original.
            painter = QPainter(self)
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(0, QColor("#111827"))
            gradient.setColorAt(1, QColor("#1e293b"))
            painter.fillRect(self.rect(), gradient)
            painter.end()
        super().paintEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.window.windowHandle():
            self.window.windowHandle().startSystemMove()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self._maximize()

