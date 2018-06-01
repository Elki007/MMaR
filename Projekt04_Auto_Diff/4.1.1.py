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

        # FigueCanvas ist ein qt-Widget, das das Diagramm anzeigen kann
        self.canvas = FigureCanvas(self.figure)

        # die Matplotlib-NavigationsLeiste
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layout (wie Sie es bereits kennen)
        self.button = qw.QPushButton('Plot')

        self.selectionList = ['0.000000001', '0.1', '0.5', '1', '3', '10', '100']
        self.button.clicked.connect(self.getSelection)

        self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    # Die Plot-Funktion kann nun wie vorher definiert werden:
    def plot(self):
        plt.cla()
        #Funktion
        self.x = np.linspace(-5,5,1000)
        self.y = self.f_x(self.x)


        ################################
        #Ableitung

        self.y_abl = self.num_Ableitung()
        self.y_abl2=self.num_Ableitung2()
        ################################


        # Zeichnen und Anzeige
        self.axis.plot(self.x, self.y,label="Polynom")
        stri="Newtonsche Differenzenquotient des Polynoms, h="+str(self.h)
        stri2="Ableitung des Polynoms(2h im Nenner), h="+str(self.h)
        self.axis.plot(self.x, self.y_abl,label=stri)
        self.axis.plot(self.x, self.y_abl2,label=stri2)


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


    def f_x(self, x):
        #print(np.array(x*x))
        #return np.array(x**4)
        #return np.cos(x)
        return np.sin(1/x)
        #return np.cos(x)*np.cos(2*x)+np.sin(x)

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
