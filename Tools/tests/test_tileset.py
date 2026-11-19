import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

from Tools.tileset.definitions import read_tiles
from Tools.tileset.generate import generate
from Tools.tileset.validate import validate


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Assets/definitions/terrain.json"
SAMPLE = ROOT / "Assets/generated/terrain.png"


class TilesetTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        self.png = self.folder / "terrain.png"

    def test_sample_pixels_and_reproducible_export(self):
        report = generate(SOURCE, self.png)
        self.assertEqual((report.size, report.total, report.distinct), ((24, 8), 3, 3))
        other = self.folder / "second.png"
        generate(SOURCE, other)
        self.assertEqual(self.png.read_bytes(), other.read_bytes())
        tiles = json.loads(SOURCE.read_text(encoding="utf-8"))
        self.assertEqual([tile["name"] for tile in tiles], ["grass", "path", "wall"])
        palette = [(7, 24, 33), (48, 104, 80), (134, 192, 108), (224, 248, 207)]
        for path in (self.png, SAMPLE):
            with Image.open(path) as sheet:
                self.assertEqual(sheet.size, (24, 8))
                self.assertEqual(sheet.mode, "RGB")
                for i, tile in enumerate(tiles):
                    for y, row in enumerate(tile["rows"]):
                        for x, shade in enumerate(row):
                            self.assertEqual(sheet.getpixel((8 * i + x, y)), palette[int(shade)])

    def test_duplicate_coordinates_and_orientation(self):
        image = Image.new("RGB", (16, 16), "#071821")
        image.putpixel((8, 0), (48, 104, 80))
        image.putpixel((7, 8), (48, 104, 80))
        image.save(self.png)
        report = validate(self.png)
        self.assertEqual((report.total, report.distinct), (4, 3))
        self.assertEqual(report.duplicate_groups, [[(0, 0), (1, 1)]])

    def test_invalid_definitions(self):
        source = self.folder / "bad.json"
        rows = ["00000000"] * 8
        for invalid, message in [(rows[:7], "8 rows"), (rows[:7] + ["012"], "row 8"),
                                 (["000x0000"] + rows[1:], "column 4")]:
            with self.subTest(invalid=invalid):
                source.write_text(json.dumps([{"name": "grass", "rows": invalid}]))
                with self.assertRaisesRegex(ValueError, message):
                    read_tiles(source)

    def test_dimensions(self):
        Image.new("RGB", (8, 9)).save(self.png)
        with self.assertRaisesRegex(ValueError, "multiples of 8"):
            validate(self.png)
        generate(SOURCE, self.png, replace=True)
        with self.assertRaisesRegex(ValueError, "Expected"):
            validate(self.png, (16, 8))

    def test_off_palette_and_alpha(self):
        for pixel in [(7, 24, 32, 255), (7, 24, 33, 127), (7, 24, 33, 0)]:
            with self.subTest(pixel=pixel):
                image = Image.new("RGBA", (8, 8), "#071821")
                image.putpixel((5, 2), pixel)
                image.save(self.png)
                with self.assertRaisesRegex(ValueError, r"Pixel \(5, 2\)"):
                    validate(self.png)

    def test_indexed_png_transparency(self):
        image = Image.new("P", (8, 8))
        image.putpalette([7, 24, 33])
        image.save(self.png)
        self.assertEqual(validate(self.png).distinct, 1)
        image.save(self.png, transparency=0)
        with self.assertRaisesRegex(ValueError, "alpha 0"):
            validate(self.png)

    def test_existing_output(self):
        self.png.write_bytes(b"existing artwork")
        with self.assertRaisesRegex(ValueError, "already exists"):
            generate(SOURCE, self.png)
        self.assertEqual(self.png.read_bytes(), b"existing artwork")
        generate(SOURCE, self.png, replace=True)
        generate(SOURCE, self.png)
        self.assertEqual(list(self.folder.iterdir()), [self.png])

    def test_cli(self):
        command = [sys.executable, "-m", "Tools.tileset", "validate"]
        for path, success in [(SAMPLE, True), (self.png, False)]:
            with self.subTest(path=path):
                result = subprocess.run(command + [str(path)], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode == 0, success)
                if success:
                    self.assertIn("3 distinct", result.stdout)
                else:
                    self.assertIn("Error:", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
