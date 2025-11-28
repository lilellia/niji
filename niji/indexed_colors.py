from .color_modes import ColorMode
from .colors import COLOR_MAP_256, RGBColor, color_distance
from .roles import ColorRole


def find_quantized_index(target: RGBColor, mode: ColorMode) -> int:
    """Return the index of the quantized color closest to the target within the given mode's space."""
    if mode not in (ColorMode.STANDARD_16, ColorMode.EXTENDED_256):
        raise ValueError(f"Quantizing is only valid on 16/256 color modes, not {mode!r}.")

    pool = COLOR_MAP_256 if mode == ColorMode.EXTENDED_256 else COLOR_MAP_256[:16]

    best_index = 0
    best_distance = float("inf")

    for index, color in enumerate(pool):
        if (distance := color_distance(color, target)) < best_distance:
            best_index = index
            best_distance = distance

    return best_index


def get_color_ansi_code_component_indexed(color: RGBColor | None, role: ColorRole, mode: ColorMode) -> str:
    if mode not in (ColorMode.STANDARD_16, ColorMode.EXTENDED_256):
        raise ValueError(f"Color mode should be 16/256 color, not {mode!r}.")

    if color is None:
        return ""

    index = find_quantized_index(color, mode)

    if mode == ColorMode.STANDARD_16:
        # fg: normal colors are 30-37 (index 0-7), bright colors are 90-97 (index 8-15)
        # bg: same as fg but 10 higher
        # Note that role.value will be 0 for FOREGROUND and 10 for BACKGROUND, so (30 if index < 8 else 90) + role.value
        # will always be the correct base.
        code = (30 if index < 8 else 90) + role.value + (index % 8)
        return str(code)

    # extended 256
    # 38;5;N for fg, 48;5;N for bg
    return f"{38 + role.value};5;{index}"
