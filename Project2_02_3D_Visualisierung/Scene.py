import sys
import random
import math
import numpy as np
from datetime import datetime, timedelta
from Polygon import Polygon
from Object3D import Object3D
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

class SceneWindow(qw.QLabel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

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
        self.fov = 1    # field of view
        self.distance = 4
        self.direction_forward = True
        self.init_ui()

    def init_ui(self):
        # center of a cube
        cubeX = self.parent.width() / 2
        cubeY = self.parent.height() / 2
        cubeZ = 300  # distance from screen*

        width = 200
        height = 200
        depth = 200

        # front/rear top/bottom left/right
        ftl =(-width/2,+height/2,-depth/2,1)
        ftr =(+width/2,+height/2,-depth/2,1)
        fbl =(-width/2,-height/2,-depth/2,1)
        fbr =(+width/2,-height/2,-depth/2,1)
        rtl =(-width/2,+height/2,depth/2,1)
        rtr =(+width/2,+height/2,depth/2,1)
        rbl =(-width/2,-height/2,depth/2,1)
        rbr =(+width/2,-height/2,depth/2,1)

        side_front = Polygon([ftl,ftr,fbr,fbl], qc.Qt.blue)
        side_back = Polygon([rtl,rtr,rbr,rbl], qc.Qt.red)
        side_left = Polygon([ftl,rtl,rbl,fbl], qc.Qt.green)
        side_right = Polygon([ftr,rtr,rbr,fbr], qc.Qt.darkGreen)
        side_top = Polygon([ftl,ftr,rtr,rtl], qc.Qt.darkBlue)
        side_down = Polygon([rbl,rbr,fbr,fbl], qc.Qt.darkBlue)

        print(f"side_front = Polygon([{ftl},{ftr},{fbl},{fbr}]")
        '''side_front = Polygon([(-100, -100, -100), (100, -100, -100), (100, 100, -100), (-100, 100, -100)], qc.Qt.blue)
        side_back = Polygon([(-100, -100, 100), (100, -100, 100), (100, 100, 100), (-100, 100, 100)], qc.Qt.red)
        side_left = Polygon([(-100, -100, -100), (-100, -100, 100), (-100, 100, 100), (-100, 100, -100)], qc.Qt.green)
        side_right = Polygon([(100, -100, -100), (100, -100, 100), (100, 100, 100), (100, 100, -100)], qc.Qt.darkGreen)
        side_top = Polygon([(-100, -100, -100), (-100, -100, 100), (100, -100, 100), (100, -100, -100)], qc.Qt.darkBlue)
        side_down = Polygon([(-100, 100, -100), (-100, 100, 100), (100, 100, 100), (100, 100, -100)], qc.Qt.darkBlue)'''


        # self.cube = Object3D(self, [side_front, side_back,side_left,side_right,side_top,side_down],cubeX,cubeY,cubeZ)
        self.cube = Object3D(self, [side_left], cubeX, cubeY, cubeZ)

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
        print(self.fov)


        if self.fov == 90:
            self.direction_forward = False
        elif self.fov == 1:
            self.direction_forward = True

        if self.direction_forward:
            self.fov += 1
            #self.distance += 1
        else:
            self.fov -= 1
            #self.distance -= 1

        self.timer()

    def draw_test_object(self):
        # self.cube.draw_parallelprojektion(self.objects_painter)
        # self.cube.draw_schraegprojektion(self.objects_painter)
        # self.cube.draw_homogen(self.objects_painter)
        self.cube.draw_perspective(self.objects_painter, self.fov, self.distance)


    def timer(self):
        qc.QTimer.singleShot(100, self.update)



