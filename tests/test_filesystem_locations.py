import unittest
from unittest.mock import Mock, patch

from PySide6.QtCore import QDir, QStandardPaths

from vbc_player.services.filesystem_locations import default_directory, standard_locations


class FilesystemLocationsTests(unittest.TestCase):
    def test_windows_locations_and_read_only_drives_are_preserved(self):
        values = {
            QStandardPaths.StandardLocation.MusicLocation: "C:/Users/User/Music",
            QStandardPaths.StandardLocation.HomeLocation: "C:/Users/User",
            QStandardPaths.StandardLocation.DownloadLocation: "C:/Users/User/Downloads",
        }
        drive = Mock()
        drive.rootPath.return_value = "D:/"
        drive.isValid.return_value = True
        drive.isReady.return_value = True
        drive.displayName.return_value = "Audio USB"
        offline = Mock()
        offline.rootPath.return_value = "E:/"
        offline.isValid.return_value = True
        offline.isReady.return_value = False
        with patch("vbc_player.services.filesystem_locations.QStandardPaths.writableLocation", side_effect=lambda kind: values.get(kind, "")), patch("vbc_player.services.filesystem_locations.QStorageInfo.mountedVolumes", return_value=[drive, drive, offline]):
            locations = standard_locations()
        paths = [path for _, path in locations]
        self.assertIn("C:/Users/User/Music", paths)
        self.assertEqual(paths.count("D:/"), 1)
        self.assertNotIn("E:/", paths)

    def test_missing_music_folder_falls_back_to_home(self):
        with patch("vbc_player.services.filesystem_locations.QStandardPaths.writableLocation", return_value=""):
            self.assertEqual(default_directory(), QDir.homePath())


if __name__ == "__main__":
    unittest.main()
