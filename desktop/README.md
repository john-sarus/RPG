# Desktop Port - There Will Be Kobolds

Desktop port of the iOS JRPG using Pygame. This port creates a compatibility layer (shim) that replicates Pythonista's `scene`, `sound`, and `ui` APIs, allowing the game to run unmodified on Windows, macOS, and Linux.

## Overview

This desktop port uses **Pygame-CE** (Community Edition) to emulate Pythonista's iOS game framework. All game logic, data files, and scene code remain unchanged — only the rendering and input systems are adapted through a shim layer.

**Key Features:**
- Full keyboard and mouse support
- 1024x896 window (4x scale of 256x224 logical resolution)
- Headless testing infrastructure for CI/CD
- Development tools for battle testing, stat viewing, map inspection, and save editing
- 100% code compatibility with iOS version

## Prerequisites

- **Python 3.8+** (tested on 3.8-3.12)
- **pip** package manager
- **Windows/macOS/Linux** (any platform that supports Pygame)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd C:\Users\johnr\Documents\JasonMullan\RPG
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r desktop/requirements.txt
   ```

   This installs:
   - `pygame-ce>=2.4.1` - Graphics and input handling
   - `pytest>=7.0` - Testing framework

3. **Verify installation:**
   ```bash
   python desktop/run.py
   ```

   You should see a 1024x896 window open with the game title screen.

## Running the Game

**Launch the game:**
```bash
python desktop/run.py
```

**On Windows (from project root):**
```bash
python desktop\run.py
```

**On macOS/Linux:**
```bash
python3 desktop/run.py
```

The game will open in a Pygame window at 1024x896 resolution (4x the logical 256x224 SNES-era resolution).

## Controls

### Keyboard Controls

| Key(s) | Action |
|--------|--------|
| **Arrow Keys** | Navigate menus / Move character on map |
| **W/A/S/D** | Navigate menus / Move character on map (alternative) |
| **Enter** | Confirm selection / Interact with NPCs |
| **Space** | Confirm selection (alternative to Enter) |
| **Escape** | Cancel / Back / Open menu |
| **M** | Open menu (in exploration mode) |
| **1-9** | Quick select menu items (number keys) |

**Navigation Tips:**
- Use arrow keys or WASD to cycle through menu options
- Press Enter or Space to select the highlighted option
- Press Escape to go back or cancel

### Mouse Controls

| Input | Action |
|-------|--------|
| **Left Click** | Select button / Interact with UI element |
| **Right Click** | Cancel / Go back (context-sensitive) |

**Coordinate System:**
- The game uses a logical 256x224 resolution (SNES-era)
- Mouse clicks are automatically converted from window coordinates (1024x896) to logical coordinates
- Y-axis origin is bottom-left (Pythonista convention), not top-left (Pygame convention)

## Development Tools

The desktop port includes four CLI development tools for testing and debugging. All tools run headlessly (no window) and use `SDL_VIDEODRIVER=dummy` for automation.

### 1. Battle Tester (`battle_tester.py`)

Automated combat simulation for testing battle balance and character performance.

**Usage:**
```bash
# Single character vs weak enemy
python desktop/tools/battle_tester.py --party javin --level 1 --enemies infected_kobold_weak

# Full party at level 10 vs multiple enemies (verbose output)
python desktop/tools/battle_tester.py --party javin,fei,iris --level 10 --enemies skeleton,skeleton --verbose

# Run 5 rounds of battles for statistical analysis
python desktop/tools/battle_tester.py --party javin --level 5 --enemies infected_kobold_weak --rounds 5
```

**Options:**
- `--party NAMES` - Comma-separated character IDs (lowercase: javin, fei, iris, etc.)
- `--level N` - Level for all party members (1-99, default: 1)
- `--enemies NAMES` - Comma-separated enemy IDs (snake_case: infected_kobold_weak, skeleton, etc.)
- `--rounds N` - Number of battle rounds (default: 1)
- `--verbose` - Print turn-by-turn battle details

**Output:**
- Battle summary (winner, turns taken, remaining HP)
- Average statistics across multiple rounds
- Damage breakdown and status effects

### 2. Stat Viewer (`stat_viewer.py`)

View and compare character stats and growth curves at any level.

**Usage:**
```bash
# View single character stats at level 50
python desktop/tools/stat_viewer.py --character javin --level 50

# Compare two characters side-by-side at level 25
python desktop/tools/stat_viewer.py --compare javin,fei --level 25

# Show summary table for all 12 characters at level 1
python desktop/tools/stat_viewer.py --all --level 1

# View endgame stats for all characters
python desktop/tools/stat_viewer.py --all --level 99
```

**Options:**
- `--character NAME` - Character ID (lowercase: javin, fei, iris, etc.)
- `--level N` - Level to calculate stats at (1-99, default: 1)
- `--compare NAME1,NAME2` - Compare two characters side-by-side
- `--all` - Show summary table for all characters

**Output:**
- Base stats and growth rates
- Calculated stats at specified level
- Class information and special abilities
- Side-by-side comparison with stat highlights

### 3. Map Inspector (`map_inspector.py`)

Inspect game map data: locations, NPCs, encounter zones, transitions, and dungeons.

**Usage:**
```bash
# List all 17 locations
python desktop/tools/map_inspector.py --list

# Show details for a location
python desktop/tools/map_inspector.py --location imperial_city

# Show NPCs at a location
python desktop/tools/map_inspector.py --npcs imperial_city

# Show exits/entrances at a location
python desktop/tools/map_inspector.py --transitions imperial_city

# Show encounter data for a location
python desktop/tools/map_inspector.py --encounters surface_forest

# List all 10 dungeons
python desktop/tools/map_inspector.py --dungeons

# Show dungeon floor layout
python desktop/tools/map_inspector.py --dungeon tutorial_warren
```

**Options:**
- `--list` - List all locations with IDs and names
- `--location NAME` - Show location properties (dimensions, terrain, encounter rate)
- `--npcs NAME` - Show NPCs at a location with positions and dialogue IDs
- `--transitions NAME` - Show exit/entrance points with coordinates
- `--encounters NAME` - Show encounter table (enemies, weights, party sizes)
- `--dungeons` - List all dungeons
- `--dungeon NAME` - Show dungeon floor details and room connections

### 4. Save Inspector (`save_inspector.py`)

View, compare, and edit JSON save files.

**Usage:**
```bash
# List all save files with summary
python desktop/tools/save_inspector.py --list

# View detailed save contents (slot 1-100, autosave, or quicksave)
python desktop/tools/save_inspector.py --view 1
python desktop/tools/save_inspector.py --view autosave

# Compare two save files
python desktop/tools/save_inspector.py --diff 1 2

# Edit save files (creates .bak backup automatically)
python desktop/tools/save_inspector.py --set-flag 1 met_orisia true
python desktop/tools/save_inspector.py --add-item 1 potion 10
python desktop/tools/save_inspector.py --set-level 1 javin 50
```

**Options:**
- `--list` - List all save files with timestamp and party summary
- `--view SLOT` - Pretty-print save contents (slot number, autosave, or quicksave)
- `--diff SLOT1 SLOT2` - Compare two saves, show only differences
- `--set-flag SLOT FLAG VALUE` - Modify a story flag (creates backup)
- `--add-item SLOT ITEM COUNT` - Add items to inventory (creates backup)
- `--set-level SLOT CHAR LEVEL` - Change character level (creates backup, recalculates stats)
- `--save-dir PATH` - Custom save directory (default: saves)

**Important Notes:**
- All edit operations create a `.bak` backup file before modifying
- Save files are JSON in the `saves/` directory
- Manual saves: `save_001.json` through `save_100.json`
- Autosave: `autosave.json`, Quicksave: `quicksave.json`

## Running Tests

The desktop port includes comprehensive headless pytest tests.

**Run all tests:**
```bash
python -m pytest desktop/tests/ -v
```

**Run specific test file:**
```bash
python -m pytest desktop/tests/test_battle_engine.py -xvs
```

**Run with verbose output and stop on first failure:**
```bash
python -m pytest desktop/tests/ -xvs
```

**Test Categories:**
- **Shim Tests** (`test_shim_rendering.py`) - Drawing primitives, color conversion, y-coordinate flipping
- **Integration Tests** (`test_title_screen_headless.py`, `test_battle_headless.py`, etc.) - Scene rendering and game systems
- **Unit Tests** (`test_battle_engine.py`, `test_level_up.py`, `test_save_load.py`, `test_game_logic.py`) - Core game logic

**All tests run headlessly** using `SDL_VIDEODRIVER=dummy` mode, so no Pygame window appears. This makes them suitable for CI/CD pipelines.

## Architecture

### The Shim Layer

The desktop port uses a **shim layer** to bridge Pythonista APIs and Pygame. The shim replicates Pythonista's `scene`, `sound`, and `ui` modules so that game code can `import scene` and get the desktop implementation instead.

**How it works:**

1. **Path Manipulation** - `desktop/run.py` inserts `desktop/shim/` at `sys.path[0]` before importing game code
2. **API Compatibility** - The shim implements all Pythonista APIs used by the game:
   - `scene.py` - Scene class, drawing primitives, geometry types, Touch input
   - `sound.py` - Audio stubs (no-ops with optional debug prints)
   - `ui.py` - UI element stubs (View, Label, Button classes)
3. **Coordinate Transforms** - Pythonista uses bottom-left origin (y=0 at bottom), Pygame uses top-left (y=0 at top). The shim handles y-flipping automatically.
4. **Color Conversion** - Pythonista uses 0-1 float colors, Pygame uses 0-255 int colors. The shim converts on every draw call.
5. **Input Mapping** - Mouse events are converted to Touch events with logical coordinates (256x224 range)

**File Structure:**
```
desktop/
├── shim/
│   ├── scene.py      # Scene class, drawing, geometry, Touch
│   ├── sound.py      # Audio stubs
│   └── ui.py         # UI element stubs
├── tools/            # Development CLI tools
├── tests/            # Pytest suite
├── run.py            # Entry point with path setup
└── README.md         # This file
```

**Key Implementation Details:**

- **Logical Surface** - The shim renders to a 256x224 surface, then scales it 4x to a 1024x896 window
- **Transform Stack** - `GState` context manager implements push/pop transforms for translate/scale
- **Selectable Regions** - Keyboard navigation works by registering clickable areas and synthesizing Touch events

### Why This Approach?

The shim layer allows **100% code reuse** between iOS and desktop:
- Game logic in `data/`, `utils/`, `scenes/` works on both platforms
- No platform-specific `#ifdef` or conditional imports
- Bug fixes and features apply to both versions
- Testing on desktop validates iOS behavior

## Known Limitations

The desktop port has feature parity with the iOS version, but with these known differences:

### Compared to iOS Version

| Feature | iOS (Pythonista) | Desktop (Pygame) |
|---------|------------------|------------------|
| **Graphics** | Colored rectangles (placeholder) | Colored rectangles (placeholder) |
| **Sound** | Stubbed (no audio) | Stubbed (no audio) |
| **Touch Input** | Native touch | Mouse emulates touch |
| **Keyboard** | None | Full keyboard navigation |
| **Performance** | Native iOS rendering | Pygame software rendering |
| **Window** | Fullscreen device | 1024x896 resizable window |

### Visual Placeholders

Both versions use placeholder graphics:
- Characters, enemies, and NPCs are colored rectangles (16x24 pixels)
- Tiles are colored squares (16x16 pixels)
- UI elements are rectangles with text
- No sprite animations

### Audio

Sound is stubbed on both platforms:
- `sound.play_effect()` and `Player` class are no-ops
- Optional debug prints available via `DEBUG_SOUND` flag in `desktop/shim/sound.py`

### Enemy AI

Enemy AI uses simple random ability selection:
- No tactical targeting
- No ability cooldowns or patterns
- No difficulty scaling within battle

### Collision Detection

Map collision is screen-bounds only:
- No tile-based collision maps
- No height/elevation
- NPCs and doors are position-based triggers (not collision boxes)

## Troubleshooting

### Game Won't Launch

**Symptom:** `ImportError: No module named 'pygame'`

**Solution:**
```bash
pip install pygame-ce>=2.4.1
```

**Symptom:** `ModuleNotFoundError: No module named 'utils'`

**Solution:** Make sure you're running from the project root:
```bash
cd C:\Users\johnr\Documents\JasonMullan\RPG
python desktop/run.py
```

### Black Screen / No Graphics

**Symptom:** Window opens but shows only black screen

**Solution:** Check console output for errors. Common causes:
- Missing scene drawing functions (check `desktop/shim/scene.py`)
- Y-coordinate flipping errors (check `_flip_y()` implementation)

**Debug:** Run the title screen test:
```bash
python -m pytest desktop/tests/test_title_screen_headless.py -xvs
```

### Mouse Clicks Not Working

**Symptom:** Clicking menu buttons does nothing

**Solution:** Verify coordinate conversion:
- Window coords (1024x896, top-left origin) → Logical coords (256x224, bottom-left origin)
- Check `Touch` class implementation in `desktop/shim/scene.py`
- Verify `touch_began()` is being called (add print statements)

**Debug:** Run the integration tests:
```bash
python -m pytest desktop/tests/test_title_screen_headless.py::test_touch_began_no_crash -xvs
```

### Tests Fail with Pygame Errors

**Symptom:** `pygame.error: No available video device`

**Solution:** The tests should automatically set `SDL_VIDEODRIVER=dummy` in `conftest.py`. Verify:
```python
# In desktop/tests/conftest.py
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # MUST be before pygame import
```

**Symptom:** Tests hang or segfault

**Solution:** This is a known Pygame issue with `pygame.quit()` in dummy mode. The `conftest.py` fixture is session-scoped and does NOT call `pygame.quit()` to avoid this.

### Slow Performance

**Symptom:** Game runs at low FPS or stutters

**Possible Causes:**
- Pygame software rendering is slower than iOS native rendering
- Drawing too many primitives per frame
- Text rendering without font caching

**Solutions:**
- Reduce frame rate: modify `frame_interval` in `run.py`
- Profile with `cProfile` to find bottlenecks
- Consider hardware acceleration (PyGame-CE 2.5+ has better support)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on:
- Where to make changes (game logic vs shim vs tools)
- Testing requirements
- Syncing between iOS and desktop versions
- Code style conventions
- Pull request process

## License

This is a fan game based on "There Will Be Kobolds" (book). Not for commercial distribution.

## Credits

- **Game Design:** Based on "There Will Be Kobolds" (book)
- **Implementation:** Claude Code
- **Inspired By:** Final Fantasy 1-6 (Square Enix)
- **iOS Engine:** Pythonista (`scene` module by omz:software)
- **Desktop Engine:** Pygame-CE (Community Edition)

---

**Version:** 1.0.0 (Desktop Port - Phase 1 Complete)
**Platform:** Windows / macOS / Linux
**Status:** ✅ Fully Playable
