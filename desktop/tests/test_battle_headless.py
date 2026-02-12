"""
Headless tests for BattleScene instantiation and draw cycle
"""

import pytest
from utils.game_state import GameState
from scenes.battle import BattleScene


class MockGameRoot:
    """Mock GameRoot for BattleScene testing"""
    def __init__(self):
        self.game_state_data = None
        self.current_scene = None
        self.battle_won = False
        self.battle_fled = False
        self.battle_lost = False

    def handle_battle_victory(self):
        """Handle battle victory callback"""
        self.battle_won = True

    def handle_battle_flee(self):
        """Handle battle flee callback"""
        self.battle_fled = True

    def handle_battle_defeat(self):
        """Handle battle defeat callback"""
        self.battle_lost = True


@pytest.fixture
def game_state():
    """Create a fresh GameState for testing"""
    gs = GameState()
    gs.reset_new_game()
    return gs


@pytest.fixture
def mock_game_root():
    """Create a mock GameRoot for testing"""
    return MockGameRoot()


def test_battle_init(headless_pygame, game_state, mock_game_root):
    """Test BattleScene instantiation with valid enemy"""
    battle_scene = BattleScene(
        mock_game_root,
        game_state,
        ['infected_kobold_weak'],
        can_flee=True
    )

    # Verify battle engine was created
    assert hasattr(battle_scene, 'battle')
    assert battle_scene.battle is not None

    # Verify enemies were loaded
    assert len(battle_scene.battle.enemies) > 0

    # Verify initial state
    assert battle_scene.menu_state == 'main'
    assert battle_scene.selected_action is None


def test_battle_draw_no_crash(headless_pygame, game_state, mock_game_root):
    """Test BattleScene draw() completes without errors"""
    battle_scene = BattleScene(
        mock_game_root,
        game_state,
        ['infected_kobold_weak']
    )

    # Draw should complete without exception
    battle_scene.draw()

    # Verify battle log exists
    assert hasattr(battle_scene, 'battle_log')


def test_battle_multi_enemy(headless_pygame, game_state, mock_game_root):
    """Test BattleScene with multiple enemies"""
    battle_scene = BattleScene(
        mock_game_root,
        game_state,
        ['infected_kobold_weak', 'skeleton'],
        can_flee=True
    )

    # Verify both enemies were loaded
    assert len(battle_scene.battle.enemies) == 2

    # Draw should complete without exception
    battle_scene.draw()


def test_battle_update_no_crash(headless_pygame, game_state, mock_game_root):
    """Test BattleScene update() completes without errors"""
    battle_scene = BattleScene(
        mock_game_root,
        game_state,
        ['infected_kobold_weak']
    )

    # Update should complete without exception
    battle_scene.update()

    # Verify battle state tracking
    assert hasattr(battle_scene, 'animating')
    assert hasattr(battle_scene, 'animation_timer')


def test_battle_can_flee_setting(headless_pygame, game_state, mock_game_root):
    """Test BattleScene respects can_flee parameter"""
    # Create battle with flee enabled
    battle_flee_enabled = BattleScene(
        mock_game_root,
        game_state,
        ['infected_kobold_weak'],
        can_flee=True
    )
    assert battle_flee_enabled.battle.can_flee == True

    # Create battle with flee disabled
    battle_flee_disabled = BattleScene(
        mock_game_root,
        game_state,
        ['infected_kobold_weak'],
        can_flee=False
    )
    assert battle_flee_disabled.battle.can_flee == False
