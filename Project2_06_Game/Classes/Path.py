import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class GroupOfPaths:
    def __init__(self, path=qg.QPainterPath(), path_type="normal", cv_size=10):
        self.list_of_paths = [Path(path, path_type, cv_size)]

    def __len__(self):
        """ Length of GroupOfPaths is amount of Path Elements """
        return len(self.list_of_paths)

    def __getitem__(self, item):
        """ defines []-Operator """
        return self.list_of_paths[item]

    def __setitem__(self, key, value):
        self.list_of_paths[key] = value

    def pop(self, index_path=-1):
        return self.list_of_paths.pop(index_path)

    def append(self, other):
        self.list_of_paths.append(other)

    def delete(self, index_path, index_cv):
        """ deletes an cv - if last cv, delete path """
        # delete path, if it's empty and not the last one
        if (len(self)) > 1 and len(self[index_path]) == 0:
            self.pop(index_path)
        # only delete points if there are some
        if (len(self) + len(self[index_path])) > 1:
            self[index_path].cvs = np.delete(self[index_path].cvs, index_cv, 0)
        # only delete paths, if there is a previous one
        if len(self[index_path]) == 0 and not len(self) == 1:
            self.pop(index_path)


class Path:
    def __init__(self, path=qg.QPainterPath(), path_type="normal", cv_size=10):
        #TODO: Einzelne x- und y-Koordinaten
        #TODO: Anstieg an beliebigen Punkt ausgeben
        # 2 Punkte übergeben -> gibt es Schnittpunkt mit einem Path?
        # -> gibt zurück:
        # - Schnittpunkt der Kollision
        # - Anstieg am Schnittpunkt
        #
        self.active = False  # is it a chosen path?
        self.path = path  # QPainter.Path
        self.path_type = path_type  # normal, fast, slow?
        self.color = qc.Qt.cyan
        self.changed_style(path_type)  # what was the previous color
        self.thickness = 1

        self.cvs = np.array([]).reshape(0, 2)  # control points
        self.cv_size = cv_size  # unterschiedliche Punkte, unterschiedliche Größe?

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

    def __getitem__(self, item):
        return self.cvs[item]

    def __setitem__(self, key, value):
        self.cvs[key] = value

    def append(self, new_cv):
        self.cvs = np.r_[self.cvs, [new_cv]]

    def __iadd__(self, value):
        """ add value to self.cvs """
        self.cvs = self.cvs + value
        return self

    def __isub__(self, value):
        """ sub value from self.cvs """
        self.cvs = self.cvs - value
        return self
