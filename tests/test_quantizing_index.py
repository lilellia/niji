import pytest

from niji import ColorMode, RGBColor
from niji.colors import COLOR_MAP_256
from niji.indexed_colors import find_quantized_index

UNIQUE_COLOR_MAP_INDICES = set(range(256)) - {16, 21, 46, 51, 196, 201, 226, 231, 244}


# These are all of the unique indices, which should map back to themselves
@pytest.mark.parametrize("index", UNIQUE_COLOR_MAP_INDICES)
def test_finding_quantized_index_for_already_quantized_colors_256_unique(index):
    color = COLOR_MAP_256[index]
    assert find_quantized_index(color, ColorMode.EXTENDED_256) == index


# There are nine pairs of duplicates which should all point to their lower occurrence.
@pytest.mark.parametrize(
    "index, expected",
    [
        (16, 0),
        (21, 12),
        (46, 10),
        (51, 14),
        (196, 9),
        (201, 13),
        (226, 11),
        (231, 15),
        (244, 8)
    ]
)
def test_finding_quantized_index_for_already_quantized_colors_256_duplicate(index, expected):
    color = COLOR_MAP_256[index]
    assert find_quantized_index(color, ColorMode.EXTENDED_256) == expected


@pytest.mark.parametrize("index", range(16))
def test_finding_quantized_index_for_already_quantized_colors_16(index):
    color = COLOR_MAP_256[index]
    assert find_quantized_index(color, ColorMode.EXTENDED_256) == index


@pytest.mark.parametrize(
    "truecolor, quantized_index",
    [
        # on-axis
        (RGBColor(0, 0, 100), 17),  # 17 -> (0, 0, 95)
        (RGBColor(0, 100, 0), 22),  # 22 -> (0, 95, 0)
        (RGBColor(100, 0, 0), 52),  # 52 -> (95, 0, 0)

        # near-axis
        (RGBColor(5, 2, 255), 12),  # 12 -> (0, 0, 255)
        (RGBColor(2, 255, 5), 10),  # 10 -> (0, 255, 0)
        (RGBColor(255, 5, 2), 9),  # 9 -> (255, 0, 0)

        # edges
        (RGBColor(96, 94, 2), 58),  # 58 -> (95, 95, 0)
        (RGBColor(93, 5, 97), 53),  # 53 -> (95, 0, 95)
        (RGBColor(8, 91, 91), 23),  # 23 -> (0, 95, 95)

        # a few random cases
        (RGBColor(129, 11, 176), 91),  # 91 -> (135, 0, 175)
        (RGBColor(59, 121, 76), 65),  # 65 -> (95, 135, 95)
        (RGBColor(199, 195, 142), 180),  # 180 -> (215, 175, 135)
    ]
)
def test_finding_quantized_index_for_nonquantized_color_256(truecolor, quantized_index):
    assert find_quantized_index(truecolor, ColorMode.EXTENDED_256) == quantized_index


@pytest.mark.parametrize(
    "truecolor, quantized_index",
    [
        # halfway between (215, 215, 95) and (215, 215, 135)
        (RGBColor(215, 215, 115), 185),

        # halfway between (175, 255, 215) and (175, 255, 255)
        (RGBColor(175, 255, 235), 158),
    ]
)
def test_finding_quantized_index_for_nonquantized_color_256_tiebreak(truecolor, quantized_index):
    assert find_quantized_index(truecolor, ColorMode.EXTENDED_256) == quantized_index


@pytest.mark.parametrize(
    "truecolor, quantized_index",
    [
        # both are adjacent to the border between red and bright red
        (RGBColor(191, 0, 0), 1),  # 1 -> (128, 0, 0)
        (RGBColor(192, 0, 0), 9),  # 9 -> (255, 0, 0)

        # near pure high values
        (RGBColor(5, 2, 255), 12),  # 12 -> (0, 0, 255)
        (RGBColor(2, 255, 5), 10),  # 10 -> (0, 255, 0)
        (RGBColor(255, 5, 2), 9),  # 9 -> (255, 0, 0)

        # other random values
        # these actually resolve to these colors in 256 color space
        # which does mean they're all actually quite close to the 16 color as well
        (RGBColor(134, 127, 23), 3),
        (RGBColor(7, 131, 114), 6),
        (RGBColor(129, 41, 113), 5)
    ]
)
def test_finding_quantized_index_for_nonquantized_color_16(truecolor, quantized_index):
    assert find_quantized_index(truecolor, ColorMode.STANDARD_16) == quantized_index


@pytest.mark.parametrize(
    "truecolor, quantized_index",
    [
        # halfway between 0 -> (0, 0, 0) and 8 -> (128, 128, 128)
        (RGBColor(64, 64, 64), 0),
    ]
)
def test_finding_quantized_index_for_nonquantized_color_16_tiebreak(truecolor, quantized_index):
    assert find_quantized_index(truecolor, ColorMode.STANDARD_16) == quantized_index


@pytest.mark.parametrize("mode", [ColorMode.AUTO, ColorMode.TRUE_COLOR, ColorMode.NONE])
def test_find_quantized_index_raises_when_not_indexed_mode(mode):
    with pytest.raises(ValueError, match="Quantizing is only valid on 16/256 color modes"):
        find_quantized_index(RGBColor(0, 0, 0), mode)
