"""
Test keyboard navigation system
"""
import sys
import os

# Setup path to use the shim
desktop_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(desktop_dir)
sys.path.insert(0, os.path.join(desktop_dir, 'shim'))
sys.path.insert(1, project_root)

from scene import Scene, run, LANDSCAPE, Rect, fill, rect, text

class TestKeyboardScene(Scene):
    """Test scene for keyboard navigation"""

    def __init__(self):
        super().__init__()
        self.menu_options = ['Option 1', 'Option 2', 'Option 3']
        self.last_action = "Press arrow keys to navigate, Enter to select"

    def setup(self):
        """Register selectable regions for menu options"""
        self.clear_selectables()

        button_y = 100
        button_spacing = 30

        for i, option in enumerate(self.menu_options):
            y = button_y - (i * button_spacing)
            # Register each button as selectable
            self.register_selectable(option, Rect(48, y, 160, 20))

    def draw(self):
        """Draw test menu"""
        # Background
        fill(0.1, 0.1, 0.15)
        rect(0, 0, 256, 224)

        # Title
        fill(1, 1, 1)
        text("Keyboard Navigation Test", 'Arial', 16, 128, 180, alignment=5)

        # Instructions
        fill(0.8, 0.8, 0.8)
        text(self.last_action, 'Arial', 10, 128, 20, alignment=5)

        # Menu options
        button_y = 100
        button_spacing = 30

        selected = self.get_selected_region()

        for i, option in enumerate(self.menu_options):
            y = button_y - (i * button_spacing)

            # Highlight if selected
            if selected and selected[0] == option:
                fill(0.3, 0.5, 0.3)  # Green highlight
            else:
                fill(0.2, 0.2, 0.3)  # Dark blue

            rect(48, y, 160, 20)

            # Draw text
            fill(1, 1, 1)
            text(option, 'Arial', 14, 128, y + 10, alignment=5)

    def touch_began(self, touch):
        """Handle touch/synthetic touch from keyboard"""
        x, y = touch.location.x, touch.location.y

        button_y = 100
        button_spacing = 30

        for i, option in enumerate(self.menu_options):
            option_y = button_y - (i * button_spacing)

            if 48 <= x <= 208 and option_y <= y <= option_y + 20:
                self.last_action = f"Selected: {option}"
                print(f"Selected: {option}")
                break

    def key_down(self, key):
        """Handle direct keyboard input"""
        if key == 'escape':
            print("Escape pressed - closing")
            self.close()
        elif key == 'm':
            self.last_action = "M key pressed (menu shortcut)"
            print("M key pressed")

if __name__ == '__main__':
    print("=== Keyboard Navigation Test ===")
    print("Controls:")
    print("  Arrow keys / WASD - Navigate menu")
    print("  Enter / Space - Select option")
    print("  Escape - Exit")
    print("  M - Test direct key handler")
    print()

    test_scene = TestKeyboardScene()
    run(test_scene, orientation=LANDSCAPE, frame_interval=2)
