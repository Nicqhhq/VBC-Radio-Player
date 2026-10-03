from PySide6.QtCore import Qt
from vbc_player.common.widgets.design_panel import DesignPanel


class HeaderWidget(DesignPanel):
    def __init__(self, window):
        super().__init__("24:2", window)
        self.window = window
        for component in ("29:6", "56:298"):
            node = self._components[component]
            self.design.setdefault("c", []).append(node)
            from vbc_player.common.widgets.design_panel import descendants
            self.nodes.update({n["id"]: n for n in descendants(node)})
        self.button("Minimizar", (1270, 0, 48, 48), window.showMinimized)
        self.button("Maximizar / restaurar", (1330, 0, 48, 48), self._maximize)
        self.button("Fechar", (1390, 0, 50, 48), window.close)

    def _maximize(self):
        self.window.showNormal() if self.window.isMaximized() else self.window.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.window.windowHandle():
            self.window.windowHandle().startSystemMove()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self._maximize()

