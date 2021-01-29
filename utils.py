import curses
from point import Point
from direction import Direction


def move_point(direction, point):
    new_point = Point(point.x, point.y)
    if direction == Direction.UP:
        new_point.y -= 1
    elif direction == Direction.DOWN:
        new_point.y += 1
    elif direction == Direction.RIGHT:
        new_point.x += 1
    elif direction == Direction.LEFT:
        new_point.x -= 1
    return new_point


def draw_char(scr, x, y, ch, style=curses.A_NORMAL):
    scr.addch(y, x, ch, style)
