import numpy as np
import scipy.interpolate as si
import sys
import math
from scipy.spatial import cKDTree, distance
from scipy.ndimage import interpolation

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

from Path import GroupOfPaths, Path
from Orientation import Orientation


"""
#Search -> Mögliche Verbesserung finden für das genannte Problem
"""

"""
Glossary:
cv -> control vertice -> point that's clicked with mouse
bbox -> bounding box -> rectangle box that surround each path 
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

        self.trackingPlayer = False

        # variables for drag and drops
        self.move_cv = False  # is a cv moved by mouse?
        self.moved_path = None
        self.moved_cv = None

        # variables for drag and drops of bounding box
        self.move_bbox = False
        self.moved_bbox_point = None

        self.orien = Orientation()

        # since attribute player does not exist in the beginning in WidgetGui -> it's this way around
        self.player = None

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

        self.plot()
        self.update()

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
        """ Set every Layer and Paths back """
        self.end_all_painters()
        self.fill_all_default()
        self.set_all_painters()
        self.paths = GroupOfPaths(path=Path())  # TODO: Why [Interessant]: Wenn path=Path() weggelassen wird: Alter Path wird neu referenziert
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
        """ turns on/off edit mode """
        self.editMode = value
        if not self.editMode:
            # back to original state
            self.paths.active_path = None
        self.update()

    def tracking_player(self, value):
        """ turns on/off edit mode """
        self.trackingPlayer = value
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
        """ draws everything user wants to see """

        if self.trackingPlayer and self.player is not None:
            #print("FEBUG!")
            self.orien.move_to_player(self.player, self.paths, self.parent.width(), self.parent.height())
            self.plot()  # TODO: muss hier dann noch einmal geplottet oder aber anders organisiert werden

        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))

        # if CV and lines in between shall be displayed
        if self.showCV:
            # draws lines between direct and manipulation cvs
            self.draw_cv_lines(qc.Qt.green, 1)

            # draws points of cvs
            self.draw_cv_points()

        if self.editMode and self.paths.active_path is not None:
            active_index = self.paths.active_path

            # draws lines between direct and manipulation cvs
            self.draw_cv_lines(qc.Qt.green, 1, active_index)
            # draws points of cvs
            self.draw_cv_points(active_index)
            # draws points and lines of bounding box
            self.draw_bounding_box(active_index)

        if self.player is not None:
            self.player.show()

        self.fill_layers()

    def player_created(self, player):
        """ If Player object was created in GuiWidget, it will be referenced in Pane """
        self.player = player

    def fill_layers(self):
        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))
        self.painter_total.drawPixmap(0, 0, self.ebene_bg)
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        self.painter_total.drawPixmap(0, 0, self.ebene_cv)
        self.painter_total.drawPixmap(0, 0, self.ebene_schlitten)
        self.setPixmap(self.ebene_total)

    def draw_cv_lines(self, color, pen_size, active_index=None):
        """ draws lines between cvs of all or just active path """
        self.paths.draw_reset()
        if active_index is None:
            for i in range(len(self.paths)):
                if self.paths[i].form == "bezier":
                    self.draw_cv_lines_bezier(i)
        else:
            if self.paths[active_index].form == "bezier":
                self.draw_cv_lines_bezier(active_index)

        self.painter_cv.setPen(qg.QPen(color, pen_size, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.paths.qpath)

    def draw_cv_lines_bezier(self, index):
        """ draws cv lines of bezier type """
        for j in range(len(self.paths[index])):
            # connects 2nd with 1st main cv (1st of 4)
            if (j + 2) % 3 == 0:
                self.paths.draw_moveTo(*self.paths[index][j])
                self.paths.draw_lineTo(*self.paths[index][j - 1])
            # connects 3rd with 4th main cv (4th of 4)
            elif (j + 1) % 3 == 0 and len(self.paths[index]) > j + 1:
                self.paths.draw_moveTo(*self.paths[index][j])
                self.paths.draw_lineTo(*self.paths[index][j + 1])

    def draw_cv_points(self, active_index=None):
        """ draws cv points """
        if active_index is None:
            for i in range(len(self.paths)):
                if self.paths[i].form == "bezier":
                    self.draw_cv_points_bezier(i)
        else:
            self.draw_cv_points_bezier(active_index)

    def draw_cv_points_bezier(self, index):
        """ draws cv points of bezier """
        for j in range(len(self.paths[index])):
            # only main cvs will be painted here, others will be painted in 'else'
            if j%3 == 0:
                self.painter_cv.setPen(qg.QPen(qc.Qt.blue, self.paths[index].cv_size, qc.Qt.SolidLine))
                self.painter_cv.drawPoint(*self.paths[index][j])
            else:
                radius = self.paths[index].cv_size/2
                self.painter_cv.setPen(qg.QPen(qc.Qt.red, radius, qc.Qt.SolidLine))
                self.painter_cv.setBrush(qc.Qt.red)
                self.painter_cv.drawEllipse(*(self.paths[index][j]-(radius/2)), radius, radius)
                self.painter_cv.setBrush(qc.Qt.transparent)

    def draw_bounding_box(self, active_index=None):
        """ draws all or a specific bounding box """
        self.paths.draw_reset_bounding_box()
        if active_index is None:
            for i in range(len(self.paths)):
                self.draw_bounding_box_single(i)
        else:
            self.draw_bounding_box_single(active_index)

        self.painter_cv.setPen(qg.QPen(qc.Qt.white, 1, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.paths.qpath_bounding_box)

    def draw_bounding_box_single(self, index):
        self.paths[index].bounding_box_refresh(self.move_bbox, self.moved_bbox_point, self.orien.get_click())
        self.painter_cv.setPen(qg.QPen(qc.Qt.white, self.paths[index].cv_size, qc.Qt.SolidLine))

        self.paths.draw_moveTo_bounding_box(*self.paths[index].bounding_box[3])
        for j in range(4):
            self.painter_cv.drawPoint(*self.paths[index].bounding_box[j])
            self.paths.draw_lineTo_bounding_box(*self.paths[index].bounding_box[j])

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
            return (1-t)**3 * four_points[0][x_y] + \
                   3*(1-t)**2 * t * four_points[1][x_y] + \
                   3*(1-t)*t**2 * four_points[2][x_y] + \
                   t**3 * four_points[3][x_y]

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

            return np.stack((x_coords, y_coords), 1)

        def draw_bezier_path(path, color):
            """ calculates points (with bezier()) to draw lines between them """
            path.plotted_points = bezier(path.cvs)
            qpath = qg.QPainterPath()

            if len(path.plotted_points) > 0:
                qpath.moveTo(*(path.plotted_points[0]))  # start point
                for j in range(len(path.plotted_points)):
                    self.track.append([*path.plotted_points[j]])
                    qpath.lineTo(*path.plotted_points[j])

                self.painter_pane.setPen(qg.QPen(color, 3, qc.Qt.SolidLine))
                self.painter_pane.drawPath(qpath)

        self.track = []

        for i in range(len(self.paths)):
            draw_bezier_path(self.paths[i], self.paths[i].color)

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

    def activate_nearest_path(self):
        """ find nearest path with ckdtree (from scipy) and return its index """
        #TODO: Generalisieren, damit mit jedem beliebigen Punkt der naheliegendste Path gefunden wird
        path_index = [None]
        if not self.paths.isempty():
            for i in range(len(self.paths)):
                tmp_tree = cKDTree(self.paths[i].plotted_points)
                dist, index = tmp_tree.query(self.orien.get_click())
                if path_index == [None]:
                    path_index = [i, dist, index]
                else:
                    if dist < path_index[1]:
                        path_index = [i, dist, index]

            if path_index != [None]:
                self.paths.activates_path(path_index[0])

    def set_new_cv(self, active_path=False):
        if active_path:
            index = 0 if self.paths.active_path is None else self.paths.active_path
            self.paths[index].append_cvs(self.orien.get_click())
        else:
            self.paths[-1].append_cvs(self.orien.get_click())

    def find_clicked_point(self, active_path=False):
        if active_path:
            index = 0 if self.paths.active_path is None else self.paths.active_path

            for index_point, each_point in enumerate(self.paths[index].bounding_box):
                # calculate if the mouse click is on the bounding position
                if self.orien.check_click_on_point(self.paths[index], each_point):
                    self.move_bbox = True
                    self.moved_bbox_point = index_point
                    return True

            for index_cv, each_cv in enumerate(self.paths[index]):
                # calculate if the mouse click is on the cv position
                if self.orien.check_click_on_point(self.paths[index], each_cv):
                    self.move_cv = True
                    self.moved_path = index
                    self.moved_cv = index_cv
                    return True

        else:
            # check if you click on a cv -> if yes -> self.move_cv activated
            for index_path, each_path in enumerate(self.paths):
                for index_cv, each_cv in enumerate(each_path):
                    # calculate if the mouse click is on the cv position
                    if self.orien.check_click_on_point(each_path, each_cv):
                        self.move_cv = True
                        self.moved_path = index_path
                        self.moved_cv = index_cv
                        return True

    def mousePressEvent(self, event):
        """ actions that happen, if mouse button will be clicked """
        self.orien.set_click(event)

        # if left mouse button is clicked
        if event.buttons() == qc.Qt.LeftButton:
            if self.editMode:
                # check if your click was on a cv of active path
                if not self.find_clicked_point(active_path=True) and self.paths.active_path is not None:
                    # If not an active point, set a point to active path
                    self.set_new_cv(active_path=True)
            else:
                # check if your click was on a cv
                if not self.find_clicked_point():
                    # If not a point, set a point to latest path
                    self.set_new_cv()

        self.plot()
        self.update()

    def mouseReleaseEvent(self, event):
        """ if left button is released, set some flags """
        # flags affect moved cv/path
        if event.button() == qc.Qt.LeftButton:
            self.move_cv = False
            self.moved_path = None
            self.moved_cv = None

            self.move_bbox = False
            self.moved_bbox_point = None

            self.plot()
            self.update()

    def mouseMoveEvent(self, event):
        """
        events of moving mouse while button is clicked
        left button: change last placed cv (dynamic view of line)
        right button: move everything, tracked by self.track_movement
        """

        self.orien.set_move(event)

        # if click began on cv
        if self.move_cv:
            # if (only?) left mouse button is on hold, drag cv to mouse position
            if event.buttons() == qc.Qt.LeftButton:
                if self.moved_path is not None and self.moved_path >= 0:
                    self.paths[self.moved_path][self.moved_cv] = self.orien.get_move()

            # if both buttons are on hold, drag cv and position of point
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                self.orien.move_points_and_screen(self.paths, self.player)

        elif self.move_bbox:
            # if (only?) left mouse button is on hold, drag cv to mouse position
            if event.buttons() == qc.Qt.LeftButton:
                # calculate with given active path and clicked bbox point
                self.orien.calculate_bbox_coordinates(self.paths[self.paths.active_path], self.moved_bbox_point)

            # if both buttons are on hold, do.. nothing?
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                pass

        # if click began somewhere else than a cv
        else:
            # TODO: BUG: Wenn neuer Punkt erstellt & gehalten wird und die rechte Maustaste hinzukommt
            index = -1 if self.paths.active_path is None else self.paths.active_path

            # left mouse button on hold: change last placed cv if there is one
            if event.buttons() == qc.Qt.LeftButton and len(self.paths[index]) > 0:
                if not self.editMode or (self.editMode and self.paths.active_path is not None):
                    self.move_last_cv(index)

            # right mouse button on hold: change position of everything
            elif event.buttons() == qc.Qt.RightButton:
                if self.editMode and self.paths.active_path is not None:
                    self.move_specific_path(index)
                    self.orien.actualize_click()
                else:
                    self.orien.move_points_and_screen(self.paths, self.player)
            # change both if both buttons are pressed (if there is a last cv)
            elif (event.buttons() & qc.Qt.LeftButton) and (event.buttons() & qc.Qt.RightButton):
                self.paths[-1].append_cvs(self.orien.get_click())

                self.move_cv = True

                self.orien.move_points_and_screen(self.paths)

        self.plot()
        self.update()

    def mouseDoubleClickEvent(self, event):
        """ delete through double click - only one at once """
        # Shouldn't it be the newest one of the old ones? -> old ones count from behind (len-index)
        point_found = False

        # if left mouse button is double clicked
        if event.buttons() == qc.Qt.LeftButton:
            if self.editMode:
                self.activate_nearest_path()

        if len(self.paths) > 0 and not point_found:
            for index_path, each_path in enumerate(self.paths):
                for index_cv, each_cv in enumerate(each_path.cvs):
                    # calculate if the mouse click is on the cv position
                    if self.click_on_cv(each_path, each_cv):
                        self.paths.delete(index_path, index_cv)
                        point_found = True
                        break
                if point_found:
                    break

        self.plot()
        self.update()

    def click_on_cv(self, path, cv):
        return self.orien.check_click_on_point(path, cv)

    def wheelEvent(self, event):
        """ Implements zoom through mouse wheel """
        # set point of zoom and direction (in/out)
        self.orien.set_zoom_settings(event)

        # to zoom in/scroll up
        if event.angleDelta().y() > 0:
            # calculate cvs
            for i in range(len(self.paths)):
                self.orien.calculate_zoom_translation(self.paths[i])
            self.orien.calculate_zoom_translation_player(self.player)

            self.orien.set_trace_zoom_in()

            # change of track_movement
            self.orien.set_trace_movement_while_zoom_in()

        # to zoom out
        else:
            for i in range(len(self.paths)):
                self.orien.calculate_zoom_translation(self.paths[i], zoom_in=False)
            self.orien.calculate_zoom_translation_player(self.player, zoom_in=False)
            self.orien.set_trace_zoom_out()

            # change of track_movement
            self.orien.set_trace_movement_while_zoom_out()

        self.plot()
        self.update()

    def move_specific_path(self, index):
        """ moves a specific chosen path """
        self.paths[index] += self.orien.get_movement()  # if it exist, change pos of all cv_paths

    def move_last_cv(self, index):
        """ moves the most recent cv of given path[index] """
        self.paths[index][-1] = self.orien.get_move()  # change last cv of last cv_path

    def move_to_center(self):
        """ Move everything to center (depends on self.track_movement and self.track_zoom """
        self.orien.move_to_center(self.paths, self.player)

        self.plot()
        self.update()

    def display_tracking(self, display):
        """ returns string to display movement/position and zoom """
        # used in GuiWidget -> update_gui()
        if display == "position":
            x, y = self.orien.get_trace_movement()
            return f"Position: ({int(x)},{int(y)})"
        elif display == "zoom":
            return f"Zoom: {round(self.orien.get_trace_zoom(), 4)}"

    def create_new_path(self, cm_type):
        """ creates new path with cm_type(normal/fast/slow) """
        if len(self.paths[-1]) != 0:
            self.paths.append(Path(path_type=cm_type))

    def change_path_style(self, text):
        self.paths[-1].changed_style(text)

    def save_all_paths(self):
        return self.paths.save_all_paths()

    def load_all_paths(self, all_paths):
        # TODO: BUG: Load ist noch nicht abhängig von Verschiebung und Zoom
        self.paths = GroupOfPaths(path=Path(*all_paths[0]))
        for i in range(1, len(all_paths)):
            self.paths.append(Path(*all_paths[i]))
        self.plot()
        self.update()
