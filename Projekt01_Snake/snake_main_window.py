import sys
import time
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from snake_settings import Settings


class Main_window(qw.QMainWindow):


    def halloYeah(self):
        y = 4
        x = y


    def __repr__(self):
        return "Main_Max()"

    def __str__(self):
        return "Main_window"

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
        new_game.triggered.connect(self.showSettings)
        menu_quit = qw.QAction('Quit', self)
        #menu_quit.triggered.connect(self.close)
        menu_quit.triggered.connect(self.close)

        fileMenu.addAction(new_game)
        fileMenu.addMenu(impSettings)
        fileMenu.addAction(menu_quit)

        #########################Window#########################

        #self.main_widget = Settings()
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


    def showSettings(self):
        print("call Settings")
        print("who is self:", self)
        #Main_window.main_widget = Settings()
        self.setCentralWidget(Settings())


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
        btn_HS = qw.QPushButton('High scores', self)
        btn_Quit = qw.QPushButton('Quit', self)
        btn_Quit.clicked.connect(Main_window.close)

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
        app = qg.QApplication.instance()
        app.closeAllWindows()


    def open_settings(self):
        self.close()
        Main_window.showSettings(self)


    def on_pushButtonClose_clicked(self):
        app = qg.QApplication.instance()
        app.closeAllWindows()

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = Main_window()
    sys.exit(app.exec_())
