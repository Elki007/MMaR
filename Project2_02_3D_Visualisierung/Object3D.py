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
        angleX = kwargs.get('angleX', 0)
        angleY = kwargs.get('angleY', 0)
        angleZ = kwargs.get('angleZ', 0)

        #print(shader)
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

            abc_source = [] # array of points
            abc_projected =[]
            for i in range(len(self.polygons[p].points)):
                start_t = self.polygons[p].points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                start = start_t.project(self.x, self.y, self.zoom, fov, dist)

                #  collect all point to calculate normal vector for surface
                abc_source.append(start_t)
                abc_projected.append(start)
                if start.z > local_max_z:
                    local_max_z = start.z

                if i != len(self.polygons[p].points) - 1:
                    end_t = self.polygons[p].points[i+1].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    end = end_t.project(self.x, self.y, self.zoom, fov, dist)
                else:
                    end_t = self.polygons[p].points[0].rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                    end = end_t.project(self.x, self.y, self.zoom,fov, dist)

                if wareframe:
                    painter.drawLine(start.x, start.y, end.x, end.y)

                if i == 0:
                    pathlist[p].moveTo(start.x, start.y)
                pathlist[p].lineTo(end.x, end.y)

            if shader:
                delta.append(self.change_color(abc_source,abc_projected, painter, p))
                self.polygons[p].cosz = self.change_color(abc_source,abc_projected, painter, p)
            else:
                delta.append(0)
            #print(self.change_color(abc))

            # function call to change color

            maxpolygon.append([p, local_max_z])

        if not wareframe:
            # sort surfaces asc to solve filling troubles
            maxpolygon.sort(key=operator.itemgetter(1),reverse=True)

            for i in range(len(pathlist)):
                #print(delta[i])
                painter.setBrush(self.polygons[maxpolygon[i][0]].color)
                # check if color is in rgb format
                if type(self.polygons[maxpolygon[i][0]].color) is not qc.Qt.GlobalColor:
                    self.polygons[maxpolygon[i][0]].color.red()
                    r = int(self.polygons[maxpolygon[i][0]].color.red()*self.polygons[maxpolygon[i][0]].cosz)
                    g = int(self.polygons[maxpolygon[i][0]].color.green()*self.polygons[maxpolygon[i][0]].cosz)
                    b = int(self.polygons[maxpolygon[i][0]].color.blue()*self.polygons[maxpolygon[i][0]].cosz)
                    #if i ==40:
                        #print(self.polygons[maxpolygon[i][0]].cosz)
                    #if r > 255:
                        #r,g,b =255,255,255
                        #print(r,g,b)
                    #painter.setPen(self.polygons[maxpolygon[i][0]].color)
                    #painter.setBrush(self.polygons[maxpolygon[i][0]].color)
                    painter.setBrush(qg.QColor(r,g,b))
                    painter.setPen(qg.QColor(r,g,b))

                #if i==40:
                painter.drawPath(pathlist[maxpolygon[i][0]])

    def change_color(self, abc, abc_p, painter, surface_index):
        light = self.parent.light_vector
        #print(self.parent.mouse_x)
        light_source = Point3D(self.parent.mouse_x,self.parent.mouse_y, -100)
        light = light_source.make_vector(abc_p[0])
        light.y = -light.y
        #light = screen_center.make_vector(abc_p[0])
        #light.z = 1
        ab = abc[0].make_vector(abc[1])
        ac = abc[0].make_vector(abc[2])
        normal = ab*ac

        ### test

        cosz = normal.scalar(light) / (normal.abs()*light.abs())
        degr = math.acos(cosz) * 180 / math.pi
        if cosz <0:
            cosz =0

        ###

        ab_p = abc_p[0].make_vector(abc_p[1])
        ac_p = abc_p[0].make_vector(abc_p[2])
        normal_p = ab_p * ac_p

        # move normal to surface
        normal2 = Point3D((abc[0].x + normal.x)*100, (abc[0].y + normal.y)*100, (abc[0].z + normal.z)*100)


        #if surface_index == 40:
            #print(cosz)
            #print(normal2)
            #print(f"normal:{normal},normal_p:{normal_p}, normal2{normal2}")
            #painter.setPen(qg.QPen(qc.Qt.darkRed,4))
            #painter.drawLine(abc_p[0].x, abc_p[0].y, abc_p[0].x+normal2.x, abc_p[0].y+normal2.y)
            #painter.setPen(qg.QPen(qc.Qt.lightGray,1))
            #print(round(cosz,2))
        return round(cosz,2)
        '''
        #print(normal)
        normal2 = Point3D(abc[0].x+normal.x*100,abc[0].y+normal.y*100,abc[0].z+normal.z*100)
        #painter.drawLine(abc[0].x,abc[0].y,(abc[0].x+normal.x*100),abc[0].y+normal.y*100)
        light = Point3D(abc[0].x + self.parent.light_vector.x * 10, abc[0].y + self.parent.light_vector.y * 10,
                        abc[0].z + +self.parent.light_vector.z * 10)

        test_norm = abc[0].make_vector(normal2)
        test_light = abc[0].make_vector(light)

        ###
        cosz = normal.z / normal.abs()
        degr = math.acos(cosz) * 180 / math.pi

        cosz2 = normal2.z / normal2.abs()
        degr2 = math.acos(cosz2) * 180 / math.pi
        if degr2>90:
            degr2=180-degr2
        degr2=round(degr2,1)

        if surface_index != 40:
            painter.setPen(qc.Qt.green)
            painter.drawLine(abc[0].x,abc[0].y,normal2.x,normal2.y)
            painter.setPen(qc.Qt.lightGray)
            #print(self.parent.light_vector.angle(normal2), light.angle(normal2))
            #print(f"dergee:{test_light.angle(test_norm)}")
        #print(f"light:{self.parent.light_vector}, normal:{normal}, normiert:{normal.norm()}")
        return degr2
        #return test_light.angle(test_norm)
        #return light.angle(normal2)
        #return self.parent.light_vector.angle(normal.norm())'''

