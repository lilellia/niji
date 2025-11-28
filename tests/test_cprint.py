import sys
from io import StringIO

import pytest

from niji import ColorMode, RGBColor, cprint
from niji.colors import COLOR_MAP_256


def test_cprint_auto_resolves_to_none():
    stream = StringIO()

    cprint("some text", fg=RGBColor(255, 0, 0), mode=ColorMode.AUTO, file=stream)

    assert stream.getvalue() == "some text\n"


def test_cprint_auto_resolves_to_truecolor(capsys, monkeypatch):
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    cprint("some text", fg=RGBColor(255, 0, 0), mode=ColorMode.AUTO, file=sys.stdout)

    output = capsys.readouterr().out
    assert output == "\033[38;2;255;0;0msome text\033[0m\n"


def test_cprint_auto_resolves_to_256color(capsys, monkeypatch):
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    cprint("some text", fg=COLOR_MAP_256[37], mode=ColorMode.AUTO, file=sys.stdout)

    output = capsys.readouterr().out
    assert output == "\033[38;5;37msome text\033[0m\n"


def test_cprint_mode_overrides_auto():
    stream = StringIO()

    cprint("some text", fg=RGBColor(127, 133, 41), mode=ColorMode.TRUE_COLOR, file=stream)

    assert stream.getvalue() == "\033[38;2;127;133;41msome text\033[0m\n"


def test_cprint_none_overrides_auto(capsys, monkeypatch):
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    cprint("some text", fg=RGBColor(127, 133, 31), mode=ColorMode.NONE, file=sys.stdout)

    output = capsys.readouterr().out
    assert output == "some text\n"


@pytest.mark.parametrize(
    "end",
    [
        "\n",  # default
        "",
        "_",
        "\r",
        "\n\n",
        "some random string that doesn't mean anything but is just here to be long and annoying"
    ]
)
def test_cprint_end_parameter(end):
    stream = StringIO()
    cprint("some text", fg=RGBColor(127, 133, 31), file=stream, end=end)
    assert stream.getvalue() == f"some text{end}"
