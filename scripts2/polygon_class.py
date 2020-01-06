
class Polygon:  # may need improvement

    def __init__(self, filter_args):
        self.args = list(filter_args)
        print(self.args)
        self.line_number = len(self.args)
        print(self.line_number)
        self.lines = [Line(self.args[i], self.args[(i+1) % self.line_number]) for i in range(self.line_number)]
        self.inside_pixel_list = []

    def inside(self, pixel):
        intersections = [line.intersect(pixel[0], pixel[1]) for line in self.lines]
        number = intersections.count(True)
        if number % 2 != 0:
            return True
        else:
            return False


class Line:

    def __init__(self, point1, point2):
        self.x1 = float(point1[0])
        self.x2 = float(point2[0])
        self.y1 = float(point1[1])
        self.y2 = float(point2[1])

        self.min_x = 0.0
        self.max_x = 0.0
        self.min_y = 0.0
        self.max_y = 0.0

        self.m = 1.0

        self.calculate_m()
        self.calculate_boundaries()

    def calculate_m(self):
        delta_y = self.y2-self.y1
        delta_x = self.x2-self.x1
        if not delta_x:
            delta_x = 999999.9
        self.m = delta_y/delta_x

    def calculate_boundaries(self):
        self.min_x = min(self.x1, self.x2)
        self.max_x = max(self.x1, self.x2)
        self.min_y = min(self.y1, self.y2)
        self.max_y = max(self.y1, self.y2)

    def intersect(self, x, y):
        x = float(x)
        y = float(y)
        intersection_point_y = self.m*(x-self.x1) + self.y1
        if self.min_x <= x < self.max_x and intersection_point_y >= y:
            return True
        else:
            return False
