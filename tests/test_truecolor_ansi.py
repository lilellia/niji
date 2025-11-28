import pytest

from niji import RGBColor
from niji.roles import ColorRole
from niji.truecolor import get_color_ansi_code_component_24bit


@pytest.mark.parametrize(
    "role, r, g, b, expected_prefix",
    [
        (ColorRole.FOREGROUND, 255, 0, 0, "38;2"),
        (ColorRole.BACKGROUND, 10, 50, 200, "48;2"),
        (ColorRole.FOREGROUND, 128, 128, 128, "38;2"),
        (ColorRole.BACKGROUND, 0, 0, 0, "48;2")
    ]
)
def test_get_color_ansi_24bit(role, r, g, b, expected_prefix):
    code = get_color_ansi_code_component_24bit(RGBColor(r, g, b), role)

    assert code == f"{expected_prefix};{r};{g};{b}"


@pytest.mark.parametrize("role", [ColorRole.FOREGROUND, ColorRole.BACKGROUND])
def test_get_color_ansi_24bit_returns_empty_string_with_null_color(role):
    assert get_color_ansi_code_component_24bit(None, role) == ""
