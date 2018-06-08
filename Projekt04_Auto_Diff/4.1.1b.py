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
        self.setWindowTitle('Aufgabe4_1_1')
        self.h=0.0000001
        self.interval_start = -5
        self.interval_end = 5
        self.interval_steps = 1000

        self.bereich = 3
        self.grad = 9

        # Berechnung der Extremwerte
        self.extremwerte_runden_auf = 3

        # FigueCanvas ist ein qt-Widget, das das Diagramm anzeigen kann
        self.canvas = FigureCanvas(self.figure)

        # die Matplotlib-NavigationsLeiste
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layout (wie Sie es bereits kennen)
        self.button = qw.QPushButton('Plot')

        #Eingabe
        self.hbox = qw.QHBoxLayout()
        defh = qw.QLabel("h: ")
        defg = qw.QLabel("grad: ")
        self.field = qw.QLineEdit(self)
        self.fieldg=qw.QLineEdit(self)
        self.field.setText("0.000001")
        self.fieldg.setText("9")
        self.hbox.addWidget(defh)
        self.hbox.addWidget(self.field)
        self.hbox.addWidget(defg)
        self.hbox.addWidget(self.fieldg)


        #self.selectionList = ['0.000000001', '0.1', '0.5', '1', '3', '10', '100']
        #self.button.clicked.connect(self.getSelection)

        self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addLayout(self.hbox)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    # Die Plot-Funktion kann nun wie vorher definiert werden:
    def plot(self):
        plt.cla()
        self.h = float(self.field.text())
        self.grad = float(self.fieldg.text())
        tabelle = np.loadtxt("wetterdaten_neu.txt", delimiter=';', skiprows=1, usecols=np.arange(15))

        #Funktion
        self.y = tabelle[:, 13]
        n= len(self.y)
        print(n)
        self.x = np.arange(n)


        ################################

        #Annäherung
        poly = np.polyfit(self.x, self.y, self.grad)
        self.poly_f = np.poly1d(poly)
        self.y_ann= self.poly_f(self.x)
        #print(self.y_abl)

        #Ableitung
        self.y_abl = self.num_Ableitung()
        self.y_abl2 = self.num_Ableitung2()

        # Parameter: Funktion, Ableitung der Funktion
        #self.extremstellen_berechnung_durch_ableitung(self.y, self.y_abl2)
        ################################


        # Zeichnen und Anzeige
        self.axis.plot(self.x, self.y,label="Daten")
        stri="Newtonsche Differenzenquotient der Daten, h="+str(self.h)
        stri2="Ableitung der Daten(2h im Nenner), h="+str(self.h)

        self.axis.plot(self.x, self.y_ann, label="ann")
        self.axis.plot(self.x, self.y_abl, label="abl")
        self.axis.plot(self.x, self.y_abl2, label="abl2")
        #self.axis.plot(self.x,y_mw, label="MLS")


        #Legende
        plt.legend()

        # (Neu-)Zeichnen des Canvas
        self.canvas.draw()


    def num_Ableitung(self):
        y=[]
        for x in self.x:
            #(f(x+h)-f(x))/h
            y.append((self.f_x(x+self.h)-self.f_x(x))/self.h)
        y_abl=np.array(y)
        return y_abl

    def num_Ableitung2(self):
        y=[]
        for x in self.x:
            #(f(x+h)-f(x-h))/2h
            y.append((self.f_x(x+self.h)-self.f_x(x-self.h))/2*self.h)
        y_abl=np.array(y)
        return y_abl

    def extremstellen_berechnung_durch_ableitung(self, polynom, ableitung):

        def tupel_erstellung(extremwert):
            x_wert = self.interval_start + ((x / self.interval_steps) * (self.interval_end - self.interval_start))
            point_as_tupel = (round(x_wert, runden_auf), round(polynom[x], runden_auf))
            extremwert.append(point_as_tupel)

        minima, maxima = [], []
        runden_auf = self.extremwerte_runden_auf

        # Überprüfung - Ist Polynom leer?
        if len(ableitung) <= 1:
            print("\nFehler - Polynom in der Funktion extremstellen_berechnung_durch_ableitung ist leer\n")
            return False

        # Überprüfung - Ist erstes Element positiv (1) oder negativ (0)
        pos_neg = 1 if ableitung[0] >= 0 else 0

        for x in range(len(ableitung)):
            # von positiv zu negativ -> Maximum
            if pos_neg == 1:
                if ableitung[x] <= 0:
                    tupel_erstellung(maxima)
                    pos_neg = 0

            # von negativ zu positiv -> Minimum
            else:
                if ableitung[x] >= 0:
                    tupel_erstellung(minima)
                    pos_neg = 1

        print("\nMinima:", minima, "\nMaxima:", maxima)

        # print("HAAALLLOOOO\n\n\n", polynom)

    def f_x(self, x):
        # Angezeigtes Polynom:
        # polynom = np.sin(1/x)
        # polynom = np.sin(x)
        # polynom = np.array(x*x)
        # polynom = np.array(x**4)
        # polynom = np.cos(x)
        # polynom = np.cos(0.5 * x + 4)
        polynom = self.poly_f(x)

        return polynom

    def getSelection(self):
        plt.cla()
        sel = qw.QInputDialog.getItem(self, 'Selection Degree', 'Select h:', self.selectionList,
                                      current=0, editable=True)
        if sel[1]:
            self.h = float(sel[0])


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())
