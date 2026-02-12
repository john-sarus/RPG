"""
Pygame shim for Pythonista scene module
Provides geometry types, constants, and Scene base class
"""

import pygame

# ============================================================================
# Module-level state for rendering
# ============================================================================

# Two-surface rendering system:
# - _surface: logical 256x224 surface where all game drawing happens
# - _window: actual display surface (1024x896) that _surface is scaled to
_surface = None
_window = None
_clock = None

# Transform stack for GState context manager
# Each entry is (translate_x, translate_y, scale_x, scale_y)
_transform_stack = [(0.0, 0.0, 1.0, 1.0)]

# ============================================================================
# Geometry Types
# ============================================================================

class Point:
    """2D point with x, y coordinates"""

    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        """Add two points"""
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """Subtract two points"""
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        """Multiply point by scalar"""
        if isinstance(scalar, (int, float)):
            return Point(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __rmul__(self, scalar):
        """Reverse multiply (scalar * point)"""
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """Divide point by scalar"""
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ZeroDivisionError("Cannot divide point by zero")
            return Point(self.x / scalar, self.y / scalar)
        return NotImplemented

    def __eq__(self, other):
        """Check equality"""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        """String representation"""
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        """String representation"""
        return self.__repr__()


class Size:
    """2D size with width and height"""

    def __init__(self, w=0, h=0):
        self._w = float(w)
        self._h = float(h)

    @property
    def w(self):
        """Width (short form)"""
        return self._w

    @property
    def width(self):
        """Width (long form)"""
        return self._w

    @property
    def h(self):
        """Height (short form)"""
        return self._h

    @property
    def height(self):
        """Height (long form)"""
        return self._h

    def __repr__(self):
        """String representation"""
        return f"Size({self._w}, {self._h})"

    def __str__(self):
        """String representation"""
        return self.__repr__()


class Rect:
    """Rectangle with position and size"""

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

    @property
    def origin(self):
        """Top-left corner as Point"""
        return Point(self.x, self.y)

    @property
    def size(self):
        """Size as Size object"""
        return Size(self.w, self.h)

    @property
    def center(self):
        """Center point"""
        return Point(self.x + self.w / 2, self.y + self.h / 2)

    @property
    def min_x(self):
        """Minimum x coordinate"""
        return self.x

    @property
    def max_x(self):
        """Maximum x coordinate"""
        return self.x + self.w

    @property
    def min_y(self):
        """Minimum y coordinate"""
        return self.y

    @property
    def max_y(self):
        """Maximum y coordinate"""
        return self.y + self.h

    def contains_point(self, point):
        """Check if point is inside rectangle"""
        if not isinstance(point, Point):
            return False
        return (self.min_x <= point.x <= self.max_x and
                self.min_y <= point.y <= self.max_y)

    def intersects(self, other):
        """Check if this rectangle intersects another"""
        if not isinstance(other, Rect):
            return False
        return not (self.max_x < other.min_x or
                   self.min_x > other.max_x or
                   self.max_y < other.min_y or
                   self.min_y > other.max_y)

    def __repr__(self):
        """String representation"""
        return f"Rect({self.x}, {self.y}, {self.w}, {self.h})"

    def __str__(self):
        """String representation"""
        return self.__repr__()


# ============================================================================
# Constants
# ============================================================================

# Orientation constants
LANDSCAPE = 'landscape'
PORTRAIT = 'portrait'

# Text alignment constants (as used in Pythonista)
# 1-9 grid: 7 8 9
#           4 5 6
#           1 2 3
# 5 = center, 4 = left, 6 = right, etc.
ALIGN_LEFT = 4
ALIGN_CENTER = 5
ALIGN_RIGHT = 6
ALIGN_TOP = 8
ALIGN_BOTTOM = 2


# ============================================================================
# Action Class (stub for animations)
# ============================================================================

class Action:
    """
    Stub action class for animations
    In the full implementation, these would drive sprite animations
    For now, they just exist to prevent AttributeError
    """

    def __init__(self, duration=1.0):
        self.duration = duration

    @staticmethod
    def move_to(x, y, duration=1.0):
        """Create a move action"""
        return Action(duration)

    @staticmethod
    def fade_to(alpha, duration=1.0):
        """Create a fade action"""
        return Action(duration)

    @staticmethod
    def scale_to(scale, duration=1.0):
        """Create a scale action"""
        return Action(duration)

    @staticmethod
    def sequence(*actions):
        """Create a sequence of actions"""
        total_duration = sum(a.duration for a in actions)
        return Action(total_duration)

    @staticmethod
    def group(*actions):
        """Create a group of parallel actions"""
        max_duration = max((a.duration for a in actions), default=1.0)
        return Action(max_duration)

    @staticmethod
    def wait(duration):
        """Create a wait action"""
        return Action(duration)

    @staticmethod
    def remove():
        """Create a remove action"""
        return Action(0)

    @staticmethod
    def call(func):
        """Create a function call action"""
        return Action(0)


# ============================================================================
# Scene Base Class (placeholder)
# ============================================================================

class Scene:
    """
    Base scene class - manages game loop lifecycle
    Subclasses override setup(), update(), draw(), and touch handlers
    """

    def __init__(self):
        self.size = Size(256, 224)  # Logical resolution
        self.t = 0.0  # Elapsed time in seconds
        self.dt = 0.0  # Delta time (time since last frame)
        self.children = []  # Child nodes (not used in this game, but part of API)
        self._quit_flag = False  # Set to True to exit the game loop
        self._modal_scene = None  # Scene stack for modal presentation

    def setup(self):
        """Called when scene is first presented"""
        pass

    def update(self):
        """Called every frame"""
        pass

    def draw(self):
        """Called every frame to draw"""
        pass

    def touch_began(self, touch):
        """Called when touch begins"""
        pass

    def touch_moved(self, touch):
        """Called when touch moves"""
        pass

    def touch_ended(self, touch):
        """Called when touch ends"""
        pass

    def did_change_size(self):
        """Called when scene size changes"""
        pass

    def close(self):
        """Close the scene and exit the game loop"""
        self._quit_flag = True

    def present_modal_scene(self, scene):
        """Present a scene modally (on top of current scene)"""
        self._modal_scene = scene
        scene.size = self.size
        scene.setup()

    def dismiss_modal_scene(self):
        """Dismiss the current modal scene"""
        self._modal_scene = None


# ============================================================================
# Drawing State
# ============================================================================

class DrawingState:
    """Tracks current drawing state (fill color, stroke color, etc.)"""

    def __init__(self):
        self.fill_color = (255, 255, 255, 255)  # RGBA as 0-255 ints
        self.stroke_color = (0, 0, 0, 255)
        self.stroke_weight_val = 1
        self.fill_enabled = True
        self.stroke_enabled = True

# Module-level drawing state
_drawing_state = DrawingState()

# Font cache to avoid recreating fonts every frame
_font_cache = {}


# ============================================================================
# Coordinate and Color Conversion Helpers
# ============================================================================

def _color_float_to_int(r, g, b, a=1.0):
    """
    Convert Pythonista 0-1 float colors to Pygame 0-255 int colors

    Args:
        r, g, b, a: Float values 0.0-1.0

    Returns:
        Tuple of (r, g, b, a) as 0-255 integers
    """
    return (
        int(r * 255),
        int(g * 255),
        int(b * 255),
        int(a * 255)
    )


def _flip_y(y, h=0):
    """
    Flip y-coordinate from Pythonista (bottom-left origin) to Pygame (top-left origin)

    Args:
        y: Y coordinate in Pythonista space (0 = bottom)
        h: Height of object (for rectangles/ellipses)

    Returns:
        Y coordinate in Pygame space (0 = top)
    """
    global _transform_stack

    # Get current transform
    tx, ty, sx, sy = _transform_stack[-1] if _transform_stack else (0, 0, 1, 1)

    # Apply transform to input coordinates
    y_transformed = y + ty

    # Flip: pygame_y = surface_height - pythonista_y - object_height
    # Logical surface is 256x224
    return 224 - y_transformed - h


def _apply_transform(x, y):
    """
    Apply current transform stack to coordinates

    Args:
        x, y: Input coordinates

    Returns:
        Transformed (x, y) tuple
    """
    global _transform_stack

    if not _transform_stack:
        return (x, y)

    tx, ty, sx, sy = _transform_stack[-1]
    return (x * sx + tx, y * sy + ty)


def _get_font(font_name, font_size):
    """
    Get a pygame font, using cache to avoid recreation

    Args:
        font_name: Font name (ignored, uses system default)
        font_size: Font size in points

    Returns:
        pygame.font.Font instance
    """
    global _font_cache

    cache_key = (font_name, font_size)
    if cache_key not in _font_cache:
        # Try to use system font, fall back to default
        try:
            _font_cache[cache_key] = pygame.font.SysFont(font_name, font_size)
        except:
            _font_cache[cache_key] = pygame.font.Font(None, font_size)

    return _font_cache[cache_key]


# ============================================================================
# Drawing Functions
# ============================================================================

def get_screen_size():
    """Get screen size - returns logical resolution"""
    return Size(256, 224)


class GState:
    """
    Context manager for graphics state (transform stack)
    Pushes current transform on entry, pops on exit
    """

    def __enter__(self):
        """Push current transform state onto stack"""
        global _transform_stack
        # Copy the top of stack
        current = _transform_stack[-1]
        _transform_stack.append(current)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Pop transform state from stack"""
        global _transform_stack
        if len(_transform_stack) > 1:
            _transform_stack.pop()
        return False


def translate(x, y):
    """Translate coordinate system - adds to current transform"""
    global _transform_stack
    if not _transform_stack:
        _transform_stack.append((x, y, 1.0, 1.0))
    else:
        tx, ty, sx, sy = _transform_stack[-1]
        _transform_stack[-1] = (tx + x, ty + y, sx, sy)


def scale(sx, sy=None):
    """Scale coordinate system - multiplies current scale"""
    global _transform_stack
    if sy is None:
        sy = sx
    if not _transform_stack:
        _transform_stack.append((0.0, 0.0, sx, sy))
    else:
        tx, ty, old_sx, old_sy = _transform_stack[-1]
        _transform_stack[-1] = (tx, ty, old_sx * sx, old_sy * sy)


def background(r, g, b):
    """
    Fill background with solid color

    Args:
        r, g, b: Float color values 0.0-1.0
    """
    global _surface
    if _surface is None:
        return

    color = _color_float_to_int(r, g, b, 1.0)
    _surface.fill(color[:3])  # Fill takes RGB only


def fill(r, g, b, a=1.0):
    """
    Set current fill color for subsequent drawing operations

    Args:
        r, g, b: Float color values 0.0-1.0
        a: Alpha (opacity) 0.0-1.0
    """
    global _drawing_state
    _drawing_state.fill_color = _color_float_to_int(r, g, b, a)
    _drawing_state.fill_enabled = True


def rect(x, y, w, h):
    """
    Draw a filled rectangle using current fill color

    Args:
        x, y: Bottom-left corner in Pythonista coordinates
        w, h: Width and height
    """
    global _surface, _drawing_state
    if _surface is None or not _drawing_state.fill_enabled:
        return

    # Apply transform and y-flip
    x_transformed, y_transformed = _apply_transform(x, y)
    pygame_y = _flip_y(y_transformed, h)

    # Draw rectangle
    color = _drawing_state.fill_color
    if len(color) == 4 and color[3] < 255:
        # Handle alpha transparency
        temp_surface = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
        temp_surface.fill(color)
        _surface.blit(temp_surface, (int(x_transformed), int(pygame_y)))
    else:
        # Opaque rectangle
        pygame.draw.rect(_surface, color[:3], (int(x_transformed), int(pygame_y), int(w), int(h)))


def ellipse(x, y, w, h):
    """
    Draw a filled ellipse using current fill color

    Args:
        x, y: Bottom-left corner of bounding box in Pythonista coordinates
        w, h: Width and height of bounding box
    """
    global _surface, _drawing_state
    if _surface is None or not _drawing_state.fill_enabled:
        return

    # Apply transform and y-flip
    x_transformed, y_transformed = _apply_transform(x, y)
    pygame_y = _flip_y(y_transformed, h)

    # Calculate center and radii
    center_x = int(x_transformed + w / 2)
    center_y = int(pygame_y + h / 2)
    radius_x = int(w / 2)
    radius_y = int(h / 2)

    # Draw ellipse
    color = _drawing_state.fill_color
    if radius_x > 0 and radius_y > 0:
        rect_bounds = (int(x_transformed), int(pygame_y), int(w), int(h))
        if len(color) == 4 and color[3] < 255:
            # Handle alpha transparency
            temp_surface = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
            pygame.draw.ellipse(temp_surface, color, (0, 0, int(w), int(h)))
            _surface.blit(temp_surface, (int(x_transformed), int(pygame_y)))
        else:
            # Opaque ellipse
            pygame.draw.ellipse(_surface, color[:3], rect_bounds)


def text(string, font_name='Helvetica', font_size=16, x=0, y=0, alignment=5):
    """
    Draw text at the specified position

    Args:
        string: Text to draw
        font_name: Font name (mapped to system font or default)
        font_size: Font size in points
        x, y: Position in Pythonista coordinates
        alignment: 1-9 grid alignment (5=center, 4=left, 6=right, 8=top, 2=bottom)
    """
    global _surface, _drawing_state
    if _surface is None or not _drawing_state.fill_enabled:
        return

    # Get font
    font = _get_font(font_name, font_size)

    # Render text
    color = _drawing_state.fill_color[:3]  # RGB only for text rendering
    text_surface = font.render(str(string), True, color)
    text_rect = text_surface.get_rect()

    # Apply transform
    x_transformed, y_transformed = _apply_transform(x, y)

    # Handle alignment
    # Alignment grid: 7 8 9
    #                 4 5 6
    #                 1 2 3
    # 5 = center, 4 = left, 6 = right, 8 = top center, 2 = bottom center
    if alignment in [4, 5, 6]:  # Middle row (vertical center)
        text_rect.centery = int(_flip_y(y_transformed, 0))
    elif alignment in [7, 8, 9]:  # Top row
        text_rect.top = int(_flip_y(y_transformed, 0))
    else:  # Bottom row [1, 2, 3]
        text_rect.bottom = int(_flip_y(y_transformed, 0))

    if alignment in [4, 7, 1]:  # Left column
        text_rect.left = int(x_transformed)
    elif alignment in [5, 8, 2]:  # Center column
        text_rect.centerx = int(x_transformed)
    else:  # Right column [6, 9, 3]
        text_rect.right = int(x_transformed)

    # Draw text
    if len(_drawing_state.fill_color) == 4 and _drawing_state.fill_color[3] < 255:
        # Handle alpha transparency
        text_surface.set_alpha(_drawing_state.fill_color[3])
    _surface.blit(text_surface, text_rect)


def line(x1, y1, x2, y2):
    """
    Draw a line using current stroke color and weight

    Args:
        x1, y1: Start point in Pythonista coordinates
        x2, y2: End point in Pythonista coordinates
    """
    global _surface, _drawing_state
    if _surface is None or not _drawing_state.stroke_enabled:
        return

    # Apply transform and y-flip
    x1_transformed, y1_transformed = _apply_transform(x1, y1)
    x2_transformed, y2_transformed = _apply_transform(x2, y2)
    pygame_y1 = _flip_y(y1_transformed, 0)
    pygame_y2 = _flip_y(y2_transformed, 0)

    # Draw line
    color = _drawing_state.stroke_color[:3]  # RGB only
    width = max(1, int(_drawing_state.stroke_weight_val))
    pygame.draw.line(_surface, color,
                    (int(x1_transformed), int(pygame_y1)),
                    (int(x2_transformed), int(pygame_y2)),
                    width)


def no_fill():
    """Disable fill for subsequent drawing operations"""
    global _drawing_state
    _drawing_state.fill_enabled = False


def no_stroke():
    """Disable stroke for subsequent drawing operations"""
    global _drawing_state
    _drawing_state.stroke_enabled = False


def stroke(r, g, b, a=1.0):
    """
    Set current stroke color for line drawing

    Args:
        r, g, b: Float color values 0.0-1.0
        a: Alpha (opacity) 0.0-1.0
    """
    global _drawing_state
    _drawing_state.stroke_color = _color_float_to_int(r, g, b, a)
    _drawing_state.stroke_enabled = True


def stroke_weight(w):
    """
    Set stroke width for line drawing

    Args:
        w: Line width in pixels
    """
    global _drawing_state
    _drawing_state.stroke_weight_val = w


def run(scene, orientation=LANDSCAPE, frame_interval=2):
    """
    Run the game with Pygame

    Args:
        scene: Scene instance to run
        orientation: LANDSCAPE or PORTRAIT (only LANDSCAPE supported)
        frame_interval: Frame interval (2 = 30fps, 1 = 60fps)
    """
    global _surface, _window, _clock

    # Initialize Pygame
    pygame.init()

    # Logical resolution (SNES-era pixel-perfect)
    LOGICAL_WIDTH = 256
    LOGICAL_HEIGHT = 224

    # Window size (4x scale)
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 896

    # Create window and surfaces
    _window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("There Will Be Kobolds")

    # Create logical surface for game rendering
    _surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

    # Create clock for frame rate control
    _clock = pygame.time.Clock()

    # Set scene size and initialize
    scene.size = Size(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    scene.setup()

    # Main game loop
    running = True
    start_time = pygame.time.get_ticks()
    last_time = start_time

    while running and not scene._quit_flag:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update time
        current_time = pygame.time.get_ticks()
        scene.t = (current_time - start_time) / 1000.0  # Convert to seconds
        scene.dt = (current_time - last_time) / 1000.0
        last_time = current_time

        # Update scene
        scene.update()

        # Draw scene to logical surface
        scene.draw()

        # Scale logical surface to window
        scaled_surface = pygame.transform.scale(_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        _window.blit(scaled_surface, (0, 0))

        # Flip display
        pygame.display.flip()

        # Control frame rate (30 FPS for frame_interval=2)
        target_fps = 60 // frame_interval
        _clock.tick(target_fps)

    # Cleanup
    pygame.quit()
