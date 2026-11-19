# Colossus — Instructions for Coding Agents

## Read first
Read `PROJECT.md` and `PROTOTYPE.md` before proposing or changing code. These files describe the project's goals and scope. If a technical assumption conflicts with the installed version of GB Studio or GB Scene Tiler, verify it and report the discrepancy rather than silently guessing.

IMPORTANT: AI will handle the python tool code/development and GB Graphic Assets creation. The User will use the tilesets to create the map PNGS in GB Scene Tiler and GB Studio to create the gameplay and build the ROM. You will also assists with some other requests.

## Mission
Build a **small, deterministic, cross-platform Python tool** that generates and validates reusable **8×8-pixel tilesets** for the original monochrome Game Boy (DMG). The user will import these tilesets into **GB Scene Tiler**, paint scene backgrounds there, export flattened PNG backgrounds, and import those PNGs into **GB Studio**.

**Do not build a map editor.** GB Scene Tiler is the map editor. **Do not build a game engine or a C framework.** Use GB Studio's native functionality for game logic; consider custom plugins or C only if a specific feature cannot reasonably be implemented natively.

## Engineering principles
- Prioritize simplicity, correctness, small scope, reproducibility, and clear documentation over elaborate architecture.
- Target Windows PowerShell first; preserve macOS compatibility for later. Avoid hard-coded paths and OS-specific shell assumptions.
- Use Python 3 and Pillow for image work. Prefer the standard library for everything else. Pin or document dependencies in a minimal `requirements.txt` or `pyproject.toml`.
- Separate tile definitions, image generation, validation, and tile analysis into small testable modules. Avoid speculative abstractions, GUI, server, cloud services, and unnecessary dependencies.
- All production graphics are **native-resolution pixel art**: integer coordinates, no interpolation, no antialiasing, no semi-transparent pixels, no accidental palette colors.
- Generate exact, deterministic PNGs and preserve editable source definitions. Do not confuse PNG file size with Game Boy ROM/VRAM usage.
- For DMG background tilesets and flattened backgrounds, allow only opaque pixels from this palette, darkest to lightest: `#071821`, `#306850`, `#86c06c`, `#e0f8cf`. A tile may use any subset. Reject off-palette pixels during validation and report their location. Check the target GB Studio version's import rules separately for actor sprites. [GB Studio background color requirements](https://www.gbstudio.dev/docs/assets/backgrounds/)
- Validate dimensions, palette membership, tile grid alignment, and tile uniqueness. Make failures actionable.
- Count unique 8×8 patterns for background analysis. Clearly distinguish raw pattern counts from the actual GB Studio scene tile budget and from compiled memory consumption.
- Treat GB Studio's tile limits, sprite rules, background size limits, and PNG import behavior as **version-specific**; confirm them from current official documentation and a test import. Never promise compatibility from PNG validation alone.
- Provide concise Windows PowerShell commands to install, generate, validate, and run tests; document macOS equivalents where useful.
- Include automated tests for core algorithms and representative sample assets.
- Before adding a feature, explain its practical value for the prototype. Ask before expanding scope significantly.

## Initial deliverable (MVP for the graphics tool)
1. A simple CLI that produces a native-resolution PNG tileset from explicitly defined 8×8 pixel matrices.
2. Three deliberately simple sample tiles: grass, path, and wall (with a consistent four-shade palette).
3. Validation of exact dimensions, palette, and tile alignment; a report of total and distinct 8×8 tiles and duplicates.
4. Tests, usage instructions, and an example export that the user can try importing into GB Scene Tiler.
5. A short manual verification checklist for GB Scene Tiler and GB Studio import.

Do **not** implement automatic sprite animation, actor sprite formats, an interactive tileset editor, complex procedural generation, or C integration in this first iteration. Those are potential future increments.

## Collaboration and workflow
- The user is using ChatGPT for design/planning and Codex CLI for implementation. The repository files are the durable source of truth; Codex does not automatically inherit this chat.
- When changing decisions, update the relevant Markdown documentation and mention the change.
- Before modifying files, inspect the repository and existing tests. Prefer small, reviewable changes.
- Never overwrite user-created art or GB Studio project files without explicit approval.
- Keep generated assets distinct from editable definitions; use Git for source and documentation.
- Report what was changed, tests run, any failures, and the exact next step for the user.

## Suggested repository layout (adapt to existing files)
```text
Colossus/
  AGENTS.md
  PROJECT.md
  PROTOTYPE.md
  tools/              # Python source and tests
  assets/
    definitions/      # Editable tile specifications
    generated/        # Exported PNG tilesets
  gbstudio/           # GB Studio project (when created)
```

## First task for Codex
Inspect these three documents and the repository. Propose the minimal CLI design, then implement a deterministic grass/path/wall tileset generator, PNG validator, unique-tile analyzer, tests, and README. Verify assumptions about GB Scene Tiler's tileset import format before claiming the output is import-ready. Keep the scope strictly to the tileset pipeline.
