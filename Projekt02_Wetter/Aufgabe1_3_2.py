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
        self.setWindowTitle('Aufgabe1_2')

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

        yAchse = tabelle[:, 6]
        n = len(yAchse)
        xAchse = np.arange(n)

        x4=np.array(range(1,18,3))
        y4=np.array(range(6))

        #xp = np.linspace(0, 10, 250)
        #yp= self.polynome(xp,x,y)

        for i in range(6):
            ii=i*3
            #x4[i] = np.mean(xAchse[ii:ii+3])
            y4[i] = np.mean(yAchse[ii:ii+3])

        print(x4)
        print(y4)

        # Zeichnen und Anzeige
        self.axis.plot(xAchse, yAchse,'o',label="Daten")
        self.axis.plot(x4, y4,'-',label="Ausgewählte Punkte")
        #self.axis.plot(xp, yp,label="Polynominterpolation")
        #plt.plot(x4, y4)
        plt.legend()


        # Achtung: keine plt.show!
        # (Neu-)Zeichnen des Canva
        self.canvas.draw()
        #plt.show()
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
