"""
Temporary test script to capture a screenshot of the game
"""
import sys
import os
import time

# Add paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
shim_dir = os.path.join(script_dir, 'shim')

sys.path.insert(0, shim_dir)
sys.path.insert(1, project_root)

# Import pygame directly for screenshot
import pygame

# Import game
from main import GameRoot
from scene import run, LANDSCAPE

def main():
    """Run game and take screenshot after delay"""
    import threading

    def take_screenshot():
        time.sleep(2)  # Wait 2 seconds
        try:
            screen = pygame.display.get_surface()
            if screen:
                pygame.image.save(screen, 'desktop/screenshot_title.png')
                print("\n✓ Screenshot saved to desktop/screenshot_title.png")
        except Exception as e:
            print(f"\n✗ Screenshot failed: {e}")

    # Start screenshot thread
    screenshot_thread = threading.Thread(target=take_screenshot, daemon=True)
    screenshot_thread.start()

    # Run game
    print("Starting game...")
    game_root = GameRoot()
    run(game_root, orientation=LANDSCAPE, frame_interval=2)

if __name__ == '__main__':
    main()
