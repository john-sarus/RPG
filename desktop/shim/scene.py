"""
Pygame shim for Pythonista scene module
Provides geometry types, constants, and Scene base class
"""

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
    Base scene class (placeholder for now)
    Will be fully implemented in SHIM-003
    """

    def __init__(self):
        self.size = Size(256, 224)
        self.t = 0.0  # elapsed time
        self.dt = 0.0  # delta time
        self.children = []

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


# ============================================================================
# Stub Functions (to be implemented in later tasks)
# ============================================================================

def get_screen_size():
    """Get screen size (stub)"""
    return Size(256, 224)


class GState:
    """Context manager for graphics state (stub)"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def translate(x, y):
    """Translate coordinate system (stub)"""
    pass


def scale(sx, sy=None):
    """Scale coordinate system (stub)"""
    pass


def background(r, g, b):
    """Fill background (stub)"""
    pass


def fill(r, g, b, a=1.0):
    """Set fill color (stub)"""
    pass


def rect(x, y, w, h):
    """Draw rectangle (stub)"""
    pass


def text(string, font_name='Helvetica', font_size=16, x=0, y=0, alignment=5):
    """Draw text (stub)"""
    pass


def run(scene, orientation=LANDSCAPE, frame_interval=2):
    """Run the game (stub)"""
    pass
