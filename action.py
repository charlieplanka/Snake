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

    # two equivalent methods
    @classmethod
    def is_move(cls, action):
        if action in [cls.MOVE_UP, cls.MOVE_DOWN, cls.MOVE_RIGHT, cls.MOVE_LEFT]:
            return True
        return False

    def is_move_my(self):
        if self in [self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT]:
            return True
        return False
