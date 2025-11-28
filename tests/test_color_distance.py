import math

import pytest

from niji.colors import RGBColor, color_distance


@pytest.mark.parametrize(
    "p,",
    [
        RGBColor(0, 0, 0),
        RGBColor(255, 255, 255),
        RGBColor(127, 13, 12)
    ]
)
def test_color_distance_zero(p: RGBColor):
    assert color_distance(p, p) == 0


@pytest.mark.parametrize(
    "p, q, expected",
    [
        # 3-4-5 triples
        (RGBColor(0, 0, 0), RGBColor(0, 3, 4), 5),
        (RGBColor(127, 17, 244), RGBColor(124, 17, 248), 5),
        # 5-12-13 triples
        (RGBColor(68, 91, 14), RGBColor(68, 86, 26), 13)
    ]
)
def test_color_distance_pythagorean(p: RGBColor, q: RGBColor, expected: float):
    # we can use == because these should be exact integers
    assert color_distance(p, q) == expected


@pytest.mark.parametrize(
    "p, q, expected",
    [
        (RGBColor(0, 0, 0), RGBColor(5, 8, 11), math.sqrt(210)),
        (RGBColor(17, 110, 41), RGBColor(12, 118, 52), math.sqrt(210)),
        (RGBColor(255, 255, 255), RGBColor(254, 254, 254), math.sqrt(3)),
        (RGBColor(0, 0, 0), RGBColor(255, 255, 255), math.sqrt(195075))
    ]
)
def test_color_distance_irrational(p: RGBColor, q: RGBColor, expected: float):
    assert color_distance(p, q) == pytest.approx(expected)


@pytest.mark.parametrize(
    "p, q",
    [
        (RGBColor(0, 0, 0), RGBColor(17, 18, 189)),
        (RGBColor(12, 147, 14), RGBColor(17, 212, 255)),
        (RGBColor(255, 255, 255), RGBColor(1, 2, 99))
    ]
)
def test_color_distance_symmetric(p: RGBColor, q: RGBColor):
    assert color_distance(p, q) == color_distance(q, p)
