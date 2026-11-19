"""CLI for Colossus background tiles."""
import argparse
from pathlib import Path

from PIL import Image

from .generate import generate
from .validate import validate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("generate", help="Render named 8x8 tiles into one PNG row.")
    build.add_argument("definition", type=Path)
    build.add_argument("output", type=Path)
    build.add_argument("--replace", action="store_true", help="Replace an existing output PNG.")
    check = commands.add_parser("validate", help="Check a PNG and count exact tile patterns.")
    check.add_argument("png", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "generate":
            report = generate(args.definition, args.output, replace=args.replace)
        else:
            report = validate(args.png)
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(report)


if __name__ == "__main__":
    main()
