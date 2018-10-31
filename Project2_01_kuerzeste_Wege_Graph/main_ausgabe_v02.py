"""
2nd version of main_ausgabe
main reason: now you can click on the map and the nearest point to your click will be highlighted

- only works till Graph_v06
"""

from Graph_v05 import Graph
import sys, random, math, numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class StreetMap(QtWidgets.QWidget):
    def __init__(self):
        # self.chosen_points = []
        QtWidgets.QWidget.__init__(self)

        # TODO: Maybe someday we can zoom in and out on the map
        self.zoom = 0

        self.setFixedWidth(1000)
        self.setFixedHeight(1000)
        self.our_graph = Graph("nodes.csv", "edges.csv")

        self.start = -1
        self.destination = -1
        self.P = -1

        self.movement_right = False
        self.movement_left = False
        self.movement_top = False
        self.movement_bottom = False
        self.zoom_in = False
        self.zoom_out = False

        # member variables
        self.nodes_screen_dict_all = {}  # dict like: nodes_screen_dict_all[nodes_number]: [x, y]
        self.nodes_chosen_dict = {}  # dict like: nodes_chosen[nodes_number]: [x, y]

        self.nearest_point_to_mouse = []  # list like: nearest_point_to_mouse: [node_number, distance]

        self.debug_counter = 0

        # transforming longitude/latitude into screen x- and y-coordinates
        self.calculate_coordinates_on_screen()

        # simple example how to choose some nodes
        self.splitting_nodes_chosen_every_second_one(self.nodes_chosen_dict)

        self.screen = QtGui.QPixmap()

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()

        self.set_pen(pen, painter, '#000000', 1)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)  # TODO: Was macht das?

        # show edges
        self.show_edges(painter, self.our_graph.edges_out_dict)

        # show all nodes
        self.show_nodes(painter, self.nodes_screen_dict_all)

        # change color and size
        self.set_pen(pen, painter, '#FF0000', 5)

        # draw nearest point to mouse click, if there's one
        if len(self.nearest_point_to_mouse) > 0:
            self.show_specific_node(painter, self.nearest_point_to_mouse[0])

        # show chosen nodes
        # self.show_nodes(painter, self.nodes_chosen_dict)

        # calculate path #
        self.calculate_path_nodes()
        #if self.P != -1:
        #    print("Strecke:", self.our_graph.get_distance_of_path(self.P), "km")
        # show visited nodes
        self.set_pen(pen, painter, '#0000FF', 2)
        self.show_visited_nodes(painter)

        # show path
        self.set_pen(pen, painter, '#FF0000', 2)
        self.show_path(painter)

        # movements in gui, value -> size of steps
        self.show_movement(5)

        # zooming in gui with i/o or +/-, values = zoom factor in/out
        self.show_zoom(1.25, 0.8)

    """
    getter and setter methods
    """

    # draws one specific point
    def show_specific_node(self, painter, node_number):
        painter.drawPoint(self.nodes_screen_dict_all[node_number][0], self.nodes_screen_dict_all[node_number][1])

    # draws one specific edge
    def show_specific_edge(self, painter, edge):
        start_node, end_node = edge[0], edge[1]
        x_start, y_start = self.nodes_screen_dict_all[start_node][0], self.nodes_screen_dict_all[start_node][1]
        x_end, y_end = self.nodes_screen_dict_all[end_node][0], self.nodes_screen_dict_all[end_node][1]
        painter.drawLine(x_start, y_start, x_end, y_end)

    # draws a point for every node
    def show_nodes(self, painter, nodes_dict):
        for node in nodes_dict:
            painter.drawPoint(self.nodes_screen_dict_all[node][0], self.nodes_screen_dict_all[node][1])

    # draws a line for every edge
    def show_edges(self, painter, edges_dict):
        for start_node in edges_dict:
            for end_node in edges_dict[start_node]:
                x_start, y_start = self.nodes_screen_dict_all[start_node][0], self.nodes_screen_dict_all[start_node][1]
                x_end, y_end = self.nodes_screen_dict_all[end_node][0], self.nodes_screen_dict_all[end_node][1]
                painter.drawLine(x_start, y_start, x_end, y_end)

    """
    methods to change gui
    """
    def set_pen(self, pen, painter, color, width):
        pen.setColor(QtGui.QColor(color))
        pen.setWidth(width)
        painter.setPen(pen)

    def show_path(self, painter):
        if self.P != -1:
            for i in range(len(self.P)-1):
                self.show_specific_edge(painter, [self.P[i], self.P[i+1]])

    def show_visited_nodes(self, painter):
        self.show_nodes(painter, self.our_graph.visited)

    def show_movement(self, value):
        if self.movement_left:
            self.show_movement_helper(False, (-1) * value)
        if self.movement_right:
            self.show_movement_helper(False, value)
        if self.movement_top:
            self.show_movement_helper(True, (-1) * value)
        if self.movement_bottom:
            self.show_movement_helper(True, value)

    def show_movement_helper(self, up_down_bool, value):
        for each in self.our_graph.nodes_list:
            self.nodes_screen_dict_all[each][up_down_bool] += value

    def show_zoom(self, zoom_in, zoom_out):
        if self.zoom_in:
            self.show_zoom(zoom_in)

        if self.zoom_out:
            self.show_zoom(zoom_out)

    """
    methods, which are working with nodes and edges
    """

    def calculate_zoom(self, zoom_factor):
        x_center = self.width() / 2
        y_center = self.height() / 2

        for each in self.our_graph.nodes_list:
            x = self.nodes_screen_dict_all[each][0]
            y = self.nodes_screen_dict_all[each][1]
            vector = np.array([x - x_center, y - y_center])
            # vector = [vector[0]/np.linalg.norm(vector),vector[1]/np.linalg.norm(vector)]

            vector *= zoom_factor
            # x_scale = vector[0] * 1.25
            # y_scale = vector[1] * 1.25
            self.nodes_screen_dict_all[each][0] = x_center + vector[0]
            self.nodes_screen_dict_all[each][1] = y_center + vector[1]

    def calculate_path_nodes(self):
        if self.start != -1 and self.destination != -1:
            self.P = self.our_graph.berechne_den_weg(self.start, self.destination)
            #self.P = self.our_graph.berechne_den_weg_original(self.start, self.destination)
        # print(self.P)

    # transforms longitude/latitude to screen x- and y-coordinates
    def calculate_coordinates_on_screen(self):
        # values to transform longitude/latitude to screen x- and y-coordinates
        left_side = self.our_graph.get_smallest_longitude()
        right_side = self.our_graph.get_biggest_longitude()
        up_side = self.our_graph.get_biggest_latitude()
        down_side = self.our_graph.get_smallest_latitude()

        for node_number in self.our_graph.nodes_list:
            tmp_coord = self.our_graph.get_coordinates(node_number)
            tmp_x = (tmp_coord[0] - left_side) * (self.width()/(right_side - left_side))
            tmp_y = (tmp_coord[1] - up_side) * (self.height()/(down_side - up_side))
            self.nodes_screen_dict_all[node_number] = [int(tmp_x), int(tmp_y)]

    # returns the minimum distance in a list [node, distance]
    def calculate_minimum_distance_to_mouse(self, event, nodes_dict):
        def calculate_distance(point_mouse, point_node_screen):
            step_one = (point_mouse[0] - point_node_screen[0])**2
            step_two = (point_mouse[1] - point_node_screen[1])**2
            return math.sqrt(step_one + step_two)

        mouse = [event.x(), event.y()]
        minimum_distance = []  # list like: [node, distance]

        # print("Position:", event.x(), event.y())

        x_max, y_max = self.width(), self.height()
        proof_x_min = mouse[0] - 50 if (mouse[0] - 50) > 0 else 0
        proof_x_max = mouse[0] + 50 if (mouse[0] + 50) < x_max else x_max
        proof_y_min = mouse[1] - 50 if (mouse[1] - 50) > 0 else 0
        proof_y_max = mouse[1] + 50 if (mouse[1] + 50) < y_max else y_max

        # runs through all nodes and searches for those in range to calculate the distance
        # if it doesn't found any, it increases the range
        while True:
            for node in nodes_dict:
                if proof_x_max > nodes_dict[node][0] > proof_x_min and proof_y_max > nodes_dict[node][1] > proof_y_min:
                    tmp_distance = calculate_distance(mouse, self.nodes_screen_dict_all[node])
                    if len(minimum_distance) == 0:
                        minimum_distance = [node, tmp_distance]
                    else:
                        if tmp_distance < minimum_distance[1]:
                            minimum_distance = [node, tmp_distance]
            if len(minimum_distance) > 0:
                return minimum_distance
            else:
                proof_x_min = proof_x_min - 50 if (proof_x_min - 50) > 0 else 0
                proof_x_max = proof_x_max + 50 if (proof_x_max + 50) < x_max else x_max
                proof_y_min = proof_y_min - 50 if (proof_y_min - 50) > 0 else 0
                proof_y_max = proof_y_max + 50 if (proof_y_max + 50) < y_max else y_max

    def splitting_nodes_chosen_every_second_one(self, nodes_dict):
        tmp_counter = 0
        for node in self.nodes_screen_dict_all:
            if tmp_counter % 2 == 0:
                nodes_dict[node] = self.nodes_screen_dict_all[node]
            tmp_counter += 1

    """
    PyQt5 methods
    """

    def mouseReleaseEvent(self, cursor_event):
        self.nearest_point_to_mouse = self.calculate_minimum_distance_to_mouse(cursor_event, self.nodes_screen_dict_all)
        if self.start == -1:
            self.start = self.nearest_point_to_mouse[0]
        else:
            if self.destination == -1:
                self.destination = self.nearest_point_to_mouse[0]
            else:
                self.start = self.destination
                self.destination = self.nearest_point_to_mouse[0]
        self.update()

    # Pressing A, D, Left or Right switches the status of self.movement_left or *_right to True
    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_D or event.key() == QtCore.Qt.Key_Right) and not event.isAutoRepeat():
            self.movement_right = True
        elif (event.key() == QtCore.Qt.Key_A or event.key() == QtCore.Qt.Key_Left) and not event.isAutoRepeat():
            self.movement_left = True
        elif (event.key() == QtCore.Qt.Key_W or event.key() == QtCore.Qt.Key_Up) and not event.isAutoRepeat():
            self.movement_top = True
        elif (event.key() == QtCore.Qt.Key_S or event.key() == QtCore.Qt.Key_Down) and not event.isAutoRepeat():
            self.movement_bottom = True
        elif (event.key() == QtCore.Qt.Key_I or event.key() == QtCore.Qt.Key_Plus) and not event.isAutoRepeat():
            self.zoom_in = True
        elif (event.key() == QtCore.Qt.Key_O or event.key() == QtCore.Qt.Key_Minus) and not event.isAutoRepeat():
            self.zoom_out = True
        # Releasing any Key switches both movement values to False
        self.update()

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.movement_right = False
            self.movement_left = False
            self.movement_top = False
            self.movement_bottom = False
            self.zoom_in = False
            self.zoom_out = False
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = StreetMap()
    w.show()
    sys.exit(app.exec_())
