from PySide6.QtCore import QDateTime, QTimer, Signal
from PySide6.QtWidgets import QDateTimeEdit, QFileDialog, QHBoxLayout, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget


class SchedulePage(QWidget):
    back_requested = Signal()
    event = Signal(str)

    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.jobs = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        back = QPushButton("← Voltar ao player")
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back)
        layout.addWidget(QLabel("Agendador"))
        layout.addWidget(QLabel("Reproduzir um arquivo no horário escolhido. O aplicativo deve permanecer aberto."))
        row = QHBoxLayout()
        self.when = QDateTimeEdit(QDateTime.currentDateTime().addSecs(60))
        self.when.setCalendarPopup(True)
        self.when.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
        row.addWidget(self.when)
        choose = QPushButton("Escolher áudio e agendar…")
        choose.clicked.connect(self.schedule)
        row.addWidget(choose)
        layout.addLayout(row)
        self.list = QListWidget()
        layout.addWidget(self.list, 1)
        cancel = QPushButton("Cancelar evento selecionado")
        cancel.clicked.connect(self.cancel)
        layout.addWidget(cancel)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_due)
        self.timer.start(500)

    def schedule(self):
        if self.when.dateTime() <= QDateTime.currentDateTime():
            QMessageBox.information(self, "Agendador", "Escolha um horário futuro.")
            return
        path, _ = QFileDialog.getOpenFileName(self, "Áudio do evento", "", "Áudio (*.mp3 *.wav *.flac *.ogg *.m4a *.aac)")
        if path:
            self.jobs.append((self.when.dateTime(), path))
            self.refresh()

    def refresh(self):
        from pathlib import Path
        self.list.clear()
        for when, path in self.jobs:
            self.list.addItem(f"{when.toString('dd/MM/yyyy HH:mm:ss')} — {Path(path).name}")

    def cancel(self):
        index = self.list.currentRow()
        if 0 <= index < len(self.jobs):
            del self.jobs[index]
            self.refresh()

    def check_due(self):
        from pathlib import Path
        now = QDateTime.currentDateTime()
        due = [job for job in self.jobs if job[0] <= now]
        if not due:
            return
        self.jobs = [job for job in self.jobs if job[0] > now]
        self.refresh()
        for _, path in due:
            path = str(Path(path).resolve())
            self.service.add_tracks([path])
            index = next((i for i, track in enumerate(self.service.tracks) if track.path == path), None)
            if index is None:
                self.event.emit(f"Arquivo do evento não encontrado: {path}")
            else:
                self.service.play_index(index)
                self.event.emit(f"Evento executado: {path}")
