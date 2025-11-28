import pytest

from niji import ColorMode, RGBColor, TextStyle, colored
from niji.colors import COLOR_MAP_256


def test_colored_raises_with_auto_mode():
    with pytest.raises(ValueError, match="is not supported"):
        colored("some string", mode=ColorMode.AUTO)


@pytest.mark.parametrize("mode", (ColorMode.TRUE_COLOR, ColorMode.EXTENDED_256, ColorMode.STANDARD_16))
def test_colored_no_styles(mode):
    output = colored("some text", mode=mode)
    assert output == "some text"


def test_colored_truecolor_fg_only():
    output = colored("some text", fg=RGBColor(128, 131, 147), mode=ColorMode.TRUE_COLOR)
    assert output == "\033[38;2;128;131;147msome text\033[0m"


def test_colored_truecolor_all_styles():
    output = colored(
        "some text",
        fg=RGBColor(128, 131, 147),
        bg=RGBColor(11, 255, 44),
        styles=TextStyle.ITALIC | TextStyle.DIM,
        mode=ColorMode.TRUE_COLOR
    )
    assert output == "\033[2;3;38;2;128;131;147;48;2;11;255;44msome text\033[0m"


def test_colored_256_fg_only():
    output = colored("some text", fg=COLOR_MAP_256[56], mode=ColorMode.EXTENDED_256)
    assert output == "\033[38;5;56msome text\033[0m"


def test_colored_256_all_styles():
    output = colored(
        "some text",
        fg=COLOR_MAP_256[37],
        bg=COLOR_MAP_256[112],
        styles=TextStyle.ITALIC | TextStyle.DIM,
        mode=ColorMode.EXTENDED_256
    )
    assert output == "\033[2;3;38;5;37;48;5;112msome text\033[0m"


def test_get_ansi_code_16_fg_only():
    output = colored("some text", fg=COLOR_MAP_256[8], mode=ColorMode.STANDARD_16)
    assert output == "\033[90msome text\033[0m"


def test_get_ansi_code_16_all_styles():
    output = colored(
        "some text",
        fg=COLOR_MAP_256[3],
        bg=COLOR_MAP_256[4],
        styles=TextStyle.ITALIC | TextStyle.DIM,
        mode=ColorMode.STANDARD_16
    )
    assert output == "\033[2;3;33;44msome text\033[0m"
