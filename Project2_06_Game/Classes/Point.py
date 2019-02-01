import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class Point:
    """ Not implemented yet - will be control vertices, bounding box points etc. """
    def __init__(self, x, y, color=qc.Qt.cyan, form="circle"):
        self.x = x
        self.y = y
        self.color = color
        self.form = form
