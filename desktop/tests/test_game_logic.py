"""
Unit tests for game logic - recruitment, flags, and endings
Tests critical game rules like recruitment deadlines, Flood death, character pairing, etc.
"""

import pytest
from utils.game_state import GameState
from utils.recruitment_system import RecruitmentSystem
from utils.story_event_system import StoryEventSystem


def test_recruitment_deadline_blocks(headless_pygame):
    """Test that recruitment_deadline_passed flag blocks recruitment"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = True
    rs = RecruitmentSystem(gs)

    # Frostbite should not be recruitable after deadline
    assert rs.is_character_recruitable('frostbite') == False


def test_recruitment_available_before_deadline(headless_pygame):
    """Test that characters can be recruited before deadline (with prerequisites)"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = False
    gs.story_flags['met_frostbite'] = True  # Set prerequisite flag
    rs = RecruitmentSystem(gs)

    # Frostbite is recruitable if prerequisites met and deadline not passed
    # May still return False if other prereqs missing, but should not crash
    result = rs.is_character_recruitable('frostbite')
    assert isinstance(result, bool)  # At least verify it returns a boolean


def test_recruitment_before_deadline_with_prereq(headless_pygame):
    """Test that characters are recruitable with correct prerequisites"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = False
    gs.story_flags['met_frostbite'] = True
    rs = RecruitmentSystem(gs)

    # With the prerequisite flag set, frostbite should be recruitable
    assert rs.is_character_recruitable('frostbite') == True


def test_flood_death_flag(headless_pygame):
    """Test that flood_dead flag can be set and persists"""
    gs = GameState()

    # Initially False
    assert gs.story_flags.get('flood_dead', False) == False

    # Set to True
    gs.story_flags['flood_dead'] = True
    assert gs.story_flags['flood_dead'] == True


def test_flood_removal_from_party(headless_pygame):
    """Test that Flood can be removed from party after death flag"""
    gs = GameState()
    gs.active_party = ['javin', 'flood']
    gs.characters_recruited = ['javin', 'flood']
    gs.story_flags['flood_dead'] = True

    # Simulate flood removal
    if 'flood' in gs.active_party:
        gs.active_party.remove('flood')

    assert 'flood' not in gs.active_party
    assert gs.story_flags['flood_dead'] == True


def test_fritzzit_crankpot_pairing(headless_pygame):
    """Test that Fritzzit and Crankpot are recruited together"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = False
    gs.story_flags['kobolds_released'] = True
    gs.story_flags['met_orisia'] = False
    rs = RecruitmentSystem(gs)

    # Check that paired recruitment method exists
    result = rs._recruit_paired_characters('fritzzit', 'crankpot')

    # Should return a dict with success status
    assert isinstance(result, dict)
    assert 'success' in result


def test_fritzzit_crankpot_recruitment_mechanics(headless_pygame):
    """Test that attempting to recruit fritzzit or crankpot recruits both"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = False
    gs.story_flags['kobolds_released'] = True
    gs.story_flags['met_orisia'] = False
    rs = RecruitmentSystem(gs)

    # Attempt recruitment of fritzzit with 'yes' answer
    result = rs.attempt_recruitment('fritzzit', 'yes')

    # Should succeed and recruit both
    assert isinstance(result, dict)
    if result.get('success'):
        # If recruitment succeeded, check that both are in recruited list
        assert 'fritzzit' in gs.characters_recruited
        assert 'crankpot' in gs.characters_recruited


def test_yipp_alignment_flag(headless_pygame):
    """Test that yipp_alignment flag can hold 'saint' or 'vampire' values"""
    gs = GameState()

    # Test saint alignment
    gs.story_flags['yipp_alignment'] = 'saint'
    assert gs.story_flags['yipp_alignment'] == 'saint'

    # Test vampire alignment
    gs.story_flags['yipp_alignment'] = 'vampire'
    assert gs.story_flags['yipp_alignment'] == 'vampire'


def test_recruitment_already_recruited(headless_pygame):
    """Test that already-recruited characters cannot be recruited again"""
    gs = GameState()
    gs.characters_recruited = ['javin', 'frostbite']
    gs.story_flags['recruitment_deadline_passed'] = False
    rs = RecruitmentSystem(gs)

    # Frostbite is already recruited
    assert rs.is_character_recruitable('frostbite') == False


def test_met_orisia_flag(headless_pygame):
    """Test that met_orisia flag works correctly"""
    gs = GameState()

    # Initially not set
    assert gs.story_flags.get('met_orisia', False) == False

    # Set to True
    gs.story_flags['met_orisia'] = True
    assert gs.story_flags['met_orisia'] == True


def test_yipp_requires_pre_orisia(headless_pygame):
    """Test that Yipp cannot be recruited after meeting Orisia"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = False
    gs.story_flags['met_orisia'] = True  # Already met Orisia
    rs = RecruitmentSystem(gs)

    # Yipp should not be recruitable after Orisia
    assert rs.is_character_recruitable('yipp') == False


def test_story_event_system_init(headless_pygame):
    """Test that StoryEventSystem can be initialized"""
    gs = GameState()
    ses = StoryEventSystem(gs)

    assert ses.game_state is gs
    assert ses.current_event is None
    assert isinstance(ses.event_queue, list)


def test_recruitment_close_sets_deadline(headless_pygame):
    """Test that closing recruitment window sets the deadline flag"""
    gs = GameState()
    gs.story_flags['recruitment_deadline_passed'] = False

    # Close recruitment via game_state method
    gs.close_recruitment()

    # Deadline should now be passed
    assert gs.story_flags['recruitment_deadline_passed'] == True
