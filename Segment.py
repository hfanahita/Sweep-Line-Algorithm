class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.m = self.slope()
        self.b = self.y_intercept()

    def slope(self):
        delta_x = self.end.x - self.start.x
        delta_y = self.end.y - self.start.y
        if delta_x != 0:
            return delta_y / delta_x
        return None

    def y_intercept(self):
        if self.m:
            return self.start.y - (self.m * self.start.x)
        else:
            return None
