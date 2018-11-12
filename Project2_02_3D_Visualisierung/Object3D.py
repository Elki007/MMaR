import math, operator
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from Point3D import Point3D
import numpy as np

class Object3D:
    def __init__(self, parent, polygons, x='not set', y='not set'):
        self.hw = parent.parent.width()
        self.hh = parent.parent.height()
        self.parent = parent
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
        #test optimized version
        self.pathlist = []
        self.maxpolygon = []
        self.run = True

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

    def draw_perspective(self, painter, fov, dist, *args, **kwargs):
        shader = kwargs.get('shader', False)
        wareframe = kwargs.get('wareframe', False)
        stable = kwargs.get('stable', False)
        angleX = kwargs.get('angleX', 0)
        angleY = kwargs.get('angleY', 0)
        angleZ = kwargs.get('angleZ', 0)

        if not stable:
            self.pathlist = []  # remember all paths to draw
            self.maxpolygon = []  # to arrange polygons

        for p in range(len(self.polygons)):
            painter.setPen(self.polygons[p].color)
            painter.setBrush(self.polygons[p].color)

            if self.run:
                self.pathlist.append(qg.QPainterPath())

                # dummy for minimum value inside a selection
                start = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                local_max_z = start.z # deepest point

                self.polygons[p].abc_source = [] # array of points
                self.polygons[p].abc_projected =[]
                for i in range(len(self.polygons[p].points)):
                    #  rotate each point
                    start_t = self.polygons[p].points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    #  project each point
                    start = start_t.project(self.x, self.y, self.zoom, fov, dist)
                    #  collect all point to calculate normal vector for surface
                    self.polygons[p].abc_source.append(start_t)  # all rotated points
                    self.polygons[p].abc_projected.append(start)  # all projected points
                    #  find the deepest point in polygon
                    if start.z > local_max_z:
                        local_max_z = start.z

                    #  choose end point for path (if it is the last one - close polygon (connect with start))
                    if i != len(self.polygons[p].points) - 1:
                        end_t = self.polygons[p].points[i+1].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                        end = end_t.project(self.x, self.y, self.zoom, fov, dist)
                    else:
                        end_t = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                        end = end_t.project(self.x, self.y, self.zoom,fov, dist)

                    #  show edges if light is off or wareframe is on
                    if wareframe or not shader:
                        painter.drawLine(start.x, start.y, end.x, end.y)

                    #  special for "path" method - start point has different command
                    if i == 0:
                        self.pathlist[p].moveTo(start.x, start.y)
                    self.pathlist[p].lineTo(end.x, end.y)
                #  store deepest point with polygon index
                self.maxpolygon.append([p, local_max_z])

            # common settings for color changing method
            if shader:
                self.polygons[p].cosz = self.change_color(self.polygons[p].abc_source, self.polygons[p].abc_projected, painter, p)
            else:
                #  if light is off, colors wouldn't be changed (*1)
                self.polygons[p].cosz = 1

        if stable:
            self.run = False

        if not wareframe:
            #  sort surfaces asc to solve filling troubles
            self.maxpolygon.sort(key=operator.itemgetter(1), reverse=True)

            #  draw polygons from the deepest to nearest
            for i in range(len(self.pathlist)):
                #print(i,p,"maxpol:",len(self.maxpolygon)," pl:",len(self.pathlist))
                #print(i,p,self.polygons[self.maxpolygon[i][0]].abc_source)
                painter.setBrush(self.polygons[self.maxpolygon[i][0]].color)
                # check if color is in rgb format
                if type(self.polygons[self.maxpolygon[i][0]].color) is not qc.Qt.GlobalColor:
                    self.polygons[self.maxpolygon[i][0]].color.red()
                    r = int(self.polygons[self.maxpolygon[i][0]].color.red()*self.polygons[self.maxpolygon[i][0]].cosz)
                    g = int(self.polygons[self.maxpolygon[i][0]].color.green()*self.polygons[self.maxpolygon[i][0]].cosz)
                    b = int(self.polygons[self.maxpolygon[i][0]].color.blue()*self.polygons[self.maxpolygon[i][0]].cosz)
                    painter.setBrush(qg.QColor(r,g,b))
                    painter.setPen(qg.QColor(0,0,0))
                    if shader:
                        painter.setPen(qg.QColor(r, g, b))

                #  draw and fill a path
                painter.drawPath(self.pathlist[self.maxpolygon[i][0]])

    def change_color(self, abc, abc_p, painter, surface_index):
        light = self.parent.light_vector
        #print(self.parent.mouse_x)
        #print(abc_p)
        light_source = Point3D(self.parent.mouse_x,self.parent.mouse_y, -100)
        light = light_source.make_vector(abc_p[0])
        light.y = -light.y
        #light = screen_center.make_vector(abc_p[0])
        #light.z = 1
        ab = abc[0].make_vector(abc[1])
        ac = abc[0].make_vector(abc[2])
        normal = ab*ac

        cosz = normal.scalar(light) / (normal.abs()*light.abs())
        degr = math.acos(cosz) * 180 / math.pi  # calculate degree
        if cosz < 0:
            cosz = 0
        return round(cosz, 2)