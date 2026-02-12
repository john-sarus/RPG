# Contributing to the Desktop Port

Thank you for your interest in contributing to the desktop port of "There Will Be Kobolds"! This guide will help you understand where to make changes, how to test them, and how to maintain compatibility between the desktop and iOS versions.

## Overview

The desktop port uses a **compatibility shim layer** to translate Pythonista's iOS-specific APIs (`scene`, `sound`, `ui`) into Pygame equivalents. This means the core game code (in `data/`, `utils/`, `scenes/`, `main.py`) runs unmodified on both platforms.

## Where to Make Changes

Changes fall into three categories, each with different platform impact:

### 1. Game Logic Changes (Cross-Platform)

**Location**: `data/`, `utils/`, `scenes/`, `main.py`, `game.py`

**Impact**: Affects both iOS and desktop platforms

**When**: Fixing bugs, adding features, balancing gameplay, adding content

These directories contain the core game logic that is shared between both platforms. Changes here automatically apply to both iOS (Pythonista) and desktop (Pygame).

**Examples**:
- Adding a new character to `data/characters.py`
- Fixing a bug in `utils/battle_engine.py`
- Creating a new scene in `scenes/`
- Modifying game progression in `utils/story_event_system.py`

**Testing requirement**: Changes MUST be tested on desktop via pytest. iOS testing is recommended but not required for desktop-only contributors.

### 2. Shim Layer Changes (Desktop Only)

**Location**: `desktop/shim/` (scene.py, sound.py, ui.py)

**Impact**: Desktop only

**When**: Adding missing Pythonista APIs, fixing rendering bugs, improving input handling

The shim layer provides Pygame implementations of Pythonista's APIs. Changes here only affect the desktop port.

**Examples**:
- Adding a missing method to the `Scene` class
- Fixing coordinate conversion in `_flip_y()`
- Improving keyboard navigation in selectable regions
- Implementing a previously-stubbed `sound` API

**Testing requirement**: Run pytest suite, visually test the game on desktop

### 3. Development Tools (Desktop Only)

**Location**: `desktop/tools/` (battle_tester.py, stat_viewer.py, map_inspector.py, save_inspector.py)

**Impact**: Desktop only (iOS has no equivalent tools)

**When**: Adding new debugging/development utilities

These CLI tools are desktop-exclusive development aids.

**Examples**:
- Adding new flags to `battle_tester.py`
- Creating a new inspector tool
- Adding features to `save_inspector.py`

**Testing requirement**: Verify tool runs without errors, output is correct

## Testing Requirements

All contributions MUST pass the test suite before being merged.

### Running Tests

```bash
# Run all tests
python -m pytest desktop/tests/ -xvs

# Run specific test file
python -m pytest desktop/tests/test_battle_engine.py -xvs

# Run with coverage report
python -m pytest desktop/tests/ --cov=utils --cov=data --cov=scenes
```

### Test Coverage Expectations

- **Game logic changes**: Add unit tests for new functionality
- **Shim changes**: Verify existing tests still pass, add tests if introducing new APIs
- **Tool changes**: Manually verify tool works correctly

### Visual Testing

For rendering or UI changes:

1. Run the game: `python desktop/run.py`
2. Navigate to the affected screen
3. Verify visual correctness:
   - Colors render correctly (no oversaturation or undersaturation)
   - Text is legible and positioned correctly
   - Rectangles/shapes appear at expected positions
   - Mouse clicks register on the correct elements
   - Keyboard navigation works smoothly

## Syncing Changes Between iOS and Desktop

The desktop port shares the core game code with the iOS version. Here's how changes propagate:

### Automatic Sync (Game Logic)

Changes to `data/`, `utils/`, `scenes/`, `main.py`, or `game.py` automatically affect both platforms because both use the same files.

**No special action needed** — just commit your changes to the shared files.

### No Sync Required (Desktop-Only Code)

Changes to `desktop/shim/` and `desktop/tools/` never affect the iOS version. These directories don't exist in the iOS environment.

### Maintaining Compatibility

When modifying shared game code:

1. **Don't import platform-specific modules conditionally** — the shim handles this via `sys.path` manipulation
2. **Don't add desktop-specific code to shared files** — keep platform-specific logic in the shim layer
3. **Preserve the API contract** — if game code calls `scene.fill()`, the shim must provide it

If you need desktop-specific behavior in game logic, consider:
- Adding it to the shim layer instead
- Using a flag in `GameState` to toggle behavior
- Creating a desktop-specific subclass

## Code Style

Follow these conventions to maintain consistency:

### General Guidelines

- **Follow existing patterns** — match the style of surrounding code
- **Minimal changes** — only modify what's necessary for your fix/feature
- **No unnecessary refactoring** — don't clean up unrelated code in the same commit
- **Descriptive variable names** — prefer `enemy_count` over `ec`
- **Comments for complex logic** — explain WHY, not WHAT

### Python Conventions

- 4 spaces for indentation (no tabs)
- Snake_case for variables and functions: `player_position`, `calculate_damage()`
- PascalCase for classes: `GameState`, `BattleEngine`, `MenuSystem`
- UPPER_CASE for constants: `MAX_PARTY_SIZE`, `LANDSCAPE`
- Double quotes for strings: `"hello"` (not `'hello'`)
- Type hints encouraged but not required

### Import Order

1. Standard library imports (`import os`, `import sys`)
2. Third-party imports (`import pygame`)
3. Local imports (`from utils.game_state import GameState`)

Separate each group with a blank line.

### Shim Layer Conventions

- **Keep implementations minimal** — provide only what's needed
- **Match Pythonista signatures exactly** — same parameters, same return types
- **Document differences** — if behavior must differ, add a comment explaining why
- **Stub unknown APIs** — if you're not sure how a Pythonista API works, stub it and log usage

Example:
```python
def some_pythonista_api(param1, param2):
    """Stub implementation - Pythonista behavior unclear.

    If this gets called, we'll see it in logs and can implement it properly.
    """
    if DEBUG:
        print(f"[STUB] some_pythonista_api called with {param1}, {param2}")
    return None
```

## Pull Request Process

### Before Submitting

1. **Run the test suite**: `python -m pytest desktop/tests/ -xvs`
2. **Run the game manually**: `python desktop/run.py` and verify your changes work
3. **Check for regressions**: Test at least the title screen and one battle
4. **Review your own changes**: Read the diff and remove any debug code, commented-out lines, or unintended changes

### Commit Message Format

Use conventional commit format:

```
type(scope): brief description

Optional longer explanation of what changed and why.
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Adding or modifying tests
- `docs`: Documentation changes
- `refactor`: Code restructuring without behavior change
- `perf`: Performance improvement
- `chore`: Tooling, dependencies, or config changes

**Scopes**:
- `shim`: Changes to desktop/shim/
- `tools`: Changes to desktop/tools/
- `tests`: Changes to desktop/tests/
- `battle`: Changes to battle system
- `menu`: Changes to menu system
- `map`: Changes to map system
- (or any other relevant system/module)

**Examples**:
```
feat(shim): add keyboard shortcut for quicksave

fix(battle): correct burn damage calculation

test(integration): add tests for save/load round-trip

docs(desktop): update README with new keyboard controls
```

### Pull Request Description

Include:

1. **What changed** — high-level summary of the changes
2. **Why** — what problem does this solve? What feature does it add?
3. **Testing done** — what tests did you run? What did you verify manually?
4. **Platform impact** — does this affect iOS, desktop, or both?

Example:
```markdown
## What Changed

Added support for gamepad input in the shim layer.

## Why

Players requested gamepad support for desktop play. This makes the game more comfortable
to play with a controller.

## Testing Done

- All existing tests pass
- Tested with Xbox and PlayStation controllers
- Verified keyboard input still works
- Verified mouse input still works

## Platform Impact

Desktop only — this is a shim layer change and doesn't affect iOS.
```

## Common Pitfalls

### 1. Coordinate System Confusion

Pythonista uses **bottom-left origin** (y=0 at bottom, increases upward).
Pygame uses **top-left origin** (y=0 at top, increases downward).

The shim's `_flip_y()` handles this conversion. If you see things rendering upside-down or at wrong positions, check the coordinate conversion.

### 2. Color Range Differences

Pythonista uses **0.0-1.0 float colors** (e.g., `fill(1.0, 0.5, 0.0)` for orange).
Pygame uses **0-255 integer colors** (e.g., `(255, 127, 0)` for orange).

The shim's `_color_float_to_int()` handles this conversion. If colors look wrong, check the conversion logic.

### 3. Touch vs Mouse Input

iOS uses multi-touch with `Touch` objects that have lifecycle events (began/moved/ended).
Desktop uses mouse with button down/motion/up events.

The shim synthesizes `Touch` objects from mouse events. If input doesn't work, check the coordinate conversion from window space to logical space.

### 4. Scene Size and Scaling

The game's logical resolution is **256x224 pixels** (SNES-era resolution).
The desktop window is **1024x896 pixels** (4x scale factor).

All game code draws to the 256x224 logical surface, which is then scaled to the window. Don't draw directly to the window — always draw to `scene._surface`.

### 5. Headless Testing

Tests run in **headless mode** using `os.environ['SDL_VIDEODRIVER'] = 'dummy'`.

This MUST be set BEFORE importing pygame. The `conftest.py` handles this for all tests. Don't call `pygame.display.set_mode()` in tests — just create a plain `Surface`.

## Getting Help

If you're stuck or have questions:

1. **Read the code** — the existing code is the best documentation
2. **Check the tests** — `desktop/tests/` shows how each system is used
3. **Read the progress file** — `progress_Jasons_RPG.txt` documents learnings and patterns
4. **Check CLAUDE.md** — project-specific context and history
5. **Open an issue** — describe what you're trying to do and where you're stuck

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
