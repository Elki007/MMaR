import sys
import random
import math
import numpy as np
from datetime import datetime, timedelta
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from Scene import SceneWindow



# Settings for the window in general
class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(768)
        self.setMinimumWidth(1366)
        self.zoom = 1
        self.init_ui()

    def init_ui(self):
        self.statusBar().showMessage('online')
        # self.setGeometry(300, 300, 250, 150)  # none - default window position?
        self.setWindowTitle('3D Engine')
        self.setCentralWidget(MainMenu(self))

        #self.center()  # move window to the screens center?

        self.show()

    def center(self):  ##### screen center
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# Settings for main menu - first displayed menu
class MainMenu(qw.QWidget):
    def __init__(self, parent):
        qw.QWidget.__init__(self)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Menu items
        b_newgame = qw.QPushButton("2D -> 3D")
        # b_highscore = qw.QPushButton("High score")  # tbd
        # b_settings = qw.QPushButton("Settings")  # tbd
        # b_credits = qw.QPushButton("Credits")  # tbd
        b_exit = qw.QPushButton("Exit")

        # Menu actions
        b_newgame.clicked.connect(self.on_click_b_newgame)
        # b_newgame.connect = parent.setCentralWidget(qw.QPushButton("inside Game"))
        # b_highscore.clicked.connect(self.on_click_b_highscore)
        # b_settings.clicked.connect(self.on_click_b_settings)
        # b_credits.clicked.connect(self.on_click_b_credits)
        b_exit.clicked.connect(self.on_click_b_exit)

        # Layout of menu
        hbox = qw.QHBoxLayout()
        vbox = qw.QVBoxLayout()

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        vbox.addStretch(1)
        vbox.addWidget(b_newgame)
        # vbox.addWidget(b_highscore)
        # vbox.addWidget(b_settings)
        # vbox.addWidget(b_credits)
        vbox.addWidget(b_exit)
        vbox.addStretch(1)

        self.setLayout(hbox)

    # Functions for clicked menu items
    def on_click_b_newgame(self):
        # print('PyQt5 button click')
        # self.parent.setCentralWidget(qw.QPushButton("inside Game"))
        self.parent.setCentralWidget(SceneWindow(self.parent))
        self.parent.statusBar().clearMessage()
        self.parent.statusBar().hide()

    def on_click_b_highscore(self):
        self.parent.statusBar().clearMessage()
        # self.parent.statusBar().hide()
        # self.parent.setCentralWidget(Test(self.parent))

    def on_click_b_settings(self):
        pass

    def on_click_b_credits(self):
        pass

    def on_click_b_exit(selfs):
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())