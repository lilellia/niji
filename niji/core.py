import re
import sys
from typing import TextIO

from .color_modes import ColorMode, get_color_mode
from .colors import ColorInput, parse_color_input
from .indexed_colors import get_color_ansi_code_component_indexed
from .roles import ColorRole
from .styles import TextStyle, get_style_ansi_code_component
from .truecolor import get_color_ansi_code_component_24bit


def get_ansi_code(*, fg: ColorInput | None = None, bg: ColorInput | None = None, styles: TextStyle | None = None,
                  mode: ColorMode) -> str:
    """Get the ANSI code sequence for the given combination of foreground (fg), background (bg) colors, using the given terminal mode."""
    if mode == ColorMode.AUTO:
        raise ValueError(f"get_ansi_code(..., mode={mode!r}) is not supported.")

    if mode == ColorMode.NONE:
        return ""

    blocks: list[str] = []

    if styles is not None:
        blocks.append(get_style_ansi_code_component(styles))

    for color, role in zip((fg, bg), (ColorRole.FOREGROUND, ColorRole.BACKGROUND)):
        if color is None:
            continue

        color = parse_color_input(color)

        if mode == ColorMode.TRUE_COLOR:
            blocks.append(get_color_ansi_code_component_24bit(color, role))
        else:
            blocks.append(get_color_ansi_code_component_indexed(color, role, mode))

    return ";".join(blocks)


def colored(text: str, *, fg: ColorInput | None = None, bg: ColorInput | None = None, styles: TextStyle | None = None,
            mode: ColorMode = ColorMode.TRUE_COLOR) -> str:
    """Return a string with injected ANSI codes to format the given text according to the given fg/bg/styles configuration.
    When mode is STANDARD_16 or EXTENDED_256, the given color is gracefully downgraded to one of the indexed colors.
    """
    if mode == ColorMode.AUTO:
        raise ValueError(f"colored(..., mode={mode!r}) is not supported.")

    if ansi := get_ansi_code(fg=fg, bg=bg, styles=styles, mode=mode):
        ansi_prefix = f"\033[{ansi}m"
        ansi_reset = "\033[0m"
        return f"{ansi_prefix}{text}{ansi_reset}"

    return text


def aware_colored(text: str, *, fg: ColorInput | None = None, bg: ColorInput | None = None,
                  styles: TextStyle | None = None, file: TextIO = sys.stdout) -> str:
    """Same as `colored`, except that it will check the capabilities of the given file to ensure that only supported code patterns are generated."""
    mode = get_color_mode(file)
    return colored(text, fg=fg, bg=bg, styles=styles, mode=mode)


def cprint(text: str, *, fg: ColorInput | None = None, bg: ColorInput | None = None, styles: TextStyle | None = None,
           mode: ColorMode = ColorMode.AUTO, file: TextIO = sys.stdout, end: str = "\n") -> None:
    """Print the given text in the given fg/bg/styles formatting to the given file."""
    if mode == ColorMode.AUTO:
        mode = get_color_mode(file)

    content = colored(text, fg=fg, bg=bg, styles=styles, mode=mode)
    file.write(content + end)


def remove_ansi_codes(s: str, /) -> str:
    """Return a copy of the given string but with all ANSI codes removed."""
    return re.sub(r"\033\[(.*?)m", "", s)
