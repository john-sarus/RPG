"""
Headless tests for MapSystem and NPCSystem.

These tests verify map movement, collision detection, location transitions,
and NPC interactions without requiring a Pygame window.
"""

import pytest
import sys
import os

# conftest.py already sets up sys.path for us
from utils.map_system import MapSystem, NPCSystem
from utils.game_state import GameState


def test_player_init_position():
    """Test that player starts at default center position"""
    gs = GameState()
    ms = MapSystem(gs)

    assert ms.player_position == [128, 112], "Player should start at center position [128, 112]"


def test_move_player_right():
    """Test moving player to the right"""
    gs = GameState()
    ms = MapSystem(gs)

    old_x = ms.player_position[0]
    result = ms.move_player(1, 0)  # Move right (dx=1, dy=0)

    assert result == True, "Movement should succeed"
    assert ms.player_position[0] == old_x + ms.move_speed, f"Player X should increase by move_speed ({ms.move_speed})"
    assert ms.player_position[1] == 112, "Player Y should not change"


def test_move_player_up():
    """Test moving player up"""
    gs = GameState()
    ms = MapSystem(gs)

    old_y = ms.player_position[1]
    result = ms.move_player(0, 1)  # Move up (dx=0, dy=1)

    assert result == True, "Movement should succeed"
    assert ms.player_position[0] == 128, "Player X should not change"
    assert ms.player_position[1] == old_y + ms.move_speed, f"Player Y should increase by move_speed ({ms.move_speed})"


def test_move_player_boundary():
    """Test that player movement is clamped at boundaries"""
    gs = GameState()
    ms = MapSystem(gs)

    # Move player to left edge
    ms.player_position = [1, 112]
    result = ms.move_player(-1, 0)  # Try to move left past boundary

    # Movement should be rejected or position should stay >= 0
    assert ms.player_position[0] >= 0, "Player X should not go below 0"

    # Move player to right edge
    ms.player_position = [254, 112]
    result = ms.move_player(1, 0)  # Try to move right past boundary

    # Movement should be rejected or position should stay < 256
    assert ms.player_position[0] < 256, "Player X should not go >= 256"


def test_walkable_center():
    """Test that center position is walkable"""
    gs = GameState()
    ms = MapSystem(gs)

    assert ms.is_position_walkable(128, 112) == True, "Center position should be walkable"


def test_not_walkable_out_of_bounds():
    """Test that out-of-bounds positions are not walkable"""
    gs = GameState()
    ms = MapSystem(gs)

    assert ms.is_position_walkable(-1, -1) == False, "Position (-1, -1) should not be walkable"
    assert ms.is_position_walkable(-1, 112) == False, "Position (-1, 112) should not be walkable"
    assert ms.is_position_walkable(128, -1) == False, "Position (128, -1) should not be walkable"
    assert ms.is_position_walkable(300, 300) == False, "Position (300, 300) should not be walkable"
    assert ms.is_position_walkable(256, 112) == False, "Position (256, 112) should not be walkable"
    assert ms.is_position_walkable(128, 224) == False, "Position (128, 224) should not be walkable"


def test_enter_location():
    """Test entering a location"""
    gs = GameState()
    ms = MapSystem(gs)

    result = ms.enter_location('tutorial_warren')

    assert result == True, "Should successfully enter tutorial_warren"
    assert gs.current_location == 'tutorial_warren', "Current location should be tutorial_warren"
    # tutorial_warren has spawn_position [20, 100]
    assert ms.player_position == [20, 100], "Player should be at spawn position [20, 100]"


def test_enter_locked_location():
    """Test that entering a locked location fails"""
    gs = GameState()
    ms = MapSystem(gs)

    # surface_forest requires 'warren_escaped' flag
    gs.story_flags['warren_escaped'] = False
    result = ms.enter_location('surface_forest')

    assert result == False, "Should fail to enter locked location"
    assert gs.current_location != 'surface_forest', "Location should not change"


def test_enter_unlocked_location():
    """Test that entering an unlocked location succeeds"""
    gs = GameState()
    ms = MapSystem(gs)

    # surface_forest requires 'warren_escaped' flag
    gs.story_flags['warren_escaped'] = True
    result = ms.enter_location('surface_forest')

    assert result == True, "Should successfully enter unlocked location"
    assert gs.current_location == 'surface_forest', "Current location should be surface_forest"


def test_npc_system_init():
    """Test NPCSystem instantiation"""
    gs = GameState()
    npc_system = NPCSystem(gs)

    assert npc_system is not None, "NPCSystem should instantiate"
    assert npc_system.game_state == gs, "NPCSystem should store game_state reference"


def test_get_current_location_name():
    """Test getting current location name"""
    gs = GameState()
    ms = MapSystem(gs)

    ms.enter_location('tutorial_warren')
    name = ms.get_current_location_name()

    assert name == 'Kobold Warren (Tutorial)', "Should return correct location name"


def test_save_and_load_position():
    """Test saving and loading player position"""
    gs = GameState()
    ms = MapSystem(gs)

    # Enter a location and move player
    ms.enter_location('tutorial_warren')
    ms.player_position = [50, 75]

    # Save position
    saved_data = ms.save_position()

    assert saved_data['location'] == 'tutorial_warren', "Saved location should be tutorial_warren"
    assert saved_data['position'] == [50, 75], "Saved position should be [50, 75]"

    # Change position
    ms.player_position = [100, 100]
    ms.game_state.current_location = 'surface_forest'

    # Load saved position
    ms.load_position(saved_data)

    assert ms.player_position == [50, 75], "Loaded position should be [50, 75]"
    assert ms.game_state.current_location == 'tutorial_warren', "Loaded location should be tutorial_warren"


def test_calculate_distance():
    """Test distance calculation between positions"""
    gs = GameState()
    ms = MapSystem(gs)

    # Test distance between [0, 0] and [3, 4] should be 5 (3-4-5 triangle)
    distance = ms.calculate_distance([0, 0], [3, 4])
    assert abs(distance - 5.0) < 0.01, "Distance should be approximately 5.0"

    # Test distance to same position should be 0
    distance = ms.calculate_distance([128, 112], [128, 112])
    assert distance == 0.0, "Distance to same position should be 0"


def test_is_in_area():
    """Test area containment check"""
    gs = GameState()
    ms = MapSystem(gs)

    # Test position inside area
    assert ms.is_in_area([10, 10], [0, 0], [20, 20]) == True, "Position should be in area"

    # Test position outside area
    assert ms.is_in_area([25, 25], [0, 0], [20, 20]) == False, "Position should not be in area"

    # Test position on edge (should be inside due to < comparison)
    assert ms.is_in_area([0, 0], [0, 0], [20, 20]) == True, "Position on min edge should be in area"
    assert ms.is_in_area([19, 19], [0, 0], [20, 20]) == True, "Position just inside should be in area"
    assert ms.is_in_area([20, 20], [0, 0], [20, 20]) == False, "Position on max edge should not be in area"
