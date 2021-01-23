import curses
from point import Point
from directions import *


def draw_char(scr, x, y, ch, style=curses.A_NORMAL):
    scr.addch(y, x, ch, style)
