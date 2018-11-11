import math

class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z)+")"

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y)+ "," + str(self.z)+")"

    def make_vector(self, another_Point3D):
        return Point3D(another_Point3D.x-self.x,another_Point3D.y-self.y,another_Point3D.z-self.z)

    def abs(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def scalar(self,other):
        return other.x*self.x + other.y*self.y + other.z*self.z

    def angle(self, other):
        cos = self.scalar(other) / (self.abs() * other.abs())
        ang = math.acos(cos)
        deg = math.degrees(ang)
        if deg > 90:
            deg = 180 - deg
        return deg

    def __mul__(self, another_Point3D):
        # calculate determinant
        i = self.y*another_Point3D.z - (self.z*another_Point3D.y)
        j = -self.x*another_Point3D.z + (self.z*another_Point3D.x)
        k = self.x*another_Point3D.y - (self.y*another_Point3D.x)
        return Point3D(i,j,k)


    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, zoom, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        #if viewer_distance + self.z == 0:
            #return Point3D(self.x, -self.y, self.z)
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor*zoom + win_width # / 2
        y = -self.y * factor*zoom + win_height # / 2
        return Point3D(x, y, self.z*zoom)