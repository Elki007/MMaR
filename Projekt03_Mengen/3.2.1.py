import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

class PlotWindow(qw.QDialog):
    def __init__(self):
        super(PlotWindow, self).__init__()

        self.xmin =-2
        self.xmax =1
        self.ymin =-1.5
        self.ymax =1.5

        # das Diagramm auf dem wir zeichnen
        self.figure, self.axis = plt.subplots()
        self.setWindowTitle('Aufgabe2_Interpolation')

        # FigueCanvas ist ein qt-Widget, das das Diagramm anzeigen kann
        self.canvas = FigureCanvas(self.figure)

        # die Matplotlib-NavigationsLeiste
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layout (wie Sie es bereits kennen)
        self.button = qw.QPushButton('Plot')
        self.button.clicked.connect(self.plotdef)
        self.button.clicked.connect(self.plot)
        layout = qw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)


    def compute_mandelbrot(self,N_max, some_threshold, nx, ny):
        # A grid of c-values
        x = np.linspace(self.xmin, self.xmax, nx) #(-0.55,-0.4,nx)#(-2, 1, nx)
        y = np.linspace(self.ymin, self.ymax, ny) #(0.4,0.6,ny)#(-1.5, 1.5, ny)

        c = x[:, np.newaxis] + 1j*y[np.newaxis, :]

        # Mandelbrot iteration

        z = c
        for j in range(N_max):
            z = z**2 + c

        #mandelbrot_set = (abs(z) < some_threshold)
        mandelbrot_set = (abs(z))
        print("ms:", mandelbrot_set[90])
        return mandelbrot_set

    def plotdef(self):
        self.xmin = -2
        self.xmax = 1
        self.ymin = -1.5
        self.ymax = 1.5
        plt.cla()
        plt.clf()
        self.resize(720, 601)
        self.center()
        self.plot()

    def plot(self):
        self.mandelbrot_set = self.compute_mandelbrot(100, 50., 601, 401)

        self.im = plt.imshow(self.mandelbrot_set.T, extent=[self.xmin, self.xmax, self.ymin, self.ymax])
        self.resize(720, 600)
        self.center()
        cid = self.canvas.mpl_connect('button_press_event', self.onclick)

    def center(self):   ##### screen center
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onclick(self, event):
        #print(self.xmin)
        xscale = (abs(self.xmax - self.xmin)) / 4
        yscale = (abs(self.ymax - self.ymin)) / 4
        #print("old:",self.xmin, self.xmax, self.ymin, self.ymax)
        self.xmin = event.xdata - xscale
        self.xmax = event.xdata + xscale
        self.ymax = event.ydata - yscale
        self.ymin = event.ydata + yscale
        #print(event.xdata, event.ydata)
        #print("new:",self.xmin, self.xmax, self.ymin, self.ymax)
        #print(self.xmin)
        plt.cla()
        plt.clf()
        self.resize(720, 601)
        self.center()
        self.plot()



if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())