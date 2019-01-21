import matplotlib.pyplot as plt
import numpy as np


def p_1(t):
    return 1/6 * t**3
def p_2(t):
    return 1/6*(1 + 3*t + 3*t**2 - 3*t**3)
def p_3(t):
    return 1/6*(4 - 6*t**2 + 3*t**3)
def p_4(t):
    return 1/6*(1 - 3*t + 3*t**2 - t**3)

def b(t):
    if t <= 0:
        return 0
    elif t <= 1:
        return p_1(t)
    elif t <= 2:
        return p_2(t-1)
    elif t <= 3:
        return p_3(t-2)
    elif t <= 4:
        return p_4(t-3)
    else:
        return 0

def b_sp(t,i):
    return b(t-i)

def show_b_t():
    x = np.linspace(0, 4, 100)
    y = [b(each) for each in x]
    plt.plot(x, y, label="Basis function b(t)")
    plt.legend()
    plt.show()

def show_b_sp(interval_for_i):
    x = np.linspace(0, 6, 100)
    y = []
    for i in range(interval_for_i[0],interval_for_i[1]+1):
        y.append([b_sp(each,i) for each in x])
        plt.plot(x, y[-1], label=str("Basis function b(t-i), i=")+str(i))
    plt.title("Basisfunktionen", fontdict=None, loc='center')
    fig = plt.gcf()
    fig.canvas.set_window_title('Aufgabe 1a: Spline Kurven')
    plt.legend()
    plt.show()

show_b_sp([-2,6])
