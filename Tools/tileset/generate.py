"""Render tiles in definition order and publish the checked PNG."""
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image

from .analyze import Report
from .definitions import PALETTE, SIZE, read_tiles
from .validate import validate


def generate(definition: Path, output: Path, *, replace: bool = False) -> Report:
    if output.suffix.lower() != ".png" or output.resolve() == definition.resolve():
        raise ValueError("Choose a separate .png output file.")
    tiles = read_tiles(definition)
    size = len(tiles) * SIZE, SIZE
    pixels = b"".join(PALETTE[int(shade)] for y in range(SIZE)
                      for tile in tiles for shade in tile[y])
    image = Image.frombytes("RGB", size, pixels)
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, delete=False) as temp:
        pending = Path(temp.name)
    try:
        image.save(pending, format="PNG", compress_level=9)
        report = validate(pending, size)
        if replace:
            os.replace(pending, output)
        else:
            try:
                # Publish the completed file only if the destination is free.
                os.link(pending, output)
            except FileExistsError:
                if pending.read_bytes() != output.read_bytes():
                    raise ValueError(f"{output} already exists. Choose a new name or pass --replace.")
        return report
    finally:
        pending.unlink(missing_ok=True)
