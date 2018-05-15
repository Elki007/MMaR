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
        self.setWindowTitle('Aufgabe2_Interpolation')

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

        # Verhältnis von Test- und Trainingswerten
        anteil = 4
        teil = n // anteil

        # Datensatz zufällig aufteilen (Interpolation)
        indices = np.random.permutation(n)

        x_zufall_1 = indices[:teil]
        x_zufall_2 = indices[teil:]

        x_zufall_1.sort()
        x_zufall_2.sort()

        y_zufall_1 = []
        y_zufall_2 = []

        # Berechnung der y-Werte für die jeweilige zufällige x-Train-Achsen
        for i in x_zufall_1:
            y_zufall_1.append(yAchse[i])

        for i in x_zufall_2:
            y_zufall_2.append(yAchse[i])

        # Anwendung auf vorherige Struktur, zur besseren Erklärung/Nachvollziehbarkeit in der Gruppe
        # Zufälligen Werte-Listen werden zugewiesen
        xAchse = np.arange(n)
        xAchse_train = x_zufall_1
        xAchse_test = x_zufall_2
        yAchse_train = y_zufall_1
        yAchse_test = y_zufall_2


        #x = np.linspace(0, n, 5)
        #y = np.cos(x) * np.cos(2 * x) + np.sin(x)

        xp = np.linspace(0, n-1, 250)
        yp = self.polynome(xp, xAchse_train, yAchse_train)
        ypp = self.polynome(xAchse, xAchse_train, yAchse_train)


        #####laut der Aufgabe müssen wir nur zwei Punkte nehmen####
        xAchseL = np.linspace(0, n-1, 19, endpoint=True)
        xAchseP = np.linspace(0, n-1, 250)

        n_anz = len(xAchse_train)

        mit_x = np.sum(xAchse_train)/teil
        mit_y = np.sum(yAchse_train)/teil
        m = (teil*mit_x*mit_y-np.sum(xAchse_train*yAchse_train))/(teil*mit_x**2-np.sum(xAchse_train**2))
        b = mit_y - m*mit_x
        l_Reg = m * xAchseL + b

        grad = self.grad

        z = np.polyfit(xAchse_train, yAchse_train, grad)
        f = np.poly1d(z)

        zz = f(xAchseP)
        zz2 = f(xAchseL)

        '''print("xAchseL",xAchseL)
        print("l_Reg",l_Reg)
        print("xAchse",xAchse)
        print("yAchse",yAchse)
        print("xAchseP",xAchseP)
        print("zz",zz)'''
        # Zeichnen und Anzeige
        self.axis.plot(xAchseL, l_Reg, label="lineare Regression")
        #self.axis.plot(xAchse_train, yAchse_train,'g-', label="spalte_tx_train")
        #self.axis.plot(xAchse_test, yAchse_test,'y-', label="spalte_tx_test")
        self.axis.plot(xAchse, yAchse, '-', label="Alle Werte")
        self.axis.plot(xAchseP, zz, label="polynomiell Regression, grad:" + str(grad))
        self.axis.plot(xp,yp,'--', label="Polynominterpolation")

        #E(b,m)#
        #for i in range (teil,n):
        Fehler_L = 0
        Fehler_P = 0
        Fehler_Po = 0

        for i in xAchse_test:  #[3,9,12]
            Fehler_L += (l_Reg[i] - yAchse[i]) ** 2
            Fehler_P += (zz2[i] - yAchse[i]) ** 2
            Fehler_Po += (ypp[i] - yAchse[i]) **2

        Fehler_L /= len(xAchse_test)
        Fehler_P /= len(xAchse_test)
        Fehler_Po /= len(xAchse_test)

        """
        for i in range(18,8,-1):
            Fehler_L += (l_Reg[i] - yAchse[i]) ** 2
            Fehler_P += (zz2[i] - yAchse[i]) ** 2

        """


        print("Fehler_L: ", Fehler_L)
        print("Fehler_P: ", Fehler_P)
        print("Fehler_Po: ", Fehler_Po)
        print()

        #
        #
        # Spontaner Durchlauftest für gemittelten Fehlerwert (# Durchläufe = fehler_durchlauf):
        #
        #

        Fehler_L_Ges = 0
        Fehler_P_Ges = 0
        Fehler_Po_Ges = 0

        Fehler_L = 0
        Fehler_P = 0
        Fehler_Po = 0

        fehler_durchlauf = 10

        for i in range(fehler_durchlauf):
            indices = np.random.permutation(n)

            x_zufall_1 = indices[:teil]
            x_zufall_2 = indices[teil:]

            x_zufall_1.sort()
            x_zufall_2.sort()

            y_zufall_1 = []
            y_zufall_2 = []

            for i in x_zufall_1:
                y_zufall_1.append(yAchse[i])

            for i in x_zufall_2:
                y_zufall_2.append(yAchse[i])

            # Anwendung auf vorherige Struktur, zur besseren Erklärung/Nachvollziehbarkeit

            xAchse_train = x_zufall_1
            xAchse_test = x_zufall_2
            yAchse_train = y_zufall_1

            #####laut der Aufgabe müssen wir nur zwei Punkte nehmen####

            xAchseL = np.linspace(0, n - 1, 19, endpoint=True)
            xAchseP = np.linspace(0, n - 1, 250)

            xp = np.linspace(0, n, 250)
            yp = self.polynome(xp, xAchse_train, yAchse_train)
            ypp = self.polynome(xAchse, xAchse_train, yAchse_train)

            mit_x = np.sum(xAchse_train) / teil
            mit_y = np.sum(yAchse_train) / teil

            m = (n * mit_x * mit_y - np.sum(xAchse_train * yAchse_train)) / (n * mit_x ** 2 - np.sum(xAchse_train ** 2))
            b = mit_y - m * mit_x

            l_Reg = m * xAchseL + b

            z = np.polyfit(xAchse_train, yAchse_train, grad)
            f = np.poly1d(z)

            zz2 = f(xAchseL)


            for i in xAchse_test:
                Fehler_L += (l_Reg[i] - yAchse[i]) ** 2
                Fehler_P += (zz2[i] - yAchse[i]) ** 2
                Fehler_Po += (ypp[i] - yAchse[i]) ** 2

            Fehler_L /= len(xAchse_test)
            Fehler_P /= len(xAchse_test)
            Fehler_Po /= len(xAchse_test)

            Fehler_L_Ges += Fehler_L
            Fehler_P_Ges += Fehler_P
            Fehler_Po_Ges += Fehler_Po

            Fehler_L = 0
            Fehler_P, Fehler_Po = 0, 0






        Fehler_P_Ges /= fehler_durchlauf
        Fehler_Po_Ges /= fehler_durchlauf
        Fehler_L_Ges /= fehler_durchlauf

        print("Fehler_L_Ges (", fehler_durchlauf, "): ", Fehler_L_Ges, sep='')
        print("Fehler_P_Ges (", fehler_durchlauf, "): ", Fehler_P_Ges, sep='')
        print("Fehler_Po_Ges (", fehler_durchlauf, "): ", Fehler_Po_Ges, sep='')

        '''print("l_Reg", l_Reg[18])
        print(len(l_Reg))

        print("zz2", zz2[18])
        print(len(l_Reg))

        print("y", yAchse_test[0])
        print(len(yAchse_test))'''
        plt.legend()

        # Achtung: keine plt.show!
        # (Neu-)Zeichnen des Canva
        self.canvas.draw()



if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())