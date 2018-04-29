import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import configparser

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
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.player_value = config.get('SectionOne', 'player')
        self.border_value = config.get('SectionOne', "Border")
        self.acceleration_value = config.get('SectionOne', "Acceleration")
        self.speed_value = config.get('SectionOne', "Speed")
        self.maxSpeed_value = config.get('SectionOne', "Maximum speed")
        self.stepSpeed_value = config.get('SectionOne', "Step Speed")
        self.length_value = config.get('SectionOne', "length")
        self.fruitPrbbl_value = config.get('SectionOne', "Fruit probability")
        self.fruitMaxLife_value = config.get('SectionOne', "Fruit maximum lifespan")
        self.fruitMinLife_value = config.get('SectionOne', "Fruit minimum lifespan")
        self.fieldWidth_value = config.get('SectionOne', "Field width")
        self.fieldHigh_value = config.get('SectionOne', "Field high")
        self.scale_value = config.get('SectionOne', "Field zoom")

        #print("I'm in settings, parent", parent)
        #self.player_str = parent.player_str
        self.initUI(parent)

    def initUI(self, parent):
        #print(parent)
        #properties = Properties()
        form = qw.QFormLayout()

        self.player = qw.QLineEdit(self)
        self.player.setText(self.player_value)

        self.fieldWidth = qw.QLineEdit(self)
        self.fieldWidth.setText(self.fieldWidth_value)
        self.fieldHigh = qw.QLineEdit(self)
        self.fieldHigh.setText(self.fieldHigh_value)
        self.fruitPrbbl = qw.QLineEdit(self)
        self.fruitPrbbl.setText(self.fruitPrbbl_value)
        self.scale = qw.QLineEdit(self)
        self.scale.setText(self.scale_value)
        #self.player_str = self.player.text()

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
        form.addRow(qw.QLabel("Fruit probability"), self.fruitPrbbl)
        form.addRow(qw.QLabel("Fruit maximum lifespan"), qw.QLineEdit())
        form.addRow(qw.QLabel("Fruit minimum lifespan"), qw.QLineEdit())

        h2box = qw.QHBoxLayout()
        h2box.addWidget(self.fieldWidth)
        h2box.addWidget(qw.QLabel("x"))
        h2box.addWidget(self.fieldHigh)

        form.addRow(qw.QLabel("Field"), h2box)

        form.addRow(qw.QLabel("Field zoom"), self.scale)

        h3box = qw.QHBoxLayout()
        self.play = qw.QPushButton("Play", self)
        self.play.clicked.connect(self.close)
        self.play.clicked.connect(parent.showGame)
        h3box.addWidget(self.play)
        h3box.addStretch()
        self.highscore = qw.QPushButton("Highscore", self)
        #self.highscore.clicked.connect(self.on_click)
        h3box.addWidget(self.highscore)


        form.addRow(h3box)
        self.setLayout(form)

        #self.player_str = self.player.text()


    def closeEvent(self, event):
        #properties = Properties()
        print("closing Settings")
        print("")
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.set('SectionOne', 'player', self.player.text())
        config.set('SectionOne', 'Field zoom', self.scale.text())
        config.set('SectionOne', "Field width", self.fieldWidth.text())
        config.set('SectionOne', "Fruit probability", self.fruitPrbbl.text())
        config.set('SectionOne', "Field high", self.fieldHigh.text())
        with open('config.ini', "w") as config_file:
            config.write(config_file)


#win.setLayout(form)      # Wichtig! Erst hier wird das Layout an win angefügt
#win.show()

#app.exec_()

