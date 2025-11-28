import pytest

from niji import ColorMode
from niji.colors import COLOR_MAP_256, RGBColor
from niji.indexed_colors import get_color_ansi_code_component_indexed
from niji.roles import ColorRole

UNIQUE_COLOR_MAP_INDICES = set(range(256)) - {16, 21, 46, 51, 196, 201, 226, 231, 244}


@pytest.mark.parametrize("index", list(range(0, 8)))
def test_get_color_ansi_indexed_16_fg_normal(index):
    color = COLOR_MAP_256[index]

    code = get_color_ansi_code_component_indexed(color, ColorRole.FOREGROUND, ColorMode.STANDARD_16)
    assert code == str(30 + index)


@pytest.mark.parametrize("index", list(range(0, 8)))
def test_get_color_ansi_indexed_16_bg_normal(index):
    color = COLOR_MAP_256[index]

    code = get_color_ansi_code_component_indexed(color, ColorRole.BACKGROUND, ColorMode.STANDARD_16)
    assert code == str(40 + index)


@pytest.mark.parametrize("index", list(range(8, 16)))
def test_get_color_ansi_indexed_16_fg_bright(index):
    color = COLOR_MAP_256[index]

    code = get_color_ansi_code_component_indexed(color, ColorRole.FOREGROUND, ColorMode.STANDARD_16)
    assert code == str(82 + index)


@pytest.mark.parametrize("index", list(range(8, 16)))
def test_get_color_ansi_indexed_16_bg_bright(index):
    color = COLOR_MAP_256[index]

    code = get_color_ansi_code_component_indexed(color, ColorRole.BACKGROUND, ColorMode.STANDARD_16)
    assert code == str(92 + index)


@pytest.mark.parametrize("index", UNIQUE_COLOR_MAP_INDICES)
def test_get_color_ansi_indexed_256_fg(index):
    color = COLOR_MAP_256[index]

    code = get_color_ansi_code_component_indexed(color, ColorRole.FOREGROUND, ColorMode.EXTENDED_256)
    assert code == f"38;5;{index}"


@pytest.mark.parametrize("index", UNIQUE_COLOR_MAP_INDICES)
def test_get_color_ansi_indexed_256_bg(index):
    color = COLOR_MAP_256[index]

    code = get_color_ansi_code_component_indexed(color, ColorRole.BACKGROUND, ColorMode.EXTENDED_256)
    assert code == f"48;5;{index}"


@pytest.mark.parametrize("mode", [ColorMode.AUTO, ColorMode.TRUE_COLOR, ColorMode.NONE])
def test_get_color_ansi_indexed_raises_when_not_indexed_mode(mode):
    with pytest.raises(ValueError, match="Color mode should be 16/256 color"):
        get_color_ansi_code_component_indexed(RGBColor(0, 0, 0), ColorRole.FOREGROUND, mode)
        get_color_ansi_code_component_indexed(RGBColor(0, 0, 0), ColorRole.BACKGROUND, mode)


@pytest.mark.parametrize("mode", [ColorMode.STANDARD_16, ColorMode.EXTENDED_256])
def test_get_color_ansi_indexed_returns_empty_string_when_color_is_none(mode):
    assert get_color_ansi_code_component_indexed(None, ColorRole.FOREGROUND, mode) == ""
    assert get_color_ansi_code_component_indexed(None, ColorRole.BACKGROUND, mode) == ""
