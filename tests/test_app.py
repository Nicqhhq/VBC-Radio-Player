import json
import os
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QDateTime, QEventLoop, QItemSelectionModel, QMimeData, QPersistentModelIndex, QTimer, QUrl
from PySide6.QtGui import QFont, QFontDatabase, QFontMetricsF
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication

from vbc_player.main_window import MainWindow
from vbc_player.models import Track, collect_audio_paths
from vbc_player.services.playlist_storage import read_playlist, save_playlist
from vbc_player.theme import ASSETS, DESIGN, STYLESHEET
from vbc_player.common.widgets.design_panel import DesignPanel, descendants
from vbc_player.pages.player.widgets.explorer import PATH_ROLE
from vbc_player.pages.player.widgets.playlist import local_paths
from vbc_player.services.filesystem_locations import standard_locations


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
        self.explorer_folder = tempfile.TemporaryDirectory()
        self.default_folder = patch("vbc_player.pages.player.widgets.explorer.default_directory", return_value=self.explorer_folder.name)
        self.default_folder.start()
        self.window = MainWindow()
        self.window.show()
        wait(20)

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        wait(20)
        self.default_folder.stop()
        self.explorer_folder.cleanup()

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

    def test_studio_clock_shows_seconds_without_elision(self):
        clock = self.window.player_page.clock
        clock._tick()
        node = clock.nodes["17:447"]
        self.assertRegex(node["t"], r"^\d{2}:\d{2}:\d{2}$")
        font = QFont(node["f"])
        font.setPixelSize(round(node["s"]))
        font.setWeight(QFont.Weight(node["w"]))
        widest_time = QFontMetricsF(font).horizontalAdvance("00:00:00")
        self.assertGreaterEqual(clock.local_rect("17:447").width() + 2, widest_time)

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

    def test_audio_folders_and_drag_drop_are_supported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            nested = root / "Álbum" / "Disco 1"
            nested.mkdir(parents=True)
            first = root / "Álbum" / "01 - Abertura.MP3"
            second = nested / "02 - Música.flac"
            ignored = nested / "capa.jpg"
            first.write_bytes(b"audio")
            second.write_bytes(b"audio")
            ignored.write_bytes(b"image")

            self.assertEqual(collect_audio_paths([root / "Álbum"]), [str(first.resolve()), str(second.resolve())])
            mime = QMimeData()
            mime.setUrls([QUrl.fromLocalFile(str(root / "Álbum"))])
            playlist = self.window.player_page.playlist
            self.assertEqual(local_paths(mime), [str(root / "Álbum")])
            playlist.table.paths_dropped.emit(local_paths(mime))
            self.assertEqual(
                [track.path for track in self.window.service.tracks],
                [str(first.resolve()), str(second.resolve())],
            )
            self.assertTrue(playlist.table.acceptDrops())
            self.assertTrue(self.window.player_page.explorer.tree.dragEnabled())

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
            self.wait_for(lambda: service.index == 1)
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

    def explorer_names(self, parent=None):
        explorer = self.window.player_page.explorer
        parent = parent if parent is not None else explorer.tree.rootIndex()
        return [explorer.proxy.index(row, 0, parent).data() for row in range(explorer.proxy.rowCount(parent))]

    def explorer_index_for_path(self, path):
        explorer = self.window.player_page.explorer
        source = explorer.model.index_for_path(str(Path(path).resolve()))
        self.assertTrue(source.isValid(), path)
        return explorer.proxy.mapFromSource(source)

    def wait_for(self, predicate):
        for _ in range(150):
            if predicate():
                return
            wait(20)
        self.fail("O modelo de arquivos não atualizou dentro de 3 segundos")

    def test_real_explorer_navigation_search_and_import(self):
        folder = Path(self.explorer_folder.name)
        music = folder / "Áudios de teste"
        music.mkdir()
        nested = music / "Vinhetas"
        nested.mkdir()
        (music / "TEMA.MP3").write_bytes(b"fixture")
        (music / "rádio.wav").write_bytes(b"fixture")
        (music / "notas.txt").write_text("não é áudio")
        (nested / "abertura.ogg").write_bytes(b"fixture")
        explorer = self.window.player_page.explorer
        self.assertTrue(explorer.navigate(str(music)))
        music_index = self.explorer_index_for_path(music)
        self.wait_for(lambda: set(self.explorer_names(music_index)) == {"Vinhetas", "TEMA.MP3", "rádio.wav"})
        root_paths = {
            explorer.proxy.index(row, 0).data(PATH_ROLE)
            for row in range(explorer.proxy.rowCount())
        }
        for _, path in standard_locations():
            self.assertIn(path, root_paths)
        self.assertNotIn("OneDrive", self.explorer_names())
        folder_index = next(explorer.proxy.index(i, 0, music_index) for i in range(explorer.proxy.rowCount(music_index)) if explorer.proxy.index(i, 0, music_index).data() == "Vinhetas")
        explorer.tree.setExpanded(folder_index, True)
        folder_index = QPersistentModelIndex(folder_index)
        self.wait_for(lambda: explorer.proxy.rowCount(folder_index) == 1 and explorer.proxy.index(0, 0, folder_index).data() == "abertura.ogg")
        self.assertEqual(explorer.proxy.index(0, 0, folder_index).data(), "abertura.ogg")
        explorer.search.setText("tema")
        music_index = self.explorer_index_for_path(music)
        self.wait_for(lambda: "TEMA.MP3" in self.explorer_names(music_index) and "rádio.wav" not in self.explorer_names(music_index))
        index = next(explorer.proxy.index(i, 0, music_index) for i in range(explorer.proxy.rowCount(music_index)) if explorer.proxy.index(i, 0, music_index).data() == "TEMA.MP3")
        explorer.tree.doubleClicked.emit(index)
        self.assertEqual(self.window.service.tracks[0].path, str((music / "TEMA.MP3").resolve()))
        explorer.search.clear()
        music_index = self.explorer_index_for_path(music)
        for row in range(explorer.proxy.rowCount(music_index)):
            index = explorer.proxy.index(row, 0, music_index)
            if index.data() in {"TEMA.MP3", "rádio.wav"}:
                explorer.tree.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)
        self.assertEqual(len(explorer.selected_audio_paths()), 2)
        explorer.tree.add_requested.emit()
        self.assertEqual(len(self.window.service.tracks), 2)
        index = next(explorer.proxy.index(i, 0, music_index) for i in range(explorer.proxy.rowCount(music_index)) if explorer.proxy.index(i, 0, music_index).data() == "Vinhetas")
        explorer.tree.doubleClicked.emit(index)
        self.wait_for(lambda: explorer.tree.isExpanded(index))
        self.assertEqual(Path(explorer.current_directory).resolve(), nested.resolve())
        self.assertEqual(explorer.proxy.index(0, 0, index).data(), "abertura.ogg")
        explorer.go_up()
        self.assertEqual(Path(explorer.current_directory).resolve(), music.resolve())
        explorer.navigate(str(music))
        music_index = self.explorer_index_for_path(music)
        self.wait_for(lambda: "rádio.wav" in self.explorer_names(music_index))
        self.assertFalse(explorer.navigate(str(music / "inexistente")))
        self.assertEqual(Path(explorer.current_directory).resolve(), music.resolve())
        self.assertIn("indisponível", explorer.status.text())
        # F5/Atualizar relê a pasta sem abrir outro painel ou diálogo.
        (music / "nova.flac").write_bytes(b"fixture")
        explorer.tree.setCurrentIndex(music_index)
        explorer.refresh()
        music_index = self.explorer_index_for_path(music)
        self.wait_for(lambda: "nova.flac" in self.explorer_names(music_index))
        self.window.grab().save(str(DESIGN / "implementation-explorer.png"))
        self.assertFalse(explorer.tree.isHidden())
        self.assertIn("26:16", explorer.hidden)


if __name__ == "__main__":
    unittest.main()
