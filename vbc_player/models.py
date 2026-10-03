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


def demo_tracks():
    """Referências visuais do Figma; não incluem arquivos de áudio."""
    return [
        Track("Ed Sheeran — Azizam", duration_ms=222000, start="21:42:50", end="21:46:32", status="NO AR", subtitle="Pop Internacional • 2025"),
        Track("VBC — A rádio que toca você", "VINHETA", 8000, start="21:46:32", end="21:46:40", status="PRÓXIMO"),
        Track("The Weeknd — Blinding Lights", duration_ms=200000, start="21:46:40", end="21:50:00"),
        Track("Bloco comercial — 21h50", "COMERCIAL", 150000, start="21:50:00", end="21:52:30", status="AGENDADO"),
        Track("Chamada — Jornal da noite", "LOCUÇÃO", 22000, start="21:52:30", end="21:52:52"),
        Track("Dua Lipa — Houdini", duration_ms=185000, start="21:52:52", end="21:55:57"),
    ]
