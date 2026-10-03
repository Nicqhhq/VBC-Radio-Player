import json
from dataclasses import asdict
from pathlib import Path

from vbc_player.models import Track


def save_playlist(path, tracks):
    Path(path).write_text(json.dumps({"version": 1, "tracks": [asdict(track) for track in tracks if track.path]}, ensure_ascii=False, indent=2), encoding="utf-8")


def read_playlist(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("tracks"), list):
        raise ValueError("Formato de lista inválido.")
    tracks = []
    for record in data["tracks"]:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str) or not isinstance(record.get("title"), str):
            raise ValueError("Item de lista inválido.")
        duration = record.get("duration_ms", 0)
        if not isinstance(duration, int) or duration < 0:
            raise ValueError("Duração inválida.")
        tracks.append(Track(title=record["title"], path=record["path"], kind=str(record.get("kind", "MÚSICA")), duration_ms=duration))
    return tracks
