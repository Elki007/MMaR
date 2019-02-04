import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import time
from Vector import Vector
import numpy as np


class Player:
    def __init__(self, x, y, map_layer, track):
        self.x = x
        self.y = y
        self.vector = Vector(0,0,0)
        self.color = qc.Qt.red
        self.g = Vector(0,9.8,0)
        self.start = time.time()
        self.map = map_layer.toImage()
        self.track = track
        self.surface_vector = Vector(0,0,0)
        print(track)

    def show(self, layer, painter):
        '''
        draws a player on special layer
        :param surface_painter: layers painter
        :return: None
        '''
        layer.fill(qg.QColor(0, 0, 0, 0))
        painter.setPen(qg.QPen(self.color, 10, qc.Qt.SolidLine))
        painter.drawPoint(self.x, self.y)
        painter.setPen(qg.QPen(qc.Qt.white, 2, qc.Qt.SolidLine))
        painter.drawLine(self.x, self.y, self.x+self.vector.x*10, self.y+self.vector.y*10)

    def next(self):
        n = 100  # n-times slower
        t = time.time() - self.start

        if not self.check_on_track():
            self.vector += self.g * (t / n)
            self.x += self.vector.x
            self.y += self.vector.y
        else:
            self.vector += self.g.proj_on(self.surface_vector) * (t / n)
            print(self.vector.y)
            #self.vector.y = self.vector.y - 0.5
            self.x += self.vector.x
            self.y += self.vector.y

        #print(self.acceleration.proj_on(self.vector))
        #print(t)

    def check_on_track(self):
        vector = self.vector
        if abs(vector) > 1:
            vector = vector.norm()
        len = 0
        x = self.x
        y = self.y-1
        x_hit = 0
        y_hit = 0
        hit = False
        while len < abs(self.vector):
            if self.map.pixel(x, y) != 0:
                hit = True
                x_hit = x
                y_hit = y
            x += vector.x
            y += vector.y
            len += 1
        if hit:
            #print("HIT:",x_hit, y_hit)
            self.x = x_hit
            self.y = y_hit
            self.project_speed(y_hit)
            return True
        return False

    def argmin_values_along_axis(self, value, axis):
        arr = np.asarray(self.track)
        y_list = arr[:,axis]
        idx = (np.abs(y_list - value)).argmin()
        return idx

    def find_surface(self, value):
        indx = self.argmin_values_along_axis(value,1)
        return Vector.make_vector(self, self.track[indx-1], self.track[indx])

    def project_speed(self,y_hit):
        self.surface_vector = self.find_surface(y_hit)
        #print(type(self.vector))
        #print(type(surface_vector))
        self.vector = self.vector.proj_on(self.surface_vector)
        #print(type(self.vector))




