import sys
import math
import numpy as np
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

import timeit

# Diese Datei dient zur Veranschaulichung, wie der Wind generiert wird

class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(480)
        self.setMinimumWidth(600)
        self.zoom = 1
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Wind Map')

        self.setCentralWidget(GameWindow(self))

        self.show()


# Settings for the window with the actual game
class GameWindow(qw.QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.map = np.zeros([self.parent.width(), self.parent.height()], dtype=np.bool)

        self.canvas = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                 self.parent.height() * self.parent.zoom)  # oder QImage

        # make layer transparent (alpha channel = 0)
        self.canvas.fill(qg.QColor(0, 0, 0, 0))

        # Qt5 tools to paint
        self.painter = qg.QPainter(self.canvas)

        # Generate Wind
        self.wind_factor = 1  # max strength of wind in both directions (absolute value not bigger than wind_factor)
        self.wind_sinus_count = 3  # how many sinus functions are added
        self.function_zoom = np.linspace(start=0.007, stop=0.015, num=self.wind_sinus_count)  # 0.05 - 0.1
        self.wind_random_one = np.random.uniform(0, 4 * math.pi, self.wind_sinus_count)
        self.wind_random_two = np.random.uniform(0, 4 * math.pi, self.wind_sinus_count)

        # will be set in wind_generator was generated
        self.wind_max_lowest = 0
        self.wind_max_highest = 0

        # 2d-array of wind power coordinates
        self.wind_map = self.wind_generator()

        self.init_ui()

    def init_ui(self):
        self.run()

    def run(self):
        self.painter.setBrush(qg.QBrush(qg.QColor(0, 0, 0)))  # '#5DBCD2'
        self.painter.setPen(qg.QPen(qg.QColor(0, 0, 0)))
        self.painter.drawRect(0, 0, self.parent.width(), self.parent.height())

        # Zeichnet wind_map von
        # blau (links) rgb(0, 0, 255) nach
        # über (0) -> schwarz (0, 0, 0) nach
        # rot (rechts) rgb(255, 0, 0)

        links = [0, 0, 255]  # blau
        still = [0, 0, 0]  # schwarz
        rechts = [255, 0, 0]  # rot

        print(len(self.wind_map), ",", len(self.wind_map[0]))
        print(self.canvas.width())
        self.painter.setPen(qg.QPen(qg.QColor(255, 255, 255)))
        self.painter.drawPoint(10, 10)

        # pixel for pixel will be set to a color dependent on value in wind_map
        for i in range(self.parent.height()):
            for j in range(self.parent.width()):
                #print(int(255 * self.wind_map[i][j] / self.wind_factor))
                if self.wind_map[i][j] >= 0:
                    red = int(255 * self.wind_map[i][j] / self.wind_max_highest)
                    #red = int(red + (1 / (red / 500) - 2))
                    if red >= 255: red = 255
                    self.painter.setPen(qg.QPen(qg.QColor(red, 0, 0)))
                elif self.wind_map[i][j] < 0:
                    blue = abs(int(255 * self.wind_map[i][j] / self.wind_max_lowest))
                    #blue = int(blue + (1 / (blue / 500) - 2))
                    if blue >= 255: blue = 255
                    self.painter.setPen(qg.QPen(qg.QColor(0, 0, blue)))
                else:
                    self.painter.setPen(qg.QPen(qg.QColor(255, 255, 255)))
                self.painter.drawPoint(j, i)

        self.setPixmap(self.canvas)

    def wind_generator(self):

        # map2d creates an 2d array with
        def calculate_wind(map2d):
            # Standard: lambda j, k: np.sin(self.function_zoom[i] * k + self.wind_random_one[i]) *
            #                                np.sin(self.function_zoom[i] * j + self.wind_random_two[i]) *
            #                                self.wind_factor
            for i in range(self.wind_sinus_count):
                map2d += np.fromfunction(lambda j, k: np.sin(self.function_zoom[i] * k + self.wind_random_one[i]) *
                                         np.sin(self.function_zoom[i] * j + self.wind_random_two[i])
                                         / self.wind_sinus_count * self.wind_factor,
                                         (self.parent.height(), self.parent.width()))

        timer_start = timeit.default_timer()

        wind_map2d = np.zeros(shape=(self.parent.height(), self.parent.width()))
        calculate_wind(wind_map2d)

        timer_stop = timeit.default_timer()
        #print("wind_map generation time: ", timer_stop - timer_start)

        self.wind_max_highest = max([max(inner_array) for inner_array in wind_map2d])
        self.wind_max_lowest = min([min(inner_array) for inner_array in wind_map2d])

        print("Maximalwert:", self.wind_max_highest)
        print("Minimalwert:", self.wind_max_lowest)

        return wind_map2d


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
