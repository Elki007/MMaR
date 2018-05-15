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
        self.setWindowTitle('Aufgabe2_1_2')

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
        '''tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';', skiprows=1, usecols=np.arange(15))

        yAchse = tabelle[:, 6]
        n = len(yAchse)

        # Verhältnis von Test- und Trainingswerten
        # bspw. anteil = 4 -> 1/4 Train-Werte, 3/4 Test-Werte
        # bspw. anteil = 1.5 -> 3/4 Train-Werte, 1/4 Test-Werte
        anteil = 1.5
        teil = int(n // anteil)
        print(teil)

        xAchse = np.arange(n)
        xAchse_train = np.arange(teil)
        xAchse_test = np.arange(teil, n)
        yAchse_train = yAchse[:teil]
        yAchse_test = yAchse[teil:]

        #####laut der Aufgabe müssen wir nur zwei Punkte nehmen####

        xAchseL = np.linspace(0,n-1,19, endpoint=True)
        xAchseP = np.linspace(0, n-1, 250)

        mit_x = np.sum(xAchse_train)/teil
        mit_y = np.sum(yAchse_train)/teil
        m = (n*mit_x*mit_y-np.sum(xAchse_train*yAchse_train))/(n*mit_x**2-np.sum(xAchse_train**2))
        b = mit_y - m*mit_x
        l_Reg = m*xAchseL+b

        grad = self.grad

        z = np.polyfit(xAchse_train, yAchse_train, grad)
        f = np.poly1d(z)
        for i in range(len(xAchseP)):
            zz = f(xAchseP)#, 'b+')
            zz2 = f(xAchseL)

        # Zeichnen und Anzeige
        self.axis.plot(xAchseL, l_Reg, label="lineare Regression")
        self.axis.plot(xAchse_train, yAchse_train,'g-', label="spalte_tx_train")
        self.axis.plot(xAchse_test, yAchse_test,'b-', label="spalte_tx_test")
        self.axis.plot(xAchseP, zz, label="polynomiell Regression, grad:" + str(grad))
        self.axis.plot(xAchse, yAchse, 'y--', label="Alle Werte")

        #E(b,m)#
        #for i in range (teil,n):

        Grad:2
        Fehler_L:  15704.246763612948
        Fehler_P:  105232.546053088

        Fehler_L = 0
        Fehler_P = 0
        #for i in range(18,8,-1):
        for i in xAchse_test:
            Fehler_L += (l_Reg[i]-yAchse[i])**2
            Fehler_P += (zz2[i] - yAchse[i]) ** 2

        Fehler_L /= len(xAchse_test)
        Fehler_P /= len(xAchse_test)

        print("Fehler_L: ", Fehler_L)
        print("Fehler_P: ", Fehler_P)

        plt.legend()'''

        # Achtung: keine plt.show!
        # (Neu-)Zeichnen des Canva

        #Teil 1_2

        x = np.linspace(0, 10, 5)
        y = np.cos(x) * np.cos(2 * x) + np.sin(x)

        x1 = np.linspace(0, 10, 250)
        y1 = np.cos(x1) * np.cos(2 * x1) + np.sin(x1)

        xp = np.linspace(0, 10, 250)
        yp = self.polynome(xp, x, y)

        # Zeichnen und Anzeige
        self.axis.plot(x, y, 'o', label="Ausgewählte Punkte")
        self.axis.plot(x1, y1, label="Ursprüngliche Funktion")
        self.axis.plot(xp, yp, label="Polynominterpolation")
        plt.legend()


        self.canvas.draw()



if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())