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

    def __init__(self):
        super().__init__()
        print("I'm in settings")
        self.initUI()

    def initUI(self):
        print(self)
        form = qw.QFormLayout()
        form.addRow(qw.QLabel("Player"), qw.QLineEdit())


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
        h3box.addWidget(qw.QPushButton("Spiel starten"))
        h3box.addStretch()
        h3box.addWidget(qw.QPushButton("Highscore-Liste"))

        form.addRow(h3box)
        self.setLayout(form)


#win.setLayout(form)      # Wichtig! Erst hier wird das Layout an win angefügt
#win.show()

#app.exec_()

