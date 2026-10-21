from pathlib import Path

from PySide6.QtCore import QEvent, QRectF, QSettings, Qt
from PySide6.QtGui import QColor, QKeySequence, QPainter, QPainterPath, QRegion, QShortcut
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QSizeGrip, QStackedWidget, QVBoxLayout, QWidget

from vbc_player.pages.events import EventsPage
from vbc_player.pages.player import PlayerPage
from vbc_player.pages.reports import ReportsPage
from vbc_player.pages.schedule import SchedulePage
from vbc_player.services.playback import PlaybackService
from vbc_player.services.playlist_storage import read_playlist, save_playlist
from vbc_player.common.widgets.header import HeaderWidget
from vbc_player.common.widgets.toolbar import ToolbarWidget
from vbc_player.common.widgets.design_panel import DesignPanel


class MainWindow(QMainWindow):
    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings if settings is not None else QSettings("VBC", "VBC Player")
        self.playlist_path = None
        self.setWindowTitle("VBC Player - Automação de Rádio")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName("mainWindow")
        self.setStyleSheet("QMainWindow#mainWindow { background: transparent; }")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 690)
        self.service = PlaybackService(self)
        root = DesignPanel("17:383")
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.header = HeaderWidget(self)
        self.header.setFixedHeight(48)
        layout.addWidget(self.header)
        self.toolbar = ToolbarWidget()
        self.toolbar.setFixedHeight(58)
        layout.addWidget(self.toolbar)
        self.pages = QStackedWidget()
        self.player_page = PlayerPage(self.service)
        self.schedule_page = SchedulePage(self.service)
        self.events_page = EventsPage()
        self.reports_page = ReportsPage()
        self.page_map = {"player": self.player_page, "schedule": self.schedule_page, "events": self.events_page, "reports": self.reports_page}
        for page in self.page_map.values():
            self.pages.addWidget(page)
            if hasattr(page, "back_requested"):
                page.back_requested.connect(lambda: self.show_page("player"))
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(root)
        root.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        root.setFocus()
        self.toolbar.page_requested.connect(self.show_page)
        self.toolbar.new_requested.connect(self.new_playlist)
        self.toolbar.open_requested.connect(self.open_playlist)
        self.toolbar.save_requested.connect(self.save_playlist)
        self.service.error.connect(self.show_error)
        self.service.played.connect(self.reports_page.record)
        self.service.played.connect(lambda title: self.events_page.add_event(f"Reprodução iniciada: {title}"))
        self.schedule_page.event.connect(self.events_page.add_event)
        self.service.queue_changed.connect(self._refresh_mode)
        self.service.mode_changed.connect(self._refresh_mode)
        self.service.output.deviceChanged.connect(self._refresh_device)
        self.devices = QMediaDevices(self)
        self.devices.audioOutputsChanged.connect(self._refresh_device)
        self._refresh_device()
        self.shortcuts = []
        for key, action in [("Space", self.service.toggle), ("Ctrl+O", self.player_page.playlist.import_audio), ("Ctrl+S", self.save_playlist), ("Ctrl+Right", self.service.next), ("Escape", lambda: self.show_page("player"))]:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(action)
            self.shortcuts.append(shortcut)
        self.grip = QSizeGrip(self)
        self.grip.setStyleSheet("background:transparent;")
        self._restore_playlist()
        self._update_window_shape()

    def _update_window_shape(self):
        root = self.centralWidget()
        if root is None:
            return
        if self.isMaximized() or self.isFullScreen():
            self.clearMask()
            root.clearMask()
        else:
            # Recorta também as páginas e o cabeçalho, que pintam fundos
            # próprios e antes preenchiam os cantos do SVG arredondado.
            path = QPainterPath()
            path.addRoundedRect(QRectF(root.rect()), 18, 18)
            shape = QRegion(path.toFillPolygon().toPolygon())
            root.setMask(shape)
            self.setMask(shape.translated(root.pos()))

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange:
            self._update_window_shape()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isMaximized() or self.isFullScreen():
            # Os SVGs também têm cantos transparentes: remover apenas a
            # máscara não preenche esses pixels quando a janela ocupa a tela.
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor("#0b0f17"))

    def _remember_playlist(self, path):
        self.playlist_path = str(Path(path).resolve())
        self.settings.setValue("playlist/default_path", self.playlist_path)
        self.settings.sync()

    def _restore_playlist(self):
        path = self.settings.value("playlist/default_path", "", type=str)
        if not path:
            return
        try:
            tracks = read_playlist(path)
        except (OSError, ValueError, TypeError) as error:
            self.events_page.add_event(f"Não foi possível restaurar a lista padrão {path}: {error}")
            return
        self.playlist_path = path
        self.service.tracks = tracks
        self.service.queue_changed.emit()

    def _refresh_device(self):
        device = self.service.output.device()
        self.toolbar.set_text("17:415", device.description() or "SEM DISPOSITIVO")

    def _refresh_mode(self):
        self.toolbar.set_text("17:412", "AUTO ATIVO" if self.service.automatic else "MANUAL")

    def show_page(self, name):
        self.pages.setCurrentWidget(self.page_map[name])

    def new_playlist(self):
        self.service.clear()
        self.playlist_path = None
        self.settings.remove("playlist/default_path")
        self.settings.sync()
        self.show_page("player")

    def open_playlist(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir lista", "", "Lista VBC (*.json)")
        if not path:
            return
        try:
            tracks = read_playlist(path)
        except (OSError, ValueError, TypeError) as error:
            self.show_error(str(error))
            return
        self.service.clear()
        self.service.tracks = tracks
        self.service.queue_changed.emit()
        self._remember_playlist(path)
        self.show_page("player")

    def save_playlist(self):
        path, _ = QFileDialog.getSaveFileName(self, "Salvar lista", self.playlist_path or "vbc-playlist.json", "Lista VBC (*.json)")
        if path:
            try:
                save_playlist(path, self.service.tracks)
            except OSError as error:
                self.show_error(str(error))
                return
            self._remember_playlist(path)

    def show_error(self, message):
        self.events_page.add_event(message)
        QMessageBox.warning(self, "VBC Player", message)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_window_shape()
        if hasattr(self, "grip"):
            self.grip.setGeometry(self.width()-16, self.height()-16, 16, 16)

    def closeEvent(self, event):
        self.service.player.stop()
        super().closeEvent(event)
