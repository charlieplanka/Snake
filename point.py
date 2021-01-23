from directions import *


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, direction):
        new_point = Point(self.x, self.y)
        if direction == DIRECTION_UP:
            new_point.y -= 1
        elif direction == DIRECTION_DOWN:
            new_point.y += 1
        elif direction == DIRECTION_RIGHT:
            new_point.x += 1
        elif direction == DIRECTION_LEFT:
            new_point.x -= 1
        return new_point

    def __eq__(self, other):
        if not isinstance(other, Point):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y)
