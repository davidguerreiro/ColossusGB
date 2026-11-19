"""Editable tiles use one character per pixel, darkest shade first."""
import json
from pathlib import Path

SIZE = 8
PALETTE = tuple(bytes.fromhex(color) for color in ("071821", "306850", "86c06c", "e0f8cf"))


def read_tiles(path: Path) -> list[list[str]]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("Expected a nonempty JSON array of named tiles.")
    tiles = []
    names = set()
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict) or not isinstance(record.get("name"), str):
            raise ValueError(f"Tile {index} needs a string name.")
        name = record["name"]
        if not name.strip() or name in names:
            raise ValueError(f"Tile {index} has an empty or duplicate name: {name!r}.")
        names.add(name)
        rows = record.get("rows")
        if not isinstance(rows, list) or len(rows) != SIZE:
            raise ValueError(f"{name}: expected {SIZE} rows.")
        for y, row in enumerate(rows, 1):
            if not isinstance(row, str) or len(row) != SIZE:
                raise ValueError(f"{name}, row {y}: expected a string of {SIZE} digits.")
            for x, shade in enumerate(row, 1):
                if shade not in "0123":
                    raise ValueError(f"{name}, row {y}, column {x}: invalid shade {shade!r}; use 0–3.")
        tiles.append(rows)
    return tiles
