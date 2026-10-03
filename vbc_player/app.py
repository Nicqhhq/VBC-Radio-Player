import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

from vbc_player.main_window import MainWindow
from vbc_player.theme import ASSETS, STYLESHEET


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("VBC Player")
    app.setOrganizationName("VBC")
    QFontDatabase.addApplicationFont(str(ASSETS / "fonts" / "Inter.ttf"))
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    return app.exec()
