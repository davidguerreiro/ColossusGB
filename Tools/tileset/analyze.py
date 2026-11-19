"""Group identical 8×8 pixel patterns in reading order."""
from dataclasses import dataclass

from PIL import Image

from .definitions import SIZE


@dataclass
class Report:
    size: tuple[int, int]
    total: int
    distinct: int
    duplicate_groups: list[list[tuple[int, int]]]

    def __str__(self) -> str:
        w, h = self.size
        lines = [f"{w}x{h} px | {self.total} tiles | {self.distinct} distinct | "
                 f"{self.total - self.distinct} duplicates"]
        for first, *others in self.duplicate_groups:
            lines.append(f"Tile {first} repeated at " + ", ".join(map(str, others)))
        return "\n".join(lines)


def analyze(image: Image.Image) -> Report:
    groups = {}
    for y in range(0, image.height, SIZE):
        for x in range(0, image.width, SIZE):
            pattern = image.crop((x, y, x + SIZE, y + SIZE)).tobytes()
            groups.setdefault(pattern, []).append((x // SIZE, y // SIZE))
    total = (image.width // SIZE) * (image.height // SIZE)
    return Report(image.size, total, len(groups), [g for g in groups.values() if len(g) > 1])
