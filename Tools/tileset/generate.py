"""Render tiles in definition order and publish the checked PNG."""
import os
from pathlib import Path

from PIL import Image

from .analyze import Report
from .definitions import PALETTE, SIZE, read_tiles
from .png import staged_png
from .validate import validate


def generate(definition: Path, output: Path, *, replace: bool = False) -> Report:
    if output.suffix.lower() != ".png" or output.resolve() == definition.resolve():
        raise ValueError("Choose a separate .png output file.")
    tiles = read_tiles(definition)
    size = len(tiles) * SIZE, SIZE
    pixels = b"".join(PALETTE[int(shade)] for y in range(SIZE)
                      for tile in tiles for shade in tile[y])
    image = Image.frombytes("RGB", size, pixels)
    with staged_png(image, output) as pending:
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
