import json
import os
import tempfile
import unittest
import wave
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QDateTime, QEventLoop, QTimer
from PySide6.QtGui import QFontDatabase
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication

from vbc_player.main_window import MainWindow
from vbc_player.models import Track
from vbc_player.services.playlist_storage import read_playlist, save_playlist
from vbc_player.theme import ASSETS, DESIGN, STYLESHEET
from vbc_player.common.widgets.design_panel import DesignPanel, descendants


def wait(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


class ApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        QFontDatabase.addApplicationFont(str(ASSETS / "fonts" / "Inter.ttf"))
        cls.app.setStyleSheet(STYLESHEET)

    def setUp(self):
        self.window = MainWindow()
        self.window.show()
        wait(20)

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        wait(20)

    def test_layout_and_navigation(self):
        self.assertEqual(self.window.player_page.top.height(), 236)
        self.assertEqual(self.window.player_page.transport.height(), 92)
        for name, page in self.window.page_map.items():
            self.window.show_page(name)
            self.assertIs(self.window.pages.currentWidget(), page)
        self.window.show_page("player")
        self.window.grab().save(str(DESIGN / "implementation-preview.png"))
        self.window.resize(1100, 690)
        wait(20)
        self.window.grab().save(str(DESIGN / "implementation-compact.png"))
        self.assertGreater(self.window.player_page.playlist.width(), 700)
        for panel in (self.window.player_page.on_air, self.window.player_page.transport):
            for widget, _ in panel.overlays:
                self.assertTrue(panel.rect().contains(widget.geometry()), widget.accessibleName())

    def test_original_assets(self):
        for asset in set(DesignPanel._asset_map.values()):
            path = ASSETS / "figma" / asset
            self.assertTrue(path.is_file() and path.stat().st_size > 0, asset)
        missing = []
        def check(n):
            if n["id"] in DesignPanel._asset_map:
                return
            if n["type"] == "VECTOR":
                missing.append(n["id"])
            for child in n.get("c", []):
                check(child)
        for n in DesignPanel._components.values():
            check(n)
        self.assertEqual(missing, [])

    def test_playlist_import_and_audio(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.wav"
            with wave.open(str(path), "wb") as file:
                file.setnchannels(1)
                file.setsampwidth(2)
                file.setframerate(8000)
                file.writeframes(b"\x00\x00" * 16000)
            service = self.window.service
            errors = []
            service.error.connect(errors.append)
            service.add_tracks([str(path), str(path)])
            self.assertEqual(len(service.tracks), 1)
            self.assertFalse(service.demo)
            self.assertEqual(self.window.player_page.playlist.table.rowCount(), 1)
            service.play_index(0)
            wait(300)
            self.assertEqual(errors, [])
            self.assertEqual(service.index, 0)
            self.assertGreater(service.player.duration(), 0)
            self.window.grab().save(str(DESIGN / "implementation-audio.png"))
            service.player.pause()
            self.assertEqual(service.player.playbackState(), QMediaPlayer.PlaybackState.PausedState)
            self.window.player_page.transport.volume.setValue(35)
            self.assertAlmostEqual(service.output.volume(), .35, places=2)
            service.remove(0)
            self.assertEqual(service.tracks, [])
            self.assertEqual(service.index, -1)

    def test_storage_round_trip_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "playlist.json"
            tracks = [Track("Faixa", path="/tmp/audio.wav", duration_ms=1000)]
            save_playlist(path, tracks)
            self.assertEqual(read_playlist(path)[0].title, "Faixa")
            path.write_text('{"version":1,"tracks":[{"title":"invalid","path":5}]}')
            with self.assertRaises(ValueError):
                read_playlist(path)

    def test_automatic_next_and_schedule(self):
        with tempfile.TemporaryDirectory() as folder:
            paths = []
            for index in range(2):
                path = Path(folder) / f"clip-{index}.wav"
                with wave.open(str(path), "wb") as file:
                    file.setnchannels(1)
                    file.setsampwidth(2)
                    file.setframerate(8000)
                    file.writeframes(b"\x00\x00" * 800)
                paths.append(str(path))
            service = self.window.service
            service.add_tracks(paths)
            service.play_index(0)
            wait(900)
            self.assertEqual(service.index, 1, "Ao terminar, o modo automático deve avançar para o segundo áudio")
            self.window.player_page.modes.set_automatic(False)
            self.assertFalse(service.automatic)
            self.assertEqual(self.window.toolbar.nodes["17:412"]["t"], "MANUAL")
            schedule = self.window.schedule_page
            schedule.jobs.append((QDateTime.currentDateTime().addSecs(-1), paths[0]))
            schedule.check_due()
            self.assertEqual(schedule.jobs, [])
            self.assertEqual(service.index, 0)
            self.assertGreater(self.window.events_page.list.count(), 0)


if __name__ == "__main__":
    unittest.main()
