import curses
from utils import move_point, draw_char


class Snake:
    def __init__(self, points: list):
        self.points = points

    def move(self, direction):
        for i in range(len(self.points)-1, 0, -1):
            prev_point = self.points[i-1]
            self.points[i] = prev_point

        head_point = self.points[0]
        self.points[0] = move_point(direction, head_point)

    def draw(self, scr):
        for point in self.points:
            draw_char(scr, point.x, point.y, "*", curses.color_pair(2))
