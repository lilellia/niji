import sys
from io import StringIO

from niji import RGBColor, TextStyle, aware_colored
from niji.colors import COLOR_MAP_256


def test_aware_colored_auto_truecolor(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    output = aware_colored(
        "some text",
        fg=RGBColor(128, 131, 147),
        bg=RGBColor(11, 255, 44),
        styles=TextStyle.ITALIC | TextStyle.DIM,
    )

    # check that we get the correct truecolor output
    assert output == "\033[2;3;38;2;128;131;147;48;2;11;255;44msome text\033[0m"


def test_aware_colored_auto_256(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    output = aware_colored(
        "some text",
        fg=COLOR_MAP_256[37],
        bg=COLOR_MAP_256[112],
        styles=TextStyle.ITALIC | TextStyle.DIM,
    )

    # check that we get the correct 256-color output
    assert output == "\033[2;3;38;5;37;48;5;112msome text\033[0m"


def test_aware_colored_auto_none(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)

    output = aware_colored(
        "some text",
        fg=RGBColor(128, 131, 147),
        bg=RGBColor(11, 255, 44),
        styles=TextStyle.ITALIC | TextStyle.DIM,
        file=StringIO()
    )

    # check that we correctly suppress the color codes
    assert output == "some text"
