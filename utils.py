import curses
from point import Point
from directions import *


def move_point(direction, point):
    new_point = Point(point.x, point.y)
    if direction == DIRECTION_UP:
        new_point.y -= 1
    elif direction == DIRECTION_DOWN:
        new_point.y += 1
    elif direction == DIRECTION_RIGHT:
        new_point.x += 1
    elif direction == DIRECTION_LEFT:
        new_point.x -= 1
    return new_point


def draw_char(scr, x, y, ch, style=curses.A_NORMAL):
    scr.addch(y, x, ch, style)
