import numpy as np
import matplotlib.pyplot as plt

# x- und y-Koordinaten

"""
X = [8,1,1,8,8,4]
Y = [8,8,1,1,4,4]
"""

"""
X = np.linspace(0,10, 250)
Y = np.cos(X)*np.cos(2*X)+np.sin(X)
"""

"""
t = np.linspace(0, 100, 2500)

# Parametrische Kurve.
a = np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12) ** 5
X = np.sin(t) * a
Y = np.cos(t) * a
"""



# Zeichnen und Anzeige
plt.plot(X, Y)
plt.show()