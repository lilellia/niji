import os
import sys
from enum import Enum, auto
from typing import TextIO


class ColorMode(Enum):
    NONE = 0  # force plain text
    AUTO = auto()  # use the color mode of the active terminal
    TRUE_COLOR = auto()  # 24-bit (full RGB)
    EXTENDED_256 = auto()  # 8-bit (256 colors)
    STANDARD_16 = auto()  # 4-bit (16 colors)


def get_color_mode(stream: TextIO = sys.stdout) -> ColorMode:
    """Determine the color mode for the active terminal."""

    if "NO_COLOR" in os.environ:
        return ColorMode.NONE

    if "FORCE_COLOR" not in os.environ and not stream.isatty():
        return ColorMode.NONE

    env_term = os.environ.get("TERM", "").lower()
    env_colorterm = os.environ.get("COLORTERM", "").lower()

    if env_colorterm in ("truecolor", "24bit"):
        return ColorMode.TRUE_COLOR

    if "256color" in env_term:
        return ColorMode.EXTENDED_256

    if env_term in ("tty", "linux", "dumb"):
        return ColorMode.NONE

    # Technically, this might pass color codes to terminals which don't support them, but we prefer this
    # over silently failing to pass colors when the user expects them.
    return ColorMode.STANDARD_16
