import csv
from datetime import datetime
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget


class ReportsPage(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.records = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        back = QPushButton("← Voltar ao player")
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back)
        self.title = QLabel("Relatório da sessão — 0 reproduções iniciadas")
        layout.addWidget(self.title)
        self.list = QListWidget()
        layout.addWidget(self.list, 1)
        export = QPushButton("Exportar CSV…")
        export.clicked.connect(self.export)
        layout.addWidget(export)

    def record(self, title):
        when = datetime.now().isoformat(timespec="seconds")
        self.records.append((when, title))
        self.list.insertItem(0, f"{when} — {title}")
        self.title.setText(f"Relatório da sessão — {len(self.records)} reproduções iniciadas")

    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar relatório", "vbc-relatorio.csv", "CSV (*.csv)")
        if path:
            try:
                with open(path, "w", encoding="utf-8-sig", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["data_hora", "titulo"])
                    for when, title in self.records:
                        # CSV can be opened in spreadsheet software.
                        writer.writerow([when, "'" + title if title.startswith(("=", "+", "-", "@")) else title])
            except OSError as error:
                QMessageBox.warning(self, "Não foi possível exportar", str(error))
