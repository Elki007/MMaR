"""
Pane Version 3
Dies ist der Zeitpunkt kurz bevor die Klassenstruktoränderung umgesetzt wurde:
-  Old class implementation wird durch New class implementation ersetzt und Fehler beseitigt
"""

import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

from Path import GroupOfPaths, Path
from Point import Point


"""
#Search -> Mögliche Verbesserung finden für das genannte Problem
"""

"""
Glossary:
cv -> control vertice -> point that's clicked with mouse
"""

#TODO: Eigene Klasse für Fenster/Painter?
#TODO: Eigene Klasse für Pfade und CVs
# What about future Undo? an own class with all copies?
#TODO: Eigene Klasse Orientierung -> MousePosition, track_movement, track_zoom

# What about two Paneclasses -> One with draw-, one with calculation-functions


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

        # New class implementation
        #self.paths = GroupOfPaths()

        # Old class implementation
        self.paths = []  # -> self.paths.list_of_paths
        self.cvs = []  # -> self.paths.list_of_paths[i].cvs
        self.current_path = Path()  # -> self.paths.list_of_paths[0]

        self.track = []

        self.painter_cv.setPen(qg.QPen(self.color, 3, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.current_path.path)

        # Old class implementation
        self.current_cv = np.array([]).reshape(0, 2)  # self.paths.list_of_paths[-1].cvs
        self.cv_size = 10  # self.paths.list_of_paths[-1].cv_size

        self.showCV = True

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

        # New class implementation
        #self.paths = GroupOfPaths()

        # Old class implementation
        self.paths = []
        self.current_path.path = qg.QPainterPath()
        self.cvs = []
        self.current_cv = np.array([]).reshape(0, 2)

        self.update()

    def undo(self):
        #TODO: outdated
        """ removes last created point """
        if len(self.current_cv) == 0:
            if len(self.cvs) != 0:
                self.current_cv = self.cvs[-1]
                self.cvs = self.cvs[:-1]
                self.paths = self.paths[:-1]

        if len(self.current_cv) != 0:
            self.current_cv = self.current_cv[:-1]
            self.draw_path_between_cv()
            self.plot()
            self.update()

    def show_cv(self, value):
        """ value = True or False -> if cv and lines will be displayed """
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
            # New class implementation
            #path = self.paths.list_of_paths[-1]
            # cv_size = self.paths.list_of_paths[-1].cv_size

            # Old class implementation
            path = self.current_path.path
            cv_size = self.cv_size

            #print(path)
            color = qc.Qt.blue
            thickness = 1
            self.painter_cv.setPen(qg.QPen(color, thickness, qc.Qt.SolidLine))

            # New class implementation
            #for i in range(len(self.paths)):
            #    self.painter_cv.drawPath(self.paths[i])

            # Old class implementation
            # draw actual cv path
            self.painter_cv.drawPath(path)
            # draw old cv paths
            for each_path in self.paths:
                self.painter_cv.drawPath(each_path.path)


            # New class implementation
            #for i in range(len(self.paths)):
            #    for j in range(len(self.paths[i])):
            #        self.painter_cv.setPen(qg.QPen(color, cv_size, qc.Qt.SolidLine))
            #        self.painter_cv.drawPoint(*self.cvs[j][i])

            # Old class implementation
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
        #TODO: outdated - can it still be useful?
        self.painter_cv.setPen(qg.QPen(color, 10, qc.Qt.SolidLine))
        self.painter_cv.drawPoint(self.cvs[j][i][0], self.cvs[j][i][1])

    def bezier_coeffs(self, cv_points, x_y):
        #print("bezier_coeffs")
        if len(cv_points) == 4:
            P0=cv_points[0][x_y]
            P1=cv_points[1][x_y]
            P2=cv_points[2][x_y]
            P3=cv_points[3][x_y]
            A = -P0+3*P1-3*P2+P3
            B = 3*P0-6*P1+3*P2
            C = -3*P0+3*P1
            D = P0
            return [A,B,C,D]
        return False

    def plot(self):
        """ plots bezier curve """
        self.painter_pane.end()
        self.ebene_pane.fill(qg.QColor(0, 0, 0, 0))
        self.painter_pane = qg.QPainter(self.ebene_pane)
        self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)

        def bezier_func(four_points, x_y, n):
            """ function from exercise - cubic bezier curve (called by bezier())"""
            # returns np.array of one cubic bezier curve (of 4 given points)
            # f(t):=(1−t)^3 * K1 + 3*(1−t)^2 * t * K2 + 3*(1−t)*t^2 * K3 + t^3 * K4 mit t->[0,1]
            t = np.linspace(0, 1, n)
            return (1-t)**3 * four_points[0][x_y] + 3*(1-t)**2 * t * four_points[1][x_y] + \
                   3*(1-t)*t**2 * four_points[2][x_y] + t**3 * four_points[3][x_y]

        def bezier(cv_points, n=50):
            """ calculates cubic bezier curves """
            # cv_points -> list of control vertices
            # n -> amount of points in between
            # returns x- and y-coordinates of paths

            x_coords, y_coords = np.array([]), np.array([])

            # splits cv_points in points of four to create a bezier curve
            for i in range(0, len(cv_points), 3):
                if i+4 <= len(cv_points):
                    x_coords = np.append(x_coords, bezier_func(cv_points[i:i+4], 0, n))
                    y_coords = np.append(y_coords, bezier_func(cv_points[i:i+4], 1, n))

            return x_coords, y_coords

        def draw_bezier_path(cv_points, color):
            """ calculates points (with bezier()) to draw lines between them """
            x, y = bezier(cv_points)
            path = qg.QPainterPath()

            if len(x) > 0:
                path.moveTo(x[0], y[0])  # start point
                for j in range(len(x)):
                    self.track.append([x[j], y[j]])
                    path.lineTo(x[j], y[j])

                self.painter_pane.setPen(qg.QPen(color, 3, qc.Qt.SolidLine))
                self.painter_pane.drawPath(path)

        self.track = []

        # New class implementation
        #for i in range(len(self.paths)):
        #    draw_bezier_path(self.paths[i].cvs, self.paths[i].color)

        # Old class implementation
        # current path
        draw_bezier_path(self.current_cv, self.current_path.color)
        # older paths
        for i in range(len(self.cvs)):
            draw_bezier_path(self.cvs[i], self.paths[i].color)

    def draw_path_between_cv(self):
        #TODO: outdated
        """ draws all paths betweens cv (optional only current ones) """
        """ new: tbd - draw just some 'strings' to the main cvs """
        if len(self.current_cv) > 0:
            self.current_path.path = qg.QPainterPath()
            self.current_path.path.moveTo(*self.current_cv[0])
            for i in range(len(self.current_cv)):
                self.current_path.path.lineTo(*self.current_cv[i])

        if len(self.cvs) > 0:
            for i in range(len(self.cvs)):
                self.paths[i].path = qg.QPainterPath()
                self.paths[i].path.moveTo(*self.cvs[i][0])
                for j in range(len(self.cvs[i])):
                    self.paths[i].path.lineTo(*self.cvs[i][j])

    def mousePressEvent(self, event):
        """ actions that happen, if mouse button will be clicked """
        self.click_x_y = np.array([event.pos().x(), event.pos().y()])

        if event.buttons() == qc.Qt.LeftButton:
            # New class implementation
            # If you click on a point, change flags, remember path and cv index
            #if len(self.paths) > 0:
            #    for index_path, each_path in enumerate(self.paths.list_of_paths):
            #        for index_cv, each_cv in enumerate(each_path.cvs):
            #            # calculate if the mouse click is on the cv position
            #            if (self.click_x_y <= each_cv + each_path.cv_size).all() and (self.click_x_y >= each_cv - each_path.cv_size).all():
            #                self.move_cv = True
            #                self.moved_path = index_path
            #                self.moved_cv = index_cv
            #                return
            ## If not a point, set a point
            #if len(self.current_cv) == 0:
            #    self.paths[-1].path.moveTo(*self.click_x_y)
            #self.paths[-1].path.lineTo(*self.click_x_y)
            #self.paths[-1].cvs = np.r_[self.paths[-1].cvs, [self.click_x_y]]

            # Old class implementation
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
            if len(self.current_cv) == 0:
                self.current_path.path.moveTo(*self.click_x_y)
            self.current_path.path.lineTo(*self.click_x_y)
            self.current_cv = np.r_[self.current_cv, [self.click_x_y]]

        self.plot()
        self.update()

    def mouseReleaseEvent(self, event):
        """ if left button is released, set some flags """
        # flags affect moved cv/path
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
        #TODO: Some structure and maybe a plan

        tmp_x_y = np.array([event.pos().x(), event.pos().y()])

        # New class implementation
        # if click began on cv
        #if self.move_cv:
        #    # if (only?) left mouse button is on hold
        #    if event.buttons() == qc.Qt.LeftButton:
        #        if self.moved_path is not None and self.moved_path >= 0:
        #            self.paths[self.moved_path][self.moved_cv] = tmp_x_y
        #    # if both buttons are on hold
        #    elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
        #        self.track_movement += tmp_x_y - self.click_x_y
        #        self.move_everything(tmp_x_y)
        #        self.click_x_y = tmp_x_y
        ## if click began somewhere else than a cv
        #else:
        #    # change current cv if there is one with holding left mouse button
        #    #TODO: Might be a problem: how to declare active path?
        #    if event.buttons() == qc.Qt.LeftButton and len(self.paths[-1]) > 0:
        #        self.move_current_cv(tmp_x_y)
        #    # change position of everything with right mouse button
        #    elif event.buttons() == qc.Qt.RightButton:
        #        self.track_movement += tmp_x_y - self.click_x_y
        #        self.move_everything(tmp_x_y)
        #        self.click_x_y = tmp_x_y
        #    # change both if both buttons are pressed (if there is a current cv)
        #    elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
        #        if len(self.paths[-1]) == 0:
        #            self.paths[-1].path.moveTo(*self.click_x_y)
        #        self.paths[-1].path.lineTo(*self.click_x_y)
        #        self.paths[-1].cvs = np.r_[self.current_cv, [self.click_x_y]]
        #
        #        self.move_cv = True
        #
        #        self.track_movement += tmp_x_y - self.click_x_y
        #        self.move_everything(tmp_x_y)
        #
        #        self.click_x_y = tmp_x_y

        # Old class implementation
        if self.move_cv:
            if event.buttons() == qc.Qt.LeftButton:
                if self.moved_path is not None and self.moved_path >= 0:
                    self.cvs[self.moved_path][self.moved_cv] = tmp_x_y
                    self.draw_path_between_cv()
                elif self.moved_path is not None and self.moved_path == -1:
                    self.current_cv[self.moved_cv] = tmp_x_y
                    self.draw_path_between_cv()
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
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
                self.draw_path_between_cv()

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

    def calculate_zoom_translation(self, cv_list, reference_point, zoom_factor, zoom_in=True):
        """ calculates zoom (in or out) for a list of points """
        for i in range(len(cv_list)):
            tmp_vector = cv_list[i] - reference_point
            if zoom_in:
                cv_list[i] = reference_point + tmp_vector * (1 + zoom_factor)
            else:
                cv_list[i] = reference_point + tmp_vector / (1 + zoom_factor)

    def wheelEvent(self, event):
        """ Implements zoom through mouse wheel """
        self.point_of_zoom = np.array([event.pos().x(), event.pos().y()])
        self.zoom += event.angleDelta().y()//120
        # New class implementation
        # to zoom in/scroll up
        #if event.angleDelta().y() > 0:
        #    # calculate cvs
        #    for i in range(len(self.paths)):
        #        for j in range(len(self.paths[i].cvs)):
        #            self.calculate_zoom_translation(self.paths[i].cvs[i], self.point_of_zoom, self.zoom_factor)
        #
        #    self.track_zoom *= (1 + self.zoom_factor)
        #
        #    # change of track_movement
        #    tmp_vector = self.track_movement - self.point_of_zoom
        #    self.track_movement = self.point_of_zoom + (tmp_vector * (1 + self.zoom_factor))
        #
        ## to zoom out
        #else:
        #    for i in range(len(self.paths)):
        #        for j in range(len(self.paths[i].cvs)):
        #            self.calculate_zoom_translation(self.paths[i].cvs[i], self.point_of_zoom, self.zoom_factor, zoom_in=False)
        #
        #    self.track_zoom /= (1 + self.zoom_factor)
        #
        #    # change of track_movement
        #    tmp_vector = self.track_movement - self.point_of_zoom
        #    self.track_movement = self.point_of_zoom + (tmp_vector / (1 + self.zoom_factor))

        # Old class implementation
        # to zoom in/scroll up
        if event.angleDelta().y() > 0:
            # calculate current_cv
            self.calculate_zoom_translation(self.current_cv, self.point_of_zoom, self.zoom_factor)
            # calculate old cvs
            for i in range(len(self.cvs)):
                self.calculate_zoom_translation(self.cvs[i], self.point_of_zoom, self.zoom_factor)

            self.track_zoom *= (1 + self.zoom_factor)

            # change of track_movement
            tmp_vector = self.track_movement - self.point_of_zoom
            self.track_movement = self.point_of_zoom + (tmp_vector * (1 + self.zoom_factor))

        # to zoom out
        else:
            self.calculate_zoom_translation(self.current_cv, self.point_of_zoom, self.zoom_factor, zoom_in=False)
            for i in range(len(self.cvs)):
                self.calculate_zoom_translation(self.cvs[i], self.point_of_zoom, self.zoom_factor, zoom_in=False)
            self.track_zoom /= (1 + self.zoom_factor)

            # change of track_movement
            tmp_vector = self.track_movement - self.point_of_zoom
            self.track_movement = self.point_of_zoom + (tmp_vector / (1 + self.zoom_factor))

        self.draw_path_between_cv()
        self.plot()
        self.update()

    def move_current_cv(self, tmp_x_y):
        #TODO: outdated
        """ moved the most recent path cvs """
        #TODO: new: tbd - moves a specific path
        self.current_cv[-1] = tmp_x_y  # change last cv of current cv_path
        self.draw_path_between_cv()

    def move_everything(self, tmp_x_y):
        """ moves every cv """
        # New class implementation
        #if len(self.paths) != 0:
        #    for i in range(len(self.paths)):
        #        self.paths[i] += tmp_x_y - self.click_x_y  # if it exist, change pos of all cv_paths

        # Old class implementation
        if len(self.current_cv) > 0:
            self.current_cv += tmp_x_y - self.click_x_y  # change position of current cv_path

        if len(self.cvs) != 0:
            for i in range(len(self.cvs)):
                self.cvs[i] += tmp_x_y - self.click_x_y  # if it exist, change pos of prior cv_paths

    def mouseDoubleClickEvent(self, event):
        """ delete through double click - only one at once """
        # Shouldn't it be the newest one of the old ones? -> old ones count from behind (len-index)
        point_found = False

        # New class implementation
        #if len(self.paths) > 0 and not point_found:
        #    for index_path, each_path in enumerate(self.paths):
        #        for index_cv, each_cv in enumerate(each_path.cvs):
        #            # calculate if the mouse click is on the cv position
        #            if (self.click_x_y <= each_cv + each_path.cv_size).all() and (self.click_x_y >= each_cv - each_path.cv_size).all():
        #                self.paths[index_path] = np.delete(self.paths[index_path], index_cv, 0)
        #                point_found = True
        #                break
        #        if point_found:
        #            break
        # if path is empty
        #for index, each_path in enumerate(self.paths):
        #    if len(each_path) == 0:
        #        self.paths.pop(index)

        # Old class implementation
        if len(self.current_cv) > 0:
            for index, each_cv in enumerate(self.current_cv):
                if (self.click_x_y <= each_cv + self.cv_size).all() and (self.click_x_y >= each_cv - self.cv_size).all():
                    self.current_cv = np.delete(self.current_cv, index, 0)
                    point_found = True
                    break
        if len(self.cvs) > 0 and not point_found:
            for index_path, each_path in enumerate(self.cvs):
                for index_cv, each_cv in enumerate(each_path):
                    # calculate if the mouse click is on the cv position
                    if (self.click_x_y <= each_cv + self.cv_size).all() and (self.click_x_y >= each_cv - self.cv_size).all():
                        self.cvs[index_path] = np.delete(self.cvs[index_path], index_cv, 0)
                        point_found = True
                        break
                if point_found:
                    break
        # if path is empty
        for index, each_path in enumerate(self.cvs):
            if len(each_path) == 0:
                self.cvs.pop(index)

        self.draw_path_between_cv()

        self.plot()
        self.update()

    #TODO: I'm here with New-Old-Class adaption
    def move_to_center(self):
        """ Move everything to center (depends on self.track_movement and self.track_zoom """
        # New class implementation
        #for i in range(len(self.paths)):
        #    self.paths[i] -= self.track_movement
        #self.track_movement -= self.track_movement
        #
        #if self.track_zoom > 1:
        #    for i in range(len(self.paths)):
        #        #TODO: Gibt eine Funktion, die hier benutzt werden kann -> calculate_zoom_translation()
        #        for j in range(len(self.paths[i])):
        #            tmp_vector = self.paths[i][j]
        #            self.paths[i][j] = tmp_vector / self.track_zoom
        #    self.track_zoom /= self.track_zoom
        #else:
        #    for i in range(len(self.paths)):
        #        for j in range(len(self.paths[i])):
        #            tmp_vector = self.paths[i][j]
        #            self.paths[i][j] = tmp_vector / self.track_zoom
        #    self.track_zoom /= self.track_zoom


        # Old class implementation
        for i in range(len(self.cvs)):
            self.cvs[i] -= self.track_movement
        self.current_cv -= self.track_movement
        self.track_movement -= self.track_movement

        if self.track_zoom > 1:
            for i in range(len(self.current_cv)):
                tmp_vector = self.current_cv[i]
                self.current_cv[i] = tmp_vector / self.track_zoom
            for i in range(len(self.cvs)):
                for j in range(len(self.cvs[i])):
                    tmp_vector = self.cvs[i][j]
                    self.cvs[i][j] = tmp_vector / self.track_zoom
            self.track_zoom /= self.track_zoom

        else:
            for i in range(len(self.current_cv)):
                tmp_vector = self.current_cv[i]
                self.current_cv[i] = tmp_vector / self.track_zoom
            # calculate old cvs
            for i in range(len(self.cvs)):
                for j in range(len(self.cvs[i])):
                    tmp_vector = self.cvs[i][j]
                    self.cvs[i][j] = tmp_vector / self.track_zoom
            self.track_zoom /= self.track_zoom

        self.draw_path_between_cv()

        self.plot()
        self.update()

    def display_tracking(self, display):
        """ returns string to display movement/position and zoom """
        # used in GuiWidget -> update_gui()
        if display == "position":
            return f"Position: ({int(self.track_movement[0])},{int(self.track_movement[1])})"
        elif display == "zoom":
            return f"Zoom: {round(self.track_zoom, 2)}"

    def create_new_path(self, cm_type):
        """ creates new path with cm_type(normal/fast/slow) """
        # New class implementation
        #if len(self.paths[-1]) != 0:
        #    self.paths.append(Path(path_type=cm_type))

        # Old class implementation
        if len(self.current_cv) != 0:
            self.paths.append(self.current_path)
            self.current_path = Path(qg.QPainterPath(), cm_type)
            self.cvs.append(self.current_cv)
            self.current_cv = np.array([]).reshape(0, 2)
