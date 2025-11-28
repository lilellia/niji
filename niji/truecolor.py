from .colors import RGBColor
from .roles import ColorRole


def get_color_ansi_code_component_24bit(color: RGBColor | None, role: ColorRole) -> str:
    if color is None:
        return ""

    return f"{38 + role.value};2;{color.red};{color.green};{color.blue}"
