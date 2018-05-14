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
        self.selectionList = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '17']

        self.button.clicked.connect(self.getSelection)
        self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

	# Die Plot-Funktion kann nun wie vorher definiert werden:

    def getSelection(self):
        plt.cla()
        sel = qw.QInputDialog.getItem(self, 'Selection Degree', 'Select degree for polynomial interpolation:', self.selectionList,
                                      current=0, editable=False)
        if sel[1]:
            self.grad = int(sel[0])

    def plot(self):
        tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';', skiprows=1, usecols=np.arange(15))

        yAchse = tabelle[:, 6]
        n = len(yAchse)
        xAchse = np.arange(n)

        #####laut der Aufgabe müssen wir nur zwei Punkte nehmen####
        xAchseL = np.linspace(0,18,2, endpoint=True)

        print(xAchseL)
        xAchseP = np.linspace(0, 18, 250)

        mit_x = np.sum(xAchse)/n
        mit_y = np.sum(yAchse)/n
        m = (n*mit_x*mit_y-np.sum(xAchse*yAchse))/(n*mit_x**2-np.sum(xAchse**2))
        b = mit_y - m*mit_x
        l_Reg = m*xAchseL+b

        grad = self.grad

        z = np.polyfit(xAchse, yAchse, grad)
        f = np.poly1d(z)
        for i in range(len(xAchseP)):
            zz = f(xAchseP)#, 'b+')


        # Zeichnen und Anzeige
        self.axis.plot(xAchseL, l_Reg, label="lineare Regression")
        self.axis.plot(xAchse, yAchse, label="spalte_tx")
        self.axis.plot(xAchseP, zz, label="polynomiell Regression, grad:" + str(grad))


        plt.legend()

        # Achtung: keine plt.show!
        # (Neu-)Zeichnen des Canva
        self.canvas.draw()



if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())