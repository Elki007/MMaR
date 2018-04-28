import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

#app = qw.QApplication(sys.argv)

#
# QFormLayout
#

class Settings(qw.QFrame):

    def __repr__(self):
        return "Settings"

    def __str__(self):
        return "Settings"

    def __init__(self, parent):
        super().__init__()
        #print("I'm in settings, parent", parent)
        self.player_str = parent.player_str
        self.initUI(parent)

    def initUI(self, parent):
        #print(parent)
        form = qw.QFormLayout()

        self.player = qw.QLineEdit(self)
        self.player.setText(self.player_str)
        self.player_str = self.player.text()

        form.addRow(qw.QLabel("Player"), self.player)


        hbox = qw.QHBoxLayout()
        hbox.addWidget(qw.QCheckBox("on"))
        hbox.addWidget(qw.QCheckBox("off"))

        form.addRow(qw.QLabel("Border"), hbox)

        form.addRow(qw.QLabel("Acceleration"), qw.QLineEdit())
        form.addRow(qw.QLabel("Speed"), qw.QLineEdit())
        form.addRow(qw.QLabel("Maximum speed"), qw.QLineEdit())
        form.addRow(qw.QLabel("Step Speed"), qw.QLineEdit())
        form.addRow(qw.QLabel("length"), qw.QLineEdit())
        form.addRow(qw.QLabel("Fruit probability"), qw.QLineEdit())
        form.addRow(qw.QLabel("Fruit maximum lifespan"), qw.QLineEdit())
        form.addRow(qw.QLabel("Fruit minimum lifespan"), qw.QLineEdit())

        h2box = qw.QHBoxLayout()
        h2box.addWidget(qw.QLineEdit())
        h2box.addWidget(qw.QLabel("x"))
        h2box.addWidget(qw.QLineEdit())

        form.addRow(qw.QLabel("Spielfeldgröße"), h2box)

        form.addRow(qw.QLabel("Spielfeldzoom"), qw.QLineEdit())

        h3box = qw.QHBoxLayout()
        self.play = qw.QPushButton("Play", self)
        self.play.clicked.connect(self.close)
        self.play.clicked.connect(parent.showGame)
        h3box.addWidget(self.play)
        h3box.addStretch()
        self.highscore = qw.QPushButton("Highscore-Liste", self)
        #self.highscore.clicked.connect(self.on_click)
        h3box.addWidget(self.highscore)


        form.addRow(h3box)
        self.setLayout(form)

        self.player_str = self.player.text()


    def intraShowGame(self):
        #print(self.parent())
        #parent.showGame
        #parent.player = self.player.text()
        print("intra")

    def closeEvent(self, event):
        print("closing Settings")
        print("")
        # report_session()

#win.setLayout(form)      # Wichtig! Erst hier wird das Layout an win angefügt
#win.show()

#app.exec_()

