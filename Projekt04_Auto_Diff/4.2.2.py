import math
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
# from PyQt5 import QtCore as qc

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class DualNumber:
    def __init__(self,wert,ableitung):
        self.wert = wert
        self.ableitung = ableitung

    def __add__(self, other):
        return DualNumber(self.wert+other.wert,self.ableitung+other.ableitung)

    def __sub__(self, other):
        return DualNumber(self.wert-other.wert,self.ableitung-other.ableitung)

    def __mul__(self, other):
        return DualNumber(self.wert*other.wert,self.ableitung*other.wert+self.wert*other.ableitung)

    def __truediv__(self, other):
        return DualNumber(self.wert/other.wert,(self.ableitung*other.wert-self.wert*other.ableitung)/other.wert**2)

    def __call__(self):
        return self.wert

    def __repr__(self):
        return print("wert:",self.wert, " abl:", self.ableitung)

    def __str__(self):
        return "wert:" + str(self.wert) + " abl:" + str(self.ableitung)

class DualFunktion:
    def __call__(self, x):
        pass

    def __add__(self, other):
        return AddDFunktion(self,other)

    def __sub__(self, other):
        return SubDFunktion(self,other)

    def __mul__(self, other):
        return MulDFunktion(self,other)

    def __truediv__(self, other):
        return DivDFunktion(self,other)

    def __pow__(self, power, modulo=None):
        return PowDFunktion(self,power)

    def __matmul__(self, other):
        return MMulDFunktion(self,other)

    def __str__(self):
        return str(self.y)

    def __repr__(self):
        return self.y

class AddDFunktion(DualFunktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " + " + g.name

    def __call__(self, x):
        self.y = self.f(x) + self.g(x)
        return self.y

class SubDFunktion(DualFunktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " - " + g.name

    def __call__(self, x):
        self.y = self.f(x) + self.g(x)
        return self.y

class MulDFunktion(DualFunktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " * " + g.name

    def __call__(self, x):
        self.y = self.f(x) * self.g(x)
        return self.y

class DivDFunktion(DualFunktion):
    def __init__(self,f,g):
        super().__init__()
        self.f = f
        self.g = g
        self.name = f.name + " / " + g.name

    def __call__(self, x):
        self.y = self.f(x) / self.g(x)
        return self.y

class MMulDFunktion(DualFunktion):
    def __init__(self,f,g):
        self.f = f
        self.g = g
        self.name = f.name.replace("(x)", "("+g.name+")")

    def __call__(self, x):
        x = self.g(x)
        self.y = self.f(x)
        return self.y

class PowDFunktion(DualFunktion):
    def __init__(self,f,p):
        #print("p:",p)
        self.f = f
        self.p = p
        self.name = "("+f.name+")**"+str(p)

    def __call__(self, x):
        self.y=DualNumber(1,0)
        for i in range(self.p):
            self.y = self.y*self.f(x)
        #self.y = self.f(x)**self.p
        return self.y

'''
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
        #print("p:",p)
        self.f = f
        self.p = p
        self.name = "("+f.name+")**"+str(p)

    def __call__(self, x):
        self.y = self.f(x)**self.p
        return self.y
'''
class Sin(DualFunktion):
    def __init__(self):
        super().__init__()
        self.name = "Sin(x)"

    def __call__(self, x):
        self.wert = math.sin(x.wert)
        self.ableitung = math.cos(x.wert)*x.ableitung
        return DualNumber(math.sin(x.wert), math.cos(x.wert)*x.ableitung)

    def __repr__(self):
        return str(self.wert)

class Cos(DualFunktion):
    def __init__(self):
        super().__init__()
        self.name = "Cos(x)"

    def __call__(self, x):
        self.wert = math.cos(x.wert)
        self.ableitung = -math.sin(x.wert) * x.ableitung
        return DualNumber(self.wert, self.ableitung)

    def __repr__(self):
        return str(self.wert)

class Tan(DualFunktion):
    def __init__(self):
        super().__init__()
        self.name = "Tan(x)"

    def __call__(self, x):
        self.wert = math.tan(x.wert)
        self.ableitung = 1/(math.cos(x.wert)**2)
        return DualNumber(self.wert, self.ableitung)

    def __repr__(self):
        return str(self.wert)


class Exp(DualFunktion):
    def __init__(self):
        super().__init__()
        self.name = "e**(x)"

    def __call__(self, x):
        self.wert = math.exp(x.wert)
        self.ableitung = math.exp(x.wert)*x.ableitung
        return DualNumber(self.wert, self.ableitung)

    def __repr__(self):
        return str(self.wert)

class Ln(DualFunktion):
    def __init__(self):
        super().__init__()
        self.name = "ln(x)"

    def __call__(self, x):
        self.wert = math.log1p(x.wert-1)
        self.ableitung = 1/x.wert
        return DualNumber(self.wert, self.ableitung)

    def __repr__(self):
        return str(self.wert)
'''
class Pow(DualFunktion):
    def __init__(self,p):
        super().__init__()
        self.name = "(x)**"+str(p)

    def __call__(self, x):
        self.y = x**2
        return self.y

    def __repr__(self):
        return str(self.y)

class Konst(DualFunktion):
    def __init__(self, c):
        super().__init__()
        self.c=c
        self.name = str(c)

    def __call__(self, x):
        self.y = self.c
        return self.y

    def __repr__(self):
        return str(self.y)

class Ident(DualFunktion):
    def __init__(self):
        super().__init__()
        self.name = " ident(x) "

    def __call__(self, x):
        self.y = x
        return self.y

    def __repr__(self):
        return str(self.y)
'''

################################
#f=sin(cos(x)+x^2)
f=Sin()**2
fa=Sin()+Sin()
fb=Sin()-Sin()
fc=Sin()*Sin()
fd=Sin()/Sin()

g=Cos()**2
ga=Cos()+Cos()
gb=Cos()-Cos()
gc=Cos()*Cos()
gd=Cos()/Cos()

h=Tan()

##### Dual Number in form (x,1) #####
d_n=DualNumber(2,1)
print(h.name, h(d_n))

h=Sin()/Cos()
print(h.name, h(d_n))

h=Sin()
x=DualNumber(5,1)
print(h.name, h(DualNumber(1,0)/x))
################################
class PlotWindow(qw.QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        # das Diagramm auf dem wir zeichnen
        self.figure, self.axis = plt.subplots()
        self.setWindowTitle('Aufgabe4_2_2')
        self.h=0.0000001
        self.interval_start = -5
        self.interval_end = 5
        self.interval_steps = 1000

        self.bereich = 3
        self.grad = 9
        self.xx = 1 # für tangent
        self.ymin=-1
        self.ymax=1

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
        deff = qw.QLabel("Funktion: ")
        self.fieldfunk=qw.QLineEdit(self)
        ### on change
        self.fieldfunk.editingFinished.connect(self.parse)

        self.field.setText("0.5")
        self.hbox.addWidget(deff)
        self.hbox.addWidget(self.fieldfunk)
        self.hbox.addWidget(defh)
        self.hbox.addWidget(self.field)

        self.hbox2 = qw.QHBoxLayout()
        ymin = qw.QLabel("y min: ")
        self.fieldymin = qw.QLineEdit(self)
        self.fieldymin.setText("-2")
        self.hbox2.addWidget(ymin)
        self.hbox2.addWidget(self.fieldymin)
        ymax = qw.QLabel("y max: ")
        self.fieldymax = qw.QLineEdit(self)
        self.fieldymax.setText("2")
        self.hbox2.addWidget(ymax)
        self.hbox2.addWidget(self.fieldymax)


        self.hbox3 = qw.QHBoxLayout()
        self.ADt = qw.QCheckBox("Show AD tangent")
        self.ADd = qw.QCheckBox("Show AD derivative")
        self.ADnt = qw.QCheckBox("Show AD numeric tangent")
        self.ADnd = qw.QCheckBox("Show AD numeric derivative")
        ### on change
        self.ADt.stateChanged.connect(self.plot)
        self.ADd.stateChanged.connect(self.plot)
        self.ADnt.stateChanged.connect(self.plot)
        self.ADnd.stateChanged.connect(self.plot)

        self.hbox3.addWidget(self.ADt)
        self.hbox3.addWidget(self.ADd)
        self.hbox3.addWidget(self.ADnt)
        self.hbox3.addWidget(self.ADnd)

        #self.selectionList = ['0.000000001', '0.1', '0.5', '1', '3', '10', '100']
        #self.button.clicked.connect(self.getSelection)

        #self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(self.hbox)
        layout.addLayout(self.hbox2)
        layout.addLayout(self.hbox3)
        #layout.addWidget(self.button)
        self.setLayout(layout)

        self.f_x = Sin()

        self.plot()

    def enterPress(self):
        if self.field.text()!="0":
            self.plot()
        else:
            print("Wrong input")


    def onclick(self, event):
        self.xx=event.xdata
        #print(self.xx)
        self.plot()
        #self.tangent()


    def parse(self):
        text = self.fieldfunk.text()
        print(text)

    def num_Ableitung2(self):
        y=[]
        for x in self.x:
            #(f(x+h)-f(x-h))/2h
            y.append((self.f_x(DualNumber(1/(x+self.h),-1/((x+self.h)** 2))).wert-
                      self.f_x(DualNumber(1/(x-self.h),-1/((x-self.h)** 2))).wert)/2*self.h)

        y_abl=np.array(y)
        return y_abl

    def num_Ableitung2_x(self,x):
        #(f(x+h)-f(x-h))/2h
        y=((self.f_x(DualNumber(1/(x+self.h),-1/((x+self.h)** 2))).wert-
                  self.f_x(DualNumber(1/(x-self.h),-1/((x-self.h)** 2))).wert)/2*self.h)
        return y

    # Die Plot-Funktion kann nun wie vorher definiert werden:
    def plot(self):
        plt.cla()
        cid = self.canvas.mpl_connect('button_press_event', self.onclick)

        ################################
        ######## Get settings ##########
        ################################

        self.h = float(self.field.text())
        #new y min and max
        self.ymin = float(self.fieldymin.text())
        self.ymax = float(self.fieldymax.text())

        ################################
        ######## Funktion ##############
        ################################

        self.x = np.linspace(self.interval_start, self.interval_end, 1000)

        ####### Funktion ########
        #self.f_x = Sin()
        #h = Sin()
        #x = DualNumber(5, 1)
        #print(h.name, h(DualNumber(1, 0) / x))


        self.y = []
        for x in self.x:
            self.y.append(self.f_x(DualNumber(1/x,-1/(x**2))).wert)

        ################################
        ######## Ableitung #############
        ################################

        self.y_abl3 = []
        for x in self.x:
            self.y_abl3.append(self.f_x(DualNumber(1 / x, -1/(x**2))).ableitung)

        # Num Ableitung
        self.y_abl2 = self.num_Ableitung2()

        ################################
        ########### Tangente ###########
        ################################

        x0 = self.xx  # - aktual x value
        y0 = self.f_x(DualNumber(1 / self.xx, -1 / (self.xx ** 2))).wert  # - aktual y value
        koef = self.f_x(DualNumber(1 / self.xx, -1 / (self.xx ** 2))).ableitung  # - aktual y_abl
        #
        b = y0 - koef * x0
        # y=koef*x+b
        self.y_t = []
        for x in self.x:
            self.y_t.append(koef * x + b)

        # Num Tangente

        x1 = self.xx  # - aktual x value
        y1 = self.f_x(DualNumber(1 / self.xx, -1 / (self.xx ** 2))).wert  # - aktual y value
        koef = self.num_Ableitung2_x(self.xx)  # - aktual y_abl
        #
        b = y1 - koef * x1
        # y=koef*x+b
        self.y_nt = []
        for x in self.x:
            self.y_nt.append(koef * x + b)


        ################################
        ##### Zeichnen und Anzeige #####
        ################################

        self.axis.plot(self.x, self.y,label="Funktion")
        if self.ADd.checkState() != 0:
            self.axis.plot(self.x, self.y_abl3, label="Ableitung")

        if self.ADnd.checkState() != 0:
            self.axis.plot(self.x, self.y_abl2, label="Num Ableitung")

        if self.ADt.checkState() != 0:
            self.axis.plot(self.x, self.y_t, label="Tangente")
            self.axis.plot(self.xx, y0, 'o')

        if self.ADnt.checkState() != 0:
            self.axis.plot(self.x, self.y_nt, label="Num Tangente")


        #Legende
        plt.legend()

        # (Neu-)Zeichnen des Canvas
        plt.ylim(self.ymin, self.ymax)
        self.canvas.draw()

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())