import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import math
import time
from Vector import Vector
import numpy as np
from scipy.spatial import distance


class Player:
    def __init__(self, x, y, pane):
        self.x = x
        self.y = y
        self.pane = pane
        self.layer = pane.ebene_schlitten
        self.painter = pane.painter_schlitten
        self.vector = Vector(0,1,0)
        self.color = qc.Qt.red
        self.g = Vector(0,9.8,0)
        self.start = time.time()
        self.map = pane.ebene_pane.toImage()
        self.track = pane.track
        self.surface_vector = Vector(0,0,0)
        self.time_direction = 1
        self.time_speed = 0.001  # 0.01 <=> 100-times slower
        self.time_control_point = time.time()
        self.hit_type = ""
        #print(pane.track)

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
        self.intersection()
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

    def intersection(self):
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.vector.x, self.y + self.vector.y

        X = [False,False]
        # create line equation as Ax+By+c=0
        A = y2-y1
        B = x1-x2
        C = x1*(y1-y2)+y1*(x2-x1)

        # now we have a line and we need fo figure out if it cross any of B.k
        # reform B.k formula to receive coefficients for t**3, t**2, t, t**0

        # TODO: B.k is made of 4 points, so if in 1 path there are multiple B.k, we need do run test multiple times
        bx = self.pane.bezier_coeffs(self.pane.current_cv, 0)
        by = self.pane.bezier_coeffs(self.pane.current_cv, 1)

        P = []
        P.append(A * bx[0] + B * by[0])
        P.append(A * bx[1] + B * by[1])
        P.append(A * bx[2] + B * by[2])
        P.append(A * bx[3] + B * by[3] + C)

        # now we need to solve a cubic equation
        def cubic_roots(P):
            a = P[0]
            b = P[1]
            c = P[2]
            d = P[3]

            A = b / a
            B = c / a
            C = d / a

            Q = (3 * B - A**2) / 9
            R = (9 * A * B - 27 * C - 2 * A**3) / 54
            D = Q**3 + R**2 # polynomial discriminant

            t = [False,False,False]

            if D >= 0:
                # complex or duplicate roots
                sgn_1 = 0
                sgn_2 = 0
                if R + math.sqrt(D)>0:
                    sgn_1=+1
                elif R + math.sqrt(D)>0:
                    sgn_1=-1
                else:
                    sgn_1=0

                if R - math.sqrt(D)>0:
                    sgn_2=+1
                elif R - math.sqrt(D)>0:
                    sgn_2=-1
                else:
                    sgn_2=0

                S = sgn_1 * abs(R + math.sqrt(D))**(1 / 3)
                T = sgn_2 * abs(R - math.sqrt(D))**(1 / 3)

                t[0] = -A / 3 + (S + T)  # real root
                t[1] = -A / 3 - (S + T) / 2  # real part of complex root
                t[2] = -A / 3 - (S + T) / 2  # real part of complex root
                Im = abs(math.sqrt(3) * (S - T) / 2)  # complex part of root pair

                # discard complex roots
                if Im != 0:
                    t[1] = -1
                    t[2] = -1
            else:
                # distinct real roots
                th = math.acos(R / math.sqrt(-math.pow(Q, 3)))

                t[0] = 2 * math.sqrt(-Q) * math.cos(th / 3) - A / 3
                t[1] = 2 * math.sqrt(-Q) * math.cos((th + 2 * math.pi) / 3) - A / 3
                t[2] = 2 * math.sqrt(-Q) * math.cos((th + 4 * math.pi) / 3) - A / 3
                Im = 0.0

            # discard out of spec roots
            for i in range(0,3):
                if t[i] < 0 or t[i] > 1.0:
                    t[i]=-1

            return t

        r = cubic_roots(P)

        print("before: ",r)
        # check if root suits to the line
        for i in range(3):
            t = r[i]
            if t and t != -1:
                X[0] = bx[0] * t ** 3 + bx[1] * t ** 2 + bx[2] * t + bx[3]
                X[1] = by[0] * t ** 3 + by[1] * t ** 2 + by[2] * t + by[3]

                if x2-x1 != 0: #  if not vertical
                    s = (X[0]-x1)/(x2-x1)
                else:
                    s = (X[1]-y1)/(y2-y1)
                print(s,"(", X[0],X[1],")")
                self.painter.setPen(qg.QPen(qc.Qt.white, 20, qc.Qt.SolidLine))
                self.painter.drawPoint(X[0],X[1])
                # between two points?
                if t<0 or t>1 or s<0 or s>1:
                    #no
                    r[i] = False

        print("after: ",r)



        # older paths
        #self.track = []
        #for i in range(len(self.cvs)):
            #self.pane.bezier(self.cvs[i])
