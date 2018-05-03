from PyQt5 import QtWidgets as qw
import configparser

#app = qw.QApplication(sys.argv)

#
# QFormLayout
#

class Highscores(qw.QFrame):

    def __repr__(self):
        return "Highscores"

    def __str__(self):
        return "Highscores"

    def __init__(self, parent):
        super().__init__()

        self.initUI(parent)

    def initUI(self, parent):
        #print(parent)
        #properties = Properties()
        hs = []
        config = configparser.ConfigParser()
        config.read('highscores.ini')
        path_items = config.items("HIGHSCORES")
        i=0
        for player, score in path_items:
            hs.append((int(score),player))
        sorted = False
        while not sorted:
            sorted = True
            for i in range(len(hs)-1):
                if hs[i][0] < hs[i+1][0]:
                    sorted = False
                    hs[i],hs[i + 1] = hs[i + 1],hs[i]
        #print(hs)
        #btn_HS = qw.QPushButton('High scores', self)
        table_HS = qw.QTableWidget()

        table_HS.setRowCount(10)
        table_HS.setColumnCount(2)
        for i in range(10):
            table_HS.setItem(i, 0, qw.QTableWidgetItem(hs[i][1]))
            table_HS.setItem(i, 1, qw.QTableWidgetItem(str(hs[i][0])))
            if i == len(hs)-1:
                break


        vbox = qw.QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addWidget(table_HS)
        #vbox.addStretch(1)

        hbox = qw.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)


#win.setLayout(form)      # Wichtig! Erst hier wird das Layout an win angef�gt
#win.show()

#app.exec_()

