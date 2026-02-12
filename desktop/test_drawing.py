"""
Temporary test script to verify drawing primitives work correctly
Tests color conversion, y-flip, rectangles, ellipses, and text rendering
"""

import sys
import os

# Add shim to path
project_root = os.path.dirname(os.path.abspath(__file__))
shim_path = os.path.join(project_root, 'desktop', 'shim')
sys.path.insert(0, shim_path)

# Import directly from scene module (not via __init__ since sound/ui aren't ready)
import scene
from scene import Scene, run, LANDSCAPE, background, fill, rect, ellipse, text


class DrawingTestScene(Scene):
    """Test scene that draws various shapes and text"""

    def setup(self):
        """Initialize test scene"""
        print("DrawingTestScene setup")

    def draw(self):
        """Draw test shapes"""
        # Black background
        background(0, 0, 0)

        # Red rectangle (bottom-left corner)
        fill(1.0, 0, 0)
        rect(10, 10, 50, 30)

        # Green rectangle (top-left in Pythonista coords = bottom-left in Pygame)
        fill(0, 1.0, 0)
        rect(10, 184, 50, 30)

        # Blue ellipse (center)
        fill(0, 0, 1.0)
        ellipse(100, 100, 60, 40)

        # Yellow rectangle with transparency
        fill(1.0, 1.0, 0, 0.5)
        rect(150, 150, 80, 50)

        # White text (center)
        fill(1, 1, 1)
        text("Drawing Test", 'Futura', 20, 128, 112, alignment=5)

        # Text at bottom
        fill(0.8, 0.8, 0.8)
        text("Bottom Left", 'Futura', 12, 10, 10, alignment=4)

        # Text at top
        fill(0.8, 0.8, 0.8)
        text("Top Center", 'Futura', 12, 128, 210, alignment=8)

        # Cyan rectangle (top-right)
        fill(0, 1.0, 1.0)
        rect(200, 170, 40, 40)


if __name__ == '__main__':
    print("Starting drawing test...")
    print("You should see:")
    print("  - Red rect at bottom-left")
    print("  - Green rect at top-left")
    print("  - Blue ellipse in center")
    print("  - Yellow transparent rect (upper-right of center)")
    print("  - 'Drawing Test' text in center")
    print("  - 'Bottom Left' text at bottom-left")
    print("  - 'Top Center' text at top")
    print("  - Cyan rect at top-right")
    print("")
    print("Close the window to exit.")

    scene = DrawingTestScene()
    run(scene, orientation=LANDSCAPE, frame_interval=2)
