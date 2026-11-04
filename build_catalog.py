"""Build a static JSON catalog from song lyric sheets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
songs = []
for path in sorted(ROOT.glob("songs/*/lyrics.md")):
    opening, header, lyrics = path.read_text(encoding="utf-8").split("---\n", 2)
    metadata = dict(line.split(": ", 1) for line in header.splitlines())
    required = {"title", "artist", "slug", "lyric_status"}
    if opening or not required <= metadata.keys() or metadata["slug"] != path.parent.name or not lyrics.strip():
        raise ValueError(f"Invalid lyric sheet: {path.relative_to(ROOT)}")
    songs.append({**metadata, "lyrics_markdown": lyrics.lstrip("\n")})

if not songs:
    raise ValueError("No lyric sheets found")
print(json.dumps({"schema_version": 1, "songs": songs}, ensure_ascii=False, indent=2))
