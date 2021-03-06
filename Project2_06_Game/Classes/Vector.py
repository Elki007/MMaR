import math
import numpy as np


class Vector:

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def make_vector(self,a,b):
        return Vector(b[0]-a[0],b[1]-a[1],0)

    def __str__(self):
        return "<" + str(self.x) + " " + str(self.y) + ">"  # " " + str(self.z) + ">"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if (type(self) == type(other)):
            #print("dealing with vectors")
            # scalar
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            #print("dealing with numbers")
            return Vector(self.x * other, self.y * other, self.z * other)

    def __imul__(self, number):
        if isinstance(number, (int, float)):
            self.x *= number
            self.y *= number
            self.z *= number
            return self
        else:
            raise ValueError(f"You used {type(number)} instead int or float.")

    def __truediv__(self, number):
        if isinstance(number, (int, float)):
            if number == 0:
                print("Pay Attention, you would've divided through 0!")
            return Vector(self.x / number, self.y / number, self.z / number)
        else:
            raise ValueError(f"You used {type(number)} instead int or float.")

    def __itruediv__(self, number):
        if isinstance(number, (int, float)):
            if number != 0:
                self.x /= number
                self.y /= number
                self.z /= number
            else:
                print("Pay Attention, you would've divided through 0!")
            return self
        else:
            raise ValueError(f"You used {type(number)} instead int or float.")

    def proj_on_x(self):
        return Vector(self.x,0,0)
    def proj_on_y(self):
        return Vector(0,self.y,0)
    def proj_on_z(self):
        return Vector(0,0,self.z)

    def proj_on(self,other):
        if (type(self) == type(other)):
            top = self*other
            bottom = abs(other)**2
            #print(type(other), type (top/bottom),type(5),type(5.0))
            return other * (top/bottom)

    def norm(self):
        if abs(self) != 0:
            return Vector(self.x/abs(self), self.y/abs(self), self.z/abs(self))
        return self

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y *self.y + self.z *self.z)

    def cos(self, other):
        """
        :param other: vector
        :return: value of cos(self,other)
        """
        if (type(self) == type(other)):
            return (self*other)/(abs(self)*abs(other))

    def rotate(self, angle):
        theta = angle*math.pi/180
        cs = math.cos(theta)
        sn = math.sin(theta)

        return Vector(self.x*cs-self.y*sn,self.x*sn+self.y*cs,0)

    def angle(self, other):
        ang1 = np.arctan2(self.x,other.x)
        ang2 = np.arctan2(self.y,other.y)
        return (ang2-ang1)%(2*np.pi)

    def reflect(self, surface):
        if (type(self) == type(surface)):
            n = surface.rotate(90).norm()
            #print(n*surface)
            temp = self*n
            r = self - n * 2 * temp
            #print(r)
            return r

    def __pow__(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

