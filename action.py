from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Action(AutoName):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    NONE = auto()
    CRASH = auto()
    EXIT = auto()
