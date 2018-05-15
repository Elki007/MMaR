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
        self.setWindowTitle('Aufgabe1_5')

        # Größe des Fensters bzw. Teildaten-Abschnitts - Wie viele Werte sollen für einen Mittelwert genommen werden?
        self.bereich = 6

		# FigueCanvas ist ein qt-Widget, das das Diagramm anzeigen kann
        self.canvas = FigureCanvas(self.figure)

        # die Matplotlib-NavigationsLeiste
        self.toolbar = NavigationToolbar(self.canvas, self)

		# Layout (wie Sie es bereits kennen)
        self.button = qw.QPushButton('Plot')
        self.selectionList = [str (x) for x in range(2, self.bereich)]

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
        plt.cla()

        # Wetterdaten
        tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';', skiprows=1, usecols=np.arange(15))

        # Grad des Polynoms - Achtung: grad < bereich
        grad = self.grad

        grenze = self.bereich//2

        yAchse = tabelle[:, 6]
        n = len(yAchse)
        xAchse = np.arange(n)

        xAchseP = np.linspace(0, n-1, 250)

        # x-Achse geht vom (bereich//2). bis zum (bereich//2).letzten Element
        # y-Achse, ist eine Liste, die später gefüllt wird
        x_teilachse = np.array(range(grenze,n-grenze))
        y_mw = []

        # Was will ich machen:
        #   polyfit in Grad "grad" über n Punkte laufen lassen, deren Mittelpunkt nehmen und als ein Punkt einfügen

        for i in range(grenze, n-grenze):
            poly = np.polyfit(xAchse[i-grenze:i+grenze+1], yAchse[i-grenze:i+grenze+1], grad)
            poly_func = np.poly1d(poly)

            mw_func = poly_func(xAchse[i-grenze:i+grenze+1])
            y_mw.append(np.mean(mw_func))


        z = np.polyfit(xAchse, yAchse, grad)
        f = np.poly1d(z)

        zz = f(xAchseP)

        # Zeichnen und Anzeige
        self.axis.plot(xAchse, yAchse, label="spalte_tx")
        self.axis.plot(x_teilachse, y_mw, 'y-', label="Moving-Least-Squares")
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