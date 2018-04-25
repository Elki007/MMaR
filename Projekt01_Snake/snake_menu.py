import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
app = qw.QApplication(sys.argv)

#
# QFormLayout
#

win = qw.QWidget()

form = qw.QFormLayout()
form.addRow(qw.QLabel("Spielername"), qw.QLineEdit())


hbox = qw.QHBoxLayout()
hbox.addWidget(qw.QCheckBox("an"))
hbox.addWidget(qw.QCheckBox("aus"))

form.addRow(qw.QLabel("Randbegrenzung"), hbox)

form.addRow(qw.QLabel("Beschleunigungsfaktor"), qw.QLineEdit())
form.addRow(qw.QLabel("Startgeschwindigkeit"), qw.QLineEdit())
form.addRow(qw.QLabel("Maximale Geschwindigkeit"), qw.QLineEdit())
form.addRow(qw.QLabel("Schrittgröße"), qw.QLineEdit())
form.addRow(qw.QLabel("Anfangslänge"), qw.QLineEdit())
form.addRow(qw.QLabel("Früchtehäufigkeit"), qw.QLineEdit())
form.addRow(qw.QLabel("Früchte max Lebenslänge"), qw.QLineEdit())
form.addRow(qw.QLabel("Früchte min Lebenslänge"), qw.QLineEdit())

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



win.setLayout(form)      # Wichtig! Erst hier wird das Layout an win angefügt
win.show()

app.exec_()