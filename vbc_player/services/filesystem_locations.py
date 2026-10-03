"""Locais do usuário e volumes informados pelo sistema operacional via Qt."""
from PySide6.QtCore import QDir, QStandardPaths, QStorageInfo


def standard_locations():
    locations = []
    seen = set()
    for label, kind in (
        ("Músicas", QStandardPaths.StandardLocation.MusicLocation),
        ("Pasta pessoal", QStandardPaths.StandardLocation.HomeLocation),
        ("Downloads", QStandardPaths.StandardLocation.DownloadLocation),
        ("Documentos", QStandardPaths.StandardLocation.DocumentsLocation),
        ("Área de trabalho", QStandardPaths.StandardLocation.DesktopLocation),
    ):
        path = QStandardPaths.writableLocation(kind)
        if path and path not in seen:
            locations.append((label, path))
            seen.add(path)
    for volume in QStorageInfo.mountedVolumes():
        path = volume.rootPath()
        if volume.isValid() and volume.isReady() and path and path not in seen:
            name = volume.displayName() or volume.name() or path
            locations.append((f"{name} ({path})" if name != path else path, path))
            seen.add(path)
    return locations


def default_directory():
    music = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MusicLocation)
    return music if music and QDir(music).exists() else QDir.homePath()
