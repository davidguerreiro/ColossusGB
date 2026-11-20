"""Read and check the encoded PNG before comparing tile patterns."""
from pathlib import Path

from .analyze import Report, analyze
from .definitions import PALETTE, SIZE
from .png import open_png

ALLOWED = {tuple(color) for color in PALETTE}


def validate(path: Path, expected_size: tuple[int, int] | None = None) -> Report:
    with open_png(path) as png:
        if expected_size and png.size != expected_size:
            raise ValueError(f"Expected {expected_size} pixels, found {png.size}.")
        if png.width % SIZE or png.height % SIZE:
            raise ValueError(f"{png.width}x{png.height}: both dimensions must be multiples of {SIZE}.")
        rgba = png.convert("RGBA")
    pixels = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = pixels[x, y]
            if a != 255 or (r, g, b) not in ALLOWED:
                raise ValueError(f"Pixel ({x}, {y}) is #{r:02x}{g:02x}{b:02x}, alpha {a}; "
                                 "use an opaque color from the project palette.")
    return analyze(rgba)
