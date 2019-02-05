import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

from Path import Path
from Point import Point


"""
#Search -> Mögliche Verbesserung finden für das genannte Problem
"""

class Pane(qw.QLabel):
    """ Paint surface class """
    def __init__(self, parent):
        """ creates Pane """
        super().__init__()
        self.parent = parent  # App - Main window
        self.style = "normal"
        self.color = qc.Qt.red
        self.thickness = 3
        self.grid = False

        self.points = []  # from class Points -> not relevant anymore
        self.click_x_y = np.array([0, 0])  # x,y-coordinates from click (to track movement of pressed mouse)
        self.track_movement = np.array([0, 0])  # difference of original position since beginning (tracks movement)

        # background for black background with lines of grid/crystal if activated
        self.ebene_bg = qg.QPixmap(self.width(), self.height())
        self.ebene_pane = qg.QPixmap(self.width(), self.height())
        self.ebene_cv = qg.QPixmap(self.width(), self.height())
        self.ebene_schlitten = qg.QPixmap(self.width(), self.height())
        self.ebene_total = qg.QPixmap(self.width(), self.height())

        self.fill_all_default()  # cleans all surfaces
        self.set_all_painters()  # create all painters

        self.paths = []
        self.cvs = []
        self.current_path = Path(qg.QPainterPath(), "normal")
        self.track = []

        self.painter_cv.setPen(qg.QPen(self.color, 3, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.current_path.path)

        self.current_cv = np.array([]).reshape(0, 2)
        self.showCV = True

        self.cv_size = 10  # size of cv points

        # variables for drag and drops
        self.move_cv = False  # is a cv moved by mouse?
        self.moved_path = None
        self.moved_cv = None

        # variables for zoom
        self.zoom = 0
        self.zoom_factor = 0.05
        self.track_zoom = 1
        self.original_current_cv = None
        self.point_of_zoom = None

        self.update()

    def resolution_of_surfaces(self):
        self.end_all_painters()  # if not -> endless loop

        self.ebene_bg = qg.QPixmap(self.width(), self.height())
        self.ebene_pane = qg.QPixmap(self.width(), self.height())
        self.ebene_cv = qg.QPixmap(self.width(), self.height())
        self.ebene_schlitten = qg.QPixmap(self.width(), self.height())
        self.ebene_total = qg.QPixmap(self.width(), self.height())

        #print(self.width(), self.h)
        self.fill_all_default()

        self.set_all_painters()

        self.update()
        self.plot()

    def fill_all_default(self):
        self.ebene_bg.fill(qg.QColor(0, 0, 0))
        self.ebene_pane.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_schlitten.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))

    def set_all_painters(self):
        self.painter_cv = qg.QPainter(self.ebene_cv)
        self.painter_cv.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_pane = qg.QPainter(self.ebene_pane)
        self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_schlitten = qg.QPainter(self.ebene_schlitten)
        self.painter_total = qg.QPainter(self.ebene_total)

    def end_all_painters(self):
        self.painter_cv.end()
        self.painter_pane.end()
        self.painter_schlitten.end()
        self.painter_total.end()

    def clear_all_surfaces(self):
        self.end_all_painters()
        self.fill_all_default()
        self.set_all_painters()

        self.paths = []
        self.current_path.path = qg.QPainterPath()

        self.cvs = []
        self.current_cv = np.array([]).reshape(0, 2)
        self.update()

    def undo(self):
        """ removes last step """
        if len(self.current_cv) == 0:
            if len(self.cvs) != 0:
                self.current_cv = self.cvs[-1]
                self.cvs = self.cvs[:-1]
                self.paths = self.paths[:-1]

        if len(self.current_cv) != 0:
            self.current_cv = self.current_cv[:-1]
            if len(self.current_cv) != 0:
                self.draw_path_between_cv(only_current=True)
            self.plot()
            self.update()

    def show_cv(self, value):
        """ value = True or False """
        self.showCV = value
        self.update()

    def update_game(self):
        #self.update()
        #self.plot()
        #self.ebene_total.fill(qg.QColor(0, 0, 0, 0))
        self.painter_total.drawPixmap(0, 0, self.ebene_bg)
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        #self.painter_total.drawPixmap(0, 0, self.ebene_cv)
        self.painter_total.drawPixmap(0, 0, self.ebene_schlitten)
        self.setPixmap(self.ebene_total)


    def update(self):
        """ draws everything (cv optional) """

        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))

        # if CV and lines in between shall be displayed
        if self.showCV:
            path = self.current_path.path
            cv_size = self.cv_size
            #print(path)
            color = qc.Qt.blue
            thickness = 1
            self.painter_cv.setPen(qg.QPen(color, thickness, qc.Qt.SolidLine))

            # draw actual cv path
            self.painter_cv.drawPath(path)

            # draw old cv paths
            for each_path in self.paths:
                self.painter_cv.drawPath(each_path.path)

            # draw old cv points
            for j in range(len(self.cvs)):
                for i in range(self.cvs[j].shape[0]):
                    self.painter_cv.setPen(qg.QPen(color, cv_size, qc.Qt.SolidLine))
                    self.painter_cv.drawPoint(*self.cvs[j][i])

            # draw actual cv points
            for i in range(self.current_cv.shape[0]):
                self.painter_cv.setPen(qg.QPen(color, cv_size, qc.Qt.SolidLine))
                self.painter_cv.drawPoint(*self.current_cv[i])

        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))  # wird woanders wiederholt/überschrieben
        self.painter_total.drawPixmap(0, 0, self.ebene_bg)
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        self.painter_total.drawPixmap(0, 0, self.ebene_cv)
        self.painter_total.drawPixmap(0, 0, self.ebene_schlitten)
        self.setPixmap(self.ebene_total)

    def draw_cv_points(self, color):
        self.painter_cv.setPen(qg.QPen(color, 10, qc.Qt.SolidLine))
        self.painter_cv.drawPoint(self.cvs[j][i][0], self.cvs[j][i][1])

    def plot(self):
        self.painter_pane.end()
        self.ebene_pane.fill(qg.QColor(0, 0, 0, 0))
        self.painter_pane = qg.QPainter(self.ebene_pane)
        self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)

        # bspline -> Bezier
        def bspline(cv, n=100, degree=3):
            """ Calculate n samples on a bspline

                cv :      Array of control vertices
                n  :      Number of samples to return
                degree:   Curve degree
            """
            cv = np.asarray(cv)
            count = len(cv)

            degree = np.clip(degree, 1, count-1)

            # Calculate knot vector
            kv = None
            kv = np.clip(np.arange(count+degree+1)-degree, 0, count-degree)

            # Calculate query range
            u = np.linspace(False, (count-degree), n)

            # Calculate result
            return np.array(si.splev(u, (kv, cv.T, degree))).T

        # older paths
        self.track = []
        n=10
        for i in range(len(self.cvs)):
            p = bspline(self.cvs[i], n=len(self.cvs[i])*n)
            x, y = p.T
            path = qg.QPainterPath()

            path.moveTo(x[0], y[0])
            for j in range(len(x)):
                self.track.append([x[j], y[j]])
                path.lineTo(x[j], y[j])

            self.painter_pane.setPen(qg.QPen(self.paths[i].color, 3, qc.Qt.SolidLine))
            self.painter_pane.drawPath(path)

        # current path, if it is not empty!
        if len(self.current_cv) != 0:
            p = bspline(self.current_cv, n=len(self.current_cv)*n)  # n - amount of interpolated points
            x, y = p.T
            path = qg.QPainterPath()

            path.moveTo(x[0], y[0])
            for j in range(len(x)):
                self.track.append([x[j], y[j]])
                path.lineTo(x[j], y[j])

            self.painter_pane.setPen(qg.QPen(self.current_path.color, 3, qc.Qt.SolidLine))
            self.painter_pane.drawPath(path)

        # self.update()  # wird einzeln aufgerufen

    def draw_path_between_cv(self, only_current=False, only_old=False):
        """ draws all paths betweens cv (optional only current ones) """
        if not only_old:
            self.current_path.path = qg.QPainterPath()
            self.current_path.path.moveTo(*self.current_cv[0])
            for i in range(len(self.current_cv)):
                self.current_path.path.lineTo(*self.current_cv[i])

        if not only_current:
            for i in range(len(self.cvs)):
                self.paths[i].path = qg.QPainterPath()
                self.paths[i].path.moveTo(*self.cvs[i][0])
                for j in range(len(self.cvs[i])):
                    self.paths[i].path.lineTo(*self.cvs[i][j])

    def mousePressEvent(self, event):
        self.click_x_y = np.array([event.pos().x(), event.pos().y()])

        if len(self.cvs) > 0:
            for index_path, each_path in enumerate(self.cvs):
                for index_cv, each_cv in enumerate(each_path):
                    # calculate if the mouse click is on the cv position
                    if (self.click_x_y <= each_cv + self.cv_size).all() and (self.click_x_y >= each_cv - self.cv_size).all():
                        self.move_cv = True
                        self.moved_path = index_path
                        self.moved_cv = index_cv
                        return

        if len(self.current_cv) > 0:
            for index, each_cv in enumerate(self.current_cv):
                if (self.click_x_y <= each_cv + self.cv_size).all() and (self.click_x_y >= each_cv - self.cv_size).all():
                    self.move_cv = True
                    self.moved_path = -1
                    self.moved_cv = index
                    return
        #print(self.click_x_y)

        if event.buttons() == qc.Qt.LeftButton:

            if len(self.current_cv) == 0:
                self.current_path.path.moveTo(*self.click_x_y)
            self.current_path.path.lineTo(*self.click_x_y)
            self.current_cv = np.r_[self.current_cv, [self.click_x_y]]

        self.plot()
        self.update()

    def mouseReleaseEvent(self, event):
        #  -> Wenn beide Buttons gedrückt sind und der linke als erstes freigegeben wird:
        # if event.buttons() & qc.Qt.RightButton:
        # TODO: What is the exact difference between event.button() and event.buttons()?
        if event.button() == qc.Qt.LeftButton:
            self.move_cv = False
            self.moved_path = None
            self.moved_cv = None

    def mouseMoveEvent(self, event):
        """
        events of moving mouse while button is clicked
        left button: change current cv (dynamic view of line)
        right button: move everything, tracked by self.track_movement
        """

        tmp_x_y = np.array([event.pos().x(), event.pos().y()])

        if self.move_cv:
            if event.buttons() == qc.Qt.LeftButton:
                if self.moved_path is not None and self.moved_path >= 0:
                    self.cvs[self.moved_path][self.moved_cv] = tmp_x_y
                    self.draw_path_between_cv(only_old=True)
                elif self.moved_path is not None and self.moved_path == -1:
                    self.current_cv[self.moved_cv] = tmp_x_y
                    self.draw_path_between_cv(only_current=True)

            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                if len(self.current_cv) > 0:
                    self.move_current_cv(tmp_x_y)

                self.track_movement += tmp_x_y - self.click_x_y
                self.move_everything(tmp_x_y)

                self.click_x_y = tmp_x_y
                self.draw_path_between_cv()

        else:
            # change current cv if there is one with holding left mouse button
            if event.buttons() == qc.Qt.LeftButton and len(self.current_cv) > 0:
                self.move_current_cv(tmp_x_y)

            # change position of everything with right mouse button
            elif event.buttons() == qc.Qt.RightButton:
                self.track_movement += tmp_x_y - self.click_x_y
                self.move_everything(tmp_x_y)

                self.click_x_y = tmp_x_y
                self.draw_path_between_cv() if len(self.current_cv) > 0 else self.draw_path_between_cv(only_old=True)

            # change both if both buttons are pressed (if there is a current cv)
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                if len(self.current_cv) == 0:
                    self.current_path.path.moveTo(*self.click_x_y)
                self.current_path.path.lineTo(*self.click_x_y)
                self.current_cv = np.r_[self.current_cv, [self.click_x_y]]

                self.move_cv = True

                self.track_movement += tmp_x_y - self.click_x_y
                self.move_everything(tmp_x_y)

                self.click_x_y = tmp_x_y
                self.draw_path_between_cv()

        self.plot()
        self.update()

    def wheelEvent(self, event):
        self.point_of_zoom = np.array([event.pos().x(), event.pos().y()])
        self.zoom += event.angleDelta().y()//120

        if event.angleDelta().y() > 0:
            for i in range(len(self.current_cv)):
                tmp_vector = self.current_cv[i] - self.point_of_zoom
                self.current_cv[i] = self.point_of_zoom + tmp_vector * (1 + self.zoom_factor)
            for i in range(len(self.cvs)):
                for j in range(len(self.cvs[i])):
                    tmp_vector = self.cvs[i][j] - self.point_of_zoom
                    self.cvs[i][j] = self.point_of_zoom + tmp_vector * (1 + self.zoom_factor)
        else:
            for i in range(len(self.current_cv)):
                tmp_vector = self.current_cv[i] - self.point_of_zoom
                self.current_cv[i] = self.point_of_zoom + tmp_vector * (1 - self.zoom_factor)
            for i in range(len(self.cvs)):
                for j in range(len(self.cvs[i])):
                    tmp_vector = self.cvs[i][j] - self.point_of_zoom
                    self.cvs[i][j] = self.point_of_zoom + tmp_vector * (1 - self.zoom_factor)

        if len(self.current_cv) > 0:
            self.draw_path_between_cv(only_current=True)
        if len(self.cvs) > 0:
            self.draw_path_between_cv(only_old=True)

        self.plot()
        self.update()

    def move_current_cv(self, tmp_x_y):
        self.current_cv[-1] = tmp_x_y  # change last cv of current cv_path
        self.draw_path_between_cv(only_current=True)

    def move_everything(self, tmp_x_y):
        if len(self.current_cv) > 0:
            self.current_cv += tmp_x_y - self.click_x_y  # change position of current cv_path

        #Search: Statt über alles zu iterieren, muss mit numpy doch auch alles auf einmal gehen?
        if len(self.cvs) != 0:
            for i in range(len(self.cvs)):
                self.cvs[i] += tmp_x_y - self.click_x_y  # if it exist, change pos of prior cv_paths

    def mouseDoubleClickEvent(self, event):
        """ delete through double click """
        if len(self.cvs) > 0:
            for index_path, each_path in enumerate(self.cvs):
                for index_cv, each_cv in enumerate(each_path):
                    # calculate if the mouse click is on the cv position
                    if (self.click_x_y <= each_cv + self.cv_size).all() and (self.click_x_y >= each_cv - self.cv_size).all():
                        self.cvs[index_path] = np.delete(self.cvs[index_path], index_cv, 0)

        if len(self.current_cv) > 0:
            for index, each_cv in enumerate(self.current_cv):
                if (self.click_x_y <= each_cv + self.cv_size).all() and (self.click_x_y >= each_cv - self.cv_size).all():
                    self.current_cv = np.delete(self.current_cv, index, 0)

        for index, each_path in enumerate(self.cvs):
            if len(each_path) == 0:
                self.cvs.pop(index)

        if len(self.current_cv) > 0:
            self.draw_path_between_cv(only_current=True)
        if len(self.cvs) > 0:
            self.draw_path_between_cv(only_old=True)

        self.plot()
        self.update()


