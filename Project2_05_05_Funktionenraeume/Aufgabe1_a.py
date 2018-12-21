import matplotlib.pyplot as plt
import numpy as np

### Teil a ###

def show_basis(x):
    y0 = 0.564*np.exp(-(x-0)**2)
    y1 = 0.564*np.exp(-(x-1)**2)
    y2 = 0.564*np.exp(-(x-2)**2)
    y3 = 0.564*np.exp(-(x-3)**2)
    y4 = 0.564*np.exp(-(x-4)**2)
    y5 = 0.564*np.exp(-(x-5)**2)
    y6 = 0.564*np.exp(-(x-6)**2)

    plt.plot(x,y0, 'red', label="t-0")
    plt.plot(x,y1, 'green', label="t-1")
    plt.plot(x,y2, 'blue', label="t-2")
    plt.plot(x,y3, 'black', label="t-3")
    plt.plot(x,y4, 'purple', label="t-4")
    plt.plot(x,y5, 'c', label="t-5")
    plt.plot(x,y6, 'yellow', label="t-6")
    plt.legend()
    plt.show()

def p1(x):
    return 1/6*np.power(x,3)
def p2(x):
    return 1/6*(1+3*x+3*x**2-3*x**3)
def p3(x):
    return 1/6*(4-6*x**2+3*x**3)
def p4(x):
    return 1/6*(1-3*x+3*x**2-x**3)
def basis_f(x):
    if x<=0:
        return 0
    elif x<=1:
        return p1(x)
    elif x<=2:
        return p2(x-1)
    elif x<=3:
        return p3(x-2)
    elif x<=4:
        return p4(x-3)
    else:
        return 0

def show_b_t(x):
    y = [basis_f(each) for each in x]
    plt.plot(x, y, label="Basis function b(t)")
    plt.legend()
    plt.show()


x = np.linspace(0, 6, 100)
show_basis(x)
show_b_t(x)

"""points = np.array([[0,0],[0,0],[0,0],[0,0],[0,0]])
points2 = np.array([[0,0.1],[0.2,0.3],[0.4,0.04],[0.6,0.7],[1,0]])


def f_x(x,points):
    x_result = 0
    for k in range(len(points)):
        x_result += points[k][0]*basis_f(x)
    return x_result

def f_y(x,points):
    y_result = 0
    for k in range(len(points)):
        sub = points[k][1]*basis_f(x)
        #print("sub: ",sub)
        y_result += sub
    print("end: ",y_result)
    return y_result

x = np.linspace(0, 1, 100)

xx = [f_x(each, points2) for each in x]
yy = [f_y(each, points2) for each in x]
print(xx)
print(yy)
plt.plot(xx, yy, 'red')

#x = [f_x(each,points2) for each in x]
#y = [f_y(each,points2) for each in x]
#plt.plot(x,y,'blue')

#x_list = [x for [x, y] in points]
#y_list = [y for [x, y] in points]
#plt.plot(x_list,y_list,'ro')
x_list = [x for [x, y] in points2]
y_list = [y for [x, y] in points2]
plt.plot(x_list,y_list,'bo')

plt.show()"""