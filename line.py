# line.py
from point import Point

class Line:
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point

    def length(self):
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return (dx**2 + dy**2) ** 0.5