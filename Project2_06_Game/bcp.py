import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import time
from Vector import Vector
import numpy as np
from scipy.spatial import distance


class Player:
    def __init__(self, x, y, layer, painter, map_layer, track):
        self.x_initial = x
        self.y_initial = y
        self.x = x
        self.y = y
        self.layer = layer
        self.painter = painter
        self.vector = Vector(0, 0, 0)
        self.color = qc.Qt.red
        self.g = Vector(0, 9.8, 0)
        self.start = time.time()
        self.map = map_layer.toImage()
        self.track = track
        self.surface_vector = Vector(0, 0, 0)
        self.time_direction = 1
        self.time_speed = 0.1  # 0.01 <=> 100-times slower
        self.time_control_point = time.time()
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
        # self.painter.setPen(qg.QPen(qc.Qt.white, 2, qc.Qt.SolidLine))
        # self.painter.drawLine(self.x, self.y, self.x+self.vector.x*10, self.y+self.vector.y*10)

    def next(self):
        #  Time - control attempt
        if self.time_direction == 1:
            t = time.time() - self.start
        else:
            t = self.time_control_point - (time.time() - self.time_control_point)

        #  am I crossing smw?
        crossing = self.check_crossing()
        crossing2 = self.check_on_track()
        print("cross check: ", crossing, crossing2)

        if crossing2:
            # print("check:",self.check_on_track())
            #  should I stick to the line or not?
            if crossing:
                self.x = crossing[0]
                self.y = crossing[1]
                indx = self.closest_node(crossing)
            else:
                self.x = crossing2[0]
                self.y = crossing2[1]
                indx = self.closest_node(crossing2)

            self.painter.drawPoint(self.track[indx][0], self.track[indx][1])

            if self.point_self_on_a_line(indx, indx + 1):
                # print("i;i+1")
                surface_vector = Vector.make_vector(self, self.track[indx], self.track[indx + 1])
            elif self.point_self_on_a_line(indx - 1, indx):
                # print("i-1;i")
                surface_vector = Vector.make_vector(self, self.track[indx - 1], self.track[indx])
            else:
                print("\nWWWWWWWWWWTTTTTTTTTTTTFFFFFFFFFFFFFFFFFFFFFFF\n")

            # in self.track we doesnt have any direction, so we will make those vectors codirectional
            # if scalar > 0 - same direction
            if self.vector * surface_vector < 0:
                surface_vector = surface_vector * (-1)

            self.vector = self.vector.proj_on(surface_vector)
            self.vector += self.g.proj_on(surface_vector) * (t * self.time_speed)
            self.x += self.vector.x
            self.y += self.vector.y

            #  now we need to define surface vector for 2 cases (closest_node may return next or prev point)
            # print("coll at (index;index+1) ", self.point_self_on_a_line(indx, indx+1))
            # print("coll at (index-1;index) ", self.point_self_on_a_line(indx-1, indx))
            # delta_prev = Vector.make_vector(self, crossing, self.track[indx-1])
            # delta = Vector.make_vector(self, crossing, self.track[indx])
            # delta_next = Vector.make_vector(self, crossing, self.track[indx+1])
            # print(abs(delta))
            # self.surface_vector = Vector.make_vector(self, self.track[indx - 1], self.track[indx])

            # self.vector = self.vector.proj_on(self.surface_vector)
        else:
            #  free fall
            self.vector += self.g * (t * self.time_speed)
            self.x += self.vector.x
            self.y += self.vector.y

        """if not self.check_on_track():
            self.vector += self.g * (t * self.time_speed)
            self.x += self.vector.x
            self.y += self.vector.y
        else:
            self.vector = self.vector.proj_on(self.surface_vector)
            self.vector += self.g.proj_on(self.surface_vector) * (t * self.time_speed)
            #print(self.vector.y)
            #self.vector.y = self.vector.y - 0.5
            self.x += self.vector.x
            self.y += self.vector.y"""

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
        # another check on hit
        self.intersection_at()

        while len < abs(self.vector):
            if x >= self.map.width() or y >= self.map.height():
                print("OUT", hit)
                self.x = self.x_initial
                self.y = self.y_initial
                self.vector = Vector(0, 0, 0)
                self.start = time.time()
                hit = False
                break
            if self.map.pixel(x, y) != 0:
                hit = True
                x_hit = x
                y_hit = y
                break
            x += vector.x
            y += vector.y
            len += 1
        if hit:
            # print("HIT:",x_hit, y_hit)
            # self.x = x_hit
            # self.y = y_hit
            # self.y -= 1
            # self.surface_vector = self.find_surface_vector_2([x_hit, y_hit])
            # self.painter.drawLine(x_hit, y_hit, x_hit + self.surface_vector.x * 10, y_hit + self.surface_vector.y * 10)
            # self.closest_node([x_hit, y_hit])
            return [x_hit, y_hit]
        return False

    def argmin_values_along_axis(self, value, axis):
        arr = np.asarray(self.track)
        y_list = arr[:, axis]
        idx = (np.abs(y_list - value)).argmin()
        return idx

    def closest_node(self, node):
        closest_index = distance.cdist([node], self.track).argmin()
        return closest_index

    def find_surface_vector(self, value):
        indx = self.argmin_values_along_axis(value, 1)
        return Vector.make_vector(self, self.track[indx - 1], self.track[indx])

    def find_surface_vector_2(self, node):
        indx = self.closest_node(node)
        # indx = self.argmin_values_along_axis(value, 1)
        return Vector.make_vector(self, self.track[indx - 1], self.track[indx])

    def intersection_at(self):
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.vector.x, self.y + self.vector.y

        indx = self.closest_node([x1, y1])
        if indx >= len(self.track) - 1:
            return False

        x3, y3 = self.track[indx][0], self.track[indx][1]
        x4, y4 = self.track[indx + 1][0], self.track[indx + 1][1]

        denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        if denominator == 0:
            return False

        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

        if ua < 0 or ua > 1 or ub < 0 or ub > 1:
            return False

        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)

        print(x, y)

    def intersection_at_v2(self, a, b):
        x1, y1, x2, y2 = a[0], a[1], a[2], a[3]

        indx = self.closest_node([x1, y1])
        if indx >= len(self.track) - 1:
            return False

        x3, y3, x4, y4 = b[0], b[1], b[2], b[3]

        denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        if denominator == 0:
            return False

        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

        if ua < 0 or ua > 1 or ub < 0 or ub > 1:
            return False

        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)

        v_1 = Vector.make_vector(self, [x1, y1], [x2, y2])
        v_2 = Vector.make_vector(self, [x3, y3], [x4, y4])
        print(v_1.cos(v_2))
        print(f"collision at ({x, y})")
        return [x, y]

    def check_crossing(self):
        speed_interval = [self.x, self.y, self.x + self.vector.x, self.y + self.vector.y]  # (x1,y1,x2,y2)
        self.painter.setPen(qg.QPen(qc.Qt.white, 2, qc.Qt.DashDotDotLine))
        self.painter.drawLine(self.x, self.y, self.x + self.vector.x, self.y + self.vector.y)
        nearest_1 = self.closest_node([self.x, self.y])
        nearest_2 = self.closest_node([self.x + self.vector.x, self.y + self.vector.y])

        self.painter.setPen(qg.QPen(qc.Qt.yellow, 4, qc.Qt.SolidLine))
        self.painter.drawPoint(self.track[nearest_1][0], self.track[nearest_1][1])
        self.painter.drawPoint(self.track[nearest_2][0], self.track[nearest_2][1])

        surface_interval = [self.track[nearest_1][0], self.track[nearest_1][1], self.track[nearest_2][0],
                            self.track[nearest_2][1]]

        res = self.intersection_at_v2(speed_interval, surface_interval)
        if res:
            return res
        return False

    def check_crossing_img(self):
        x1, y1, x2, y2 = int(self.x), int(self.y), int(self.x + self.vector.x), int(self.y + self.vector.y)
        x_step = -1
        y_step = -1
        x_temp, y_temp = x2, y2
        x_max, y_max = x1, y1
        hit = False
        if x2 - x1 > 0:
            x_step = 1
            x_temp = x1
            x_max = x2
        if y2 - y1 > 0:
            y_step = 1
            y_temp = y1
            y_max = y1

        while x_temp < x_max and y_temp < y_max:
            if self.map.pixel(x_temp, y_temp) != 0:
                hit = True
                break
            x_temp += x_step
            y_temp += y_step
        return hit

    def point_self_on_a_line(self, i, j):
        dxc = self.x - self.track[i][0]
        dyc = self.y - self.track[i][1]

        dxl = self.track[j][0] - self.track[i][0]
        dyl = self.track[j][1] - self.track[i][1]

        cross = dxc * dyl - dyc * dxl
        if cross <= 1:
            return True
        return False

    def nearest_is_greater(self, i):
        x = self.x
        y = self.y
        x1, y1 = self.track[i].x, self.track[i].y
