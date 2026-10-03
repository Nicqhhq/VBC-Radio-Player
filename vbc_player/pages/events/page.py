from datetime import datetime
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget


class EventsPage(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        back = QPushButton("← Voltar ao player")
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back)
        layout.addWidget(QLabel("Eventos da sessão"))
        self.list = QListWidget()
        layout.addWidget(self.list, 1)

    def add_event(self, message):
        self.list.insertItem(0, f"{datetime.now():%H:%M:%S} — {message}")
