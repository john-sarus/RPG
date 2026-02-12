#!/usr/bin/env python3
"""
Desktop launcher for 'There Will Be Kobolds' JRPG.

This script manipulates sys.path so that imports like 'from scene import *'
resolve to the Pygame shim layer instead of Pythonista's modules.
"""

import sys
import os
from pathlib import Path

def main():
    # Compute paths relative to this script
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    shim_dir = script_dir / "shim"

    # Insert shim directory at position 0 so 'from scene import *' finds our shim
    sys.path.insert(0, str(shim_dir))

    # Insert project root into sys.path so 'from utils.game_state import GameState' works
    sys.path.insert(1, str(project_root))

    print("Desktop launcher ready")
    print(f"Project root: {project_root}")
    print(f"Shim directory: {shim_dir}")
    print(f"sys.path[0]: {sys.path[0]}")
    print(f"sys.path[1]: {sys.path[1]}")
    print()

    # Import the game
    try:
        print("Importing scene module (shim)...")
        from scene import run, LANDSCAPE
        print("✓ Scene module imported")
    except ImportError as e:
        print(f"✗ Failed to import scene module: {e}")
        return 1
    except AttributeError as e:
        print(f"✗ Scene module missing required attribute: {e}")
        return 1

    try:
        print("Importing GameRoot from main.py...")
        from main import GameRoot
        print("✓ GameRoot imported")
    except ImportError as e:
        print(f"✗ Failed to import GameRoot: {e}")
        print("This likely means a game module couldn't import required dependencies.")
        return 1
    except AttributeError as e:
        print(f"✗ main.py missing GameRoot class: {e}")
        return 1

    # Launch the game
    print()
    print("Launching 'There Will Be Kobolds' on desktop...")
    print("Window size: 1024x896 (4x scale of 256x224 logical resolution)")
    print()

    try:
        run(GameRoot(), orientation=LANDSCAPE, frame_interval=2)
    except Exception as e:
        print(f"✗ Game crashed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
