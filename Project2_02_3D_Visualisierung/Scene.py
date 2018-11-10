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

        self.init_ui()

    def init_ui(self):
        # test circle
        side_front = Polygon([(-100, -100, 1), (100, -100, 1), (100, 100, 1), (-100, 100, 1)], qc.Qt.blue)
        side_back = Polygon([(-100, -100, 10), (100, -100, 10), (100, 100, 10), (-100, 100, 10)], qc.Qt.red)
        side_left = Polygon([(-100, -100, 1), (-100, -100, 10), (-100, 100, 10), (-100, 100, 1)], qc.Qt.green)
        side_right = Polygon([(100, -100, 1), (100, -100, 10), (100, 100, 10), (100, 100, 1)], qc.Qt.darkGreen)
        side_top = Polygon([(-100, -100, 1), (-100, -100, 10), (100, -100, 10), (100, -100, 1)], qc.Qt.darkBlue)
        side_down = Polygon([(-100, 100, 1), (-100, 100, 10), (100, 100, 10), (100, 100, 1)], qc.Qt.darkBlue)
        cubeX = self.parent.width() / 2
        cubeY = self.parent.height() / 2

        self.cube = Object3D([side_front, side_back,side_left,side_right,side_top,side_down],cubeX,cubeY)

        self.update()
        self.timer()

    def update_layers(self):
        self.main_painter.drawPixmap(0, 0, self.ebene_object)
        self.setPixmap(self.ebene_main)

    def update(self):
        self.draw_test_object()
        self.update_layers()

    def draw_test_object(self):
        #self.cube.draw_parallelprojektion(self.objects_painter)
        self.cube.draw_schraegprojektion(self.objects_painter)
        #self.cube.draw_homogen(self.objects_painter)


    def timer(self):
        qc.QTimer.singleShot(1000, self.update)



