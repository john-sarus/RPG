"""
Test title screen mouse interaction
"""
import sys
import os

# Add paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
shim_dir = os.path.join(script_dir, 'shim')

sys.path.insert(0, shim_dir)
sys.path.insert(1, project_root)

# Import scene and pygame
from scene import Scene, run, LANDSCAPE, Point
import pygame

class TestTitleInteraction(Scene):
    """Test scene to verify title screen touch handling"""

    def __init__(self):
        super().__init__()
        self.clicks = []

    def setup(self):
        print("\n=== Title Screen Interaction Test ===")
        print("Click on menu items to test touch handling")
        print("Expected logical coordinates:")
        print("  New Game button: x=48-208, y=80-100")
        print("  Continue button: x=48-208, y=52-72")
        print("  Load Game button: x=48-208, y=24-44")
        print("Press ESC to exit")

    def draw(self):
        from scene import background, fill, rect, text

        # Draw same title screen
        background(0.1, 0.1, 0.15)

        # Title
        fill(1, 1, 1)
        text("THERE WILL BE KOBOLDS", 'Futura', 20, 128, 180, alignment=5)

        # Subtitle
        fill(0.8, 0.8, 0.8)
        text("A Dark Fantasy JRPG", 'Futura', 12, 128, 160, alignment=5)

        # Menu options
        menu_options = ['New Game', 'Continue', 'Load Game', 'Settings', 'Exit']
        button_height = 20
        button_spacing = 8
        menu_start_y = 80

        for i, option in enumerate(menu_options):
            y = menu_start_y - (i * (button_height + button_spacing))

            # Highlight
            fill(0.3, 0.3, 0.5)
            rect(48, y, 160, button_height)

            # Text
            fill(1, 1, 1)
            text(option, 'Futura', 14, 128, y + button_height/2, alignment=5)

        # Show last click coordinates
        if self.clicks:
            fill(1, 1, 0)
            last_click = self.clicks[-1]
            text(f"Last click: ({last_click[0]:.1f}, {last_click[1]:.1f})",
                 'Courier', 10, 128, 10, alignment=5)

    def touch_began(self, touch):
        """Handle mouse click"""
        x, y = touch.location.x, touch.location.y
        self.clicks.append((x, y))

        print(f"\n✓ Click detected: logical coordinates ({x:.2f}, {y:.2f})")

        # Check which button was clicked
        menu_options = ['New Game', 'Continue', 'Load Game', 'Settings', 'Exit']
        button_height = 20
        button_spacing = 8
        menu_start_y = 80

        for i, option in enumerate(menu_options):
            y_btn = menu_start_y - (i * (button_height + button_spacing))

            if (48 <= x <= 208 and y_btn <= y <= y_btn + button_height):
                print(f"  → Detected: {option} button")
                if option == 'Exit':
                    print("Exit button clicked - closing game")
                    self.close()
                return

        print("  → Click outside menu buttons")

if __name__ == '__main__':
    scene = TestTitleInteraction()
    run(scene, orientation=LANDSCAPE, frame_interval=2)
