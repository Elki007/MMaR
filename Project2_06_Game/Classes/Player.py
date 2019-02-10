import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import math
import time
from Vector import Vector
import numpy as np
from scipy.spatial import distance


class Player:
    def __init__(self, x, y, pane, gui):
        self.gui = gui
        self.x = x
        self.y = y
        self.pane = pane
        self.layer = pane.ebene_schlitten
        self.painter = pane.painter_schlitten
        self.paths = pane.paths
        self.vector = Vector(0,1,0)
        self.color = qc.Qt.red
        self.g = Vector(0,9.8,0)
        self.start = time.time()
        self.time_speed = 0.01  # 0.01 <=> 100-times slower
        #print(type(self.paths.list_of_paths), len(self.paths.list_of_paths), self.paths.list_of_paths[0].plotted_points)
        #print(self.intersection_with_array_test([4,1.5],Vector(0,-2.5),[[0,4],[3,1],[5,2]]))

    def show(self):
        '''
        draws a player on special layer
        :param surface_painter: layers painter
        :return: None
        '''
        self.layer.fill(qg.QColor(0, 0, 0, 0))
        self.painter.setPen(qg.QPen(self.color, 10, qc.Qt.SolidLine))
        #self.painter.drawPoint(self.x, self.y)
        #  draw vector
        self.painter.setPen(qg.QPen(qc.Qt.green, 2, qc.Qt.SolidLine))
        self.painter.drawLine(self.x, self.y, self.x+self.vector.x, self.y+self.vector.y)

    def next(self):
        t = time.time() - self.start

        intersection = self.intersection_by_plotted()
        if intersection:
            dummy, path_type = intersection
            at, a, b = dummy
            aa = Vector.make_vector(Vector, [self.x, self.y], a)
            bb = Vector.make_vector(Vector, [self.x, self.y], b)
            #if self.vector.cos(aa) * self.vector.cos(bb) > 0:
                #print("COSINUS - check not passed!")

            surface = Vector.make_vector(Vector,a,b)
            self.painter.setPen(qg.QPen(qc.Qt.red, 4, qc.Qt.SolidLine))
            self.painter.drawLine(a[0], a[1], b[0], b[1])

            cos = self.vector.cos(surface)
            if cos < 0:
                # prbbl not really needed :)
                #print("Surface correction")
                surface = surface * (-1)

            if surface.x>0 and surface.y>0:
                surface_quarter = 1
            elif surface.x<0 and surface.y>0:
                surface_quarter = 2
            elif surface.x<0 and surface.y<0:
                surface_quarter = 3
            else:
                surface_quarter = 4

            # was player below / above the line:
            #p1 = a if a[0] > b[0] else b
            #p2 = b if a[0] > b[0] else a
            # line equation:
            #p1 = a
            #p2 = [a[0] + surface.x, a[1] + surface.y]
            #det = (p1[0]-self.x)*(p2[1]-self.y)-(p1[1]-self.y)*(p2[0]-self.x)
            #print(det)
            # another try:
            m = (a[1]-b[1])/(a[0]-b[0])
            if self.y > m*self.x + (a[1]-m*a[0]):
                hit_type = "hit_roof"
            else:
                hit_type = "hit_floor"

            #print("hit:", hit_type, surface_quarter)

            #print("tst", abs(cos), abs(self.vector))
            if abs(cos) > 0.7 or abs(self.vector)<4:
                #print("slide")
                # angle is not enough to reflect, so just project it
                # may opinion: if we'll always reflect a vector, point will "shake"
                # set actual coordinates to a cross point
                self.x, self.y = at[0], at[1]
                #print(path_type)
                if path_type == "speed up":
                    if self.vector.proj_on(surface)*self.g > 0 :
                        # acceleration
                        #print("acc")
                        self.vector = self.vector.proj_on(surface)
                        self.vector += self.g.proj_on(surface) * 1.2 * self.time_speed
                    else:
                        # breaking
                        #if self.vector.y > -2:
                        #    self.vector *= 1.2
                        self.vector = self.vector.proj_on(surface)
                        #b = ((self.g * (-1)).proj_on(surface) * self.time_speed).norm()*0.5
                        coeff = abs(Vector(1,0).cos(self.vector))
                        #print("brk", self.vector, coeff)
                        if abs(self.vector) < 10 / (2-coeff):
                            self.vector += self.vector*coeff
                        #print("after", abs(self.vector))
                elif path_type == "slow down":
                    self.vector = self.vector.proj_on(surface)
                    self.vector += self.g.proj_on(surface) * self.time_speed
                    self.vector *= 0.9
                else:
                    self.vector = self.vector.proj_on(surface)
                    self.vector += self.g.proj_on(surface) * self.time_speed

                # normal vector to surface:
                # warning # reflection depends on self.vector.x
                if hit_type == "hit_floor":
                    if surface_quarter == 1 or surface_quarter == 4:
                        norm = Vector(surface.y, -surface.x)
                    else:
                        norm = Vector(-surface.y, surface.x)
                else:
                    if surface_quarter == 1 or surface_quarter == 4:
                        norm = Vector(-surface.y, surface.x)
                    else:
                        norm = Vector(surface.y, -surface.x)
                norm = norm.norm() * 3
                self.x, self.y = self.x + norm.x, self.y + norm.y

            else:
                #reflecting part
                #print("reflecting")
                self.x, self.y = at[0], at[1]
                before = self.vector
                self.vector = self.vector.reflect(surface)*0.3
                if path_type == "speed up":
                    self.vector *= 1.3
                elif path_type == "slow down":
                    self.vector *= 0.7

                after = self.vector*2
                # normal vector to surface:
                # warning # reflection depends on self.vector.x and hit_floor/roof ?
                if hit_type == "hit_floor":
                    if surface_quarter == 1 or surface_quarter == 4:
                        norm = Vector(surface.y, -surface.x)
                    else:
                        norm = Vector(-surface.y, surface.x)
                else:
                    if surface_quarter == 1 or surface_quarter == 4:
                        norm = Vector(-surface.y, surface.x)
                    else:
                        norm = Vector(surface.y, -surface.x)

                norm = norm.norm() * 3
                self.x, self.y = self.x + norm.x, self.y + norm.y
                # check if stopped
                if hit_type == "hit_floor" and before.cos(after) < -0.999 and self.vector.x*2 < 0.001:
                    print("calm")
                    self.vector = Vector(0, 0)
                    self.g = Vector(0, 0)
        else:
            # free fall part
            self.x, self.y = self.x + self.vector.x, self.y + self.vector.y
            self.vector += self.g * self.time_speed  # *  t

    def closest_node2(self, node, where):
        closest_index = distance.cdist([node], where).argmin()
        return closest_index

    def intersection(self, x1, y1, x2, y2):
        # old Version!!!
        x_correction = 0
        y_correction = 0
        special = ""
        def line_eq(x1, y1, x2, y2):
            if x2 - x1 == 0:
                return False, False
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1

            return m, b

        #x1, y1 = self.x, self.y
        #x2, y2 = self.x + self.vector.x, self.y + self.vector.y

        four_points = self.pane.paths[-1]

        X = [False,False]
        # create line equation as Ax+By+c=0
        A = y2-y1
        B = x1-x2
        C = x1*(y1-y2)+y1*(x2-x1)

        # now we have a line and we need fo figure out if it cross any of B.k
        # reform B.k formula to receive coefficients for t**3, t**2, t, t**0

        # TODO: B.k is made of 4 points, so if in 1 path there are multiple B.k, we need do run test multiple times
        bx = self.pane.bezier_coeffs(four_points, 0)
        by = self.pane.bezier_coeffs(four_points, 1)

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

        #print("before: ",r)
        # check if root suits to the line
        result = []
        result_t = []
        for i in range(3):
            t = r[i]
            if t and t != -1:
                X[0] = bx[0] * t ** 3 + bx[1] * t ** 2 + bx[2] * t + bx[3]
                X[1] = by[0] * t ** 3 + by[1] * t ** 2 + by[2] * t + by[3]

                if x2-x1 != 0: #  if not vertical
                    s = (X[0]-x1)/(x2-x1)
                else:
                    s = (X[1]-y1)/(y2-y1)
                #print(s,"(", X[0],X[1],")")
                self.painter.setPen(qg.QPen(qc.Qt.white, 2, qc.Qt.SolidLine))
                if not np.isnan(X[0]):
                    self.painter.drawPoint(X[0],X[1])

                # between two points?
                """if x1 > x2:
                    x_max, x_min = x1, x2
                else:
                    x_max, x_min = x2, x1
                if y1 > y2:
                    y_max, y_min = y1, y2
                else:
                    y_max, y_min = y2, y1
                if X[0] < x_max + 5 and X[0] > x_min - 5 and X[1] < y_max + 5 and X[1] > y_min - 5:
                    result.append([X[0], X[1]])
                    result_t.append(t)"""

                # smoller and in same direction looking:
                abstand = Vector.make_vector(Vector,[x1, y1],[X[0], X[1]])
                """"while abs(abstand) < 0.5:
                    x_correction, y_correction = - self.vector.x*0.2, - self.vector.y*0.2
                    abstand = Vector.make_vector(Vector, [x1 + x_correction, y1 + y_correction], [X[0], X[1]])"""
                if abs(abstand) <= abs(self.vector):
                    if abstand*self.vector >= 0:
                        result.append([X[0], X[1]])
                        result_t.append(t)
                    else:
                        if not self.math_reflected_before:
                            # cos is the answer!
                            x = self.pane.bezier_diff(four_points, t, 0)
                            y = self.pane.bezier_diff(four_points, t, 1)
                            s = self.vector.reflect(Vector(x,y))*0.5
                            if self.vector.cos(s) < -0.9999:
                                #print("!!!!!!!\nI should stay calm\n!!!!!!!")
                                if abs(self.vector) <1:
                                    special = "calm"
                            else:
                                special = "slide"
                            """print("reflected before: ", self.math_reflected_before)
                            print("abstand:", abstand, "self.vector:", self.vector)
                            print("scalar =", abstand * self.vector, "  |abstand|=", abs(abstand), "  |v|=",
                                  abs(self.vector),
                                  "cos:", self.vector.cos(abstand), "cos2:", self.vector.cos(s))
                            print("reflected v:", s, "  |s|=",abs(s))
                            print("r: ",r)
                            print(f"self:{x1, y1}")
                            print(f"X: ({X[0],X[1]})")
                            self.layer.fill((qg.QColor(0, 0, 0, 0)))
                            self.painter.setPen(qg.QPen(qc.Qt.green, 2, qc.Qt.SolidLine))
                            self.painter.drawLine(x1, y1, x1 + self.vector.x, y1 + self.vector.y)
                            self.painter.setPen(qg.QPen(qc.Qt.white, 2, qc.Qt.SolidLine))
                            self.painter.drawPoint(X[0], X[1])
                            self.painter.setPen(qg.QPen(qc.Qt.red, 2, qc.Qt.SolidLine))
                            self.painter.drawPoint(x1, y1)"""

                            result.append([X[0], X[1]])
                            result_t.append(t)

                            #self.gui.on_click_play_pause()


                """m,b = line_eq(x1,y1,x2,y2)
    
                on_the_line = False
                if m:
                    #print("check: ",X[1], m*X[0]+b)
                    # TODO: check pixel-wise find f'(t) at x,y position
                    # try 3
                    #if abs(self.x -X[0]) < 5 and abs(self.y-X[1]<5):
                        #on_the_line = True
                    #try 2
                    dxc = X[0] - round(x1)
                    dyc = X[1] - round(y1)
    
                    dxl = round(x2) - round(x1)
                    dyl = round(y2) - round(y1)
                    cross = dxc * dyl - dyc * dxl
                    # try 1
                    print(abs(X[1] - m*X[0]+b),cross)
                    if abs(cross)<1:
                        on_the_line = True
                    if abs(X[1] - m*X[0]+b) < 0.01:
                        on_the_line = True
                else:
                    #print("check: ", X[0], x1)
                    if abs(X[0] - x1) < 0.01:
                        on_the_line = True
    
                if on_the_line:
                    if x1>x2: x_max, x_min = x1, x2
                    else: x_max, x_min = x2, x1
                    if y1>y2: y_max, y_min = y1, y2
                    else: y_max, y_min = y2, y1
                    if X[0]< x_max+5 and X[0]>x_min-5 and X[1]<y_max+5 and X[1]>y_min-5:
                        result.append([X[0], X[1]])
                        result_t.append(t)"""
                """if t<0 or t>1 or s<0 or s>1:
                    #no
                    r[i] = False"""

        # if there are many intersections along self.vector, we'll choose the closest one
        if result:
            #print(result)
            closest_index = self.closest_node2([self.x, self.y], result)
            x = self.pane.bezier_diff(four_points, result_t[closest_index], 0)
            y = self.pane.bezier_diff(four_points, result_t[closest_index], 1)
            #  (x,y) is a slope vector!
            # TODO: return type may be ust vector of the surface? no, also x,y
            #print("cross point: ",result[closest_index])
            return result[closest_index], Vector(x, y), special  # hit point and surface vector
        return False




        # older paths
        #self.track = []
        #for i in range(len(self.cvs)):
            #self.pane.bezier(self.cvs[i])

    def intersection_by_plotted(self):
        amount = len(self.paths.list_of_paths)
        for n in range(amount):
            res = self.intersection_with_array(self.paths.list_of_paths[n])
            if res:
                return res, self.paths.list_of_paths[n].path_type
        return False

    def intersection_with_array(self, arr):
        arr = arr.plotted_points
        player = [self.x, self.y]
        player_next = [self.x + self.vector.x, self.y + self.vector.y]
        temp_arr = arr
        if len(arr)>1:
            p1_i = self.closest_node2(player, arr)
            temp_arr = np.delete(temp_arr, p1_i, axis=0)
            extra_points = 0
            p2_i = self.closest_node2(player_next, temp_arr)
            while arr[p1_i][0] == temp_arr[p2_i][0] and arr[p1_i][1] == temp_arr[p2_i][1]:
                temp_arr = np.delete(temp_arr, p2_i, axis=0)
                extra_points += 1
            abst1 = Vector.make_vector(Vector,player,temp_arr[p2_i])

            # make sure that another point > self.vector
            while abs(abst1) < abs(self.vector):
                temp_arr = np.delete(temp_arr, p2_i, axis=0)
                extra_points += 1
                p2_i = self.closest_node2(player_next, temp_arr)
                abst1 = Vector.make_vector(Vector, player, temp_arr[p2_i])

            if p2_i >= p1_i:
                p2_i += 1+extra_points

            #
            if abs(p1_i-p2_i) > len(arr)-10: # difference in 10 is allowed
                #print("first and last")
                return False

            x1,y1 = player[0], player[1]
            x2,y2 = player_next[0], player_next[1]
            x3,y3 = arr[p1_i][0],arr[p1_i][1]
            x4,y4 = arr[p2_i][0],arr[p2_i][1]
            # show found points at B.k
            self.painter.setPen(qg.QPen(qc.Qt.blue, 4, qc.Qt.SolidLine))
            self.painter.drawPoint(x3, y3)
            self.painter.drawPoint(x4, y4)
            #print(arr[p1_i], arr[p2_i])

            x_max = x3 if x3 > x4 else x4
            x_min = x4 if x3 > x4 else x3
            dx = x_max-x_min if x_max-x_min < 5 else 5
            x_max, x_min = x_max+dx, x_min-dx

            y_max = y3 if y3 > y4 else y4
            y_min = y4 if y3 > y4 else y3
            dy = y_max-y_min if y_max-y_min < 5 else 5
            y_max,y_min = y_max+dy,y_min-dy

            X = [False,False]
            X[0] =((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1))/((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            X[1] =((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1))/((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))

            abstand = Vector.make_vector(Vector,player,X)
            #print(self.vector * abstand, " |a|:",abs(abstand), " |v|:", abs(self.vector), (self.vector * abstand >= 0 and abs(abstand) <= abs(self.vector* 1.2)),
                  #X[0]>=x_min and X[0]<=x_max and X[1] >=y_min and X[1]<=y_max)
            # checks if cross point enough close to player
            if self.vector * abstand >= 0 and abs(abstand) <= abs(self.vector * 1.2):
                # checks if cross point between a, b
                #print(f"X:{X}, intervals: x:[{x_min,x_max}], y:[{y_min,y_max}]")
                if X[0]>=x_min and X[0]<=x_max and X[1] >=y_min and X[1]<=y_max:
                    self.painter.setPen(qg.QPen(qc.Qt.blue, 4, qc.Qt.SolidLine))
                    self.painter.drawPoint(X[0], X[1])
                    #aa = Vector.make_vector(Vector, [self.x, self.y], arr[p1_i])
                    #bb = Vector.make_vector(Vector, [self.x, self.y], arr[p2_i])
                    #if self.vector.cos(aa) * self.vector.cos(bb) > 0:
                        #print("COSINUS - check not passed!")
                        #return False
                    return X, arr[p1_i], arr[p2_i]
            return False

    def intersection_with_array_test(self, point, speed, arr):
        #arr = arr.plotted_points
        player = point
        player_next = [player[0] + speed.x, player[1] + speed.y]
        temp_arr = arr
        if len(arr)>1:
            p1_i = self.closest_node2(player, arr)
            #print(temp_arr)
            temp_arr = np.delete(temp_arr, p1_i, axis=0)
            #print(temp_arr)
            p2_i = self.closest_node2(player, temp_arr)
            #print(arr[p1_i] , temp_arr[p2_i])
            if p2_i >= p1_i:
                p2_i += 1

            x1,y1 = player[0], player[1]
            x2,y2 = player_next[0], player_next[1]
            x3,y3 = arr[p1_i][0],arr[p1_i][1]
            x4,y4 = arr[p2_i][0],arr[p2_i][1]
            X = [False,False]
            X[0] =((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1))/((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            X[1] =((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1))/((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))

            abstand = Vector.make_vector(Vector,player,X)
            #print(self.vector * abstand, " |a|:",abs(abstand), " |v|:",abs(self.vector), (self.vector * abstand >= 0 and abs(abstand) <= abs(self.vector)))
            if speed * abstand >= 0 and abs(abstand) <= abs(speed):
                return X, arr[p1_i], arr[p2_i]
            return False
