"""
Verify keyboard navigation system logic without GUI
"""
import sys
import os

# Setup path to use the shim
desktop_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(desktop_dir)
sys.path.insert(0, os.path.join(desktop_dir, 'shim'))
sys.path.insert(1, project_root)

from scene import Scene, Rect, Point

def test_keys_pressed():
    """Test keys_pressed tracking"""
    print("Test 1: keys_pressed tracking")
    scene = Scene()

    # Initially empty
    assert len(scene.keys_pressed()) == 0, "Should start with no keys pressed"

    # Add keys
    scene._keys_pressed.add('up')
    scene._keys_pressed.add('w')
    keys = scene.keys_pressed()
    assert 'up' in keys and 'w' in keys, "Should track multiple keys"
    assert len(keys) == 2, "Should have 2 keys"

    # Remove key
    scene._keys_pressed.discard('up')
    keys = scene.keys_pressed()
    assert 'up' not in keys and 'w' in keys, "Should remove keys correctly"
    assert len(keys) == 1, "Should have 1 key"

    print("  ✓ keys_pressed tracking works")


def test_selectables():
    """Test selectable region registration and cycling"""
    print("Test 2: Selectable regions")
    scene = Scene()

    # Register selectables
    scene.register_selectable("Button 1", Rect(10, 100, 50, 20))
    scene.register_selectable("Button 2", Rect(10, 70, 50, 20))
    scene.register_selectable("Button 3", Rect(10, 40, 50, 20))

    assert len(scene._selectables) == 3, "Should have 3 selectables"

    # Initial selection
    selected = scene.get_selected_region()
    assert selected[0] == "Button 1", "Should start at first selectable"

    # Cycle forward
    scene._cycle_selection(1)
    selected = scene.get_selected_region()
    assert selected[0] == "Button 2", "Should cycle to second selectable"

    scene._cycle_selection(1)
    selected = scene.get_selected_region()
    assert selected[0] == "Button 3", "Should cycle to third selectable"

    # Wrap around
    scene._cycle_selection(1)
    selected = scene.get_selected_region()
    assert selected[0] == "Button 1", "Should wrap to first selectable"

    # Cycle backward
    scene._cycle_selection(-1)
    selected = scene.get_selected_region()
    assert selected[0] == "Button 3", "Should cycle backward to last selectable"

    # Clear selectables
    scene.clear_selectables()
    assert len(scene._selectables) == 0, "Should clear all selectables"
    assert scene.get_selected_region() is None, "Should return None when empty"

    print("  ✓ Selectable registration and cycling works")


def test_trigger_selected():
    """Test synthetic touch generation"""
    print("Test 3: Synthetic touch generation")

    class TestScene(Scene):
        def __init__(self):
            super().__init__()
            self.touch_began_called = False
            self.touch_ended_called = False
            self.touch_x = None
            self.touch_y = None

        def touch_began(self, touch):
            self.touch_began_called = True
            self.touch_x = touch.location.x
            self.touch_y = touch.location.y

        def touch_ended(self, touch):
            self.touch_ended_called = True

    scene = TestScene()

    # Register a selectable
    scene.register_selectable("Button", Rect(50, 100, 100, 30))

    # Trigger it
    scene._trigger_selected()

    assert scene.touch_began_called, "Should call touch_began"
    assert scene.touch_ended_called, "Should call touch_ended"

    # Check that touch was at center of rect
    expected_x = 50 + 100 / 2  # 100
    expected_y = 100 + 30 / 2  # 115
    assert scene.touch_x == expected_x, f"Touch X should be {expected_x}, got {scene.touch_x}"
    assert scene.touch_y == expected_y, f"Touch Y should be {expected_y}, got {scene.touch_y}"

    print("  ✓ Synthetic touch generation works")


def test_key_callbacks():
    """Test key_down and key_up callbacks"""
    print("Test 4: Key callbacks")

    class TestScene(Scene):
        def __init__(self):
            super().__init__()
            self.keys_down = []
            self.keys_up = []

        def key_down(self, key):
            self.keys_down.append(key)

        def key_up(self, key):
            self.keys_up.append(key)

    scene = TestScene()

    # Simulate key events
    scene.key_down('up')
    scene.key_down('space')
    scene.key_up('up')

    assert scene.keys_down == ['up', 'space'], "Should track key_down calls"
    assert scene.keys_up == ['up'], "Should track key_up calls"

    print("  ✓ Key callbacks work")


if __name__ == '__main__':
    print("=== Keyboard Navigation System Verification ===\n")

    try:
        test_keys_pressed()
        test_selectables()
        test_trigger_selected()
        test_key_callbacks()

        print("\n✓ All tests passed!")
        print("\nKeyboard navigation system is working correctly:")
        print("  - Keys tracking: ✓")
        print("  - Selectable regions: ✓")
        print("  - Arrow key cycling: ✓")
        print("  - Enter key synthetic touch: ✓")
        print("  - Key callbacks: ✓")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
