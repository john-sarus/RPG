"""
Test TitleScreen rendering without crashing in headless mode
"""

import pytest
from scenes.title_screen import TitleScreen
from scene import Point


class MockGameRoot:
    """Mock GameRoot for TitleScreen testing"""

    def __init__(self):
        self.game_state_data = None
        self.new_game_called = False
        self.load_called = False
        self.quit_called = False

    def new_game(self):
        """Mock new game method"""
        self.new_game_called = True

    def load_game_from_file(self, filename=None):
        """Mock load game method"""
        self.load_called = True
        return False  # No save file in tests

    def quit_game(self):
        """Mock quit game method"""
        self.quit_called = True


class MockTouch:
    """Mock Touch object for testing touch input"""

    def __init__(self, x, y):
        self.location = Point(x, y)
        self.prev_location = Point(x, y)


def test_draw_no_crash(headless_pygame):
    """Verify TitleScreen.draw() completes without errors"""
    mock_root = MockGameRoot()
    title_screen = TitleScreen(mock_root)

    # This should not raise any exception
    title_screen.draw()


def test_draw_with_selection(headless_pygame):
    """Verify TitleScreen.draw() works with different selected_index"""
    mock_root = MockGameRoot()
    title_screen = TitleScreen(mock_root)

    # Test drawing with different selections
    title_screen.selected_index = 1
    title_screen.draw()

    title_screen.selected_index = 4
    title_screen.draw()


def test_menu_options_exist(headless_pygame):
    """Verify TitleScreen has menu_options list"""
    mock_root = MockGameRoot()
    title_screen = TitleScreen(mock_root)

    assert hasattr(title_screen, 'menu_options')
    assert isinstance(title_screen.menu_options, list)
    assert len(title_screen.menu_options) >= 3
    assert 'New Game' in title_screen.menu_options


def test_touch_began_no_crash(headless_pygame):
    """Verify touch_began doesn't crash even if it doesn't hit a button"""
    mock_root = MockGameRoot()
    title_screen = TitleScreen(mock_root)

    # Create mock touch at center of screen
    mock_touch = MockTouch(128, 100)

    # This should not raise any exception
    title_screen.touch_began(mock_touch, 128, 100)


def test_menu_selection_callbacks(headless_pygame):
    """Verify menu selection calls the correct game_root methods"""
    mock_root = MockGameRoot()
    title_screen = TitleScreen(mock_root)

    # Test New Game selection
    title_screen.handle_menu_selection('New Game')
    assert mock_root.new_game_called

    # Test Load selection
    title_screen.handle_menu_selection('Continue')
    assert mock_root.load_called

    # Test Exit selection
    title_screen.handle_menu_selection('Exit')
    assert mock_root.quit_called
