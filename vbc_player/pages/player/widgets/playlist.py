from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QAbstractItemView, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem

from vbc_player.common.widgets.design_panel import DesignPanel


class PlaylistWidget(DesignPanel):
    import_requested = Signal()

    def __init__(self, service, parent=None):
        super().__init__("24:8", parent)
        self.service = service
        self.selected = 0
        self.button("Adicionar áudio", self.local_rect("17:545"), self.import_audio)
        self.button("Remover item selecionado", self.local_rect("17:547"), self.remove_selected)
        self.button("Propriedades do item", self.local_rect("17:549"), self.properties)
        self.table = QTableWidget(0, 8, self)
        self.table.setHorizontalHeaderLabels(["#", "TIPO", "ARQUIVO / TÍTULO", "DURAÇÃO", "INÍCIO", "FIM", "STATUS", ""])
        self.table.setColumnHidden(7, True)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("QTableWidget{background:#111827;border:0;padding:0;font-size:11px;} QHeaderView::section{background:#182335;color:#64748b;border:0;padding:8px;font-size:10px;} QTableWidget::item{padding:4px;}")
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAccessibleName("Lista de reprodução")
        self.table.cellDoubleClicked.connect(lambda row, _col: service.play_index(row))
        self.table.itemSelectionChanged.connect(self._selected)
        self.add_control(self.table, QRectF(12, 44, 986, 312))
        self.table.hide()
        service.queue_changed.connect(self.refresh)
        self.setToolTip("Lista inicial: referência do Figma, sem arquivos de áudio. Adicione seus arquivos para reproduzir.")

    def import_audio(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Adicionar áudios", "", "Áudio (*.mp3 *.wav *.flac *.ogg *.m4a *.aac);;Todos os arquivos (*)")
        self.service.add_tracks(paths)

    def add_tracks(self, paths):
        self.service.add_tracks(paths)

    def remove_selected(self):
        self.service.remove(self.selected)

    def properties(self):
        if 0 <= self.selected < len(self.service.tracks):
            track = self.service.tracks[self.selected]
            QMessageBox.information(self, "Propriedades", f"{track.title}\n\nTipo: {track.kind}\nArquivo: {track.path or 'Referência visual — sem áudio'}")

    def _selected(self):
        self.selected = self.table.currentRow()

    def refresh(self):
        if self.service.demo:
            self.update()
            return
        # Hide the original demo header/rows, while reusing the frame and actions.
        for node in self.design.get("c", []):
            if node["id"] not in {"17:481", "17:482", "17:483", "17:545", "17:546", "17:547", "17:548", "17:549", "17:550"}:
                self.hidden.add(node["id"])
        self.table.show()
        self.table.setRowCount(len(self.service.tracks))
        for row, track in enumerate(self.service.tracks):
            duration = f"{track.duration_ms//60000:02d}:{track.duration_ms//1000%60:02d}" if track.duration_ms else "—"
            values = [f"{row+1:02d}", track.kind, track.title, duration, track.start, track.end, track.status]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setBackground(QColor("#141d2b" if row % 2 == 0 else "#111827"))
                if row == self.service.index:
                    item.setBackground(QColor("#421c24"))
                elif row == self.service.index+1:
                    item.setBackground(QColor("#113a32"))
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, 46)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 86)
        self.table.setColumnWidth(2, max(140, self.table.width()-480))
        for col in (3,4,5,6):
            self.table.setColumnWidth(col, 82)
        self.set_text("17:483", f"{len(self.service.tracks)} itens")
        self.update()

    def mousePressEvent(self, event):
        if self.service.demo:
            y = event.position().y()*self.design_height/self.height()
            row = int((y-80)/46)
            if 0 <= row < len(self.service.tracks):
                self.selected = row
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.service.demo:
            self.service.play_index(self.selected)
        super().mouseDoubleClickEvent(event)
