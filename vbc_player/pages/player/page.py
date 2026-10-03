from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from vbc_player.pages.player.widgets.clock import StudioClockWidget
from vbc_player.pages.player.widgets.deck import DeckWidget
from vbc_player.pages.player.widgets.explorer import FileExplorerWidget
from vbc_player.pages.player.widgets.modes import PlaybackModesWidget
from vbc_player.pages.player.widgets.playlist import PlaylistWidget
from vbc_player.pages.player.widgets.transport import TransportWidget


class PlayerPage(QWidget):
    def __init__(self, service, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(16)
        self.top = QWidget()
        top_layout = QHBoxLayout(self.top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(16)
        self.on_air = DeckWidget(service, True)
        self.next_deck = DeckWidget(service, False)
        self.clock = StudioClockWidget()
        self.modes = PlaybackModesWidget(service)
        for widget, stretch in [(self.on_air,396), (self.next_deck,396), (self.clock,236), (self.modes,328)]:
            top_layout.addWidget(widget, stretch)
        layout.addWidget(self.top, 236)
        middle = QWidget()
        middle_layout = QHBoxLayout(middle)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(16)
        self.playlist = PlaylistWidget(service)
        self.explorer = FileExplorerWidget(service)
        middle_layout.addWidget(self.playlist, 1010)
        middle_layout.addWidget(self.explorer, 378)
        layout.addWidget(middle, 400)
        self.transport = TransportWidget(service)
        layout.addWidget(self.transport, 92)

    def add_tracks(self, paths):
        self.playlist.add_tracks(paths)
