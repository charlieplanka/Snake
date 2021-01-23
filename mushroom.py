import random
import curses
from point import Point
from utils import draw_char


class Mushroom:
    def __init__(self, point):
        self.point = point

    def draw(self, scr):
        draw_char(scr, self.point.x, self.point.y, "T", curses.color_pair(1))


def create_random_mushroom_on_screen(scr):
    height, width = scr.getmaxyx()
    x = random.randint(1, width-2)
    y = random.randint(1, height-2)
    return Mushroom(Point(x, y))
