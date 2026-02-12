"""
Verify pygame key mapping
"""
import sys
import os

# Setup path to use the shim
desktop_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(desktop_dir)
sys.path.insert(0, os.path.join(desktop_dir, 'shim'))
sys.path.insert(1, project_root)

import pygame
from scene import _get_key_name

def test_key_mapping():
    """Test that pygame key constants map correctly"""
    print("Testing pygame key mapping...")

    # Test arrow keys
    assert _get_key_name(pygame.K_UP) == 'up', "K_UP should map to 'up'"
    assert _get_key_name(pygame.K_DOWN) == 'down', "K_DOWN should map to 'down'"
    assert _get_key_name(pygame.K_LEFT) == 'left', "K_LEFT should map to 'left'"
    assert _get_key_name(pygame.K_RIGHT) == 'right', "K_RIGHT should map to 'right'"

    # Test WASD
    assert _get_key_name(pygame.K_w) == 'w', "K_w should map to 'w'"
    assert _get_key_name(pygame.K_a) == 'a', "K_a should map to 'a'"
    assert _get_key_name(pygame.K_s) == 's', "K_s should map to 's'"
    assert _get_key_name(pygame.K_d) == 'd', "K_d should map to 'd'"

    # Test special keys
    assert _get_key_name(pygame.K_RETURN) == 'return', "K_RETURN should map to 'return'"
    assert _get_key_name(pygame.K_SPACE) == 'space', "K_SPACE should map to 'space'"
    assert _get_key_name(pygame.K_ESCAPE) == 'escape', "K_ESCAPE should map to 'escape'"
    assert _get_key_name(pygame.K_m) == 'm', "K_m should map to 'm'"

    # Test number keys
    assert _get_key_name(pygame.K_1) == '1', "K_1 should map to '1'"
    assert _get_key_name(pygame.K_5) == '5', "K_5 should map to '5'"
    assert _get_key_name(pygame.K_9) == '9', "K_9 should map to '9'"

    # Test unmapped key
    assert _get_key_name(pygame.K_z) is None, "Unmapped keys should return None"

    print("✓ All key mappings correct!")


if __name__ == '__main__':
    pygame.init()  # Initialize pygame to get key constants
    test_key_mapping()
    pygame.quit()
