"""
Test full game initialization chain and scene transitions headlessly
Tests GameRoot setup, new_game, and VictoryScreen/GameOverScreen rendering
"""

import pytest
from main import GameRoot
from scene import Size
from scenes.victory import VictoryScreen
from scenes.game_over import GameOverScreen


def test_gameroot_setup(headless_pygame):
    """Test that GameRoot.setup() completes without errors"""
    gr = GameRoot()
    gr.size = Size(256, 224)
    gr.setup()

    # Verify that setup() created expected attributes
    assert hasattr(gr, 'current_scene'), "GameRoot should have current_scene after setup()"
    assert gr.current_scene is not None, "current_scene should be initialized (TitleScreen)"
    assert hasattr(gr, 'game_systems_initialized'), "GameRoot should have game_systems_initialized flag"


def test_gameroot_new_game(headless_pygame):
    """Test that GameRoot.new_game() initializes game state"""
    gr = GameRoot()
    gr.size = Size(256, 224)
    gr.setup()

    # Start new game
    gr.new_game()

    # Verify game state is initialized
    assert hasattr(gr, 'game_state_data'), "GameRoot should have game_state_data after new_game()"
    assert gr.game_state_data is not None, "game_state_data should be initialized"
    assert gr.game_systems_initialized == True, "game_systems_initialized should be True"


def test_gameroot_draw_no_crash(headless_pygame):
    """Test that GameRoot.draw() can be called without crashing"""
    gr = GameRoot()
    gr.size = Size(256, 224)
    gr.setup()

    # Draw should work even without new_game()
    gr.draw()

    # No assertion needed - just verifying no exception


def test_victory_screen_init(headless_pygame):
    """Test that VictoryScreen can be instantiated"""
    # Build mock game_root with attributes VictoryScreen needs
    # Note: VictoryScreen expects 'game_state' attribute (not 'game_state_data')
    class MockGameRoot:
        def __init__(self):
            from utils.game_state import GameState
            self.game_state = GameState()
            self.game_state.reset_new_game()

    mock_root = MockGameRoot()
    vs = VictoryScreen(mock_root)

    # Verify basic attributes
    assert hasattr(vs, 'game_root')
    assert vs.game_root == mock_root


def test_victory_screen_draw(headless_pygame):
    """Test that VictoryScreen.draw() completes without errors"""
    # Build mock game_root
    # Note: VictoryScreen expects 'game_state' attribute
    class MockGameRoot:
        def __init__(self):
            from utils.game_state import GameState
            self.game_state = GameState()
            self.game_state.reset_new_game()

    mock_root = MockGameRoot()
    vs = VictoryScreen(mock_root)

    # Draw should complete without crashing
    vs.draw()


def test_game_over_screen_init(headless_pygame):
    """Test that GameOverScreen can be instantiated"""
    # Build mock game_root with required methods
    class MockGameRoot:
        def __init__(self):
            self.load_called = False
            self.quit_called = False

        def load_game_from_file(self, filename='autosave.json'):
            self.load_called = True
            return True

        def quit_game(self):
            self.quit_called = True

    mock_root = MockGameRoot()
    gos = GameOverScreen(mock_root)

    # Verify basic attributes
    assert hasattr(gos, 'game_root')
    assert gos.game_root == mock_root
    assert hasattr(gos, 'menu_options')
    assert len(gos.menu_options) >= 3  # At least 3 menu options


def test_game_over_screen_draw(headless_pygame):
    """Test that GameOverScreen.draw() completes without errors"""
    # Build mock game_root
    class MockGameRoot:
        def __init__(self):
            self.load_called = False
            self.quit_called = False

        def load_game_from_file(self, filename='autosave.json'):
            self.load_called = True
            return True

        def quit_game(self):
            self.quit_called = True

    mock_root = MockGameRoot()
    gos = GameOverScreen(mock_root)

    # Draw should complete without crashing
    gos.draw()


def test_game_over_screen_update(headless_pygame):
    """Test that GameOverScreen.update() completes without errors"""
    class MockGameRoot:
        def __init__(self):
            pass

        def load_game_from_file(self, filename='autosave.json'):
            return True

        def quit_game(self):
            pass

    mock_root = MockGameRoot()
    gos = GameOverScreen(mock_root)

    # Update should work for fade-in logic
    gos.update()

    # Verify fade alpha increases
    assert gos.fade_alpha > 0.0
