import numpy
import matplotlib.pyplot as plt

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

def func(x, offset):
    out = numpy.ndarray((len(x)))
    print(x)
    for i, v in enumerate(x):
        # i - index
        # v - value
        # means for all x - es get index and value of x
        s = v - offset

        if s >= 0 and s < 1:
            out[i] = s * s / 2.0
        elif s >= 1 and s < 2:
            out[i] = 3.0 / 4.0 - (s - 3.0 / 2.0) * (s - 3.0 / 2.0)
        elif s >= 2 and s < 3:
            out[i] = (s - 3.0) * (s - 3.0) / 2.0
        else:
            out[i] = 0.0

    return out

# We have 7 things to fit, so let do 7 basis functions?
y = numpy.array([0, 2, 3, 0, 3, 2, 0])

# We need enough x points for all the basis functions... That why the weird linspace max here
x = numpy.linspace(0, len(y) + 2, 100)

B = numpy.ndarray((len(x), len(y)))

for k in range(len(y)):
    B[:, k] = func(x, k)

plt.plot(x, B.dot(y), label="B-spline")
# The x values in the next statement are the maximums of each basis function. I'm not sure at all this is right
plt.plot(numpy.array(range(len(y))) + 1.5, y, '-o', label="Control points")
plt.legend()
plt.show()

for k in range(len(y)):
    plt.plot(x, B[:, k])
plt.title('Basis functions')
plt.show()