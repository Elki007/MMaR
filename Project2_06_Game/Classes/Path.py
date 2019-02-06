import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class GroupOfPaths:
    def __init__(self):
        self.list_of_paths = [Path()]

    def __len__(self):
        """ Length of GroupOfPaths is amount of Path Elements """
        return len(self.list_of_paths)


class Path:
    def __init__(self, path=qg.QPainterPath(), path_type="normal", size=10):
        #TODO: Einzelne x- und y-Koordinaten
        #TODO: Anstieg an beliebigen Punkt ausgeben
        # 2 Punkte übergeben -> gibt es Schnittpunkt mit einem Path?
        # -> gibt zurück:
        # - Schnittpunkt der Kollision
        # - Anstieg am Schnittpunkt
        #
        self.path = path
        self.path_type = path_type
        self.color = qc.Qt.cyan
        self.changed_style(path_type)

        self.cvs = np.array([]).reshape(0, 2)  # control points
        self.cv_size = size  # unterschiedliche Punkte, unterschiedliche Größe?

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

    def __str__(self):
        return f"{self.cvs}"

    def __len__(self):
        """ Length of Path is amount of cvs """
        return len(self.cvs)
