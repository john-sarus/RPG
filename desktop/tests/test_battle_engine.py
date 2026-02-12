"""
Unit tests for battle engine combat system
Tests damage calculation, turn order, status effects, and battle end detection
"""

import pytest
from unittest.mock import patch, MagicMock
from utils.battle_engine import BattleEngine
from utils.game_state import GameState


@pytest.fixture
def game_state():
    """Create a fresh GameState for testing"""
    gs = GameState()
    gs.reset_new_game()
    return gs


@pytest.fixture
def battle_engine(game_state):
    """Create a BattleEngine with a single weak enemy"""
    return BattleEngine(game_state, ['infected_kobold_weak'])


def test_engine_init(battle_engine):
    """Test that BattleEngine initializes correctly"""
    assert battle_engine.party is not None
    assert isinstance(battle_engine.party, list)
    assert len(battle_engine.party) > 0

    assert battle_engine.enemies is not None
    assert isinstance(battle_engine.enemies, list)
    assert len(battle_engine.enemies) > 0

    assert battle_engine.can_flee == True
    assert battle_engine.battle_over == False
    assert battle_engine.victory == False


def test_turn_order(battle_engine):
    """Test that turn order is calculated correctly"""
    battle_engine.calculate_turn_order()

    assert battle_engine.turn_order is not None
    assert isinstance(battle_engine.turn_order, list)

    # Turn order should include all party members and enemies
    expected_count = len(battle_engine.party) + len(battle_engine.enemies)
    assert len(battle_engine.turn_order) == expected_count

    # Verify turn order is sorted by speed (highest first)
    for i in range(len(battle_engine.turn_order) - 1):
        # Allow for equal speeds due to randomization
        assert battle_engine.turn_order[i]['speed'] >= battle_engine.turn_order[i + 1]['speed'] - 1


def test_physical_damage(battle_engine):
    """Test that physical damage calculation returns a valid number"""
    attacker = battle_engine.party[0]
    target = battle_engine.enemies[0]

    damage = battle_engine.calculate_physical_damage(attacker, target)

    assert isinstance(damage, int)
    assert damage >= 1  # Minimum damage is 1


def test_physical_damage_with_bonus(battle_engine):
    """Test physical damage with bonus multiplier"""
    attacker = battle_engine.party[0]
    target = battle_engine.enemies[0]

    normal_damage = battle_engine.calculate_physical_damage(attacker, target, bonus_multiplier=1.0)
    bonus_damage = battle_engine.calculate_physical_damage(attacker, target, bonus_multiplier=2.0)

    # With 2x multiplier, damage should be significantly higher (accounting for random variance)
    assert bonus_damage > normal_damage * 1.5


def test_battle_end_detection_victory(battle_engine):
    """Test battle end detection when all enemies are defeated"""
    # Set all enemies to 0 HP
    for enemy in battle_engine.enemies:
        enemy['hp'] = 0

    battle_engine.check_battle_end()

    assert battle_engine.battle_over == True
    assert battle_engine.victory == True


def test_battle_end_detection_defeat(battle_engine):
    """Test battle end detection when party is defeated"""
    # Set all party members to 0 HP
    for member in battle_engine.party:
        member['data']['hp'] = 0

    battle_engine.check_battle_end()

    assert battle_engine.battle_over == True
    assert battle_engine.victory == False


def test_battle_end_detection_ongoing(battle_engine):
    """Test that battle continues when both sides have living members"""
    # Ensure at least one party member and one enemy are alive
    battle_engine.party[0]['data']['hp'] = 10
    battle_engine.enemies[0]['hp'] = 10

    battle_engine.check_battle_end()

    # Battle should NOT be over
    assert battle_engine.battle_over == False


def test_burn_spread_with_mock(battle_engine):
    """Test burn spread logic with mocked random"""
    # Create a battle with multiple enemies
    battle_engine_multi = BattleEngine(battle_engine.game_state,
                                      ['infected_kobold_weak', 'skeleton'])

    # Apply burn status to first enemy
    from utils.status_effects import apply_status_effect
    apply_status_effect(battle_engine_multi.enemies[0], 'burn', duration=3, potency=5)

    # Mock random.random to return 0.01 (below 15% threshold)
    with patch('random.random', return_value=0.01):
        # This should trigger burn spread
        battle_engine_multi.process_burn_spread()

    # Test passes if no exception raised
    assert True


def test_process_all_status_effects(battle_engine):
    """Test that status effect processing runs without error"""
    # Apply a status effect to test processing
    from utils.status_effects import apply_status_effect

    apply_status_effect(battle_engine.party[0]['data'], 'poison', duration=2, potency=5)

    # Process status effects
    battle_engine.process_all_status_effects()

    # Test passes if no exception raised
    assert True


def test_multi_enemy_battle(game_state):
    """Test battle initialization with multiple enemies"""
    be = BattleEngine(game_state, ['infected_kobold_weak', 'skeleton'])

    assert len(be.enemies) == 2
    assert be.enemies[0]['id'] == 'infected_kobold_weak'
    assert be.enemies[1]['id'] == 'skeleton'


def test_can_flee_setting(game_state):
    """Test that can_flee parameter is respected"""
    # Default: can flee
    be_can_flee = BattleEngine(game_state, ['infected_kobold_weak'], can_flee=True)
    assert be_can_flee.can_flee == True

    # Boss battle: cannot flee
    be_cannot_flee = BattleEngine(game_state, ['infected_kobold_weak'], can_flee=False)
    assert be_cannot_flee.can_flee == False
