import sys
from PyQt5 import QtWidgets as qw
from Draw_v3 import DrawWidget


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        #qw.QMainWindow.__init__(self)  # why not?
        # set Window to screen height/2 and width/2
        self.setMinimumHeight(qw.QDesktopWidget().height()//1.5)
        self.setMinimumWidth(qw.QDesktopWidget().width()//1.5)
        # print(self)  # prints 'MainWindow' (__repr__)
        # print(self.height(), self.width())  # prints current hight and width
        self.init_ui()

        self.setObjectName("MainWindow")  # to be able to refer to it in our new stylish css :)
        with open("stylesheet.css", "r") as style:  # reads stylesheets
            self.setStyleSheet(style.read())

    def __repr__(self):
        return str("MainWindow")

    def init_ui(self):
        self.setWindowTitle('Symmetry')
        self.setCentralWidget(MainMenu(self))
        self.show()


# Settings for main menu - first displayed menu
class MainMenu(qw.QWidget):
    def __init__(self, parent):
        #super().__init__()  # why not?
        qw.QWidget.__init__(self)
        self.parent = parent
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.init_ui()

        self.setObjectName("MainMenu")
        with open("stylesheet.css", "r") as style:  # reads stylesheets
            self.setStyleSheet(style.read())

    def __repr__(self):
        return str("MainMenu")

    def init_ui(self):

        # Title
        prog_title = qw.QLabel()
        prog_title.setObjectName("Title")
        prog_title.setText("Symmetrie - Malprogramm")

        # Menu items
        b_start = qw.QPushButton("Paint")
        # b_button02 = qw.QPushButton("Button 2")
        # b_button03 = qw.QPushButton("Button 3")
        b_exit = qw.QPushButton("Exit")

        # Menu actions
        b_start.clicked.connect(self.on_click_b_start)
        b_start.setObjectName("StartButton")
        # b_button02.clicked.connect(self.on_click_b_button02)
        # b_button03.clicked.connect(self.on_click_b_button03)
        b_exit.clicked.connect(self.on_click_b_exit)
        b_exit.setObjectName("ExitButton")

        # Layout of menu
        hbox = qw.QHBoxLayout()
        vbox = qw.QVBoxLayout()

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        vbox.addStretch(8)
        vbox.addWidget(prog_title)
        vbox.addStretch(8)
        vbox.addWidget(b_start)
        vbox.addStretch(1)
        # vbox.addWidget(b_button02)
        # vbox.addWidget(b_button03)
        vbox.addWidget(b_exit)
        vbox.addStretch(16)

        self.setLayout(hbox)

    # Functions for clicked menu items
    def on_click_b_start(self):
        self.parent.setCentralWidget(DrawWidget(self))

    def on_click_b_button02(self):
        self.parent.statusBar().clearMessage()
        # self.parent.statusBar().hide()
        # self.parent.setCentralWidget(Test(self.parent))

    def on_click_b_button03(self):
        pass

    @staticmethod
    def on_click_b_exit():
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    execute = MainWindow()
    sys.exit(app.exec_())
