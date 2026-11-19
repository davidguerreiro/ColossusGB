"""Read and check the encoded PNG before comparing tile patterns."""
from pathlib import Path

from PIL import Image

from .analyze import Report, analyze
from .definitions import PALETTE, SIZE

ALLOWED = {tuple(color) for color in PALETTE}


def validate(path: Path, expected_size: tuple[int, int] | None = None) -> Report:
    with path.open("rb") as source:
        with Image.open(source, formats=["PNG"]) as png:
            png.verify()
        # Pillow downconverts 16-bit RGB samples when decoding. Require an
        # 8-bit or lower source so off-palette values cannot be rounded away.
        source.seek(24)
        if source.read(1) == b"\x10":
            raise ValueError("Export the PNG with 8-bit RGB or indexed color.")
        source.seek(0)
        with Image.open(source, formats=["PNG"]) as png:
            if png.n_frames != 1:
                raise ValueError("Expected a single-frame background PNG.")
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
