"""Read exact PNG samples and stage complete PNGs for publication."""
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image


@contextmanager
def open_png(path: Path):
    with path.open("rb") as source:
        with Image.open(source, formats=["PNG"]) as png:
            png.verify()
        # Pillow rounds 16-bit RGB samples when decoding.
        source.seek(24)
        if source.read(1) == b"\x10":
            raise ValueError("Export the PNG with 8-bit RGB or indexed color.")
        source.seek(0)
        with Image.open(source, formats=["PNG"]) as png:
            if png.n_frames != 1:
                raise ValueError("Expected a single-frame background PNG.")
            yield png


@contextmanager
def staged_png(image: Image.Image, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, delete=False) as temp:
        pending = Path(temp.name)
    try:
        image.save(pending, format="PNG", compress_level=9)
        yield pending
    finally:
        pending.unlink(missing_ok=True)
