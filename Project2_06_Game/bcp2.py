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
        self.vector = Vector(0,0,0)
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
        self.painter.drawLine(self.x, self.y, self.x+self.vector.x*10, self.y+self.vector.y*10)

    def next(self):
        t = time.time() - self.start
        #  am I crossing smw?
        crossing = self.check_on_track()
        if crossing:
            indx = self.closest_node(crossing)
            nearest_node = self.track[indx]
            self.painter.setPen(qg.QPen(qc.Qt.white, 2, qc.Qt.SolidLine))
            self.painter.drawPoint(nearest_node[0],nearest_node[1])

            # strat argument
            self.surface_vector = Vector.make_vector(self, self.track[0], self.track[1])

            cr_1 = self.exact_intersection(indx-1, indx)
            cr_2 = self.exact_intersection(indx, indx+1)
            #print("crossing", crossing, cr_1, cr_2)

            if self.vector.y < 0:
                self.hit_type = "hit roof"
            else:
                self.hit_type = "hit floor"

            if self.hit_type == "hit floor" and not cr_1 and not cr_2:
                self.hit_type = "slide"

            if cr_1:
                self.surface_vector = Vector.make_vector(self, self.track[indx-1], self.track[indx])
            elif cr_2:
                self.surface_vector = Vector.make_vector(self, self.track[indx], self.track[indx + 1])

            #if self.surface_vector * self.vector < 0:
                #print(self.surface_vector * self.vector)
                #self.surface_vector = self.surface_vector * (-1)

            if self.hit_type == "hit floor":
                self.vector = self.vector.proj_on(self.surface_vector)
                self.vector += self.g.proj_on(self.surface_vector) * (t * self.time_speed)
            elif self.hit_type == "hit roof":
                self.vector = self.vector.proj_on(self.surface_vector)
                self.vector += self.g * (t * self.time_speed)
            elif self.hit_type == "slide":
                self.vector = self.vector.proj_on(self.surface_vector)
                self.vector += self.g.proj_on(self.surface_vector) * (t * self.time_speed)

            """if cr_1:
                self.surface_vector = Vector.make_vector(self, self.track[indx-1], self.track[indx])
                if self.surface_vector*self.vector < 0:
                    self.surface_vector = self.surface_vector*(-1)
                self.vector = self.vector.proj_on(self.surface_vector)
                if self.hit_type == "hit floor":
                    self.vector += self.g.proj_on(self.surface_vector) * (t * self.time_speed)
                self.x, self.y = cr_1[0], cr_1[1]
            elif cr_2:
                self.surface_vector = Vector.make_vector(self, self.track[indx], self.track[indx+1])
                if self.surface_vector*self.vector < 0:
                    self.surface_vector = self.surface_vector*(-1)
                self.vector = self.vector.proj_on(self.surface_vector)
                if self.hit_type == "hit floor":
                    self.vector += self.g.proj_on(self.surface_vector) * (t * self.time_speed)
                self.x, self.y = cr_2[0], cr_2[1]
            else:
                if self.hit_type != "hit roof":
                    self.hit_type = "slide"
                    self.surface_vector = Vector.make_vector(self, self.track[indx-1], self.track[indx])
                    if self.surface_vector*self.vector < 0:
                        self.surface_vector = self.surface_vector*(-1)
                    self.vector = self.vector.proj_on(self.surface_vector)
                    self.vector += self.g.proj_on(self.surface_vector) * (t * self.time_speed)
                else:
                    print("here")
                    self.surface_vector = Vector.make_vector(self, self.track[indx - 1], self.track[indx])
                    if self.surface_vector * self.vector < 0:
                        self.surface_vector = self.surface_vector * (-1)
                    self.vector = self.vector.proj_on(self.surface_vector)
                    self.vector += self.g * (t * self.time_speed)"""


            print(self.hit_type)

            self.x += self.vector.x
            self.y += self.vector.y

            #  should I stick to the line or not?

        else:
            #  free fall
            print("free fall")
            self.vector += self.g * (t * self.time_speed)
            self.x += self.vector.x
            self.y += self.vector.y

    def check_on_track(self):
        vector = self.vector
        if abs(vector) > 1:
            vector = vector.norm()
        len = 0
        x = self.x
        y = self.y
        x_hit = 0
        y_hit = 0
        hit = False
        while len < abs(self.vector):
            if x >= self.map.width() or y >= self.map.height():
                print("OUT", hit)
                self.x = self.x_initial
                self.y = self.y_initial
                self.vector = Vector(0, 0, 0)
                self.surface_vector = Vector.make_vector(self, self.track[0], self.track[1])
                self.start = time.time()
                hit = False
                break
            if self.map.pixel(x, y) != 0:
                hit = True
                x_hit = x
                y_hit = y
                return [x_hit, y_hit]
            if self.hit_type == "slide":
                for i in range(-10,-1):
                    y_t = y+i
                    if self.map.pixel(x, y_t) != 0:
                        hit = True
                        print("support")
                        x_hit = x
                        y_hit = y_t
                        self.y = y_t
                        return [x_hit, y_hit]
            x += vector.x
            y += vector.y
            len += 1
        if hit:
            return [x_hit, y_hit]
        return False

    def closest_node(self, node):
        closest_index = distance.cdist([node], self.track).argmin()
        return closest_index

    def exact_intersection(self, i, j):
        x1, y1 = self.x, self.y
        x2, y2 = self.x+self.vector.x, self.y+self.vector.y

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
