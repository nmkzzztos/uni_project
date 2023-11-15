import enum

class Content(enum.Enum):
    EMPTY = "."
    PLAYER = "P"
    BEAST_LESS = "<"
    BEAST_MORE = ">"
    EQUALS = "="
    FOOD = "*"