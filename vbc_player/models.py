from dataclasses import dataclass
import os
from pathlib import Path


AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}


def collect_audio_paths(paths):
    """Expande arquivos e pastas em uma lista ordenada de áudios locais."""
    audio_paths = []
    seen = set()

    def append(path):
        resolved = str(Path(path).resolve())
        if resolved not in seen:
            seen.add(resolved)
            audio_paths.append(resolved)

    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file():
            if path.suffix.casefold() in AUDIO_EXTENSIONS:
                append(path)
            continue
        if not path.is_dir():
            continue
        for root, directories, files in os.walk(path):
            directories.sort(key=str.casefold)
            for filename in sorted(files, key=str.casefold):
                file = Path(root, filename)
                if file.suffix.casefold() in AUDIO_EXTENSIONS:
                    append(file)
    return audio_paths


@dataclass
class Track:
    title: str
    kind: str = "MÚSICA"
    duration_ms: int = 0
    path: str = ""
    start: str = "—"
    end: str = "—"
    status: str = "AGUARDA"
    subtitle: str = "Arquivo local"

    @classmethod
    def from_path(cls, path):
        file = Path(path).resolve()
        return cls(title=file.stem, path=str(file))
