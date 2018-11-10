import math, operator
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

class Object3D:
    def __init__(self, parent, polygons):
        self.hw = parent.parent.width()
        self.hh = parent.parent.height()
        self.polygons = []
        for each in polygons:
            self.polygons.append(each)

    def draw_parallelprojektion(self, painter):
        for each in self.polygons:
            painter.setPen(each.color)
            for i in range(len(each.points)):
                if i != len(each.points) - 1:
                    painter.drawLine(self.x + each.points[i].x + each.points[i].z,
                                     self.y + each.points[i].y + each.points[i].z,
                                     self.x + each.points[i + 1].x + each.points[i + 1].z,
                                     self.y + each.points[i + 1].y + each.points[i + 1].z)

                else:
                    painter.drawLine(self.x + each.points[i][0] + each.points[i][2],
                                     self.y + each.points[i][1] + each.points[i][2],
                                     self.x + each.points[0][0] + each.points[0][2],
                                     self.y + each.points[0][1] + each.points[0][2])

    def draw_schraegprojektion(self, painter):
        for each in self.polygons:
            painter.setPen(each.color)
            for i in range(len(each.points)):
                if i != len(each.points) - 1:
                    painter.drawLine(self.x + each.points[i][0] + math.sqrt(2) / 2 * each.points[i][2],
                                     self.y + each.points[i][1] + math.sqrt(2) / 2 * each.points[i][2],
                                     self.x + each.points[i + 1][0] + math.sqrt(2) / 2 * each.points[i + 1][2],
                                     self.y + each.points[i + 1][1] + math.sqrt(2) / 2 * each.points[i + 1][2])

                else:
                    painter.drawLine(self.x + each.points[i][0] + math.sqrt(2) / 2 * each.points[i][2],
                                     self.y + each.points[i][1] + math.sqrt(2) / 2 * each.points[i][2],
                                     self.x + each.points[0][0] + math.sqrt(2) / 2 * each.points[0][2],
                                     self.y + each.points[0][1] + math.sqrt(2) / 2 * each.points[0][2])

    def draw_homogen(self, painter):
        for each in self.polygons:
            painter.setPen(each.color)
            for i in range(len(each.points)):
                if i != len(each.points) - 1:
                    painter.drawLine(self.x + each.points[i][0] / each.points[i][2],
                                     self.y + each.points[i][1] / each.points[i][2],
                                     self.x + each.points[i + 1][0] / each.points[i + 1][2],
                                     self.y + each.points[i + 1][1] / each.points[i + 1][2])

                else:
                    painter.drawLine(self.x + each.points[i][0] / each.points[i][2],
                                     self.y + each.points[i][1] / each.points[i][2],
                                     self.x + each.points[0][0] / each.points[0][2],
                                     self.y + each.points[0][1] / each.points[0][2])

    def draw_perspective(self, painter, fov, dist, angleX, angleY, angleZ):
        pathlist = []
        maxpolygon = []
        for p in range(len(self.polygons)):
            painter.setPen(self.polygons[p].color)
            painter.setBrush(self.polygons[p].color)
            pathlist.append(qg.QPainterPath())

            # dummy for minimum value inside a selection
            start = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
            local_max_z = start.z # deepest point

            for i in range(len(self.polygons[p].points)):
                start_t = self.polygons[p].points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                start = start_t.project(self.hw, self.hh, fov, dist)

                if start.z > local_max_z:
                    local_max_z = start.z

                if i != len(self.polygons[p].points) - 1:
                    end_t = self.polygons[p].points[i+1].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    end = end_t.project(self.hw, self.hh, fov, dist)
                else:
                    end_t = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    end = end_t.project(self.hw, self.hh, fov, dist)

                #painter.drawLine(start.x, start.y, end.x, end.y)

                if i == 0:
                    pathlist[p].moveTo(start.x, start.y)
                pathlist[p].lineTo(end.x, end.y)
            maxpolygon.append([p, local_max_z])

        # sort surfaces asc to solve filling troubles
        maxpolygon.sort(key=operator.itemgetter(1),reverse=True)

        for i in range(len(pathlist)):
            painter.setPen(self.polygons[maxpolygon[i][0]].color)
            painter.setBrush(self.polygons[maxpolygon[i][0]].color)
            painter.drawPath(pathlist[maxpolygon[i][0]])
