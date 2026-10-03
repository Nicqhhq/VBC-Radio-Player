from PySide6.QtCore import Signal
from vbc_player.common.widgets.design_panel import DesignPanel


class ToolbarWidget(DesignPanel):
    page_requested = Signal(str)
    new_requested = Signal()
    open_requested = Signal()
    save_requested = Signal()

    def __init__(self, parent=None):
        super().__init__("24:3", parent)
        actions = [
            ("17:398", "Nova lista", self.new_requested.emit),
            ("17:400", "Abrir lista", self.open_requested.emit),
            ("17:402", "Salvar lista", self.save_requested.emit),
            ("17:404", "Agendador", lambda: self.page_requested.emit("schedule")),
            ("17:406", "Eventos", lambda: self.page_requested.emit("events")),
            ("17:408", "Relatórios", lambda: self.page_requested.emit("reports")),
        ]
        for node, label, callback in actions:
            self.button(label, self.local_rect(node), callback)

