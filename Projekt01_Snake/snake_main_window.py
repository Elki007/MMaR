import sys
import time
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from snake_settings import Settings
from snake_game import Board


class MainWindow(qw.QMainWindow):

    def __repr__(self):
        return "MainWindow"

    def __str__(self):
        return "MainWindow"

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        #########################Menu#########################
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('Game')

        impSettings = qw.QMenu('Settings', self)
        impCus = qw.QAction('Customize', self)
        impCus.triggered.connect(self.showSettings)
        impDef = qw.QAction('Defaults', self)

        impSettings.addAction(impCus)
        impSettings.addAction(impDef)

        new_game = qw.QAction('New game', self)
        new_game.triggered.connect(self.showGame)
        menu_quit = qw.QAction('Quit', self)
        #menu_quit.triggered.connect(self.close)
        menu_quit.triggered.connect(self.close)

        fileMenu.addAction(new_game)
        fileMenu.addMenu(impSettings)
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


    def keyPressEvent(self, e):
        key = e.key()

        if key == qc.Qt.Key_P:
            self.board.pause()
        elif key == qc.Qt.Key_Right:
            self.board.direct = 0
        elif key == qc.Qt.Key_Left:
            self.board.direct = 1
        elif key == qc.Qt.Key_Up:
            self.board.direct = 2
        elif key == qc.Qt.Key_Down:
            self.board.direct = 3


    def showSettings(self):
        print("call Settings")
        print("who is self:", self)
        #Main_window.main_widget = Settings()
        Board.close
        self.setCentralWidget(Settings())


    def showGame(self):
        print("call Game")
        print("who is self:", self)

        self.board = Board(self)
        board = self.board
        self.setCentralWidget(board)

        self.statusbar = self.statusBar()
        self.board.ScoreSignal[str].connect(self.statusbar.showMessage)

        board.start()

        self.resize(board.BoardWidth * board.scale, board.BoardHeight * board.scale)
        self.center()
        self.setWindowTitle('Snake')
        self.show()


class Main_menu(qw.QFrame):
    def __repr__(self):
        return "Main menu()"


    def __str__(self):
        return "Main menu"


    def __init__(self):
        super().__init__()
        print("main menu")
        self.initUI()


    def initUI(self):
        btn_newgame = qw.QPushButton('New game', self)
        #btn_newgame.clicked.connect(self.on_pushButtonCall_newGame())
        btn_HS = qw.QPushButton('High scores', self)
        btn_Quit = qw.QPushButton('Quit', self)
        btn_Quit.clicked.connect(self.on_pushButtonClose_clicked)

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


    def on_pushButtonClose_clicked(self):
        app = qw.QApplication.instance()
        app.closeAllWindows()


    def open_settings(self):
        self.close()
        MainWindow.showSettings(self)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
