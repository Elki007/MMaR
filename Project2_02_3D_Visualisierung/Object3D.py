import math, operator
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from Point3D import Point3D

class Object3D:
    def __init__(self, parent, polygons, x='not set', y='not set'):
        self.hw = parent.parent.width()
        self.hh = parent.parent.height()
        self.x = x
        self.y = y
        self.zoom = 7
        if x == 'not set':
            self.x = self.hw/2
        if y == 'not set':
            self.y = self.hh/2

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
        pathlist = []  # remember all paths to draw
        maxpolygon = []  # to arrange polygons
        delta = []  # change color for each polygon
        for p in range(len(self.polygons)):
            painter.setPen(self.polygons[p].color)
            painter.setBrush(self.polygons[p].color)
            pathlist.append(qg.QPainterPath())

            # dummy for minimum value inside a selection
            start = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
            local_max_z = start.z # deepest point

            abc =[] # array of points

            for i in range(len(self.polygons[p].points)):
                start_t = self.polygons[p].points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                start = start_t.project(self.x, self.y, self.zoom,fov, dist)

                #  collect all point to calculate normal vector for surface
                abc.append(start)

                if start.z > local_max_z:
                    local_max_z = start.z

                if i != len(self.polygons[p].points) - 1:
                    end_t = self.polygons[p].points[i+1].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    end = end_t.project(self.x, self.y, self.zoom, fov, dist)
                else:
                    end_t = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    end = end_t.project(self.x, self.y, self.zoom,fov, dist)

                #painter.drawLine(start.x, start.y, end.x, end.y)

                if i == 0:
                    pathlist[p].moveTo(start.x, start.y)
                pathlist[p].lineTo(end.x, end.y)

            delta.append(self.change_color(abc))
            #print(self.change_color(abc))

            # function call to change color

            maxpolygon.append([p, local_max_z])

        # sort surfaces asc to solve filling troubles
        maxpolygon.sort(key=operator.itemgetter(1),reverse=True)

        for i in range(len(pathlist)):
            r = self.polygons[maxpolygon[i][0]].color.red() + delta[i]
            g = self.polygons[maxpolygon[i][0]].color.green() + delta[i]
            b = self.polygons[maxpolygon[i][0]].color.blue() + delta[i]
            #painter.setPen(self.polygons[maxpolygon[i][0]].color)
            #painter.setBrush(self.polygons[maxpolygon[i][0]].color)
            painter.setBrush(qg.QColor(r,g,b))
            painter.drawPath(pathlist[maxpolygon[i][0]])

    def change_color(self,abc):
        ab = abc[0].make_vector(abc[1])
        ac = abc[0].make_vector(abc[2])
        normal = ab*ac
        comp_vector = Point3D(0, 0, 1)
        return comp_vector.angle(normal)

