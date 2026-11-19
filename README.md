# Colossus background tiles

[Download the native-size sample sheet](Assets/generated/terrain.png) to try grass, path and wall in GB Scene Tiler. The 24×8 PNG has three 8×8 cells in that order, with zero margin or spacing.

## Generate and check tiles

From the repository root in Windows PowerShell, set up the local environment once. Development was tested with 64-bit Python 3.14.7.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Run the generator, inspect an existing PNG, or run the tests:

```powershell
.\.venv\Scripts\python -m Tools.tileset generate Assets/definitions/terrain.json Assets/generated/terrain.png
.\.venv\Scripts\python -m Tools.tileset validate Assets/generated/terrain.png
.\.venv\Scripts\python -m unittest discover -s Tools/tests -v
```

On macOS, create the environment with `python3 -m venv .venv` and use `.venv/bin/python` for the remaining commands. Paths are relative to the current directory. Use a new output filename for a variation or add `--replace` to intentionally update an existing generated PNG.

## Design and output

Ask Codex to design a tile or edit [the source matrices](Assets/definitions/terrain.json) yourself. Each named tile has eight strings of eight digits. A digit specifies one opaque pixel. From darkest to lightest, `0` = `#071821`, `1` = `#306850`, `2` = `#86c06c`, and `3` = `#e0f8cf`. A tile may use a subset.

Python lays the tiles side by side in JSON array order. The command runs offline and reads the saved pixels directly. Fixed definitions and palette produce identical pixels. Tests check repeatable PNG bytes within the same environment. The generator validates the encoded file before publishing it.

Expected sample report: `24x8 px | 3 tiles | 3 distinct | 0 duplicates`. Validation accepts single-frame PNGs using up to 8 bits per channel. It checks grid alignment and each decoded pixel, including transparency in indexed PNGs. A failing command exits with a nonzero status. Pixel and tile coordinates start at (0, 0) in the upper left. Duplicate locations reference the first identical 8×8 pattern, preserving orientation. The report measures patterns in the image. GB Studio determines the scene budget and compiled ROM/VRAM usage.

## Manual editor check

The Windows installation used for development has GB Scene Tiler 1.0.0 and GB Studio 4.3.2. Inspection of Scene Tiler's installed importer confirmed PNG input, native-pixel decoding and an 8×8 grid starting at the image origin. The interactive round trip below still needs verification. The author documents tileset import, the default scene size and flat PNG export. [GB Scene Tiler](https://pcool.itch.io/gb-scene-tiler)

- [ ] In GB Scene Tiler, choose **Import Tileset** and open `Assets/generated/terrain.png`. Confirm three individually selectable cells, from grass on the left to wall on the right.
- [ ] Start a 160×144 scene, fill it with grass, and paint a strip of path and a strip of wall. Use the four project colors. Check adjacent edges and export a flattened PNG at **1×**.
- [ ] Run the same `validate` command on the exported PNG. A fully filled scene made only from the three unmodified tiles should report 360 cells and 3 distinct patterns. An unexpected color error gives the pixel coordinate to inspect.
- [ ] Put the flattened PNG under a fresh filename in `GBGame/assets/backgrounds/`, select it as a test scene's background in GB Studio, and inspect the shades and alignment in the editor and preview. Record the result in the Phase 0 checklist after testing. [GB Studio background import](https://www.gbstudio.dev/docs/assets/backgrounds/)
