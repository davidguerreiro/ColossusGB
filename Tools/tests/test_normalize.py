from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PIL import Image

from Tools.tileset import __main__ as cli
from Tools.tileset.normalize import normalize
from Tools.tileset.validate import validate


SOURCE = [(233, 242, 228), (181, 214, 156), (91, 144, 116), (36, 50, 66)]
LEVEL_1_SOURCE = [(232, 248, 224), (176, 240, 136), (80, 152, 120), (32, 40, 80)]
TARGET = [(224, 248, 207), (134, 192, 108), (48, 104, 80), (7, 24, 33)]


class NormalizeTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        self.source = self.folder / "source.png"
        self.output_dir = self.folder / "converted"

    def run_batch_expecting_error(self):
        argv = ["Tools.tileset", "normalize", "--output-dir", str(self.output_dir)]
        with patch.object(cli, "BACKGROUNDS", self.folder), patch.object(sys, "argv", argv):
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()) as stderr:
                with self.assertRaises(SystemExit) as exit_info:
                    cli.main()
        self.assertEqual(exit_info.exception.code, 1)
        return stderr.getvalue()

    def test_exact_rgb_conversion_and_dimensions(self):
        size = (13, 7)
        shades = [2, 0, 1, 0, 3, 2, 3] * 13
        for index, palette in enumerate((SOURCE, LEVEL_1_SOURCE)):
            with self.subTest(palette=palette):
                source = self.folder / f"palette_{index}.png"
                image = Image.new("RGB", size)
                image.putdata([palette[shade] for shade in shades])
                image.save(source)
                with Image.open(normalize(source, self.output_dir)) as output:
                    self.assertEqual(output.size, size)
                    self.assertEqual(output.mode, "RGB")
                    self.assertEqual(output.get_flattened_data(), tuple(TARGET[shade] for shade in shades))

    def test_indexed_png_converts_to_valid_background(self):
        image = Image.new("P", (8, 8))
        image.putpalette(bytes(channel for color in SOURCE for channel in color))
        image.putdata([0, 1, 2, 3] * 16)
        image.save(self.source)
        output = normalize(self.source, self.output_dir)
        self.assertEqual(validate(output).size, (8, 8))
        with Image.open(output) as image:
            self.assertEqual(image.get_flattened_data(), tuple(TARGET * 16))

    def test_lists_all_unexpected_colors_including_transparent_pixels(self):
        image = Image.new("RGBA", (8, 8), (*SOURCE[0], 255))
        image.putdata([(*SOURCE[0], 127), (18, 52, 86, 255), (*TARGET[0], 255)] +
                      [(*SOURCE[0], 255)] * 61)
        image.save(self.source)
        with self.assertRaisesRegex(ValueError, r"#123456 .*#E0F8CF .*#E9F2E4 \(alpha 127\)"):
            normalize(self.source, self.output_dir)
        self.assertFalse(self.output_dir.exists())

    def test_preserves_source_and_existing_output(self):
        Image.new("RGB", (8, 8), SOURCE[0]).save(self.source)
        original = self.source.read_bytes()
        with self.assertRaisesRegex(ValueError, "separate"):
            normalize(self.source, self.source.parent)
        self.output_dir.mkdir()
        output = self.output_dir / self.source.name
        output.write_bytes(b"existing artwork")
        with self.assertRaisesRegex(ValueError, "already exists"):
            normalize(self.source, self.output_dir)
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual(output.read_bytes(), b"existing artwork")
        self.assertEqual(list(self.output_dir.iterdir()), [output])

    def test_directory_processes_valid_pngs_and_reports_failures(self):
        bad = self.folder / "bad.png"
        Image.new("RGB", (8, 8), "#123456").save(bad)
        second = self.folder / "second.PNG"
        for path in (self.source, second):
            Image.new("RGB", (8, 8), SOURCE[0]).save(path)
        (self.folder / "scene.gbscene.json").write_text("{}", encoding="utf-8")
        originals = {path: path.read_bytes() for path in (bad, self.source, second)}

        errors = self.run_batch_expecting_error()

        self.assertIn("bad.png", errors)
        self.assertIn("#123456", errors)
        self.assertEqual({path.name for path in self.output_dir.iterdir()}, {"source.png", "second.PNG"})
        self.assertEqual({path: path.read_bytes() for path in originals}, originals)

    def test_batch_creates_output_directory_when_no_pngs_exist(self):
        self.assertIn("contains no PNG files", self.run_batch_expecting_error())
        self.assertTrue(self.output_dir.is_dir())
