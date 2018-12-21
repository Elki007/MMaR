import matplotlib.pyplot as plt
import numpy as np

### Teil b ###
'''all functions should be splitted into 1-D functions'''
def p1_y(x):
    return 1/6*np.power(x,3)
def p2_y(x):
    return 1/6*(1+3*x+3*x**2-3*x**3)
def p3_y(x):
    return 1/6*(4-6*x**2+3*x**3)
def p4_y(x):
    return 1/6*(1-3*x+3*x**2-x**3)
def p1_x(x):
    return x
def p2_x(x):
    return x
def p3_x(x):
    return x
def p4_x(x):
    return x

def basis_f_y(x):
    if x<=0:
        return 0
    elif x<=1:
        return p1_y(x)
    elif x<=2:
        return p2_y(x-1)
    elif x<=3:
        return p3_y(x-2)
    elif x<=4:
        return p4_y(x-3)
    else:
        return 0

def basis_f_x(x):
    return x

def f_x(x,points):
    x_result = 0
    for k in range(len(points)):
        x_result += points[k][0]*basis_f_x(x)
    return x_result

def f_y(x,points):
    y_result = 0
    for k in range(len(points)):
        sub = points[k][1]*basis_f_y(x)
        #print("sub: ",sub)
        y_result += sub
    print("end: ",y_result)
    return y_result

x = np.linspace(0, 6, 100)
points2 = np.array([[0,0.1],[0.2,0.3],[0.4,0.04],[0.6,0.7],[1,0]])

xx = [f_x(each, points2) for each in x]
yy = [f_y(each, points2) for each in x]
plt.plot(xx, yy, 'red')

x_list = [x for [x, y] in points2]
y_list = [y for [x, y] in points2]
plt.plot(x_list,y_list,'ro')
plt.show()
