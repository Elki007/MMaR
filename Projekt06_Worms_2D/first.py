import sys
import random
import math
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(480)
        self.setMinimumWidth(600)
        self.h = 480
        self.w = 600
        self.z = 1

        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('online')


        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Worms 2D')

        self.setCentralWidget(MainMenu(self))

        self.show()


class MainMenu(qw.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        b_ng = qw.QPushButton("New Game")
        b_ng.clicked.connect(self.on_click_b_ng)
        #b_ng.connect = parent.setCentralWidget(qw.QPushButton("inside Game"))
        b_hs = qw.QPushButton("High score")
        b_hs.clicked.connect(self.on_click_b_hs)
        b_st = qw.QPushButton("Settings")
        b_cr = qw.QPushButton("Credits")
        b_ex = qw.QPushButton("Exit")
        hbox = qw.QHBoxLayout()
        vbox = qw.QVBoxLayout()

        vbox.addStretch(1)
        vbox.addWidget(b_ng)
        vbox.addWidget(b_hs)
        vbox.addWidget(b_st)
        vbox.addWidget(b_cr)
        vbox.addWidget(b_ex)
        vbox.addStretch(1)

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def on_click_b_ng(self):
        #print('PyQt5 button click')
        self.parent.setCentralWidget(qw.QPushButton("inside Game"))

    def on_click_b_hs(self):
        self.parent.statusBar().clearMessage()
        self.parent.statusBar().hide()
        self.parent.setCentralWidget(Test(self.parent))


class Test(qw.QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # layers
        self.canvas = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage
        self.ebene2 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage

        self.point=[]
        for i in range(100):
            self.point.append(Point(self))
        self.initUI()

    def initUI(self):
        self.update_const()
        self.f()

    def update_const(self):

        #make 'em transparent (alpha channel = 0)
        self.canvas.fill(qg.QColor(0, 0, 0, 0))
        self.ebene2.fill(qg.QColor(0, 0, 0, 0))

        #connect paint methods to layers
        self.painter = qg.QPainter(self.canvas)
        self.painter2 = qg.QPainter(self.ebene2)
        self.painter2.setBrush(qg.QBrush(qg.QColor('#773b19')))
        self.painter2.drawRect(0, self.parent.height()-80, self.parent.width(), 80)
        self.painter2.setBrush(qg.QBrush(qg.QColor(0, 0, 0)))
        #self.painter2.drawRect(self.parent.width() / 2 - 10, self.parent.height() / 2 - 10, 20, 20)
        # self.painter2.drawEllipse(self.parent.width()/2,self.parent.height()/2,2,2)

    def f(self):
        try:
            #self.update_const()
            # no need in rect - black by default (changed to transparent)
            self.painter.setBrush(qg.QBrush(qg.QColor(0, 0, 0)))  # '#5DBCD2'
            self.painter.drawRect(-1, -1, self.parent.width() + 1, self.parent.height() + 1)

            self.painter.setPen(qg.QPen(qg.QColor(255,255,255)))

            for i in range(100):
                if self.point[i].y == 0:
                    print("x,y: ", self.point[i].x, self.point[i].y)
                self.point[i].show()
                if self.point[i].x<0 or self.point[i].x > self.parent.width():
                    self.point[i].initialize()
                    #print("x,y: ",self.point[i].x,self.point[i].y)
                if self.point[i].y<0 or self.point[i].y > self.parent.height():
                    self.point[i].initialize()
                    #print("x,y: ", self.point[i].x, self.point[i].y)
            #self.painter.drawPoint(self.x,self.y)
            #self.x +=1
            #self.y +=1

            # draw a layer - painer drows ebene2 on canvas (as painer is connected with canvas)
            self.painter.drawPixmap(0, 0, self.ebene2)

            # display all
            self.setPixmap(self.canvas)
        finally:
            qc.QTimer.singleShot(16, self.f)


class vector_2d:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __repr__(self):
        return str(self.x) +" "+ str(self.y)

    def normalize(self):
        self.x = self.x / (math.sqrt(self.x*self.x + self.y*self.y))
        self.y = self.y / (math.sqrt(self.x*self.x + self.y*self.y))

    def __add__(self, other):
        return vector_2d(self.x+other.x,self.y+other.y)

    def __sub__(self, other):
        return vector_2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if other is vector_2d:
            return self.x * other.x + self.y * other.y
        return vector_2d(self.x * other, self.y * other)

class Point:
    def __init__(self, parent):
        self.parent=parent
        self.x = random.randint(1, parent.parent.width() - 1)
        self.y = random.randint(1, parent.parent.height() - 1)
        self.r = vector_2d(self.x - parent.parent.width()/2, self.y - parent.parent.height()/2)
        self.r.normalize()
        self.v = 10
        #300 = max distance between center and point
        #self.v = 2*(1+300/math.sqrt(self.x**2 + self.y**2))

    def initialize(self):
        self.x = self.parent.parent.width()/2
        self.y = self.parent.parent.height()/2
        cho=[1,1]
        self.r.x = random.choice(cho)*math.sin(random.uniform(0,2*math.pi))
        self.r.y = random.choice(cho)*math.cos(random.uniform(0,2*math.pi))
        self.r.normalize()

        self.x += self.r.x
        self.y += self.r.y
        #self.r = vector_2d(self.x - self.parent.parent.width() / 2, self.y - self.parent.parent.height() / 2)

        #print(self.r)
        # 300 = max distance between center and point
        self.velocity_upd()

    def velocity_upd(self):
        diagonal = math.sqrt((self.parent.parent.width()) ** 2 + (self.parent.parent.height()) ** 2)
        a = math.sqrt((self.x - self.parent.parent.width() / 2) ** 2 + (self.y - self.parent.parent.height() / 2) ** 2)


        koeff = 20*a/diagonal
        self.v *=koeff
        #if self.v<1:
            #self.v=1
        #print(self.v)

    def show(self):
        self.parent.painter.drawPoint(self.x, self.y)
        self.velocity_upd()
        self.x += self.r.x * self.v
        self.y += self.r.y * self.v


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


