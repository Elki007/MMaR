import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class Path:
    def __init__(self, path_type="normal", thickness=1, form="bezier", cvs=np.array([]).reshape(0, 2), cv_size=10):
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
        self.thickness = thickness
        self.form = form  # not implemented yet -> "bezier", "circle", "line"
        self.bounding_box = self.bounding_box_initialize()
        self.plotted_points = np.ndarray([])  # to locate nearest points, maybe for intersection with player vector?

        self.cvs = cvs  # control points
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

    def bounding_box_refresh(self, move_bbox=False, moved_point=None, position=None):
        if move_bbox:
            self.bounding_box[moved_point] = position
        else:
            if len(self.cvs) > 0:
                min, max = np.amin(self.cvs, 0), np.amax(self.cvs, 0)

                self.bounding_box = np.r_[min[0], min[1],
                                          max[0], min[1],
                                          max[0], max[1],
                                          min[0], max[1]].reshape(4, 2)


class GroupOfPaths:
    def __init__(self, qpath=qg.QPainterPath(), path=Path()):
        self.list_of_paths = [path]
        self.qpath = qpath  # QPainter.Path
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

    def append(self, path):
        self.list_of_paths.append(path)

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

    def save_all_paths(self):
        return [[each.path_type, each.thickness, each.form, each.cvs, each.cv_size] for each in self.list_of_paths]

    def isempty(self):
        if len(self) == 1 and len(self[0].plotted_points) == 0:
            return True
        else:
            return False

