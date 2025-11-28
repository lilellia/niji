import pytest

from niji import RGBColor
from niji.colors import parse_color_input


@pytest.mark.parametrize(
    "rgb_color",
    [
        RGBColor(0, 0, 0),
        RGBColor(127, 102, 113),
        RGBColor(255, 255, 255)
    ]
)
def test_parse_color_input_passthrough(rgb_color: RGBColor):
    # don't just test equality: the value should be passed through unchanged
    assert parse_color_input(rgb_color) is rgb_color


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ((0, 0, 0), RGBColor(0, 0, 0)),
        ((127, 102, 113), RGBColor(127, 102, 113)),
        ((255, 255, 255), RGBColor(255, 255, 255))
    ]
)
def test_parse_color_tuple_input_valid(input_value: tuple[int, int, int], expected_output: RGBColor):
    assert parse_color_input(input_value) == expected_output


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ([0, 0, 0], RGBColor(0, 0, 0)),
        ([127, 102, 113], RGBColor(127, 102, 113)),
        ([255, 255, 255], RGBColor(255, 255, 255))
    ]
)
def test_parse_color_list_input_valid(input_value: list[int], expected_output: RGBColor):
    assert parse_color_input(input_value) == expected_output


@pytest.mark.parametrize(
    "index, expected_rgb",
    [
        # standard 16 colors
        (0, RGBColor(0, 0, 0)),
        (1, RGBColor(128, 0, 0)),
        (6, RGBColor(0, 128, 128)),
        (15, RGBColor(255, 255, 255)),

        # cube colors (16-231),
        (16, RGBColor(0, 0, 0)),
        (17, RGBColor(0, 0, 95)),
        (116, RGBColor(135, 215, 215)),
        (200, RGBColor(255, 0, 215)),
        (231, RGBColor(255, 255, 255)),

        # grey-scale (232-255)
        (232, RGBColor(8, 8, 8)),
        (241, RGBColor(98, 98, 98)),
        (255, RGBColor(238, 238, 238))
    ]
)
def test_parse_color_indexed_valid(index: int, expected_rgb: RGBColor):
    assert parse_color_input(index) == expected_rgb


@pytest.mark.parametrize(
    "index",
    [
        -1,  # out of range
        256,  # out of range
    ]
)
def test_parse_color_indexed_out_of_range(index: int):
    with pytest.raises(ValueError, match="256-color index should be 0 <= x <= 255"):
        parse_color_input(index)


@pytest.mark.parametrize(
    "index",
    [
        0.,  # integer float
        17.4323,  # noninteger float,
    ]
)
def test_parse_color_indexed_floats(index: int):
    with pytest.raises(ValueError, match="Invalid color input"):
        parse_color_input(index)


@pytest.mark.parametrize(
    "input_value",
    [
        (12, 13),  # incorrect length
        tuple(),
        (17, 102, 144, 12)
    ]
)
def test_parse_color_tuple_input_invalid_lengths(input_value):
    with pytest.raises(ValueError, match="Invalid color input."):
        parse_color_input(input_value)


@pytest.mark.parametrize(
    "input_value",
    [
        ("12", "13", "255"),  # str vals instead of int
        (12.0, 13, 17),  # floats
        (12.5, 13.2, 17.122)
    ]
)
def test_parse_color_tuple_input_invalid_types(input_value):
    with pytest.raises(TypeError, match="RGB color triple must be integers"):
        parse_color_input(input_value)


@pytest.mark.parametrize(
    "input_value",
    [
        (-1, -1, -1),
        (0, 17, -12),
        (256, 256, 256)
    ]
)
def test_parse_color_tuple_input_out_of_bounds(input_value):
    with pytest.raises(ValueError, match="RGB color triple should have values 0 <= x <= 255"):
        parse_color_input(input_value)


@pytest.mark.parametrize(
    "hex_input, expected_rgb",
    [
        ("#FF0000", RGBColor(255, 0, 0)),  # valid, includes leading #
        ("00AA00", RGBColor(0, 170, 0)),  # valid, does not include leading #
        ("#123456", RGBColor(18, 52, 86)),  # valid, numbers only
        ("abcdef", RGBColor(171, 205, 239)),  # valid, lowercase
        ("#AbCdeF", RGBColor(171, 205, 239)),  # valid, mixed case
        ("#000000", RGBColor(0, 0, 0)),
        ("#FFFFFF", RGBColor(255, 255, 255)),
    ]
)
def test_parse_color_input_valid_hex_strings(hex_input: str, expected_rgb: RGBColor):
    assert parse_color_input(hex_input) == expected_rgb


@pytest.mark.parametrize(
    "hex_input",
    [
        "red",
        "6chars",  # correct length, but letters outside A-F
        "#12345-",  # invalid character
        "#123456#",  # invalid because only lead # should be stripped
        "#1234 56",  # invalid because contains space
        "#12345Á",  # invalid because Á is not A
        "#12345\N{GREEK CAPITAL LETTER ALPHA}",  # Α (alpha) looks like A (valid), but they are different characters
        "#12345",  # incorrect length after stripping lead #
        "12345",
        "#1234567",  # incorrect length
        "1234567",
        "#A00",  # invalid length (shorthand codes are not supported)
        "A00",
        "127",  # string index for 256 map
        "",  # empty string
        "     ",
    ]
)
def test_parse_color_input_invalid_hex_strings(hex_input: str):
    with pytest.raises(ValueError, match="Should be a hex string."):
        parse_color_input(hex_input)
