
class Polygon:
    #  numpy
    def __init__(self, list_3d, color):
        self.points = []
        self.color = color
        self.cosz = 0
        self.abc_source = []
        self.abc_projected = []
        for each in list_3d:
            self.points.append(each)

    def scale(self, scale_factor):
        scaled_points = []
        for i in range(len(self.points)):
            scaled_points.append(self.points[i].scale(scale_factor))
        return Polygon(scaled_points, self.color)

"""
Test area
"""
