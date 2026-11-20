# Colossus — Project Context

## Overview
**Colossus** is a single-player, top-down action-adventure game inspired by classic Zelda titles, especially *The Legend of Zelda: Link's Awakening* on Game Boy. The game will feature exploration, towns, NPCs, conversations, environmental puzzles, and **real-time** combat on the overworld map. It is **not** a turn-based RPG.

There are two planned adaptations sharing a story, characters, and world:
1. **First release:** a deliberately small, original-Game-Boy-compatible 2D game built in **GB Studio**. Planned as a free release on itch.io, with a possible paid physical edition made to order.
2. **Later release:** a modern stylized 3D adaptation in **Unity**. The Unity project's technical architecture is separate from the GB Studio project.

This repository currently focuses on the **Game Boy prototype** and its graphics tooling, not the later Unity version. The user is preparing a broader game design document; do not invent lore, characters, plot, or production mechanics beyond what is documented.

## Confirmed platform and constraints
- Target hardware: **original monochrome Game Boy (DMG)**, not Game Boy Color-only.
- Primary engine: **GB Studio**.
- Development machine now: **Windows PC**; later transition to **macOS**. The tooling must run on both.
- Visual style for the prototype: extremely simple placeholder pixel art; functional readability is more important than polish.
- DMG graphics: four shade values per palette; backgrounds use 8×8-pixel tiles. Hardware graphics use 2 bits per pixel, i.e. 16 bytes of raw graphics data per 8×8 tile. These facts alone do not establish the actual scene limits enforced by GB Studio.
- Confirm the exact accepted PNG colors, background dimensions, tile budgets, sprite transparency conventions, and actor sprite restrictions against the installed GB Studio version before implementing import-specific rules.

## Toolchain and ownership of each stage
1. **ChatGPT / Codex CLI:** planning and code assistance; Codex works on local project files.
2. **Python 3 + Pillow:** deterministic creation of small reusable tilesets, exact DMG palette normalization for exported backgrounds, image validation, and tile-pattern analysis.
3. **GB Scene Tiler:** the user's chosen **visual background/level editor**. Import Python-generated tilesets, paint village/interior/outdoor scenes, and export finished background PNGs.
4. **GB Studio:** import the background PNGs; place actors, collisions, triggers, interactions, dialogues, puzzles, and combat logic; compile a playable Game Boy ROM.
5. **Git + VS Code:** version control and editing. Codex CLI is intended to authenticate using the user's ChatGPT subscription, subject to plan usage limits.

**Critical distinction:** GB Studio does not serve as the tile-painting editor in this workflow. Python generates *tilesets*, GB Scene Tiler builds *backgrounds*, and GB Studio implements *gameplay*.

## Graphics pipeline objectives
- Design tiles using editable 8×8 pixel matrices or similarly explicit structured definitions.
- Produce native-resolution PNGs with exactly controlled palette values; never resize with smoothing.
- Organize reusable terrain/building tiles into importable tileset images.
- Report duplicate and unique tiles and warn about budget concerns without inventing hardware-compatibility guarantees.
- Later, if needed, add actor sprites, directional animation frames, swords, slimes, NPCs, hearts, and switches using separately verified GB Studio sprite conventions.
- The first test set should be **grass, path, and wall**. A village set will eventually need houses, roofs, doors, windows, roads, trees, fences, and interior furnishings.
- Do not optimize merely for compressed PNG bytes: what matters for the game is the engine's tile allocation and compiled ROM/VRAM behavior.

## Game-development principles
- Small scope and simplicity are deliberate project constraints.
- Prefer **native GB Studio events and features** wherever possible.
- Use custom events/plugins or C only for a demonstrated need; do not eject and modify the engine by default.
- No custom C game framework for the Game Boy game. The user's separate Unity RPG framework plans do not apply here.
- Use placeholder art and simple mechanics for the vertical slice; defer production-quality art and elaborate systems.
- Test on an emulator and, if available later, real compatible hardware.

## Design notes
- Overworld movement in four directions.
- One directional sword attack and simple hit/damage logic.
- At least one moving enemy (a slime) that can damage the player and be defeated.
- A small village with houses, static NPCs, moving NPCs, and conversations triggered by player interaction.
- A connected exterior combat area, an enterable interior, a basic environmental puzzle, and save/load.
- Prototype-only proposed tuning: player 3 HP, slime 2 HP, sword 1 damage, brief post-hit invulnerability. These values are **suggestions, not final design decisions**.

## Open questions to validate rather than assume
- Installed versions of GB Studio and GB Scene Tiler.
- Exact tileset image arrangement expected by GB Scene Tiler.
- Accepted DMG PNG palette and transparency handling for each asset category.
- Current GB Studio background size, tile-count, and sprite limits for the selected scene types.
- Whether any planned combat mechanics need extensions beyond native GB Studio events.
