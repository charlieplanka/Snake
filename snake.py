import curses
from utils import draw_char


class Snake:
    def __init__(self, points: list):
        self.points = points

    def move(self, direction):
        for i in range(len(self.points)-1, 0, -1):
            prev_point = self.points[i-1]
            self.points[i] = prev_point

        head_point = self.points[0]
        self.points[0] = head_point.move(direction)

    def draw(self, scr):
        for point in self.points:
            draw_char(scr, point.x, point.y, "*", curses.color_pair(2))

    def check_border_collision(self, width, height):
        head = self.points[0]
        if head.x in (0, width-1) or \
           head.y in (0, height-1):
            return True

        return False
