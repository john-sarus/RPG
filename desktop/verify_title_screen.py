"""
Comprehensive verification test for title screen rendering and interaction
"""
import sys
import os

# Add paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
shim_dir = os.path.join(script_dir, 'shim')

sys.path.insert(0, shim_dir)
sys.path.insert(1, project_root)

print("=" * 60)
print("TITLE SCREEN VERIFICATION TEST")
print("=" * 60)

# Test 1: Import checks
print("\n[Test 1] Checking imports...")
try:
    from scene import background, fill, rect, text, Point, Size, Rect, LANDSCAPE
    print("✓ Scene module imports successful")
except ImportError as e:
    print(f"✗ Scene module import failed: {e}")
    sys.exit(1)

try:
    from scenes.title_screen import TitleScreen
    print("✓ TitleScreen imports successful")
except ImportError as e:
    print(f"✗ TitleScreen import failed: {e}")
    sys.exit(1)

try:
    from main import GameRoot
    print("✓ GameRoot imports successful")
except ImportError as e:
    print(f"✗ GameRoot import failed: {e}")
    sys.exit(1)

# Test 2: Color conversion verification
print("\n[Test 2] Verifying color conversion...")
from scene import _color_float_to_int
test_colors = [
    ((0.1, 0.1, 0.15), (25, 25, 38, 255)),
    ((1.0, 1.0, 1.0), (255, 255, 255, 255)),
    ((0.3, 0.3, 0.5), (76, 76, 127, 255)),
]
all_passed = True
for input_rgb, expected in test_colors:
    result = _color_float_to_int(*input_rgb)
    if result == expected:
        print(f"✓ {input_rgb} → {result}")
    else:
        print(f"✗ {input_rgb} → {result} (expected {expected})")
        all_passed = False

if all_passed:
    print("✓ All color conversions correct")
else:
    print("✗ Some color conversions failed")

# Test 3: Y-flip verification
print("\n[Test 3] Verifying y-flip calculations...")
from scene import _flip_y
test_flips = [
    ((0, 0), 224),  # Bottom of screen
    ((224, 0), 0),   # Top of screen
    ((80, 20), 124), # Menu button position
]
all_passed = True
for (y, h), expected in test_flips:
    result = _flip_y(y, h)
    if result == expected:
        print(f"✓ y={y}, h={h} → {result}")
    else:
        print(f"✗ y={y}, h={h} → {result} (expected {expected})")
        all_passed = False

if all_passed:
    print("✓ All y-flip calculations correct")
else:
    print("✗ Some y-flip calculations failed")

# Test 4: TitleScreen instantiation
print("\n[Test 4] Testing TitleScreen instantiation...")
try:
    class MockGameRoot:
        pass

    mock_root = MockGameRoot()
    title = TitleScreen(mock_root)
    print(f"✓ TitleScreen created")
    print(f"  - Menu options: {len(title.menu_options)}")
    print(f"  - Selected index: {title.selected_index}")
    print(f"  - Title text: '{title.title_text}'")
except Exception as e:
    print(f"✗ TitleScreen instantiation failed: {e}")
    sys.exit(1)

# Test 5: Touch region calculation
print("\n[Test 5] Verifying touch regions...")
button_height = 20
button_spacing = 8
menu_start_y = 80

menu_items = [
    ("New Game", 0),
    ("Continue", 1),
    ("Load Game", 2),
    ("Settings", 3),
    ("Exit", 4),
]

print("Touch regions (in logical coordinates):")
for name, index in menu_items:
    y = menu_start_y - (index * (button_height + button_spacing))
    print(f"  {name:12s}: x=48-208, y={y}-{y + button_height}")

# Test 6: Visual rendering test (requires pygame window)
print("\n[Test 6] Visual rendering test...")
print("This test will open a window with the title screen.")
print("Visual checks to perform:")
print("  1. Background is dark blue-gray")
print("  2. Title 'THERE WILL BE KOBOLDS' is white and centered at top")
print("  3. Subtitle 'A Dark Fantasy JRPG' is gray and centered below title")
print("  4. Five menu options are visible")
print("  5. 'New Game' has blue highlight rectangle")
print("  6. Clicking a menu option prints detection message")
print("\nStarting visual test in 3 seconds...")
print("(Window will auto-close after 5 seconds, or click Exit to close)")

import time
time.sleep(3)

# Run actual game
from scene import run
game = GameRoot()
print("\n✓ Starting game window...")

# Override new_game to just close for testing
original_new_game = game.new_game
def test_new_game():
    print("\n✓ New Game selection detected - working correctly!")
    print("Closing window...")
    import pygame
    pygame.quit()
    sys.exit(0)

game.new_game = test_new_game

# Auto-close timer
import threading
def auto_close():
    time.sleep(5)
    print("\n✓ Auto-close timer reached - test complete")
    import pygame
    pygame.quit()
    sys.exit(0)

threading.Thread(target=auto_close, daemon=True).start()

try:
    run(game, orientation=LANDSCAPE, frame_interval=2)
except SystemExit:
    pass

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
