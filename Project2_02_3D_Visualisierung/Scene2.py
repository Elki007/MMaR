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
        self.fov = 90    # field of view
        self.distance = 4
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.light_vector = Point3D(0,0,10)
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


        self.cube = Object3D(self, [side_front, side_back,side_left,side_right,side_top,side_down])
        # self.cube = Object3D(self, [side_left])

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
                                    str(self.angleX) + '°,' + str(self.angleY) + '°,' + str(self.angleZ) + '°)')


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
        self.cube.draw_perspective(self.objects_painter, self.fov, self.distance,self.angleX, self.angleY, self.angleZ)


    def timer(self):
        qc.QTimer.singleShot(50, self.update)



