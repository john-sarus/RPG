"""
Headless tests for shim rendering functions
Verifies drawing primitives work correctly without opening a window
"""

import pytest
import scene


def test_background_fills_surface(headless_pygame):
    """Test that background() fills the entire surface with specified color"""
    # Fill with red
    scene.background(1.0, 0.0, 0.0)

    # Check center pixel is red
    color = scene._surface.get_at((128, 112))
    assert color == (255, 0, 0, 255), f"Expected red (255,0,0,255), got {color}"


def test_fill_rect_draws_green(headless_pygame):
    """Test that fill() and rect() draw a green rectangle"""
    # Clear to black first
    scene.background(0.0, 0.0, 0.0)

    # Set fill color to green
    scene.fill(0.0, 1.0, 0.0)

    # Draw rectangle at Pythonista coords (10, 10, 50, 30)
    # In Pythonista: bottom-left at (10, 10), width 50, height 30
    # Y-flip: pygame_y = 224 - 10 - 30 = 184
    scene.rect(10, 10, 50, 30)

    # Check pixel inside the rectangle (in pygame coords)
    # X: 10 + 25 = 35 (middle of width)
    # Y: 184 + 15 = 199 (middle of height)
    color = scene._surface.get_at((35, 199))
    assert color == (0, 255, 0, 255), f"Expected green (0,255,0,255), got {color}"


def test_color_float_to_int(headless_pygame):
    """Test color conversion from 0-1 floats to 0-255 ints"""
    # Test full red
    result = scene._color_float_to_int(1.0, 0.5, 0.0, 1.0)
    assert result == (255, 127, 0, 255), f"Expected (255,127,0,255), got {result}"

    # Test black
    result = scene._color_float_to_int(0.0, 0.0, 0.0, 1.0)
    assert result == (0, 0, 0, 255), f"Expected (0,0,0,255), got {result}"

    # Test white
    result = scene._color_float_to_int(1.0, 1.0, 1.0, 1.0)
    assert result == (255, 255, 255, 255), f"Expected (255,255,255,255), got {result}"


def test_text_renders_without_crash(headless_pygame):
    """Test that text rendering doesn't crash"""
    # Clear to black
    scene.background(0.0, 0.0, 0.0)

    # Set fill color to white
    scene.fill(1.0, 1.0, 1.0)

    # Render text at center
    # Should not raise an exception
    # Font rendering is system-dependent, so we don't assert pixel colors
    try:
        scene.text('Test', 'Helvetica', 16, 128, 112, alignment=5)
        success = True
    except Exception as e:
        success = False
        pytest.fail(f"text() raised exception: {e}")

    assert success, "text() should not crash"


def test_y_flip_calculation(headless_pygame):
    """Test y-coordinate flipping from Pythonista to Pygame coords"""
    # Pythonista: y=0 is bottom, y increases upward
    # Pygame: y=0 is top, y increases downward
    # Surface height is 224

    # Test y=0 (bottom in Pythonista) maps to y=224 (bottom in Pygame)
    flipped = scene._flip_y(0, 0)
    assert flipped == 224, f"Expected y=0 to flip to 224, got {flipped}"

    # Test y=224 (top in Pythonista) maps to y=0 (top in Pygame)
    flipped = scene._flip_y(224, 0)
    assert flipped == 0, f"Expected y=224 to flip to 0, got {flipped}"

    # Test rect at y=10 with height=30
    # Bottom edge at y=10, top edge at y=40 (Pythonista)
    # In Pygame: top edge at y = 224-40 = 184, bottom edge at y = 224-10 = 214
    flipped = scene._flip_y(10, 30)
    assert flipped == 184, f"Expected rect y=10 h=30 to flip to 184, got {flipped}"


def test_drawing_state_initialization(headless_pygame):
    """Test that DrawingState initializes with correct defaults"""
    # _drawing_state is module-level in scene.py
    state = scene._drawing_state

    # Check default fill color is white
    assert state.fill_color == (255, 255, 255, 255), f"Expected white fill, got {state.fill_color}"

    # Check default stroke color is black
    assert state.stroke_color == (0, 0, 0, 255), f"Expected black stroke, got {state.stroke_color}"

    # Check fill is enabled by default
    assert state.fill_enabled == True, "Fill should be enabled by default"

    # Check stroke is enabled by default
    assert state.stroke_enabled == True, "Stroke should be enabled by default"

    # Check default stroke weight
    assert state.stroke_weight_val == 1, f"Expected stroke weight 1, got {state.stroke_weight_val}"
