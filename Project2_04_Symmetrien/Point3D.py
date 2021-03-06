import math


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z)+")"

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y)+ "," + str(self.z)+")"

    def __neg__(self):
        return Point3D(-self.x, -self.y, -self.z)

    '''
    def __mul__(self, other):
        """ multiplicates every coordinate with a factor """
        return Point3D(self.x * other.x, self.y * other.y, self.z * other.z)
    '''

    def __mul__(self, factor):
        """ multiplicates every coordinate with a factor """
        return Point3D(self.x * factor, self.y * factor, self.z * factor)

    def make_vector(self, other):
        """ creates vector of 2 Point3Ds """
        return Point3D(other.x-self.x, other.y-self.y, other.z-self.z)

    def norm(self):
        return Point3D(self.x/self.abs(), self.y/self.abs(), self.z/self.abs())

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
        #print(deg)
        return deg

    def __add__(self, other):
        return Point3D(other.x+self.x, other.y+self.y, other.z+self.z)

    """
    # was commentized because of other __mul__()-function -> to multiply with a factor
    def __mul__(self, other):
        # calculate determinant
        i = self.y*other.z - (self.z*other.y)
        j = -self.x*other.z + (self.z*other.x)
        k = self.x*other.y - (self.y*other.x)
        return Point3D(i,j,k)
    """

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
        y = -self.y * factor*zoom + win_height # /
        return Point3D(x, y, self.z)
