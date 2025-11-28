import sys
from io import StringIO

import pytest

from niji import ColorMode, get_color_mode


def test_get_color_mode_with_explicit_no_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert get_color_mode() == ColorMode.NONE


def test_get_color_mode_when_colorterm_shows_truecolor(monkeypatch):
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert get_color_mode() == ColorMode.TRUE_COLOR


def test_get_color_mode_when_colorterm_shows_24bit(monkeypatch):
    monkeypatch.setenv("COLORTERM", "24bit")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert get_color_mode() == ColorMode.TRUE_COLOR


def test_get_color_mode_when_truecolor_but_explicit_stream(monkeypatch):
    monkeypatch.setenv("COLORTERM", "truecolor")

    assert get_color_mode(stream=StringIO()) == ColorMode.NONE


def test_get_color_mode_with_explicit_force_color_truecolor(monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setenv("COLORTERM", "truecolor")

    assert get_color_mode(stream=StringIO()) == ColorMode.TRUE_COLOR


def test_get_color_mode_when_not_truecolor_but_xterm256(monkeypatch):
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert get_color_mode() == ColorMode.EXTENDED_256


def test_get_color_mode_when_not_truecolor_but_any_garbage256(monkeypatch):
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "any-garbage-string-with-256color-somewhere-in-it")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert get_color_mode() == ColorMode.EXTENDED_256


def test_get_color_mode_when_256color_but_explicit_stream(monkeypatch):
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    assert get_color_mode(stream=StringIO()) == ColorMode.NONE


def test_get_color_mode_with_explicit_force_color_256(monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    assert get_color_mode(stream=StringIO()) == ColorMode.EXTENDED_256


@pytest.mark.parametrize(
    "option",
    [
        "tty",
        "dumb",
        "linux"
    ]
)
def test_get_color_mode_when_terminal_is_dumb(monkeypatch, option):
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.setenv("TERM", option)

    assert get_color_mode() == ColorMode.NONE


def test_get_color_mode_standard16_fallback(monkeypatch):
    monkeypatch.delenv("COLORTERM", raising=False)
    monkeypatch.delenv("TERM", raising=False)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert get_color_mode() == ColorMode.STANDARD_16


def test_get_color_mode_conflicting_no_color_and_force_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert get_color_mode() == ColorMode.NONE
