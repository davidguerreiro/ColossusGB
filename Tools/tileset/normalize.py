"""Map opaque GB Scene Tiler pixels to the Colossus DMG palette."""
import os
from pathlib import Path

from PIL import Image

from .definitions import PALETTE
from .png import open_png, staged_png

# Match shades in the project palette's darkest-to-lightest order.
SOURCE_PALETTES = (
    ("243242", "5B9074", "B5D69C", "E9F2E4"),
    ("202850", "509878", "B0F088", "E8F8E0"),  # Observed in BackgroundScenes/level_1.png.
)
COLOR_MAP = {(*bytes.fromhex(color), 255): target
             for source_palette in SOURCE_PALETTES
             for color, target in zip(source_palette, PALETTE, strict=True)}


def normalize(source: Path, output_dir: Path) -> Path:
    if source.suffix.lower() != ".png":
        raise ValueError("Expected a .png input file.")
    if source.parent.resolve() == output_dir.resolve():
        raise ValueError("Choose an output directory separate from the input directory.")

    with open_png(source) as png:
        rgba = png.convert("RGBA")
    pixels = rgba.get_flattened_data()
    unexpected = set(pixels) - COLOR_MAP.keys()
    if unexpected:
        colors = ", ".join(f"#{r:02X}{g:02X}{b:02X} (alpha {a})"
                           for r, g, b, a in sorted(unexpected))
        raise ValueError(f"Unexpected colors in the GB Scene Tiler export: {colors}.")

    image = Image.frombytes("RGB", rgba.size, b"".join(COLOR_MAP[pixel] for pixel in pixels))
    output = output_dir / source.name
    with staged_png(image, output) as pending:
        try:
            os.link(pending, output)
        except FileExistsError as exc:
            raise ValueError(f"{output} already exists. Choose a different output directory.") from exc
    return output
