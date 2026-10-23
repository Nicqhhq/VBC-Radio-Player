from pathlib import Path

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPen
from PySide6.QtWidgets import (
    QAbstractItemView, QFileDialog, QHeaderView, QStyledItemDelegate,
    QTableWidget, QTableWidgetItem,
)

from vbc_player.common.widgets.design_panel import DesignPanel


def local_paths(mime_data):
    if not mime_data.hasUrls():
        return []
    return [
        url.toLocalFile()
        for url in mime_data.urls()
        if url.isLocalFile() and Path(url.toLocalFile()).exists()
    ]


class PlaylistTable(QTableWidget):
    paths_dropped = Signal(list)
    hovered_row_changed = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hovered_row = -1
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

    def mouseMoveEvent(self, event):
        row = self.indexAt(event.position().toPoint()).row()
        if row != self._hovered_row:
            self._hovered_row = row
            self.hovered_row_changed.emit(row)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self._hovered_row != -1:
            self._hovered_row = -1
            self.hovered_row_changed.emit(-1)
        super().leaveEvent(event)

    def dragEnterEvent(self, event):
        if local_paths(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if local_paths(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = local_paths(event.mimeData())
        if not paths:
            event.ignore()
            return
        self.paths_dropped.emit(paths)
        event.setDropAction(Qt.DropAction.CopyAction)
        event.accept()


class PlaylistItemDelegate(QStyledItemDelegate):
    """Pinta o estado da linha sem usar o destaque nativo do sistema."""

    def paint(self, painter, option, index):
        background = index.data(Qt.ItemDataRole.BackgroundRole)
        color = background.color() if background is not None else QColor("#111827")
        painter.save()
        painter.fillRect(option.rect, color)
        painter.setPen(QPen(QColor("#29364a"), 1))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        column = index.column()
        font = QFont(option.font)
        font.setPixelSize(14 if column == 2 else 12 if column in (0, 1, 6) else 13)
        font.setWeight(QFont.Weight.DemiBold if column in (1, 2, 6) else QFont.Weight.Medium)
        painter.setFont(font)
        value = str(index.data(Qt.ItemDataRole.DisplayRole) or "")
        rect = option.rect.adjusted(10, 0, -10, 0)
        text_color = "#f1f5f9" if column == 2 else "#d3deed"
        alignment = Qt.AlignmentFlag.AlignLeft if column in (1, 2) else Qt.AlignmentFlag.AlignHCenter
        if column == 6:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            badge = QRectF(rect.x(), rect.center().y() - 12, rect.width(), 24)
            background, text_color = {"NO AR": ("#6d293b", "#ffe1e6"), "PRÓXIMO": ("#155542", "#9af2cf")}.get(value, ("#25344a", "#d3deed"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(background))
            painter.drawRoundedRect(badge, 6, 6)
            rect = rect.adjusted(5, 0, -5, 0)
        painter.setPen(QColor(text_color))
        value = QFontMetricsF(font).elidedText(value, Qt.TextElideMode.ElideRight, rect.width())
        painter.drawText(rect, alignment | Qt.AlignmentFlag.AlignVCenter, value)
        painter.restore()


class PlaylistWidget(DesignPanel):
    import_requested = Signal()

    def __init__(self, service, parent=None):
        super().__init__("24:8", parent)
        self.service = service
        self.selected = 0
        self.hovered_row = -1
        self.setAcceptDrops(True)
        self.table = PlaylistTable(0, 8, self)
        self.table.setAcceptDrops(True)
        self.table.setHorizontalHeaderLabels(["#", "TIPO", "ARQUIVO / TÍTULO", "DURAÇÃO", "INÍCIO", "FIM", "STATUS", ""])
        self.table.setColumnHidden(7, True)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setItemDelegate(PlaylistItemDelegate(self.table))
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #111827;
                border: 0;
                padding: 0;
                font-size: 14px;
                outline: 0;
                selection-color: #f4f7fc;
            }
            QHeaderView::section {
                background: #25344a;
                color: #d3deed;
                border: 0;
                padding: 10px;
                font-size: 11px;
                font-weight: 600;
            }
            QTableWidget::item {
                padding: 4px;
                border: 0;
            }
            QTableWidget QScrollBar:vertical{background:#131e2e;width:9px;margin:0;border:0;}
            QTableWidget QScrollBar::handle:vertical{background:#526782;border-radius:4px;min-height:26px;}
            QTableWidget QScrollBar::handle:vertical:hover{background:#7189a8;}
            QTableWidget QScrollBar::add-line:vertical,QTableWidget QScrollBar::sub-line:vertical{
                height:0;border:0;background:transparent;}
            QTableWidget QScrollBar::add-page:vertical,QTableWidget QScrollBar::sub-page:vertical{
                background:transparent;}
        """)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setFixedHeight(36)
        self.table.setAccessibleName("Lista de reprodução")
        self.table.cellDoubleClicked.connect(lambda row, _col: service.play_index(row))
        self.table.itemSelectionChanged.connect(self._selected)
        self.table.hovered_row_changed.connect(self._hovered)
        self.table.paths_dropped.connect(self.add_tracks)
        self.add_control(self.table, QRectF(12, 46, 986, 342))
        self.table.hide()
        service.queue_changed.connect(self.refresh)
        self.setToolTip("Arraste arquivos de áudio ou pastas do explorador para adicionar à lista.")
        self.refresh()

    def dragEnterEvent(self, event):
        if local_paths(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if local_paths(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = local_paths(event.mimeData())
        if not paths:
            event.ignore()
            return
        self.add_tracks(paths)
        event.setDropAction(Qt.DropAction.CopyAction)
        event.accept()

    def import_audio(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Adicionar áudios", "", "Áudio (*.mp3 *.wav *.flac *.ogg *.m4a *.aac);;Todos os arquivos (*)")
        self.service.add_tracks(paths)

    def add_tracks(self, paths):
        self.service.add_tracks(paths)

    def _selected(self):
        self.selected = self.table.currentRow()
        self._apply_row_colors()

    def _hovered(self, row):
        self.hovered_row = row
        self._apply_row_colors()

    def _row_color(self, row):
        if row == self.service.index:
            return QColor("#421c24")
        if row == self.service.index + 1:
            return QColor("#113a32")
        if row == self.selected:
            return QColor("#1e293b")
        if row == self.hovered_row:
            return QColor("#192538")
        return QColor("#1b283b" if row % 2 == 0 else "#131e2e")

    def _apply_row_colors(self):
        for row in range(self.table.rowCount()):
            color = self._row_color(row)
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    item.setBackground(color)
        self.table.viewport().update()

    def refresh(self):
        # Mantém apenas o painel, o título e a contagem do desenho original.
        for node in self.design.get("c", []):
            if node["id"] not in {"17:481", "17:482", "17:483"}:
                self.hidden.add(node["id"])
        self.table.show()
        self.table.setRowCount(len(self.service.tracks))
        for row, track in enumerate(self.service.tracks):
            duration = f"{track.duration_ms//60000:02d}:{track.duration_ms//1000%60:02d}" if track.duration_ms else "—"
            values = [f"{row+1:02d}", track.kind, track.title, duration, track.start, track.end, track.status]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(f"{track.title}\n{track.path}" if col == 2 and track.path else value)
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, 52)
        self._apply_row_colors()
        self._layout_columns()
        self.set_text("17:483", f"{len(self.service.tracks)} itens")
        self.update()

    def _layout_columns(self):
        # Em janelas menores, prioriza título/duração/status; horários
        # reaparecem quando houver espaço para todas as colunas.
        compact = self.table.width() < 850
        for column in (4, 5):
            self.table.setColumnHidden(column, compact)
        for column, width in ((0, 42), (1, 96), (3, 88), (4, 88), (5, 88), (6, 110)):
            self.table.setColumnWidth(column, width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "table"):
            self._layout_columns()
