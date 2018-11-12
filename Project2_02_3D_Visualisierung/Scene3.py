import sys
import random
import math
import numpy as np
from datetime import datetime, timedelta
from Polygon import Polygon
from Object3D import Object3D
from Point3D import Point3D
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from plyfile import PlyData, PlyElement

class SceneWindow(qw.QLabel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.status_bar = self.parent.statusBar()

        # default value is false - means track mouse only when at least one button is pressed
        self.setMouseTracking(True)
        self.grabKeyboard()

        # -- layers -- #
        # main layer (to collect other layers)
        self.ebene_main = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                        self.parent.height() * self.parent.zoom)  # oder QImage
        # objects
        self.ebene_object = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                        self.parent.height() * self.parent.zoom)  # oder QImage

        # fill transparent
        self.ebene_main.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_object.fill(qg.QColor(0, 0, 0, 0))

        # -- painting tools -- #
        # main painter
        self.main_painter = qg.QPainter(self.ebene_main)
        # objects painter
        self.objects_painter = qg.QPainter(self.ebene_object)

        # objects
        self.cube = Object3D  # declare
        self.bunny = Object3D  # declare
        self.light = Object3D  # declare
        self.fov = 90    # field of view
        self.distance = 5
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.light_vector = Point3D(1,0,0)
        self.direction_forward = True

        self.init_ui()

    def init_ui(self):
        ftl = Point3D(-1, 1, -1)
        ftr = Point3D(1, 1, -1)
        fbl = Point3D(-1, -1, -1)
        fbr = Point3D(1, -1, -1)
        rtl = Point3D(-1, 1, 1)
        rtr = Point3D(1, 1, 1)
        rbl = Point3D(-1, -1, 1)
        rbr = Point3D(1, -1, 1)

        side_front = Polygon([ftl,ftr,fbr,fbl], qc.Qt.blue)
        side_back = Polygon([rtl,rtr,rbr,rbl], qc.Qt.red)
        side_left = Polygon([ftl,rtl,rbl,fbl], qc.Qt.green)
        side_right = Polygon([ftr,rtr,rbr,fbr], qc.Qt.cyan)
        side_top = Polygon([ftl,ftr,rtr,rtl], qc.Qt.black)
        side_down = Polygon([rbl,rbr,fbr,fbl], qc.Qt.lightGray)

        print(f"side_front = Polygon([{ftl},{ftr},{fbl},{fbr}]")

        # connect to ply
        plydata = PlyData.read('bun_zipper_res3.ply')
        # array of all vertexes
        bunny_vert = []
        # array of all surfaces
        bunny_surf = []

        for each in plydata.elements[0].data:
            bunny_vert.append(Point3D(each[0], each[1], -each[2]))

        for each in plydata['face']:
            # each[0][] is an index of a point
            a = each[0][0]
            b = each[0][1]
            c = each[0][2]
            p1 = bunny_vert[a]
            p2 = bunny_vert[b]
            p3 = bunny_vert[c]
            bunny_surf.append(Polygon([p1,p2,p3], qg.QColor(200,200,200))) #qc.Qt.lightGray #qg.QColor(140+random.randint(0,10), 140+random.randint(0,10), 140+random.randint(0,10))))

        #print(plydata.elements[0].data[0])
        #print(bunny_vert[0])
        #print(plydata['face'][0][0][0])

        self.cube = Object3D(self, [side_front, side_back,side_left,side_right,side_top,side_down])
        # self.cube = Object3D(self, [side_left])
        self.bunny = Object3D(self, bunny_surf[:], 'not set', 550)

        self.light = Object3D(self, [Polygon([Point3D(0,0,0), self.light_vector], qg.QColor(255,0,0))], 'not set', 550)

        #self.update()
        self.timer()

    def update_layers(self):

        self.main_painter.drawPixmap(0, 0, self.ebene_object)
        self.setPixmap(self.ebene_main)

    def update(self):
        self.ebene_main.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_object.fill(qg.QColor(0, 0, 0, 0))

        self.draw_test_object()
        self.update_layers()
        #print(self.fov)
        self.status_bar.showMessage(str(self.fov) + '°, distance: ' + str(round(self.distance,2)) + ' rotation(x,y,z):(' +
                                    str(round(self.angleX,2)) + '°,' + str(round(self.angleY,2)) + '°,' + str(round(self.angleZ,2)) + '°)')


        if self.fov == 110:
            self.direction_forward = False
        elif self.fov == 90:
            self.direction_forward = True

        if self.direction_forward:
            self.fov += 1
            self.distance -= 0.1
        else:
            self.fov -= 1
            self.distance += 0.1

        # rotate
        self.angleX += 3
        self.angleY += 1
        self.angleZ += 2

        self.angleX = self.angleX % 360
        self.angleY = self.angleY % 360
        self.angleZ = self.angleZ % 360



        self.timer()

    def draw_test_object(self):
        # self.cube.draw_parallelprojektion(self.objects_painter)
        # self.cube.draw_schraegprojektion(self.objects_painter)
        # self.cube.draw_homogen(self.objects_painter)

        # only wareframe
        # self.cube.draw_perspective(self.objects_painter, self.fov,self.distance, angleX=self.angleX, angleY=self.angleY, angleZ=self.angleZ, wareframe=True)
        # with surfaces
        # self.cube.draw_perspective(self.objects_painter, self.fov, self.distance, angleX=self.angleX, angleY=self.angleY, angleZ=self.angleZ)

        #self.light_vector = self.light_vector.rotateX(self.angleX/10).rotateY(0).rotateZ(0)
        #self.light_vector = self.light_vector.rotateX(self.angleX/10).rotateY(self.angleY/10).rotateZ(self.angleZ/10)
        #self.bunny.draw_perspective(self.objects_painter, 300, 1, angleX=-10, shader=True)
        self.bunny.draw_perspective(self.objects_painter, 300, 1, angleX=-10,shader=True)
        #self.bunny.draw_perspective(self.objects_painter, self.fov, self.distance/6)
        #self.bunny.draw_perspective(self.objects_painter, 250, 1, angleX=self.angleX, angleY=self.angleY, angleZ=self.angleZ)
        #self.light.draw_perspective(self.objects_painter, 100, 1, angleX=-10)

    def timer(self):
        qc.QTimer.singleShot(50, self.update)



