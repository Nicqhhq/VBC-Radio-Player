from pathlib import Path

from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QFileDialog, QLineEdit, QListWidget, QListWidgetItem

from vbc_player.common.widgets.design_panel import DesignPanel


class FileExplorerWidget(DesignPanel):
    def __init__(self, service, parent=None):
        super().__init__("24:9", parent)
        self.service = service
        self.files = []
        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Buscar arquivos e pastas")
        self.search.setAccessibleName("Buscar áudio")
        self.search.setStyleSheet("QLineEdit{background:transparent;border:0;color:#c7d2e3;padding:0;font-size:11px;}")
        self.add_control(self.search, QRectF(56, 67, 270, 36))
        self.hidden.add("26:11")
        self.search.textChanged.connect(self.filter_files)
        self.button("Escolher pasta de músicas", QRectF(18, 142, 340, 198), self.choose_folder)
        self.list = QListWidget(self)
        self.list.setAccessibleName("Arquivos da pasta")
        self.list.itemDoubleClicked.connect(lambda item: service.add_tracks([item.toolTip()]))
        self.add_control(self.list, QRectF(18, 142, 340, 198))
        self.list.hide()
        self.setToolTip("Clique na árvore para escolher uma pasta. Clique duas vezes em um áudio para adicioná-lo à lista.")

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta de músicas", str(Path.home()))
        if not folder:
            return
        try:
            self.files = sorted(path for path in Path(folder).iterdir() if path.is_file() and path.suffix.lower() in {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"})
        except OSError as error:
            self.service.error.emit(str(error))
            return
        self.hidden.add("26:16")
        self.set_text("26:13", "Pasta local")
        self.set_text("26:15", Path(folder).name)
        self.set_text("26:69", f"{len(self.files)} arquivos • pasta selecionada")
        self.list.show()
        self.filter_files(self.search.text())

    def filter_files(self, query):
        self.list.clear()
        for path in self.files:
            if query.casefold() in path.name.casefold():
                item = QListWidgetItem(path.name)
                item.setToolTip(str(path))
                self.list.addItem(item)
