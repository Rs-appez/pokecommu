from enum import Enum


class Color(Enum):
    BLUE = 1
    GREEN = 2
    RED = 3
    BLACK = 4
    YELLOW = 5
    MAGENTA = 6
    CYAN = 7
    WHITE = 8


def get_color(color: Color) -> str:
    match color:
        case Color.BLUE:
            return "\033[94m"
        case Color.GREEN:
            return "\033[92m"
        case Color.RED:
            return "\033[91m"
        case Color.BLACK:
            return "\033[90m"
        case Color.YELLOW:
            return "\033[93m"
        case Color.MAGENTA:
            return "\033[95m"
        case Color.CYAN:
            return "\033[96m"
        case Color.WHITE:
            return "\033[97m"
        case _:
            return "\033[0m"


def get_bool_color(value: bool) -> str:
    return get_color(Color.GREEN) if value else get_color(Color.RED)


def reset_color() -> str:
    return "\033[0m"
