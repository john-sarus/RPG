"""Pygame shim for Pythonista sound module.

This module provides stub implementations of Pythonista's sound APIs.
The iOS game has minimal sound usage, so these are primarily no-ops
to prevent ImportError. Console prints can be enabled for debugging.
"""

# Debug flag - set to True to print sound events to console
DEBUG_SOUND = False


def play_effect(name, volume=1.0, pitch=1.0):
    """Play a sound effect (stub implementation).

    Args:
        name: Name or path of the sound effect file
        volume: Volume level (0.0-1.0)
        pitch: Pitch adjustment (0.5-2.0)
    """
    if DEBUG_SOUND:
        print(f"[SOUND] play_effect: {name} (volume={volume}, pitch={pitch})")


def set_volume(volume):
    """Set global sound volume (stub implementation).

    Args:
        volume: Volume level (0.0-1.0)
    """
    if DEBUG_SOUND:
        print(f"[SOUND] set_volume: {volume}")


class Player:
    """Sound player class for music/long audio (stub implementation).

    Pythonista's Player is used for background music and looping sounds.
    This stub version just tracks the file path and provides no-op methods.
    """

    def __init__(self, file_path):
        """Initialize player with audio file path.

        Args:
            file_path: Path to audio file
        """
        self.file_path = file_path
        self._playing = False
        if DEBUG_SOUND:
            print(f"[SOUND] Player created: {file_path}")

    def play(self):
        """Start playing audio (stub)."""
        self._playing = True
        if DEBUG_SOUND:
            print(f"[SOUND] Player.play: {self.file_path}")

    def pause(self):
        """Pause audio playback (stub)."""
        self._playing = False
        if DEBUG_SOUND:
            print(f"[SOUND] Player.pause: {self.file_path}")

    def stop(self):
        """Stop audio playback (stub)."""
        self._playing = False
        if DEBUG_SOUND:
            print(f"[SOUND] Player.stop: {self.file_path}")

    def __del__(self):
        """Cleanup when player is destroyed."""
        if DEBUG_SOUND and hasattr(self, 'file_path'):
            print(f"[SOUND] Player destroyed: {self.file_path}")


# Export public API
__all__ = ['play_effect', 'set_volume', 'Player', 'DEBUG_SOUND']
