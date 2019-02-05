import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import time
from Vector import Vector
import numpy as np
from scipy.spatial import distance


class Player:
    def __init__(self, x, y, layer, painter,map_layer, track):
        self.x_initial = x
        self.y_initial = y
        self.x = x
        self.y = y
        self.layer = layer
        self.painter = painter
        self.vector = Vector(0,1,0)
        self.color = qc.Qt.red
        self.g = Vector(0,9.8,0)
        self.start = time.time()
        self.map = map_layer.toImage()
        self.track = track
        self.surface_vector = Vector(0,0,0)
        self.time_direction = 1
        self.time_speed = 0.001  # 0.01 <=> 100-times slower
        self.time_control_point = time.time()
        self.hit_type = ""
        print(track)

    def show(self):
        '''
        draws a player on special layer
        :param surface_painter: layers painter
        :return: None
        '''
        self.layer.fill(qg.QColor(0, 0, 0, 0))
        self.painter.setPen(qg.QPen(self.color, 10, qc.Qt.SolidLine))
        self.painter.drawPoint(self.x, self.y)
        #  draw vector
        self.painter.setPen(qg.QPen(qc.Qt.green, 2, qc.Qt.SolidLine))
        self.painter.drawLine(self.x, self.y, self.x+self.vector.x, self.y+self.vector.y)

    def next(self):
        self.x += self.vector.x
        self.y += self.vector.y

        t = time.time() - self.start
        #  am I crossing smw?
        indx_a = self.closest_node([self.x, self.y])
        if abs(self.vector)< 10:
            indx_b = self.closest_node([self.x+self.vector.norm().x*10, self.y+self.vector.norm().y*10])
        else:
            indx_b = self.closest_node([self.x + self.vector.x, self.y + self.vector.y])

        if indx_a == indx_b:
            if indx_a > 0:
                indx_a -= 1
            else:
                indx_b += 1
        else:
            # expand selection
            if indx_a>indx_b:
                indx_a += 2
                indx_b -= 2
            else:
                indx_a -= 2
                indx_b += 2
        if indx_b >= len(self.track):
            indx_b = len(self.track)-1
        if indx_a >= len(self.track):
            indx_a = len(self.track)-1


        collision = self.exact_intersection(indx_a, indx_b)
        #  show support points
        self.painter.setPen(qg.QPen(qc.Qt.darkGreen, 3, qc.Qt.SolidLine))
        self.painter.drawLine(self.track[indx_a][0],self.track[indx_a][1],self.track[indx_b][0],self.track[indx_b][1])
        if collision:
            self.painter.setPen(qg.QPen(qc.Qt.darkMagenta, 30, qc.Qt.SolidLine))
            self.painter.drawPoint(collision[0], collision[1])
        if collision and self.map.pixel(collision[0], collision[1]) != 0:

            surface = Vector.make_vector(Vector,self.track[indx_a], self.track[indx_b])
            if self.vector.y > 0:
                # hit floor
                self.y -= 1
            self.vector = self.vector.proj_on(surface)
            print("collision at: ",collision)

        self.vector += self.g * (t * self.time_speed)





    def closest_node(self, node):
        closest_index = distance.cdist([node], self.track).argmin()
        return closest_index

    def exact_intersection(self, i, j):
        x1, y1 = self.x, self.y
        x2, y2 = self.x+self.vector.x, self.y+self.vector.y
        if abs(self.vector) < 10:
            x2, y2 = self.x + self.vector.norm().x*10, self.y + self.vector.norm().y*10

        if i >= len(self.track) - 1 or i == 0 or j >= len(self.track) - 1 or j == 0:
            return False

        x3, y3 = self.track[i][0], self.track[i][1]
        x4, y4 = self.track[j][0], self.track[j][1]

        denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        if denominator == 0:
            return False

        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

        if ua < 0 or ua > 1 or ub < 0 or ub > 1:
            return False

        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return [x, y]