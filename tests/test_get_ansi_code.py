import pytest

from niji import ColorMode, RGBColor, TextStyle, get_ansi_code
from niji.colors import COLOR_MAP_256


def test_get_ansi_code_raises_with_auto_mode():
    with pytest.raises(ValueError, match="is not supported"):
        get_ansi_code(fg=RGBColor(255, 0, 0), mode=ColorMode.AUTO)


def test_get_ansi_code_returns_empty_string_with_nocolor_mode():
    assert get_ansi_code(fg=RGBColor(128, 128, 128), mode=ColorMode.NONE) == ""


def test_get_ansi_code_truecolor_fg_only():
    code = get_ansi_code(fg=RGBColor(128, 131, 147), mode=ColorMode.TRUE_COLOR)
    assert code == "38;2;128;131;147"


def test_get_ansi_code_truecolor_all_styles():
    code = get_ansi_code(
        fg=RGBColor(128, 131, 147),
        bg=RGBColor(11, 255, 44),
        styles=TextStyle.ITALIC | TextStyle.DIM,
        mode=ColorMode.TRUE_COLOR
    )
    assert code == "2;3;38;2;128;131;147;48;2;11;255;44"


def test_get_ansi_code_256_fg_only():
    code = get_ansi_code(fg=COLOR_MAP_256[56], mode=ColorMode.EXTENDED_256)
    assert code == "38;5;56"


def test_get_ansi_code_256_all_styles():
    code = get_ansi_code(
        fg=COLOR_MAP_256[37],
        bg=COLOR_MAP_256[112],
        styles=TextStyle.ITALIC | TextStyle.DIM,
        mode=ColorMode.EXTENDED_256
    )
    assert code == "2;3;38;5;37;48;5;112"


def test_get_ansi_code_16_fg_only():
    code = get_ansi_code(fg=COLOR_MAP_256[8], mode=ColorMode.STANDARD_16)
    assert code == "90"


def test_get_ansi_code_16_all_styles():
    code = get_ansi_code(
        fg=COLOR_MAP_256[3],
        bg=COLOR_MAP_256[4],
        styles=TextStyle.ITALIC | TextStyle.DIM,
        mode=ColorMode.STANDARD_16
    )
    assert code == "2;3;33;44"
