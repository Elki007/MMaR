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

        self.paths = GroupOfPaths()

        self.track = []

        self.showCV = True

        self.editMode = False

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

        self.paths = GroupOfPaths()

        self.update()

    def undo(self):
        """ removes last created point -> if it's the last point on path -> delete path """
        self.paths.delete(-1, -1)
        self.plot()
        self.update()

    def show_cv(self, value):
        """ value = True or False -> if cv and lines will be displayed """
        self.showCV = value
        self.update()

    def edit_mode(self, value):
        self.editMode = value
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

            # draws lines between direct and manipulation cvs
            self.draw_cv_lines(qc.Qt.green, 1)

            # draws points of cvs
            self.draw_cv_points()

        if self.editMode:
            # draws lines between direct and manipulation cvs
            self.draw_cv_lines(qc.Qt.green, 1)
            # draws points of cvs
            self.draw_cv_points()
            # draws points and lines of bounding box
            self.draw_bounding_box()

        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))  # wird woanders wiederholt/überschrieben?
        self.painter_total.drawPixmap(0, 0, self.ebene_bg)
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        self.painter_total.drawPixmap(0, 0, self.ebene_cv)
        self.painter_total.drawPixmap(0, 0, self.ebene_schlitten)
        self.setPixmap(self.ebene_total)

    def draw_cv_points(self, only_active=False):
        """ draws cv points of bezier lines """
        for i in range(len(self.paths)):
            if only_active:
                if not self.paths[i].active:
                    continue

            if self.paths[i].form == "bezier":
                for j in range(len(self.paths[i])):
                    # only main cvs will be painted here, others will be painted in 'else'
                    if j%3 == 0:
                        self.painter_cv.setPen(qg.QPen(qc.Qt.blue, self.paths[i].cv_size, qc.Qt.SolidLine))
                        self.painter_cv.drawPoint(*self.paths[i][j])
                    else:
                        radius = self.paths[i].cv_size/2
                        self.painter_cv.setPen(qg.QPen(qc.Qt.red, radius, qc.Qt.SolidLine))
                        self.painter_cv.setBrush(qc.Qt.red)
                        self.painter_cv.drawEllipse(*(self.paths[i][j]-(radius/2)), radius, radius)
                        self.painter_cv.setBrush(qc.Qt.transparent)

    def draw_cv_lines(self, color, pen_size):
        """ draws lines between cvs """
        self.paths.draw_reset()
        for i in range(len(self.paths)):
            if self.paths[i].form == "bezier":
                for j in range(len(self.paths[i])):
                    # connects 2nd with 1st main cv (1st of 4)
                    if (j+2) % 3 == 0:
                        self.paths.draw_moveTo(*self.paths[i][j])
                        self.paths.draw_lineTo(*self.paths[i][j-1])
                    # connects 3rd with 4th main cv (4th of 4)
                    elif (j+1) % 3 == 0 and len(self.paths[i]) > j+1:
                        self.paths.draw_moveTo(*self.paths[i][j])
                        self.paths.draw_lineTo(*self.paths[i][j+1])
        self.painter_cv.setPen(qg.QPen(color, pen_size, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.paths.qpath)

    def draw_bounding_box(self):
        self.paths.draw_reset_bounding_box()
        self.paths[0].bounding_box_refresh()
        self.painter_cv.setPen(qg.QPen(qc.Qt.white, self.paths[0].cv_size, qc.Qt.SolidLine))

        self.paths.draw_moveTo_bounding_box(*self.paths[0].bounding_box[0])
        for i in range(1, 5):
            self.painter_cv.drawPoint(*self.paths[0].bounding_box[i % 4])
            self.paths.draw_lineTo_bounding_box(*self.paths[0].bounding_box[i % 4])

        self.painter_cv.setPen(qg.QPen(qc.Qt.white, 1, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.paths.qpath_bounding_box)

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

    def bezier_diff(self, cv_points,t, x_y):

        if len(cv_points) == 4:
            P0=cv_points[0][x_y]
            P1=cv_points[1][x_y]
            P2=cv_points[2][x_y]
            P3=cv_points[3][x_y]
            return (1-t)**2*(P1-P0)+2*t*(1-t)*(P2-P1)+t**2*(P3-P2)
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

        for i in range(len(self.paths)):
            draw_bezier_path(self.paths[i].cvs, self.paths[i].color)

    def draw_path_between_cv(self):
        #TODO: outdated
        """ draws all paths betweens cv (optional only current ones) """
        """ new: tbd - draw just some 'strings' to the main cvs - put it in update() """
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

        # if left mouse button is clicked
        if event.buttons() == qc.Qt.LeftButton:
            # If you click on a point, change flags, remember path and cv index
            #TODO: self.paths ist immer mindestens 1 - kann das weg oder ist das Kunst?
            if len(self.paths) > 0:
                for index_path, each_path in enumerate(self.paths):
                    for index_cv, each_cv in enumerate(each_path):
                        # calculate if the mouse click is on the cv position
                        if (self.click_x_y <= each_cv + each_path.cv_size).all() and (self.click_x_y >= each_cv - each_path.cv_size).all():
                            self.move_cv = True
                            self.moved_path = index_path
                            self.moved_cv = index_cv
                            return
            # If not a point, set a point
            self.paths[-1].append_cvs(self.click_x_y)

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
        left button: change last placed cv (dynamic view of line)
        right button: move everything, tracked by self.track_movement
        """
        #TODO: Some structure and maybe a plan

        tmp_x_y = np.array([event.pos().x(), event.pos().y()])

        # if click began on cv
        if self.move_cv:
            # if (only?) left mouse button is on hold
            if event.buttons() == qc.Qt.LeftButton:
                if self.moved_path is not None and self.moved_path >= 0:
                    self.paths[self.moved_path][self.moved_cv] = tmp_x_y
            # if both buttons are on hold
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                self.track_movement += tmp_x_y - self.click_x_y
                self.move_everything(tmp_x_y)
                self.click_x_y = tmp_x_y
        # if click began somewhere else than a cv
        else:
            # TODO: BUG: Wenn neuer Punkt erstellt & gehalten wird und die rechte Maustaste hinzukommt
            # left mouse button on hold: change last placed cv if there is one
            # TODO: Might be a problem: how to declare active path?
            if event.buttons() == qc.Qt.LeftButton and len(self.paths[-1]) > 0:
                self.move_last_cv(tmp_x_y)
            # right mouse button on hold: change position of everything
            elif event.buttons() == qc.Qt.RightButton:
                self.track_movement += tmp_x_y - self.click_x_y
                self.move_everything(tmp_x_y)
                self.click_x_y = tmp_x_y
            # change both if both buttons are pressed (if there is a last cv)
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                self.paths[-1].append_cvs(self.click_x_y)

                self.move_cv = True

                self.track_movement += tmp_x_y - self.click_x_y
                self.move_everything(tmp_x_y)

                self.click_x_y = tmp_x_y

        self.plot()
        self.update()

    def mouseDoubleClickEvent(self, event):
        """ delete through double click - only one at once """
        # Shouldn't it be the newest one of the old ones? -> old ones count from behind (len-index)
        point_found = False

        if len(self.paths) > 0 and not point_found:
            for index_path, each_path in enumerate(self.paths):
                for index_cv, each_cv in enumerate(each_path.cvs):
                    # calculate if the mouse click is on the cv position
                    if (self.click_x_y <= each_cv + each_path.cv_size).all() and (self.click_x_y >= each_cv - each_path.cv_size).all():
                        self.paths.delete(index_path, index_cv)
                        point_found = True
                        break
                if point_found:
                    break

        self.plot()
        self.update()

    def wheelEvent(self, event):
        """ Implements zoom through mouse wheel """
        self.point_of_zoom = np.array([event.pos().x(), event.pos().y()])
        self.zoom += event.angleDelta().y()//120

        # to zoom in/scroll up
        if event.angleDelta().y() > 0:
            # calculate cvs
            for i in range(len(self.paths)):
                self.calculate_zoom_translation(self.paths[i], self.point_of_zoom, self.zoom_factor)

            self.track_zoom *= (1 + self.zoom_factor)

            # change of track_movement
            tmp_vector = self.track_movement - self.point_of_zoom
            self.track_movement = self.point_of_zoom + (tmp_vector * (1 + self.zoom_factor))

        # to zoom out
        else:
            for i in range(len(self.paths)):
                self.calculate_zoom_translation(self.paths[i], self.point_of_zoom, self.zoom_factor, zoom_in=False)

            self.track_zoom /= (1 + self.zoom_factor)

            # change of track_movement
            tmp_vector = self.track_movement - self.point_of_zoom
            self.track_movement = self.point_of_zoom + (tmp_vector / (1 + self.zoom_factor))

        self.plot()
        self.update()

    @staticmethod
    def calculate_zoom_translation(cv_list, reference_point, zoom_factor, zoom_in=True):
        """ calculates zoom (in or out) for a list of points """
        for i in range(len(cv_list)):
            tmp_vector = cv_list[i] - reference_point
            if zoom_in:
                cv_list[i] = reference_point + tmp_vector * (1 + zoom_factor)
            else:
                cv_list[i] = reference_point + tmp_vector / (1 + zoom_factor)

    def move_specific_path(self):
        """ moves a specific chosen path """
        # TODO: tbd
        pass

    def move_last_cv(self, tmp_x_y):
        """ moves the most recent cv """
        self.paths[-1][-1] = tmp_x_y  # change last cv of last cv_path

    def move_everything(self, tmp_x_y):
        """ moves every cv of every path """
        if len(self.paths) != 0:
            for i in range(len(self.paths)):
                self.paths[i] += tmp_x_y - self.click_x_y  # if it exist, change pos of all cv_paths

    def move_to_center(self):
        """ Move everything to center (depends on self.track_movement and self.track_zoom """
        for i in range(len(self.paths)):
            self.paths[i] -= self.track_movement
        self.track_movement -= self.track_movement

        if self.track_zoom > 1:
            for i in range(len(self.paths)):
                #TODO: Gibt eine Funktion, die hier benutzt werden kann -> calculate_zoom_translation()
                for j in range(len(self.paths[i])):
                    tmp_vector = self.paths[i][j]
                    self.paths[i][j] = tmp_vector / self.track_zoom
            self.track_zoom /= self.track_zoom
        else:
            for i in range(len(self.paths)):
                for j in range(len(self.paths[i])):
                    tmp_vector = self.paths[i][j]
                    self.paths[i][j] = tmp_vector / self.track_zoom
            self.track_zoom /= self.track_zoom

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
        if len(self.paths[-1]) != 0:
            self.paths.append(Path(path_type=cm_type))

    def change_path_style(self, text):
        self.paths[-1].changed_style(text)

