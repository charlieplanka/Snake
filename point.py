class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def equals(self, another_point):
        return (self.x == another_point.x) and (self.y == another_point.y)
