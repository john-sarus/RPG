"""
Pytest configuration for headless rendering tests
Sets up pygame in dummy mode for testing without display
"""

import os
# CRITICAL: Set SDL_VIDEODRIVER before any pygame import
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import sys
import pytest
import pygame

# Add shim to sys.path[0] so 'import scene' finds our shim
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
shim_path = os.path.join(os.path.dirname(__file__), '..', 'shim')
sys.path.insert(0, shim_path)
sys.path.insert(1, project_root)

# Import scene module after path setup
import scene


@pytest.fixture
def headless_pygame():
    """
    Fixture that sets up pygame in headless mode for testing
    Creates a 256x224 surface and assigns it to scene._surface
    """
    pygame.init()

    # Create logical surface (256x224) for drawing
    surface = pygame.Surface((256, 224))
    scene._surface = surface

    # Yield the surface for tests to use
    yield surface

    # Teardown: clear the surface and quit pygame
    surface.fill((0, 0, 0))
    pygame.quit()
