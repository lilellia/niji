from enum import Flag, auto


class TextStyle(Flag):
    NONE = 0
    BOLD = auto()
    DIM = auto()
    ITALIC = auto()
    UNDERLINE = auto()
    BLINK = auto()
    REVERSE = auto()
    CONCEALED = auto()
    STRIKEOUT = auto()


_SGR_ATTRIBUTE_CODES = {
    TextStyle.NONE: 0,
    TextStyle.BOLD: 1,
    TextStyle.DIM: 2,
    TextStyle.ITALIC: 3,
    TextStyle.UNDERLINE: 4,
    TextStyle.BLINK: 5,
    TextStyle.REVERSE: 7,
    TextStyle.CONCEALED: 8,
    TextStyle.STRIKEOUT: 9
}


def get_style_ansi_code_component(styles: TextStyle | None) -> str:
    """For the given collection of styles (e.g., TextStyle.BOLD | TextStyle.UNDERLINE), generate the corresponding attribute/style ANSI code (e.g., 1;4)."""
    if styles is None:
        return ""

    if styles == TextStyle.NONE:
        return "0"

    codes: set[int] = set()
    for style, code in _SGR_ATTRIBUTE_CODES.items():
        if styles & style:
            codes.add(code)

    return ";".join(sorted(str(c) for c in codes))
