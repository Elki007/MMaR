import math
class Vector:

    def __init__(self, x, y, z):
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
        return Vector(self.x/abs(self), self.y/abs(self), self.z/abs(self))


    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y *self.y + self.z *self.z)

    def cos(self, other):
        """
        :param other: vector
        :return: value of cos(self,other)
        """
        if (type(self) == type(other)):
            return (self*other)/(abs(self)*abs(other))

    def __pow__(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

