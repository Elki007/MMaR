import sys
import random
import math
import numpy as np
from datetime import datetime, timedelta
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


        # objects
        self.ebene3_object = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                        self.parent.height() * self.parent.zoom)  # oder QImage

        self.ebene3_object.fill(qg.QColor(0, 0, 0, 0))

        self.main_painter = qg.QPainter(self.ebene1_background)

        self.painter3_object = qg.QPainter(self.ebene3_object)

        self.init_ui()

    def init_ui(self):
        self.main_painter.drawPixmap(0, 0, self.ebene3_object)

