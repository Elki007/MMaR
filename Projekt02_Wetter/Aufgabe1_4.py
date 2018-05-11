import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
# from PyQt5 import QtCore as qc

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

class PlotWindow(qw.QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        # das Diagramm auf dem wir zeichnen
        self.figure, self.axis = plt.subplots()
        self.setWindowTitle('Aufgabe1_4')

		# FigueCanvas ist ein qt-Widget, das das Diagramm anzeigen kann
        self.canvas = FigureCanvas(self.figure)

        # die Matplotlib-NavigationsLeiste
        self.toolbar = NavigationToolbar(self.canvas, self)

		# Layout (wie Sie es bereits kennen)
        self.button = qw.QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

	# Die Plot-Funktion kann nun wie vorher definiert werden:
    def plot(self):
        tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';', skiprows=1, usecols=np.arange(15))

        x = np.linspace(0,10, 10)
        y = np.cos(x)*np.cos(2*x)+np.sin(x)

        x1 = np.linspace(0, 10, 250)
        y1 = np.cos(x1) * np.cos(2 * x1) + np.sin(x1)

        xp = np.linspace(0, 10, 250)
        yp= self.polynome(xp,x,y)

        yAchse = tabelle[:, 6]
        spalte_rr = tabelle[:, 14]


        n = len(yAchse)
        xAchse = np.arange(n)
        mit_x = np.sum(xAchse)/n
        mit_y = np.sum(yAchse)/n


        m = (n*mit_x*mit_y-np.sum(xAchse*yAchse))/(n*mit_x**2-np.sum(xAchse**2))
        b = mit_y - m*mit_x

        l_Reg = m*xAchse+b


        # Zeichnen und Anzeige
        self.axis.plot(xAchse, l_Reg,label="lineare Regression")
        self.axis.plot(xAchse, yAchse, label="spalte_tx")
        plt.legend()

        # Achtung: keine plt.show!
        # (Neu-)Zeichnen des Canva
        self.canvas.draw()

    def polynome(self, x, pointx, pointy):
        total = 0
        n = len(pointx)
        for i in range(n):
            xi, yi = pointx[i], pointy[i]

            total += yi * self.g(i, n, x, pointx, xi)
        return total

    def g(self, i, n, x, pointx, xk):
        tot_mul = 1
        for j in range(n):
            if i != j:
                xj = pointx[j]
                tot_mul *= (x - xj) / (xk - xj)
        return tot_mul


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())