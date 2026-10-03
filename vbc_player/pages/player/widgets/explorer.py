from pathlib import Path

from PySide6.QtCore import (
    QDir, QFileInfo, QModelIndex, QRectF, QSortFilterProxyModel, Qt, Signal,
)
from PySide6.QtGui import QKeySequence, QShortcut, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView, QFileDialog, QFileIconProvider, QLabel, QLineEdit,
    QMenu, QTreeView,
)

from vbc_player.common.widgets.design_panel import DesignPanel
from vbc_player.services.filesystem_locations import default_directory, standard_locations

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}
PATH_ROLE = Qt.ItemDataRole.UserRole + 1
DIRECTORY_ROLE = Qt.ItemDataRole.UserRole + 2
LOADED_ROLE = Qt.ItemDataRole.UserRole + 3
PLACEHOLDER_ROLE = Qt.ItemDataRole.UserRole + 4


class LocationsModel(QStandardItemModel):
    """Árvore somente leitura com raízes reais e carregamento sob demanda."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icons = QFileIconProvider()
        self.setHorizontalHeaderLabels(["Pastas e arquivos"])
        self.reload()

    def reload(self):
        self.clear()
        self.setHorizontalHeaderLabels(["Pastas e arquivos"])
        for label, path in standard_locations():
            self.invisibleRootItem().appendRow(self._item(label, QFileInfo(path), is_root=True))

    def add_location(self, path):
        info = QFileInfo(path)
        if not info.exists() or not info.isDir():
            return QModelIndex()
        existing = self.index_for_path(info.absoluteFilePath())
        if existing.isValid():
            return existing
        item = self._item(info.fileName() or QDir.toNativeSeparators(info.absoluteFilePath()), info, is_root=True)
        self.invisibleRootItem().appendRow(item)
        return item.index()

    def index_for_path(self, path, parent=QModelIndex()):
        target = QDir.cleanPath(path)
        for row in range(self.rowCount(parent)):
            index = self.index(row, 0, parent)
            if QDir.cleanPath(index.data(PATH_ROLE) or "") == target:
                return index
        return QModelIndex()

    def _item(self, label, info, is_root=False):
        item = QStandardItem(label)
        item.setEditable(False)
        item.setData(info.absoluteFilePath(), PATH_ROLE)
        item.setData(info.isDir(), DIRECTORY_ROLE)
        item.setData(False, LOADED_ROLE)
        item.setToolTip(QDir.toNativeSeparators(info.absoluteFilePath()))
        item.setIcon(self.icons.icon(info))
        if info.isDir():
            placeholder = QStandardItem("Carregando…")
            placeholder.setData(True, PLACEHOLDER_ROLE)
            item.appendRow(placeholder)
        return item

    def load_children(self, index):
        item = self.itemFromIndex(index)
        if not item or not item.data(DIRECTORY_ROLE) or item.data(LOADED_ROLE):
            return
        item.removeRows(0, item.rowCount())
        directory = QDir(item.data(PATH_ROLE))
        entries = directory.entryInfoList(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot | QDir.Filter.Readable,
            QDir.SortFlag.DirsFirst | QDir.SortFlag.Name | QDir.SortFlag.IgnoreCase,
        )
        for info in entries:
            if info.isDir() or ("." + info.suffix().casefold()) in AUDIO_EXTENSIONS:
                item.appendRow(self._item(info.fileName(), info))
        item.setData(True, LOADED_ROLE)

    def reload_item(self, index):
        item = self.itemFromIndex(index)
        if not item or not item.data(DIRECTORY_ROLE):
            return
        item.setData(False, LOADED_ROLE)
        self.load_children(index)


class AudioFileFilter(QSortFilterProxyModel):
    """Mantém pastas navegáveis e filtra os áudios carregados pelo nome."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = ""
        self.setDynamicSortFilter(True)
        self.setRecursiveFilteringEnabled(True)

    def set_query(self, query):
        self.beginFilterChange()
        self.query = query.casefold().strip()
        self.endFilterChange(QSortFilterProxyModel.Direction.Rows)

    def filterAcceptsRow(self, row, parent):
        index = self.sourceModel().index(row, 0, parent)
        if index.data(PLACEHOLDER_ROLE):
            return not self.query
        if index.data(DIRECTORY_ROLE):
            return True
        return self.query in str(index.data() or "").casefold()


class AudioTreeView(QTreeView):
    add_requested = Signal()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.add_requested.emit()
            event.accept()
        else:
            super().keyPressEvent(event)


class FileExplorerWidget(DesignPanel):
    def __init__(self, service, parent=None):
        super().__init__("24:9", parent)
        self.service = service
        self.current_directory = ""
        # The original Figma tree is sample content. The live Qt tree occupies
        # exactly the same slot and contains only locations that exist.
        self.hidden.update({"26:11", "26:16", "26:69"})

        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Buscar arquivos e pastas")
        self.search.setAccessibleName("Buscar arquivos e pastas")
        self.search.setClearButtonEnabled(True)
        self.search.setStyleSheet(
            "QLineEdit{background:transparent;border:0;color:#c7d2e3;"
            "padding:0;font-size:11px;}"
        )
        self.add_control(self.search, QRectF(56, 67, 270, 36))

        self.root_button = self.button(
            "Atualizar locais do computador",
            self.local_rect("26:13").adjusted(0, -6, 0, 6),
            self.refresh_locations,
        )
        self.folder_button = self.button(
            "Escolher outra pasta", QRectF(116, 113, 220, 24), self.choose_folder
        )

        self.model = LocationsModel(self)
        self.proxy = AudioFileFilter(self)
        self.proxy.setSourceModel(self.model)
        self.tree = AudioTreeView(self)
        self.tree.setModel(self.proxy)
        self.tree.setAccessibleName("Locais, pastas e arquivos de áudio")
        self.tree.setHeaderHidden(True)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setUniformRowHeights(True)
        self.tree.setExpandsOnDoubleClick(True)
        self.tree.setIndentation(16)
        self.tree.setStyleSheet("""
            QTreeView{background:#111c2d;border:1px solid #223149;border-radius:7px;
                color:#c7d2e3;font-size:11px;padding:3px;}
            QTreeView::item{height:25px;border:0;}
            QTreeView::item:selected{background:#173a68;color:#f2f5fa;}
            QTreeView::item:hover{background:#162c50;}
            QTreeView::branch{background:transparent;}
        """)
        self.add_control(self.tree, QRectF(18, 142, 340, 198))
        self.tree.expanded.connect(self.load_folder)
        self.tree.clicked.connect(self.expand_folder)
        self.tree.doubleClicked.connect(self.activate_index)
        self.tree.add_requested.connect(self.activate_selection)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)

        self.status = QLabel("", self)
        self.status.setStyleSheet(
            "QLabel{background:transparent;color:#64748b;font-size:9px;}"
        )
        self.add_control(self.status, QRectF(19, 361, 294, 12))

        self.search.textChanged.connect(self.filter_files)
        self.find_shortcut = QShortcut(QKeySequence.StandardKey.Find, self)
        self.find_shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self.find_shortcut.activated.connect(self.search.setFocus)
        self.navigation_shortcuts = []
        for key, callback in (
            ("Backspace", self.collapse_or_parent),
            ("F5", self.refresh),
            ("Ctrl+Return", self.add_selected),
        ):
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            shortcut.activated.connect(callback)
            self.navigation_shortcuts.append(shortcut)

        self.refresh_locations()
        self.expand_location(default_directory())
        self.setToolTip(
            "Somente locais reais são exibidos. Clique numa pasta para expandi-la "
            "na árvore; dois cliques num áudio o adicionam à playlist."
        )

    def refresh_locations(self):
        expanded = self.expanded_paths()
        selected = self.current_directory
        self.model.reload()
        for path in expanded:
            self.expand_location(path)
        if selected:
            self.select_path(selected)
        self._update_status()

    def expanded_paths(self):
        paths = []
        def visit(parent=QModelIndex()):
            for row in range(self.proxy.rowCount(parent)):
                index = self.proxy.index(row, 0, parent)
                if self.tree.isExpanded(index):
                    path = index.data(PATH_ROLE)
                    if path:
                        paths.append(path)
                    visit(index)
        visit()
        return paths

    def select_path(self, path):
        source = self.model.index_for_path(path)
        if source.isValid():
            proxy = self.proxy.mapFromSource(source)
            self.tree.setCurrentIndex(proxy)
            self.tree.scrollTo(proxy)
            return proxy
        return QModelIndex()

    def expand_location(self, path):
        info = QFileInfo(path)
        if not info.exists() or not info.isDir():
            return False
        source = self.model.index_for_path(info.absoluteFilePath())
        if not source.isValid():
            source = self.model.add_location(info.absoluteFilePath())
        if not source.isValid():
            return False
        proxy = self.proxy.mapFromSource(source)
        self.load_folder(proxy)
        self.tree.setExpanded(proxy, True)
        self.tree.setCurrentIndex(proxy)
        self.tree.scrollTo(proxy)
        self.current_directory = info.absoluteFilePath()
        self._sync_location()
        self._update_status(proxy)
        return True

    # Kept as the public navigation entry used by the folder chooser and tests.
    def navigate(self, path):
        if not self.expand_location(path):
            self.status.setText("Pasta indisponível ou sem permissão de leitura.")
            return False
        return True

    def _sync_location(self):
        native = QDir.toNativeSeparators(self.current_directory)
        self.folder_button.setToolTip(native)
        self.set_text(
            "26:15",
            QDir(self.current_directory).dirName() or native,
        )
        self.nodes["26:15"]["b"][2] = 225

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Escolher pasta de músicas",
            self.current_directory or QDir.homePath(),
        )
        if folder:
            self.expand_location(folder)

    def load_folder(self, proxy_index):
        source = self.proxy.mapToSource(proxy_index)
        self.model.load_children(source)
        self._update_status(proxy_index)

    def expand_folder(self, index):
        source = self.proxy.mapToSource(index)
        if source.data(DIRECTORY_ROLE):
            self.model.load_children(source)
            self.tree.setExpanded(index, True)
            self.current_directory = source.data(PATH_ROLE)
            self._sync_location()
            self._update_status(index)

    def activate_index(self, index):
        source = self.proxy.mapToSource(index)
        if source.data(DIRECTORY_ROLE):
            self.expand_folder(index)
        else:
            self._add_paths([source.data(PATH_ROLE)])

    def activate_selection(self):
        selected = self.tree.selectionModel().selectedRows(0)
        if len(selected) == 1:
            source = self.proxy.mapToSource(selected[0])
            if source.data(DIRECTORY_ROLE):
                self.expand_folder(selected[0])
                return
        self.add_selected()

    def selected_audio_paths(self):
        paths = []
        for index in self.tree.selectionModel().selectedRows(0):
            source = self.proxy.mapToSource(index)
            if not source.data(DIRECTORY_ROLE):
                path = source.data(PATH_ROLE)
                if path and Path(path).suffix.casefold() in AUDIO_EXTENSIONS:
                    paths.append(path)
        return paths

    def filter_files(self, query):
        self.proxy.set_query(query)
        self._update_status()

    def collapse_or_parent(self):
        index = self.tree.currentIndex()
        if index.isValid() and self.tree.isExpanded(index):
            self.tree.collapse(index)
            return
        self.go_up()

    def go_up(self):
        """Seleciona o pai sem trocar a raiz nem abrir outra visualização."""
        index = self.tree.currentIndex()
        parent = index.parent() if index.isValid() else QModelIndex()
        if not parent.isValid():
            return False
        self.tree.setCurrentIndex(parent)
        self.tree.scrollTo(parent)
        self.current_directory = parent.data(PATH_ROLE)
        self._sync_location()
        self._update_status(parent)
        return True

    def refresh(self):
        index = self.tree.currentIndex()
        source = self.proxy.mapToSource(index) if index.isValid() else QModelIndex()
        if source.isValid() and source.data(DIRECTORY_ROLE):
            self.model.reload_item(source)
            self.tree.setExpanded(self.proxy.mapFromSource(source), True)
        else:
            self.refresh_locations()
        self._update_status(index)

    def context_menu(self, point):
        index = self.tree.indexAt(point)
        menu = QMenu(self)
        if index.isValid() and index.data(DIRECTORY_ROLE):
            menu.addAction("Expandir pasta", lambda: self.expand_folder(index))
        add = menu.addAction("Adicionar áudios selecionados", self.add_selected)
        add.setEnabled(bool(self.selected_audio_paths()))
        menu.addSeparator()
        menu.addAction("Escolher outra pasta…", self.choose_folder)
        menu.addAction("Atualizar", self.refresh)
        menu.exec(self.tree.viewport().mapToGlobal(point))

    def _update_status(self, parent=None):
        parent = parent if parent is not None and parent.isValid() else QModelIndex()
        count = self.proxy.rowCount(parent)
        if parent.isValid():
            self.status.setText(f"{count} itens • {parent.data()}")
        else:
            self.status.setText(f"{count} locais reais • Ctrl+F")

    def add_selected(self):
        self._add_paths(self.selected_audio_paths())

    def _add_paths(self, paths):
        valid = [
            path for path in paths
            if path and Path(path).is_file()
            and Path(path).suffix.casefold() in AUDIO_EXTENSIONS
        ]
        if valid:
            self.service.add_tracks(valid)
            self.status.setText(f"{len(valid)} áudio(s) enviado(s) à playlist.")
