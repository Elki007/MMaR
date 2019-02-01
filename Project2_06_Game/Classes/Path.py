import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class Path:
    def __init__(self, path, path_type):
        self.path = path
        self.path_type = path_type
        self.color = qc.Qt.cyan
        self.changed_style(path_type)

    def changed_style(self, text):
        self.path_type = text
        if text == "normal":
            self.color = qc.Qt.cyan
        elif text == "speed up":
            self.color = qc.Qt.darkRed
        elif text == "slow down":
            self.color = qc.Qt.gray
        elif text == "ignore":
            self.color = qc.Qt.green
