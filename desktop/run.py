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

if __name__ == "__main__":
    main()
