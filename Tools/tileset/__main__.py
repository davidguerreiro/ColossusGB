"""CLI for Colossus background tiles."""
import argparse
from pathlib import Path
import sys

from PIL import Image

from .generate import generate
from .normalize import normalize
from .validate import validate

BACKGROUNDS = Path(__file__).resolve().parents[2] / "BackgroundScenes"
INPUT_ERRORS = (OSError, ValueError, SyntaxError, Image.DecompressionBombError)


def normalize_inputs(source: Path, output_dir: Path) -> bool:
    if source.resolve() == output_dir.resolve():
        raise ValueError("Choose an output directory separate from the input directory.")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted(path for path in source.iterdir()
                   if path.suffix.lower() == ".png" and path.is_file())
    if not paths:
        raise ValueError(f"{source} contains no PNG files.")

    success = True
    for path in paths:
        try:
            output = normalize(path, output_dir)
        except INPUT_ERRORS as exc:
            print(f"Error: {path}: {exc}", file=sys.stderr)
            success = False
        else:
            print(f"{path} -> {output}")
    return success


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("generate", help="Render named 8x8 tiles into one PNG row.")
    build.add_argument("definition", type=Path)
    build.add_argument("output", type=Path)
    build.add_argument("--replace", action="store_true", help="Replace an existing output PNG.")
    check = commands.add_parser("validate", help="Check a PNG and count exact tile patterns.")
    check.add_argument("png", type=Path)
    conversion = commands.add_parser("normalize", help="Convert BackgroundScenes PNGs to the DMG palette.")
    conversion.add_argument("--output-dir", type=Path, required=True,
                            help="Separate directory for normalized PNGs.")
    args = parser.parse_args()
    try:
        if args.command == "generate":
            report = generate(args.definition, args.output, replace=args.replace)
        elif args.command == "normalize":
            if not normalize_inputs(BACKGROUNDS, args.output_dir):
                parser.exit(1)
            return
        else:
            report = validate(args.png)
    except INPUT_ERRORS as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(report)


if __name__ == "__main__":
    main()
