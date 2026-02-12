"""
Pygame shim for Pythonista ui module

This module provides stub implementations of Pythonista's ui module.
The ui module provides native iOS UI elements. On desktop these are
currently no-ops since the game uses the scene module for all UI.

All classes and methods are stubs that do nothing but prevent ImportError.
"""

__all__ = [
    'View',
    'Label',
    'Button',
    'TableView',
    'ListDataSource',
    'load_view',
    'in_background',
    'get_screen_size',
]

# Debug flag - set to True to print when UI methods are called
DEBUG_UI = False


class View:
    """
    Stub for Pythonista's ui.View class.

    In Pythonista, View is the base class for all UI elements.
    On desktop this is a no-op since the game doesn't use native UI.
    """

    def __init__(self, frame=None, bg_color=None, **kwargs):
        """Initialize View stub"""
        self._frame = frame or (0, 0, 100, 100)
        self._background_color = bg_color or (1, 1, 1, 1)
        self._subviews = []
        self._superview = None
        if DEBUG_UI:
            print(f"[UI] View created: frame={self._frame}")

    @property
    def frame(self):
        """Get view frame (x, y, width, height)"""
        return self._frame

    @frame.setter
    def frame(self, value):
        """Set view frame"""
        self._frame = value
        if DEBUG_UI:
            print(f"[UI] View.frame set to {value}")

    @property
    def background_color(self):
        """Get background color"""
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        """Set background color"""
        self._background_color = value
        if DEBUG_UI:
            print(f"[UI] View.background_color set to {value}")

    def add_subview(self, view):
        """Add a subview"""
        self._subviews.append(view)
        view._superview = self
        if DEBUG_UI:
            print(f"[UI] View.add_subview: {type(view).__name__}")

    def remove_from_superview(self):
        """Remove this view from its superview"""
        if self._superview:
            self._superview._subviews.remove(self)
            self._superview = None
        if DEBUG_UI:
            print("[UI] View.remove_from_superview")

    def present(self, style='fullscreen', **kwargs):
        """Present the view (iOS-specific - no-op on desktop)"""
        if DEBUG_UI:
            print(f"[UI] View.present: style={style}")

    def close(self):
        """Close the view (iOS-specific - no-op on desktop)"""
        if DEBUG_UI:
            print("[UI] View.close")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if DEBUG_UI:
            print("[UI] View context manager exited")
        return False


class Label(View):
    """
    Stub for Pythonista's ui.Label class.

    In Pythonista, Label displays text.
    On desktop this is a no-op.
    """

    def __init__(self, text='', frame=None, **kwargs):
        """Initialize Label stub"""
        super().__init__(frame=frame, **kwargs)
        self._text = text
        self._font = kwargs.get('font', ('Helvetica', 16))
        self._text_color = kwargs.get('text_color', (0, 0, 0, 1))
        self._alignment = kwargs.get('alignment', 1)  # 1=left, 2=center, 3=right
        if DEBUG_UI:
            print(f"[UI] Label created: text='{text}'")

    @property
    def text(self):
        """Get label text"""
        return self._text

    @text.setter
    def text(self, value):
        """Set label text"""
        self._text = value
        if DEBUG_UI:
            print(f"[UI] Label.text set to '{value}'")

    @property
    def font(self):
        """Get font (name, size) tuple"""
        return self._font

    @font.setter
    def font(self, value):
        """Set font"""
        self._font = value
        if DEBUG_UI:
            print(f"[UI] Label.font set to {value}")

    @property
    def text_color(self):
        """Get text color"""
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        """Set text color"""
        self._text_color = value
        if DEBUG_UI:
            print(f"[UI] Label.text_color set to {value}")

    @property
    def alignment(self):
        """Get text alignment"""
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        """Set text alignment"""
        self._alignment = value
        if DEBUG_UI:
            print(f"[UI] Label.alignment set to {value}")


class Button(View):
    """
    Stub for Pythonista's ui.Button class.

    In Pythonista, Button is a clickable UI element.
    On desktop this is a no-op.
    """

    def __init__(self, title='', frame=None, action=None, **kwargs):
        """Initialize Button stub"""
        super().__init__(frame=frame, **kwargs)
        self._title = title
        self._action = action
        if DEBUG_UI:
            print(f"[UI] Button created: title='{title}'")

    @property
    def title(self):
        """Get button title"""
        return self._title

    @title.setter
    def title(self, value):
        """Set button title"""
        self._title = value
        if DEBUG_UI:
            print(f"[UI] Button.title set to '{value}'")

    @property
    def action(self):
        """Get button action callback"""
        return self._action

    @action.setter
    def action(self, value):
        """Set button action callback"""
        self._action = value
        if DEBUG_UI:
            print(f"[UI] Button.action set")


class TableView(View):
    """
    Stub for Pythonista's ui.TableView class.

    In Pythonista, TableView displays a scrollable list.
    On desktop this is a no-op.
    """

    def __init__(self, frame=None, **kwargs):
        """Initialize TableView stub"""
        super().__init__(frame=frame, **kwargs)
        self._data_source = None
        self._delegate = None
        if DEBUG_UI:
            print("[UI] TableView created")

    @property
    def data_source(self):
        """Get data source"""
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        """Set data source"""
        self._data_source = value
        if DEBUG_UI:
            print(f"[UI] TableView.data_source set")

    @property
    def delegate(self):
        """Get delegate"""
        return self._delegate

    @delegate.setter
    def delegate(self, value):
        """Set delegate"""
        self._delegate = value
        if DEBUG_UI:
            print(f"[UI] TableView.delegate set")

    def reload(self):
        """Reload table data"""
        if DEBUG_UI:
            print("[UI] TableView.reload")


class ListDataSource:
    """
    Stub for Pythonista's ui.ListDataSource class.

    In Pythonista, ListDataSource provides data for TableView.
    On desktop this is a no-op.
    """

    def __init__(self, items=None):
        """Initialize ListDataSource stub"""
        self._items = items or []
        if DEBUG_UI:
            print(f"[UI] ListDataSource created: {len(self._items)} items")

    @property
    def items(self):
        """Get items list"""
        return self._items

    @items.setter
    def items(self, value):
        """Set items list"""
        self._items = value or []
        if DEBUG_UI:
            print(f"[UI] ListDataSource.items set: {len(self._items)} items")


def load_view(name):
    """
    Stub for Pythonista's ui.load_view() function.

    In Pythonista, load_view loads a view from a .pyui file.
    On desktop this returns an empty View stub.

    Args:
        name: Name of the view file to load (ignored)

    Returns:
        View: Empty View stub
    """
    if DEBUG_UI:
        print(f"[UI] load_view('{name}')")
    return View()


def in_background(func):
    """
    Stub for Pythonista's ui.in_background decorator.

    In Pythonista, in_background runs a function on a background thread.
    On desktop this just calls the function immediately (no threading).

    Args:
        func: Function to decorate

    Returns:
        Decorated function that calls func immediately
    """
    def wrapper(*args, **kwargs):
        if DEBUG_UI:
            print(f"[UI] in_background: calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def get_screen_size():
    """
    Get the screen size.

    In Pythonista, this returns the iOS device screen size.
    On desktop, return the window size (1024x896 to match our desktop window).

    Returns:
        tuple: (width, height) in pixels
    """
    if DEBUG_UI:
        print("[UI] get_screen_size() -> (1024, 896)")
    return (1024, 896)
