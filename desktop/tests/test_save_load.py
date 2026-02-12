"""
Unit tests for save/load round-trip
Tests SaveSystem class integrity with file I/O
"""

import pytest
import os
from utils.save_system import SaveSystem
from utils.game_state import GameState


def flatten_game_state(gs):
    """
    Flatten GameState into the format SaveSystem.create_save_data expects.
    SaveSystem expects a flat dict with story flags at top level, not nested.
    """
    flat = gs.__dict__.copy()
    # Merge story_flags into top level
    if 'story_flags' in flat:
        for flag, value in flat['story_flags'].items():
            flat[flag] = value
    return flat


def test_save_load_roundtrip(tmp_path, headless_pygame):
    """Test basic save and load round-trip preserves data"""
    # Create SaveSystem with temp directory
    ss = SaveSystem(save_directory=str(tmp_path))

    # Create GameState and modify some values
    gs = GameState()
    gs.gil = 500
    gs.story_flags['met_orisia'] = True

    # SaveSystem.create_save_data expects flat dict with story flags at top level
    state_dict = flatten_game_state(gs)

    # Save game
    result = ss.save_game(state_dict, slot=1, save_type='manual')
    assert result == True, "Save should succeed"

    # Load game
    loaded_data = ss.load_game(slot=1, save_type='manual')
    assert loaded_data is not None, "Load should return data"

    # Verify gil was preserved
    assert loaded_data['inventory']['gil'] == 500

    # Verify story flag was preserved
    assert loaded_data['story_flags']['met_orisia'] == True


def test_party_preserved(tmp_path, headless_pygame):
    """Test that party composition is preserved through save/load"""
    ss = SaveSystem(save_directory=str(tmp_path))
    gs = GameState()

    # Modify party
    gs.active_party = ['javin', 'fei', 'iris']
    gs.characters_recruited = ['javin', 'fei', 'iris', 'frostbite']

    # Save
    state_dict = flatten_game_state(gs)
    ss.save_game(state_dict, slot=2)

    # Load
    loaded_data = ss.load_game(slot=2)

    # Verify party
    assert loaded_data['party']['active'] == ['javin', 'fei', 'iris']
    assert 'frostbite' in loaded_data['characters_recruited']


def test_inventory_preserved(tmp_path, headless_pygame):
    """Test that inventory items and gil are preserved"""
    ss = SaveSystem(save_directory=str(tmp_path))
    gs = GameState()

    # Set inventory
    gs.items = {'potion': 10, 'ether': 3, 'elixir': 1}
    gs.gil = 9999
    gs.key_items = ['crown_of_flowers', 'ruby_ring']

    # Save
    state_dict = flatten_game_state(gs)
    ss.save_game(state_dict, slot=3)

    # Load
    loaded_data = ss.load_game(slot=3)

    # Verify inventory
    assert loaded_data['inventory']['items']['potion'] == 10
    assert loaded_data['inventory']['items']['ether'] == 3
    assert loaded_data['inventory']['items']['elixir'] == 1
    assert loaded_data['inventory']['gil'] == 9999
    assert 'crown_of_flowers' in loaded_data['inventory']['key_items']
    assert 'ruby_ring' in loaded_data['inventory']['key_items']


def test_story_flags_preserved(tmp_path, headless_pygame):
    """Test that story flags are preserved through save/load"""
    ss = SaveSystem(save_directory=str(tmp_path))
    gs = GameState()

    # Set multiple story flags
    gs.story_flags['met_orisia'] = True
    gs.story_flags['flood_dead'] = True
    gs.story_flags['recruitment_deadline_passed'] = True
    gs.story_flags['yipp_alignment'] = 'saint'
    gs.story_flags['cure_found'] = False

    # Save
    state_dict = flatten_game_state(gs)
    ss.save_game(state_dict, slot=4)

    # Load
    loaded_data = ss.load_game(slot=4)

    # Verify all flags
    assert loaded_data['story_flags']['met_orisia'] == True
    assert loaded_data['story_flags']['flood_dead'] == True
    assert loaded_data['story_flags']['recruitment_deadline_passed'] == True
    assert loaded_data['story_flags']['yipp_alignment'] == 'saint'
    assert loaded_data['story_flags']['cure_found'] == False


def test_invalid_slot_handling(tmp_path, headless_pygame):
    """Test that loading non-existent save slot returns None"""
    ss = SaveSystem(save_directory=str(tmp_path))

    # Try to load from slot that doesn't exist
    result = ss.load_game(slot=99)

    # Should return None, not crash
    assert result is None


def test_autosave_and_quicksave(tmp_path, headless_pygame):
    """Test autosave and quicksave functionality"""
    ss = SaveSystem(save_directory=str(tmp_path))
    gs = GameState()
    gs.gil = 777

    state_dict = flatten_game_state(gs)

    # Test autosave
    result = ss.save_game(state_dict, save_type='auto')
    assert result == True
    loaded_auto = ss.load_game(save_type='auto')
    assert loaded_auto is not None
    assert loaded_auto['inventory']['gil'] == 777

    # Test quicksave
    gs.gil = 888
    state_dict = flatten_game_state(gs)
    result = ss.save_game(state_dict, save_type='quick')
    assert result == True
    loaded_quick = ss.load_game(save_type='quick')
    assert loaded_quick is not None
    assert loaded_quick['inventory']['gil'] == 888


def test_character_state_preserved(tmp_path, headless_pygame):
    """Test that character stats and levels are preserved"""
    ss = SaveSystem(save_directory=str(tmp_path))
    gs = GameState()

    # Modify character state (Javin starts in party)
    if 'javin' in gs.characters:
        gs.characters['javin']['level'] = 25
        gs.characters['javin']['stats']['hp'] = 500
        gs.characters['javin']['stats']['mp'] = 100

    # Save
    state_dict = flatten_game_state(gs)
    ss.save_game(state_dict, slot=5)

    # Load
    loaded_data = ss.load_game(slot=5)

    # Verify character state
    assert 'javin' in loaded_data['party']['characters']
    assert loaded_data['party']['characters']['javin']['level'] == 25
    assert loaded_data['party']['characters']['javin']['stats']['hp'] == 500
    assert loaded_data['party']['characters']['javin']['stats']['mp'] == 100


def test_location_and_position_preserved(tmp_path, headless_pygame):
    """Test that current location and player position are preserved"""
    ss = SaveSystem(save_directory=str(tmp_path))
    gs = GameState()

    # Set location and position
    gs.current_location = 'imperial_city'
    gs.player_position = [200, 150]

    # Save
    state_dict = flatten_game_state(gs)
    ss.save_game(state_dict, slot=6)

    # Load
    loaded_data = ss.load_game(slot=6)

    # Verify location
    assert loaded_data['current_location'] == 'imperial_city'
    assert loaded_data['player_position'] == [200, 150]


def test_import_state_reconstructs_gamestate(tmp_path, headless_pygame):
    """Test that GameState.import_state() correctly reconstructs state from save data"""
    ss = SaveSystem(save_directory=str(tmp_path))

    # Create and modify original GameState
    gs_original = GameState()
    gs_original.gil = 1234
    gs_original.story_flags['met_orisia'] = True
    gs_original.story_flags['flood_dead'] = True
    gs_original.current_location = 'desert'

    # Save
    state_dict = flatten_game_state(gs_original)
    ss.save_game(state_dict, slot=7)

    # Load into new GameState
    gs_new = GameState()
    loaded_data = ss.load_game(slot=7)
    gs_new.import_state(loaded_data)

    # Verify state was imported correctly
    assert gs_new.gil == 1234
    assert gs_new.story_flags['met_orisia'] == True
    assert gs_new.story_flags['flood_dead'] == True
    assert gs_new.current_location == 'desert'
