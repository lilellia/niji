import pytest

from niji.styles import TextStyle, get_style_ansi_code_component


@pytest.mark.parametrize(
    "style, expected_ansi",
    [
        (TextStyle.NONE, "0"),
        (TextStyle.BOLD, "1"),
        (TextStyle.DIM, "2"),
        (TextStyle.REVERSE, "7")
    ]
)
def test_style_ansi_code_single(style: TextStyle, expected_ansi: str):
    assert get_style_ansi_code_component(style) == expected_ansi


@pytest.mark.parametrize(
    "style, expected_ansi",
    [
        (TextStyle.NONE | TextStyle.BOLD, "1"),  # NONE gets "ignored"
        (TextStyle.DIM | TextStyle.REVERSE, "2;7"),
        (TextStyle.ITALIC | TextStyle.UNDERLINE, "3;4"),
        (TextStyle.UNDERLINE | TextStyle.ITALIC, "3;4"),  # order doesn't matter
        (TextStyle.BOLD | TextStyle.ITALIC | TextStyle.STRIKEOUT, "1;3;9")
    ]
)
def test_style_ansi_code_multiple(style: TextStyle, expected_ansi: str):
    assert get_style_ansi_code_component(style) == expected_ansi


def test_style_ansi_code_none():
    assert get_style_ansi_code_component(styles=None) == ""
