import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

from GuiWidget import GuiWidget


class App(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Project: Line Rider')
        self.setCentralWidget(GuiWidget(self))
        self.setMinimumHeight(qw.QDesktopWidget().height() // 2)
        self.setMinimumWidth(qw.QDesktopWidget().width() // 2)
        self.show()
