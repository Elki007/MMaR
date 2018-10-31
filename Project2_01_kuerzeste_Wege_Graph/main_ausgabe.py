
from Projekt1_Datenstrukturen_und_kuerzeste_Wege.Graph_v04 import Graph
import sys, random
from PyQt5 import QtWidgets
from PyQt5 import QtGui
# from k_W_A import bereche_den_weg
from kuerzester_wege_algorithmus_v03 import bereche_den_weg
# from PyQt5 import QtCore


class StreetMap(QtWidgets.QWidget):
    def __init__(self):
        # self.chosen_points = []
        QtWidgets.QWidget.__init__(self)

        self.setFixedWidth(1000)
        self.setFixedHeight(1000)
        self.our_graph = Graph("nodes.csv", "edges.csv")
        # import berechnung
        self.P = bereche_den_weg(self.our_graph,self.our_graph.nodes_list[5],self.our_graph.nodes_list[55])
        self.screen_left = self.our_graph.get_smallest_longitude()
        self.screen_right = self.our_graph.get_biggest_longitude()
        self.screen_up = self.our_graph.get_biggest_latitude()
        self.screen_down = self.our_graph.get_smallest_latitude()

        self.nodes_screen_dict = {}  # dict like: nodes_screen[nodes_number]: [x, y]
        self.calculate_coordinates_on_screen()
        self.debug_counter = 0
        self.screen = QtGui.QPixmap()

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor('#ff0000'))
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        self.show_nodes(painter, self.nodes_screen_dict)
        self.show_edges(painter, self.our_graph.edges_out_dict)

    # draws one specific point
    def show_specific_node(self, painter, node_number):
        painter.drawPoint(self.nodes_screen_dict[node_number][0], self.nodes_screen_dict[node_number][1])

    # draws a point for every node
    def show_nodes(self, painter, nodes_dict):
        for node in nodes_dict:
            if node in self.P:
                pen = QtGui.QPen()
                if node == self.P[0]:
                    pen.setWidth(15)
                    pen.setColor(QtGui.QColor('#00ff00'))
                elif node == self.P[len(self.P)-1]:
                    pen.setWidth(15)
                    pen.setColor(QtGui.QColor('#0000ff'))
                else:
                    pen.setWidth(2)
                    pen.setColor(QtGui.QColor('#ff0000'))
                painter.setPen(pen)
            else:
                pen = QtGui.QPen()
                pen.setWidth(1)
                pen.setColor(QtGui.QColor('#000000'))
                painter.setPen(pen)

            painter.drawPoint(nodes_dict[node][0], nodes_dict[node][1])

    # draws one specific edge
    def show_specific_edge(self, painter, edge):
        start_node, end_node = edge[0], edge[1]
        x_start, y_start = self.nodes_screen_dict[start_node][0], self.nodes_screen_dict[start_node][1]
        x_end, y_end = self.nodes_screen_dict[end_node][0], self.nodes_screen_dict[end_node][1]
        painter.drawLine(x_start, y_start, x_end, y_end)

    # draws a line for every edge
    def show_edges(self, painter, edges_dict):
        for start_node in edges_dict:
            for end_node in edges_dict[start_node]:
                x_start, y_start = self.nodes_screen_dict[start_node][0], self.nodes_screen_dict[start_node][1]
                x_end, y_end = self.nodes_screen_dict[end_node][0], self.nodes_screen_dict[end_node][1]
                if start_node in self.P and end_node in self.P:
                    #print("FOUND##############")
                    pen = QtGui.QPen()
                    pen.setWidth(1)
                    pen.setColor(QtGui.QColor('#ff0000'))
                    painter.setPen(pen)
                else:
                    pen = QtGui.QPen()
                    pen.setWidth(1)
                    pen.setColor(QtGui.QColor('#000000'))
                    painter.setPen(pen)

                painter.drawLine(x_start, y_start, x_end, y_end)

    # transforms longitude/latitude to screen x- and y-coordinates
    def calculate_coordinates_on_screen(self):
        for node_number in self.our_graph.nodes_list:
            tmp_coord = self.our_graph.get_coordinates(node_number)
            tmp_x = (tmp_coord[0]-self.screen_left) * (self.width()/(self.screen_right - self.screen_left))
            tmp_y = (tmp_coord[1]-self.screen_up) * (self.height()/(self.screen_down - self.screen_up))
            self.nodes_screen_dict[node_number] = [int(tmp_x), int(tmp_y)]

    def mouseReleaseEvent(self, cursor_event):
        #self.update()
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = StreetMap()
    w.show()
    sys.exit(app.exec_())
