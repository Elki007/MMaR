import math
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
# from PyQt5 import QtCore as qc

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Funktion:
    def __call__(self, x):
        pass

    def __add__(self, other):
        return AddFunktion(self,other)

    def __sub__(self, other):
        return SubFunktion(self,other)

    def __mul__(self, other):
        return MulFunktion(self,other)

    def __truediv__(self, other):
        return DivFunktion(self,other)

    def __pow__(self, power, modulo=None):
        return PowFunktion(self,power)

    def __matmul__(self, other):
        return MMulFunktion(self,other)

    def __str__(self):
        return str(self.y)

    def __repr__(self):
        return self.y

class AddFunktion(Funktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " + " + g.name

    def __call__(self, x):
        self.y = self.f(x) + self.g(x)
        return self.y

class SubFunktion(Funktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " - " + g.name

    def __call__(self, x):
        self.y = self.f(x) - self.g(x)
        return self.y

class MulFunktion(Funktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " * " + g.name

    def __call__(self, x):
        self.y = self.f(x) * self.g(x)
        return self.y

class DivFunktion(Funktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " / " + g.name

    def __call__(self, x):
        self.y = self.f(x) / self.g(x)
        return self.y

class MMulFunktion(Funktion):
    def __init__(self,f,g):
        self.f = f
        self.g = g
        self.name = f.name.replace("(x)", "("+g.name+")")

    def __call__(self, x):
        x = self.g(x)
        self.y = self.f(x)
        return self.y

class PowFunktion(Funktion):
    def __init__(self,f,p):
        print("p:",p)
        self.f = f
        self.p = p
        self.name = "("+f.name+")**"+str(p)

    def __call__(self, x):
        self.y = self.f(x)**self.p
        return self.y

class Sin(Funktion):
    def __init__(self):
        super().__init__()
        self.name = "Sin(x)"

    def __call__(self, x):
        self.y = math.sin(x)
        return self.y

    def __repr__(self):
        return str(self.y)

class Cos(Funktion):
    def __init__(self):
        super().__init__()
        self.name = "Cos(x)"

    def __call__(self, x):
        self.y = math.cos(x)
        return self.y

    def __repr__(self):
        return str(self.y)

class Exp(Funktion):
    def __init__(self):
        super().__init__()
        self.name = "e**(x)"

    def __call__(self, x):
        self.y = math.exp(x)
        return self.y

    def __repr__(self):
        return str(self.y)

class Ln(Funktion):
    def __init__(self):
        super().__init__()
        self.name = "ln(x)"

    def __call__(self, x):
        self.y = math.log1p(x-1)
        return self.y

    def __repr__(self):
        return str(self.y)

class Pow(Funktion):
    def __init__(self,p):
        super().__init__()
        self.name = "(x)**"+str(p)

    def __call__(self, x):
        self.y = x**2
        return self.y

    def __repr__(self):
        return str(self.y)

class Konst(Funktion):
    def __init__(self, c):
        super().__init__()
        self.c=c
        self.name = str(c)

    def __call__(self, x):
        self.y = self.c
        return self.y

    def __repr__(self):
        return str(self.y)

class Ident(Funktion):
    def __init__(self):
        super().__init__()
        self.name = " ident(x) "

    def __call__(self, x):
        self.y = x
        return self.y

    def __repr__(self):
        return str(self.y)


################################
#f=sin(cos(x)+x^2)


################################
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
        #self.button = qw.QPushButton('Plot')

        #Eingabe
        self.hbox = qw.QHBoxLayout()
        defh = qw.QLabel("Step size: ")
        self.field = qw.QLineEdit(self)
        ### on change
        self.field.editingFinished.connect(self.enterPress)

        self.field.setText("0.5")
        self.hbox.addWidget(defh)
        self.hbox.addWidget(self.field)


        self.hbox2 = qw.QHBoxLayout()
        self.ADt = qw.QCheckBox("Show AD tangent")
        self.ADd = qw.QCheckBox("Show AD derivative")
        self.ADnt = qw.QCheckBox("Show AD numeric tangent")
        self.ADnd = qw.QCheckBox("Show AD numeric derivative")
        ### on change
        self.ADt.stateChanged.connect(self.plot)
        self.ADd.stateChanged.connect(self.plot)
        self.ADnt.stateChanged.connect(self.plot)
        self.ADnd.stateChanged.connect(self.plot)

        self.hbox2.addWidget(self.ADt)
        self.hbox2.addWidget(self.ADd)
        self.hbox2.addWidget(self.ADnt)
        self.hbox2.addWidget(self.ADnd)

        #self.selectionList = ['0.000000001', '0.1', '0.5', '1', '3', '10', '100']
        #self.button.clicked.connect(self.getSelection)

        #self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(self.hbox)
        layout.addLayout(self.hbox2)
        #layout.addWidget(self.button)
        self.setLayout(layout)

        self.plot()

    def enterPress(self):
        if self.field.text()!="0":
            self.plot()
        else:
            print("Wrong input")

    def onclick(self, event):
        self.xx=event.xdata
        print(self.xx)

    # Die Plot-Funktion kann nun wie vorher definiert werden:
    def plot(self):
        plt.cla()

        cid = self.canvas.mpl_connect('button_press_event', self.onclick)

        self.h = float(self.field.text())


        #Funktion

        self.x = np.linspace(self.interval_start, self.interval_end, 1000)

        ####### Funktion ########
        self.f_x = Sin() @ (Cos() + Pow(2))


        self.y = []
        for x in self.x:
            self.y.append(self.f_x(x))

        ################################

        #Annäherung

        #fenster definieren, mittelwert berechnen, dann polyfit

        #poly = np.polyfit(self.x, self.y, self.grad)
        #self.poly_f = np.poly1d(poly)
        #self.y_ann= self.poly_f(self.x)
        #print(self.y_abl)

        #Ableitung
        self.y_abl = self.num_Ableitung()
        self.y_abl2 = self.num_Ableitung2()

        # Parameter: Funktion, Ableitung der Funktion
        #self.extremstellen_berechnung_durch_ableitung(self.y, self.y_abl2)
        ################################
        #test

        # Zeichnen und Anzeige
        self.axis.plot(self.x, self.y,label="Funktion")
        stri="Newtonsche Differenzenquotient der Daten, h="+str(self.h)
        stri2="Ableitung der Daten(2h im Nenner), h="+str(self.h)

        #self.axis.plot(self.x, self.y_ann, label="ann")
        if self.ADd.checkState() != 0:
            self.axis.plot(self.x, self.y_abl, label="Newt_abl")
        if self.ADnd.checkState() != 0:
            self.axis.plot(self.x, self.y_abl2, label="alt_abl")
        #self.axis.plot(10,5,"o", label="punkt")
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


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())