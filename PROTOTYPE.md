# Colossus — Game Boy Vertical Slice Checklist

## Goal
Create one small, coherent, playable top-down adventure prototype for the **original Game Boy (DMG)** in **GB Studio**, using placeholder art and mostly native engine features. The player should be able to explore a village, enter a house, talk to NPCs, visit a nearby field, fight and defeat a moving slime with a sword, solve a simple puzzle, save, and reload.

The list below is a **scope checklist**, not a claim that any tasks are complete. Mark boxes only after testing them.

## Phase 0 — Graphics tooling (current first priority)
- [ ] Set up Python 3, Pillow, tests, and a cross-platform CLI.
- [ ] Generate a basic 8×8 grass/path/wall tileset PNG from editable pixel definitions.
- [ ] Validate dimensions, allowed colors, tile alignment, and tile uniqueness.
- [ ] Import the generated tileset into GB Scene Tiler and verify the tile grid and colors.
- [ ] Paint and export a small test background PNG; import it into GB Studio.

## Phase 1 — Player and scenes
- [ ] Create the player character with four-direction movement and simple animations.
- [ ] Create a small village with streets, paths, decoration, and approximately 3–4 houses.
- [ ] Create a nearby exterior area with trees, obstacles, and space for combat.
- [ ] Create at least one house interior and working entry/exit transitions.

## Phase 2 — NPCs and dialogue
- [ ] Create at least one static NPC in the village.
- [ ] Create at least one NPC that walks along a simple path or movement pattern.
- [ ] Create another NPC inside a house (target: approximately 3 NPCs total).
- [ ] Allow the player to interact with NPCs using a button and display dialogue boxes.

## Phase 3 — Real-time combat
- [ ] Equip/use a sword that attacks in the direction the player faces.
- [ ] Detect sword hits and reduce enemy HP.
- [ ] Create a basic slime enemy that moves around the map.
- [ ] Let the slime damage the player on contact.
- [ ] Add brief invulnerability after the player takes damage, if practical.
- [ ] Defeat the slime when its HP reaches zero and remove it from the scene.

Suggested prototype values only: player 3 HP, slime 2 HP, sword 1 damage per successful hit. Keep enemy AI simple (e.g., limited wandering).

## Phase 4 — Other mechanics
- [ ] Add one simple environmental puzzle, such as a switch that opens a door.
- [ ] Implement save and load for the relevant player/progress state.

## Phase 5 — Verification and export
- [ ] Export a working Game Boy-compatible ROM.
- [ ] Test the connected gameplay flow in an emulator: village → NPC conversation → house → exterior → slime combat → puzzle → save/load.
- [ ] Fix critical bugs; avoid adding unplanned features before the vertical slice works.

## Scope boundaries
- **In scope:** functional placeholder art, a small number of scenes, simple NPCs, one basic enemy, one weapon, one puzzle, and saving.
- **Out of scope for this prototype:** polished production art, complex combat, multiple enemy families, full story, elaborate inventories, multiplayer, Unity adaptation, custom engine framework, and speculative optimization systems.
- **Preferred implementation:** native GB Studio events first; C or plugins only if a concrete requirement cannot be met cleanly otherwise.

## Graphics workflow
```text
Editable 8×8 tile definitions
           ↓
Python + Pillow generator
           ↓
PNG validation and unique-tile report
           ↓
GB Scene Tiler (visual background editing)
           ↓
Flattened background PNG
           ↓
GB Studio (actors, collisions, events, gameplay)
           ↓
Game Boy ROM and emulator testing
```

## Immediate next milestone
A **grass/path/wall tileset PNG** that is generated deterministically on Windows, passes automated checks, imports correctly into GB Scene Tiler, and can be used to export a test background that GB Studio accepts. Once verified, expand the tile library to the village and house interiors.
