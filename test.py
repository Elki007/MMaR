import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class Main_window(qw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        #########################Menu#########################
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Game')

        impMenu = qw.QMenu('Settings', self)
        impCus = qw.QAction('Customize', self)
        impDef = qw.QAction('Defaults', self)
        impMenu.addAction(impCus)
        impMenu.addAction(impDef)

        newAct = qw.QAction('New', self)
        menu_quit = qw.QAction('Quit', self)
        #menu_quit.triggered.connect(self.close)
        menu_quit.triggered.connect(self.close)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        fileMenu.addAction(menu_quit)

        #########################Window#########################

        self.main_widget = Main_menu()
        self.setCentralWidget(self.main_widget)

        #########################Initialize#########################
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Snake')
        self.setWindowIcon(qg.QIcon('icon.png'))
        self.show()

    def center(self):   ##### screen center
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event): #### Dialog on quit
        reply = qw.QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", qw.QMessageBox.Yes |
                                     qw.QMessageBox.No, qw.QMessageBox.No)

        if reply == qw.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Main_menu(qw.QFrame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn_newgame = qw.QPushButton('New game', self)
        btn_HS = qw.QPushButton('High scores', self)
        btn_Quit = qw.QPushButton('Quit', self)
        btn_Quit.clicked.connect(self.close)

        vbox = qw.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(btn_newgame)
        vbox.addWidget(btn_HS)
        vbox.addWidget(btn_Quit)
        vbox.addStretch(1)

        hbox = qw.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)





if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = Main_window()
    sys.exit(app.exec_())
