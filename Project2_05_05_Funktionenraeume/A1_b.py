import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt
import sys

import PyQt5.QtWidgets as qw

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import random


class App(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'Aufgabe 1: Spline Kurven'
        self.width = 640
        self.height = 400
        self.setFixedSize(self.width, self.height)
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.canvas = PlotCanvas(self, width=5, height=4)
        self.canvas.move(0, 0)

        self.clear = qw.QPushButton('Clear', self)
        self.clear.setToolTip('Clear the Graph')
        self.clear.clicked.connect(self.on_click_clear)
        self.clear.move(500, 0)
        self.clear.resize(140, 100)

        self.plot = qw.QPushButton('Plot', self)
        self.plot.setToolTip('Plot a Graph')
        self.plot.clicked.connect(self.on_click_plot)
        self.plot.move(500, 100)
        self.plot.resize(140, 100)

        self.show()

    def on_click_clear(self):
        self.canvas.clear()
        print(self.canvas.test_cv)
        print("clear")

    def on_click_plot(self):
        if len(self.canvas.test_cv) >= 4:
            self.canvas.plot()
        print("plot")


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.parent = parent
        self.test_cv = np.array([]).reshape(0,2)
        self.cv = np.array([[ 50.,  25.],
                            [ 57.,   2.],
                            [ 45.,   20.],
                            [ 40.,   14.]])


        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        self.ax.set_xlim(0, 400)
        self.ax.set_ylim(0, 300)
        FigureCanvas.setSizePolicy(self,
                                   qw.QSizePolicy.Expanding,
                                   qw.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        #self.plot()

    def plot(self):

        def bspline(cv, n=100, degree=3):
            """ Calculate n samples on a bspline

                cv :      Array ov control vertices
                n  :      Number of samples to return
                degree:   Curve degree
            """
            cv = np.asarray(cv)
            count = len(cv)

            degree = np.clip(degree,1,count-1)

            # Calculate knot vector
            kv = None
            kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)

            # Calculate query range
            u = np.linspace(False,(count-degree),n)

            # Calculate result
            return np.array(si.splev(u, (kv,cv.T,degree))).T

        p = bspline(self.test_cv, n=100)
        x, y = p.T
        print(self.test_cv)
        #print(x,y)

        self.ax.plot(self.test_cv[:,0],self.test_cv[:,1], 'o-', 'green', label='Control Points')
        self.ax.plot(x, y, 'k-', label='Degree %s' % 3)
        self.ax.axis('off')
        #ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def clear(self):
        self.test_cv = np.array([]).reshape(0, 2)
        self.fig.clf()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 400)
        self.ax.set_ylim(0, 300)
        self.ax.axis('off')
        self.draw()

    def mousePressEvent(self, event):
        x = event.pos().x() -55
        y = 350 - event.pos().y()
        self.test_cv = np.r_[self.test_cv, [[x, y]]]
        self.draw_cv()


    def draw_cv(self):
        self.fig.clf()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 400)
        self.ax.set_ylim(0, 300)
        self.ax.axis('off')

        self.ax.plot(self.test_cv[:, 0], self.test_cv[:, 1], 'o-', 'green', label='Control Points')
        self.draw()


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
