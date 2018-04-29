import sys
import sip
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from snake_settings import Settings
from snake_game import Board
import configparser


class MainWindow(qw.QMainWindow):

    def __repr__(self):
        return "MainWindow"

    def __str__(self):
        return "MainWindow"

    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.player = config.get('SectionOne', 'player')
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

        ########initialize board as None #####################
        self.board = None
        #########################Window#########################

        self.main_widget = Main_menu(self)
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

    def defaultSettings(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.set('SectionOne', 'player', 'Player_1')
        config.set('SectionOne', "Border", "0")
        config.set('SectionOne', "Acceleration", "")
        config.set('SectionOne', "Speed", "500")
        config.set('SectionOne', "Maximum speed","1500")
        config.set('SectionOne', "Step Speed","10")
        config.set('SectionOne', "length", "3")
        config.set('SectionOne', "Fruit probability", "1")
        config.set('SectionOne', "Fruit maximum lifespan", "1")
        config.set('SectionOne', "Fruit minimum lifespan", "1")
        config.set('SectionOne', "Field", "20")
        config.set('SectionOne', "Field zoom", "30")
        with open('config.ini', "w") as config_file:
            config.write(config_file)

    def closeEvent(self, event): #### Dialog on quit
        reply = qw.QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", qw.QMessageBox.Yes |
                                     qw.QMessageBox.No, qw.QMessageBox.No)

        if reply == qw.QMessageBox.Yes:
            ############# place to set defaults##############
            self.defaultSettings()
            event.accept()
        else:
            event.ignore()


    def keyPressEvent(self, e):
        key = e.key()
        #print(self.board.direct)
        if key == qc.Qt.Key_P:
            self.board.pause()
        elif key == qc.Qt.Key_E:
            self.exit()
        elif key == qc.Qt.Key_Right:
            self.board.newdirect = 1
        elif key == qc.Qt.Key_Left:
            self.board.newdirect = -1
        elif key == qc.Qt.Key_Up:
            self.board.newdirect = 2
        elif key == qc.Qt.Key_Down:
            self.board.newdirect = -2

    def exit(self):
        ########## am i in board ? #############################
        if self.board != None:
            if self.board.timerOn:
                self.board.timer.stop()
            self.board.deleteLater()
            self.board = None
            ##################################################
            # Right place to show message that the game is over
            ##################################################
            self.setCentralWidget(Main_menu(self))

    def showSettings(self):
        #print(self.board)
        if self.board != None:
            if self.board.timerOn:
                self.board.timer.stop()
            self.board.deleteLater()
            self.board = None
            #Main_window.main_widget = Settings()
            Board.close
        #print("call Settings")
        #print("who is self:", self)
        self.setCentralWidget(Settings(self))


    def showGame(self):
        #print("call Game")
        #print("who is self:", self)
        #Settings.get_values(Settings, self)

        self.board = Board(self)
        board = self.board
        self.setCentralWidget(board)

        self.statusbar = self.statusBar()
        self.board.ScoreSignal[str].connect(self.statusbar.showMessage)



        self.resize((self.board.BoardWidth+1.1) * self.board.scale, (self.board.BoardHeight+2.5) * self.board.scale)
        self.center()

        board.start()



class Main_menu(qw.QFrame):
    def __repr__(self):
        return "Main menu()"


    def __str__(self):
        return "Main menu"


    def __init__(self,parent):
        super().__init__()
        #print("main menu")
        #print("parent", parent)
        self.initUI(parent)


    def initUI(self,parent):
        btn_newgame = qw.QPushButton('New game', self)
        btn_newgame.clicked.connect(parent.showGame)
        btn_HS = qw.QPushButton('High scores', self)
        btn_Quit = qw.QPushButton('Quit', self)
        btn_Quit.clicked.connect(parent.close)#self.on_pushButtonClose_clicked)

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


    ########## no need in this function, Question: are all processes terminated with self.close?###################
    #def on_pushButtonClose_clicked(self):
    #    app = qw.QApplication.instance()
    #    app.closeAllWindows()


    #def open_settings(self):
    #    self.close()
    #    MainWindow.showSettings(self)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
