import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class GroupOfPaths:
    def __init__(self, qpath=qg.QPainterPath(), path_type="normal", cv_size=10):
        self.list_of_paths = [Path(path_type, cv_size)]
        self.qpath = qg.QPainterPath()  # QPainter.Path
        self.qpath_bounding_box = qg.QPainterPath()
        self.active_path = None

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

    def activates_path(self, index):
        self.active_path = index

    def draw_reset(self):
        self.qpath = qg.QPainterPath()

    def draw_moveTo(self, np_point_x, np_point_y):
        self.qpath.moveTo(np_point_x, np_point_y)

    def draw_lineTo(self, np_point_x, np_point_y):
        self.qpath.lineTo(np_point_x, np_point_y)

    def draw_reset_bounding_box(self):
        self.qpath_bounding_box = qg.QPainterPath()

    def draw_moveTo_bounding_box(self, np_point_x, np_point_y):
        self.qpath_bounding_box.moveTo(np_point_x, np_point_y)

    def draw_lineTo_bounding_box(self, np_point_x, np_point_y):
        self.qpath_bounding_box.lineTo(np_point_x, np_point_y)


class Path:
    def __init__(self, path_type="normal", cv_size=10):
        #TODO: Einzelne x- und y-Koordinaten
        #TODO: Anstieg an beliebigen Punkt ausgeben
        # 2 Punkte übergeben -> gibt es Schnittpunkt mit einem Path?
        # -> gibt zurück:
        # - Schnittpunkt der Kollision
        # - Anstieg am Schnittpunkt
        #
        self.path_type = path_type  # normal, fast, slow?
        self.color = qc.Qt.cyan
        self.changed_style(path_type)  # what was the previous color
        self.thickness = 1
        self.form = "bezier"  # not implemented yet -> "bezier", "circle", "line"
        self.bounding_box = self.bounding_box_initialize()

        self.plotted_points = np.ndarray([])

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

    def append_cvs(self, new_cv):
        self.cvs = np.r_[self.cvs, [new_cv]]
        self.bounding_box_refresh()

    def __iadd__(self, value):
        """ add value to self.cvs """
        self.cvs = self.cvs + value
        self.bounding_box_refresh()
        return self

    def __isub__(self, value):
        """ sub value from self.cvs """
        self.cvs = self.cvs - value
        self.bounding_box_refresh()
        return self

    @staticmethod
    def bounding_box_initialize():
        return np.zeros((4, 2))

    def bounding_box_refresh(self):
        min, max = np.amin(self.cvs, 0), np.amax(self.cvs, 0)

        self.bounding_box = np.r_[min[0], min[1], max[0], min[1],
                                  max[0], max[1], min[0], max[1]].reshape(4, 2)


