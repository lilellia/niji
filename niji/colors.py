import re
from collections.abc import Sequence
from typing import NamedTuple, cast


class RGBColor(NamedTuple):
    red: int
    green: int
    blue: int


# An ordered collection of the indexed colors.
# 256-color mode can use all of them; 16-color mode can only use indices 0-15.
COLOR_MAP_256 = [
    # 0-15 are the original 16 colors
    RGBColor(0, 0, 0),
    RGBColor(128, 0, 0),
    RGBColor(0, 128, 0),
    RGBColor(128, 128, 0),
    RGBColor(0, 0, 128),
    RGBColor(128, 0, 128),
    RGBColor(0, 128, 128),
    RGBColor(192, 192, 192),
    RGBColor(128, 128, 128),
    RGBColor(255, 0, 0),
    RGBColor(0, 255, 0),
    RGBColor(255, 255, 0),
    RGBColor(0, 0, 255),
    RGBColor(255, 0, 255),
    RGBColor(0, 255, 255),
    RGBColor(255, 255, 255),
    # 16-255 are the extended 256 color standard
    RGBColor(0, 0, 0),
    RGBColor(0, 0, 95),
    RGBColor(0, 0, 135),
    RGBColor(0, 0, 175),
    RGBColor(0, 0, 215),
    RGBColor(0, 0, 255),
    RGBColor(0, 95, 0),
    RGBColor(0, 95, 95),
    RGBColor(0, 95, 135),
    RGBColor(0, 95, 175),
    RGBColor(0, 95, 215),
    RGBColor(0, 95, 255),
    RGBColor(0, 135, 0),
    RGBColor(0, 135, 95),
    RGBColor(0, 135, 135),
    RGBColor(0, 135, 175),
    RGBColor(0, 135, 215),
    RGBColor(0, 135, 255),
    RGBColor(0, 175, 0),
    RGBColor(0, 175, 95),
    RGBColor(0, 175, 135),
    RGBColor(0, 175, 175),
    RGBColor(0, 175, 215),
    RGBColor(0, 175, 255),
    RGBColor(0, 215, 0),
    RGBColor(0, 215, 95),
    RGBColor(0, 215, 135),
    RGBColor(0, 215, 175),
    RGBColor(0, 215, 215),
    RGBColor(0, 215, 255),
    RGBColor(0, 255, 0),
    RGBColor(0, 255, 95),
    RGBColor(0, 255, 135),
    RGBColor(0, 255, 175),
    RGBColor(0, 255, 215),
    RGBColor(0, 255, 255),
    RGBColor(95, 0, 0),
    RGBColor(95, 0, 95),
    RGBColor(95, 0, 135),
    RGBColor(95, 0, 175),
    RGBColor(95, 0, 215),
    RGBColor(95, 0, 255),
    RGBColor(95, 95, 0),
    RGBColor(95, 95, 95),
    RGBColor(95, 95, 135),
    RGBColor(95, 95, 175),
    RGBColor(95, 95, 215),
    RGBColor(95, 95, 255),
    RGBColor(95, 135, 0),
    RGBColor(95, 135, 95),
    RGBColor(95, 135, 135),
    RGBColor(95, 135, 175),
    RGBColor(95, 135, 215),
    RGBColor(95, 135, 255),
    RGBColor(95, 175, 0),
    RGBColor(95, 175, 95),
    RGBColor(95, 175, 135),
    RGBColor(95, 175, 175),
    RGBColor(95, 175, 215),
    RGBColor(95, 175, 255),
    RGBColor(95, 215, 0),
    RGBColor(95, 215, 95),
    RGBColor(95, 215, 135),
    RGBColor(95, 215, 175),
    RGBColor(95, 215, 215),
    RGBColor(95, 215, 255),
    RGBColor(95, 255, 0),
    RGBColor(95, 255, 95),
    RGBColor(95, 255, 135),
    RGBColor(95, 255, 175),
    RGBColor(95, 255, 215),
    RGBColor(95, 255, 255),
    RGBColor(135, 0, 0),
    RGBColor(135, 0, 95),
    RGBColor(135, 0, 135),
    RGBColor(135, 0, 175),
    RGBColor(135, 0, 215),
    RGBColor(135, 0, 255),
    RGBColor(135, 95, 0),
    RGBColor(135, 95, 95),
    RGBColor(135, 95, 135),
    RGBColor(135, 95, 175),
    RGBColor(135, 95, 215),
    RGBColor(135, 95, 255),
    RGBColor(135, 135, 0),
    RGBColor(135, 135, 95),
    RGBColor(135, 135, 135),
    RGBColor(135, 135, 175),
    RGBColor(135, 135, 215),
    RGBColor(135, 135, 255),
    RGBColor(135, 175, 0),
    RGBColor(135, 175, 95),
    RGBColor(135, 175, 135),
    RGBColor(135, 175, 175),
    RGBColor(135, 175, 215),
    RGBColor(135, 175, 255),
    RGBColor(135, 215, 0),
    RGBColor(135, 215, 95),
    RGBColor(135, 215, 135),
    RGBColor(135, 215, 175),
    RGBColor(135, 215, 215),
    RGBColor(135, 215, 255),
    RGBColor(135, 255, 0),
    RGBColor(135, 255, 95),
    RGBColor(135, 255, 135),
    RGBColor(135, 255, 175),
    RGBColor(135, 255, 215),
    RGBColor(135, 255, 255),
    RGBColor(175, 0, 0),
    RGBColor(175, 0, 95),
    RGBColor(175, 0, 135),
    RGBColor(175, 0, 175),
    RGBColor(175, 0, 215),
    RGBColor(175, 0, 255),
    RGBColor(175, 95, 0),
    RGBColor(175, 95, 95),
    RGBColor(175, 95, 135),
    RGBColor(175, 95, 175),
    RGBColor(175, 95, 215),
    RGBColor(175, 95, 255),
    RGBColor(175, 135, 0),
    RGBColor(175, 135, 95),
    RGBColor(175, 135, 135),
    RGBColor(175, 135, 175),
    RGBColor(175, 135, 215),
    RGBColor(175, 135, 255),
    RGBColor(175, 175, 0),
    RGBColor(175, 175, 95),
    RGBColor(175, 175, 135),
    RGBColor(175, 175, 175),
    RGBColor(175, 175, 215),
    RGBColor(175, 175, 255),
    RGBColor(175, 215, 0),
    RGBColor(175, 215, 95),
    RGBColor(175, 215, 135),
    RGBColor(175, 215, 175),
    RGBColor(175, 215, 215),
    RGBColor(175, 215, 255),
    RGBColor(175, 255, 0),
    RGBColor(175, 255, 95),
    RGBColor(175, 255, 135),
    RGBColor(175, 255, 175),
    RGBColor(175, 255, 215),
    RGBColor(175, 255, 255),
    RGBColor(215, 0, 0),
    RGBColor(215, 0, 95),
    RGBColor(215, 0, 135),
    RGBColor(215, 0, 175),
    RGBColor(215, 0, 215),
    RGBColor(215, 0, 255),
    RGBColor(215, 95, 0),
    RGBColor(215, 95, 95),
    RGBColor(215, 95, 135),
    RGBColor(215, 95, 175),
    RGBColor(215, 95, 215),
    RGBColor(215, 95, 255),
    RGBColor(215, 135, 0),
    RGBColor(215, 135, 95),
    RGBColor(215, 135, 135),
    RGBColor(215, 135, 175),
    RGBColor(215, 135, 215),
    RGBColor(215, 135, 255),
    RGBColor(215, 175, 0),
    RGBColor(215, 175, 95),
    RGBColor(215, 175, 135),
    RGBColor(215, 175, 175),
    RGBColor(215, 175, 215),
    RGBColor(215, 175, 255),
    RGBColor(215, 215, 0),
    RGBColor(215, 215, 95),
    RGBColor(215, 215, 135),
    RGBColor(215, 215, 175),
    RGBColor(215, 215, 215),
    RGBColor(215, 215, 255),
    RGBColor(215, 255, 0),
    RGBColor(215, 255, 95),
    RGBColor(215, 255, 135),
    RGBColor(215, 255, 175),
    RGBColor(215, 255, 215),
    RGBColor(215, 255, 255),
    RGBColor(255, 0, 0),
    RGBColor(255, 0, 95),
    RGBColor(255, 0, 135),
    RGBColor(255, 0, 175),
    RGBColor(255, 0, 215),
    RGBColor(255, 0, 255),
    RGBColor(255, 95, 0),
    RGBColor(255, 95, 95),
    RGBColor(255, 95, 135),
    RGBColor(255, 95, 175),
    RGBColor(255, 95, 215),
    RGBColor(255, 95, 255),
    RGBColor(255, 135, 0),
    RGBColor(255, 135, 95),
    RGBColor(255, 135, 135),
    RGBColor(255, 135, 175),
    RGBColor(255, 135, 215),
    RGBColor(255, 135, 255),
    RGBColor(255, 175, 0),
    RGBColor(255, 175, 95),
    RGBColor(255, 175, 135),
    RGBColor(255, 175, 175),
    RGBColor(255, 175, 215),
    RGBColor(255, 175, 255),
    RGBColor(255, 215, 0),
    RGBColor(255, 215, 95),
    RGBColor(255, 215, 135),
    RGBColor(255, 215, 175),
    RGBColor(255, 215, 215),
    RGBColor(255, 215, 255),
    RGBColor(255, 255, 0),
    RGBColor(255, 255, 95),
    RGBColor(255, 255, 135),
    RGBColor(255, 255, 175),
    RGBColor(255, 255, 215),
    RGBColor(255, 255, 255),
    RGBColor(8, 8, 8),
    RGBColor(18, 18, 18),
    RGBColor(28, 28, 28),
    RGBColor(38, 38, 38),
    RGBColor(48, 48, 48),
    RGBColor(58, 58, 58),
    RGBColor(68, 68, 68),
    RGBColor(78, 78, 78),
    RGBColor(88, 88, 88),
    RGBColor(98, 98, 98),
    RGBColor(108, 108, 108),
    RGBColor(118, 118, 118),
    RGBColor(128, 128, 128),
    RGBColor(138, 138, 138),
    RGBColor(148, 148, 148),
    RGBColor(158, 158, 158),
    RGBColor(168, 168, 168),
    RGBColor(178, 178, 178),
    RGBColor(188, 188, 188),
    RGBColor(198, 198, 198),
    RGBColor(208, 208, 208),
    RGBColor(218, 218, 218),
    RGBColor(228, 228, 228),
    RGBColor(238, 238, 238),
]


def color_distance(p: RGBColor, q: RGBColor, /) -> float:
    """Calculate the Euclidean distance between two colours."""
    return pow((p.red - q.red) ** 2 + (p.green - q.green) ** 2 + (p.blue - q.blue) ** 2, 0.5)


# valid color definitions:
#                  int -> 16/256 color index
#                  str -> hex color code
# tuple[int, int, int] -> (R, G, B)
#             RGBColor -> (R, G, B)
ColorInput = int | str | tuple[int, int, int] | RGBColor | Sequence[int]


def parse_color_input(color: ColorInput) -> RGBColor:
    match color:
        case RGBColor():
            # simple passthrough
            return color

        case (r, g, b):
            if not all(isinstance(x, int) for x in (r, g, b)):
                raise TypeError(f"RGB color triple must be integers, not {color!r}.")

            # assert to mypy that r, g, b really *are* ints (they are)
            r, g, b = (cast(int, x) for x in (r, g, b))

            if not all(0 <= x <= 255 for x in (r, g, b)):
                raise ValueError(f"RGB color triple should have values 0 <= x <= 255, not {color!r}.")

            return RGBColor(r, g, b)

        case int():
            # interpret as 256-color index
            if not (0 <= color <= 255):
                raise ValueError(f"256-color index should be 0 <= x <= 255, not {color!r}.")
            return COLOR_MAP_256[color]

        case str():
            # interpret as hex color
            if not (m := re.fullmatch(r"#?([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})", color.upper())):
                raise ValueError(f"Invalid string color input: {color!r}. Should be a hex string.")

            r, g, b = [int(x, 16) for x in m.groups()]
            return RGBColor(r, g, b)

        case _:
            raise ValueError(f"Invalid color input: {color!r}.")
