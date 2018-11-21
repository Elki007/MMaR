import math, operator
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from Point3D import Point3D
import numpy as np

class Object3D:
    def __init__(self, parent, polygons, **kwargs):
        self.hw = parent.parent.width()
        self.hh = parent.parent.height()
        self.parent = parent

        self.x = kwargs.get('x', self.hw/2)
        self.y = kwargs.get('y', self.hh/2)
        self.z = kwargs.get('z', 0)
        self.scale = kwargs.get('scale', 1)

        self.camera_pos = Point3D(self.hw/2,  self.hh/2, -100)

        self.polygons = []
        for each in polygons:
            self.polygons.append(each)
        for i in range(len(self.polygons)):
            self.polygons[i] = self.polygons[i].scale(self.scale)

        #test optimized version
        self.pathlist = []
        self.maxpolygon = []
        self.run = True

    def draw_perspective(self, painter, fov, dist, *args, **kwargs):
        dist += self.z
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
                    start = start_t.project(self.x, self.y, fov, dist)
                    #  collect all point to calculate normal vector for surface
                    self.polygons[p].abc_source.append(start_t)  # all rotated points
                    self.polygons[p].abc_projected.append(start)  # all projected points
                    #  find the deepest point in polygon
                    if start.z > local_max_z:
                        local_max_z = start.z

                    #  choose end point for path (if it is the last one - close polygon (connect with start))
                    if i != len(self.polygons[p].points) - 1:
                        end_t = self.polygons[p].points[i+1].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                        end = end_t.project(self.x, self.y, fov, dist)
                    else:
                        end_t = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                        end = end_t.project(self.x, self.y,fov, dist)

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
                    r = int(self.polygons[self.maxpolygon[i][0]].color.red()*(0.2 + 0.8*self.polygons[self.maxpolygon[i][0]].cosz))
                    g = int(self.polygons[self.maxpolygon[i][0]].color.green()*(0.2 + 0.8*self.polygons[self.maxpolygon[i][0]].cosz))
                    b = int(self.polygons[self.maxpolygon[i][0]].color.blue()*(0.2 + 0.8*self.polygons[self.maxpolygon[i][0]].cosz))
                    #print(f"rgb:{r,g,b}")
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
        light_source = Point3D(self.parent.mouse_x,self.parent.mouse_y, 0)
        #light_source = self.camera_pos
        light = light_source.make_vector(abc_p[0])
        light.y = -light.y
        #light = screen_center.make_vector(abc_p[0])
        #light.z = 1
        ab = abc[0].make_vector(abc[1])
        ac = abc[0].make_vector(abc[2])
        normal = ab*ac

        cosz = normal.scalar(light) / (normal.abs()*light.abs())
        # degr = math.acos(cosz) * 180 / math.pi  # calculate degree
        # cosz = abs(cosz)
        if cosz < 0:
            cosz = 0
        return round(cosz, 2)