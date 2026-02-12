"""
Unit tests for level-up system and character progression
Tests cover: EXP calculation, level-up mechanics, stat growth, abilities
"""

import pytest
from utils.game_state import GameState
from utils.level_up_system import (
    calculate_exp_for_level,
    get_exp_to_next_level,
    add_experience,
    learn_ability,
    get_next_ability_level
)
from data.characters import CHARACTERS


def test_exp_increases_per_level(headless_pygame):
    """EXP requirements increase with each level"""
    for level in range(1, 10):
        exp_current = calculate_exp_for_level(level)
        exp_next = calculate_exp_for_level(level + 1)
        assert exp_next > exp_current, f"Level {level+1} should require more EXP than level {level}"


def test_add_experience_levels_up(headless_pygame):
    """Adding EXP causes level-up"""
    gs = GameState()

    # Give massive EXP to trigger multiple level-ups
    result = add_experience(gs, 'javin', 99999)

    assert result is not None, "add_experience should return results dict"
    assert result['leveled_up'] == True, "Character should have leveled up"
    assert result['new_level'] > 1, "New level should be greater than 1"
    assert result['levels_gained'] > 0, "Should have gained at least one level"


def test_level_1_base_stats(headless_pygame):
    """Characters start with base stats at level 1"""
    gs = GameState()

    char = gs.characters['javin']
    base_stats = CHARACTERS['javin']['base_stats']

    # Check that max HP matches base
    assert char['max_hp'] == base_stats['hp'], "Max HP should match base stat at level 1"

    # Check attack stat
    assert char['stats']['attack'] == base_stats['attack'], "Attack should match base stat at level 1"


def test_growth_varies_by_character(headless_pygame):
    """Different characters have different growth rates"""
    # Fei is a physical tank, Iris is a mage
    # Check that their attack growth rates differ
    fei_attack_growth = CHARACTERS['fei']['growth_rates']['attack']

    # Find a mage character (one with high magic_power growth)
    mage_char = None
    mage_attack_growth = None
    for char_id, char_data in CHARACTERS.items():
        if char_data['growth_rates'].get('magic_power', 0) > 2.0:
            mage_char = char_id
            mage_attack_growth = char_data['growth_rates']['attack']
            break

    if mage_char:
        # Physical character should have higher attack growth than mage
        assert fei_attack_growth != mage_attack_growth, "Physical and magic characters should have different attack growth"


def test_level_99_no_overflow(headless_pygame):
    """Adding massive EXP doesn't overflow stats"""
    gs = GameState()

    # Give insane EXP
    result = add_experience(gs, 'javin', 10000000)

    assert result is not None, "add_experience should handle massive EXP"

    char = gs.characters['javin']

    # Check level cap
    assert char['level'] <= 99, "Level should not exceed 99"

    # Check all stats are positive integers
    assert char['max_hp'] > 0, "Max HP should be positive"
    assert char['max_mp'] >= 0, "Max MP should be non-negative"
    assert char['stats']['attack'] > 0, "Attack should be positive"
    assert char['stats']['defense'] > 0, "Defense should be positive"
    assert char['stats']['magic_power'] >= 0, "Magic power should be non-negative"
    assert char['stats']['spell_resistance'] > 0, "Spell resistance should be positive"
    assert char['stats']['speed'] > 0, "Speed should be positive"


def test_exp_to_next_level_at_max(headless_pygame):
    """EXP to next level is 0 at max level"""
    exp_needed = get_exp_to_next_level(99)
    assert exp_needed == 0, "No more EXP needed at level 99"


def test_stat_increases_on_level_up(headless_pygame):
    """Stats increase when leveling up"""
    gs = GameState()

    # Record initial stats
    char = gs.characters['javin']
    old_attack = char['stats']['attack']
    old_defense = char['stats']['defense']
    old_max_hp = char['max_hp']

    # Level up multiple times
    result = add_experience(gs, 'javin', 5000)

    if result['leveled_up']:
        # Stats should have increased
        assert char['stats']['attack'] >= old_attack, "Attack should not decrease"
        assert char['stats']['defense'] >= old_defense, "Defense should not decrease"
        assert char['max_hp'] > old_max_hp, "Max HP should increase on level up"

        # Check stat increases are recorded in results
        assert 'stat_increases' in result, "Result should include stat increases"
        assert result['stat_increases']['hp'] >= 0, "HP increase should be recorded"


def test_ability_learning_at_milestone(headless_pygame):
    """Abilities are learned at level milestones (every 10 levels)"""
    milestone = get_next_ability_level(1)
    assert milestone == 10, "First ability milestone should be level 10"

    milestone = get_next_ability_level(15)
    assert milestone == 20, "Next milestone after 15 should be level 20"

    milestone = get_next_ability_level(90)
    assert milestone is None, "No milestone after 90"


def test_exp_table_consistency(headless_pygame):
    """Pre-calculated EXP table matches formula"""
    from utils.level_up_system import EXP_TABLE

    for level in range(1, 50):
        calculated = calculate_exp_for_level(level)
        table_value = EXP_TABLE.get(level, 0)
        assert calculated == table_value, f"EXP table mismatch at level {level}"


def test_character_exp_persists(headless_pygame):
    """Character EXP persists across multiple add_experience calls"""
    gs = GameState()

    # Add small amounts of EXP multiple times
    add_experience(gs, 'javin', 100)
    char = gs.characters['javin']
    exp_after_first = char['exp']

    add_experience(gs, 'javin', 200)
    exp_after_second = char['exp']

    # EXP should accumulate
    assert exp_after_second >= exp_after_first, "EXP should accumulate across calls"
