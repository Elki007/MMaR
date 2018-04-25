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
        impAct = qw.QAction('Defaults', self)
        impMenu.addAction(impAct)


        newAct = qw.QAction('New', self)
        menu_quit = qw.QAction('Quit', self)
        menu_quit.triggered.connect(self.close)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        fileMenu.addAction(menu_quit)

        #########################Window#########################
        btn_newgame = qw.QPushButton('New game', self)
        btn_newgame.move(350, 200)

        btn_HS = qw.QPushButton('High scores', self)
        btn_HS.move(350, 250)

        btn_Quit = qw.QPushButton('Quit', self)
        btn_Quit.move(350, 300)
        btn_Quit.clicked.connect(self.close)


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



if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = Main_window()
    sys.exit(app.exec_())