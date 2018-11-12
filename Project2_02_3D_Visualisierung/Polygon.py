
class Polygon:
    def __init__(self, list_3d, color):
        self.points = []
        self.color = color
        self.cosz = 0
        self.abc_source = []
        self.abc_projected = []
        for each in list_3d:
            self.points.append(each)

"""
Test area
"""
