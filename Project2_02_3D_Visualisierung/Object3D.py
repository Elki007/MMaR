import math


class Object3D:
    def __init__(self, polygons,x,y):
        self.x = x
        self.y = y
        self.polygons = []
        for each in polygons:
            self.polygons.append(each)

    def draw_parallelprojektion(self, painter):
        for each in self.polygons:
            painter.setPen(each.color)
            for i in range(len(each.points)):
                if i != len(each.points)-1:
                    painter.drawLine(self.x + each.points[i][0] + each.points[i][2], self.y + each.points[i][1] + each.points[i][2],
                                     self.x + each.points[i + 1][0] + each.points[i + 1][2],
                                     self.y + each.points[i + 1][1] + each.points[i + 1][2])

                else:
                    painter.drawLine(self.x + each.points[i][0] + each.points[i][2], self.y + each.points[i][1] + each.points[i][2],
                                     self.x + each.points[0][0] + each.points[0][2],
                                     self.y + each.points[0][1] + each.points[0][2])

    def draw_schraegprojektion(self, painter):
        for each in self.polygons:
            painter.setPen(each.color)
            for i in range(len(each.points)):
                if i != len(each.points)-1:
                    painter.drawLine(self.x + each.points[i][0] + math.sqrt(2)/2*each.points[i][2], self.y + each.points[i][1] + math.sqrt(2)/2*each.points[i][2],
                                     self.x + each.points[i + 1][0] + math.sqrt(2)/2*each.points[i + 1][2],
                                     self.y + each.points[i + 1][1] + math.sqrt(2)/2*each.points[i + 1][2])

                else:
                    painter.drawLine(self.x + each.points[i][0] + math.sqrt(2)/2*each.points[i][2], self.y + each.points[i][1] + math.sqrt(2)/2*each.points[i][2],
                                     self.x + each.points[0][0] + math.sqrt(2)/2*each.points[0][2],
                                     self.y + each.points[0][1] + math.sqrt(2)/2*each.points[0][2])

    def draw_homogen(self, painter):
        for each in self.polygons:
            painter.setPen(each.color)
            for i in range(len(each.points)):
                if i != len(each.points)-1:
                    painter.drawLine(self.x + each.points[i][0]/each.points[i][2], self.y + each.points[i][1] / each.points[i][2],
                                     self.x + each.points[i + 1][0] / each.points[i + 1][2],
                                     self.y + each.points[i + 1][1] / each.points[i + 1][2])

                else:
                    painter.drawLine(self.x + each.points[i][0] / each.points[i][2], self.y + each.points[i][1] / each.points[i][2],
                                     self.x + each.points[0][0] / each.points[0][2],
                                     self.y + each.points[0][1] / each.points[0][2])