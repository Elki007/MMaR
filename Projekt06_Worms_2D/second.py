import sys
import random
import math
import numpy as np
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

#test
class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(480)
        self.setMinimumWidth(600)
        self.z=1
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('online')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Worms 2D')

        self.setCentralWidget(GameWindow(self))

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
        #b_hs.clicked.connect(self.on_click_b_hs)
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
        self.parent.setCentralWidget(GameWindow(self.parent))
        self.parent.statusBar().clearMessage()
        #self.parent.statusBar().hide()

    def on_click_b_hs(self):
        self.parent.statusBar().clearMessage()
        self.parent.statusBar().hide()
        #self.parent.setCentralWidget(Test(self.parent))


class GameWindow(qw.QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.m_x=0
        self.m_y=0
        self.anz_max=10
        self.anz_start=1
        self.alpha=0
        self.map = np.zeros([self.parent.width(),self.parent.height()], dtype=np.bool)
        self.collisions=[]
        #print(self.collisions[1][1])

        self.canvas = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage
        self.ebene2 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage
        # make 'em transparent (alpha channel = 0)
        self.canvas.fill(qg.QColor(0, 0, 0, 0))
        self.ebene2.fill(qg.QColor(0, 0, 0, 0))

        self.a = self.ebene2.toImage()

        #self.canvas.fill(qg.QColor(0, 0, 0, 0))

        self.painter = qg.QPainter(self.canvas)
        self.painter2 = qg.QPainter(self.ebene2)



        #default value is false - means track mouse only when at least one button is pressed
        self.setMouseTracking(True)
        self.point = []
        self.point.append(Point(self))

        self.initUI()

    def initUI(self):

        self.Run()

    def Run(self):
        try:
            #print("a")
            self.painter.setBrush(qg.QBrush(qg.QColor(0, 0, 0)))  # '#5DBCD2'
            self.painter.drawRect(-1, -1, self.parent.width() + 1, self.parent.height() + 1)
            self.painter.setPen(qg.QPen(qg.QColor(255, 255, 255)))

            for i in range(self.anz_start):
                if self.point[i].y == 0:
                    self.point[i].initialize()
                    print("x,y: ", self.point[i].x, self.point[i].y)
                self.point[i].show()
                if self.point[i].x < 0 or self.point[i].x > self.parent.width():
                    self.point[i].initialize()
                    # print("x,y: ",self.point[i].x,self.point[i].y)
                if self.point[i].y < 0 or self.point[i].y > self.parent.height():
                    self.point[i].initialize()
            if self.anz_start< self.anz_max:
                self.anz_start+=1
                self.point.append(Point(self))

            self.update_const()

            self.a = self.ebene2.toImage()
            self.setPixmap(self.canvas)
        finally:
            qc.QTimer.singleShot(16, self.Run)

    def update_const(self):

        #make 'em transparent (alpha channel = 0)


        #connect paint methods to layers
        self.painter2.setBrush(qg.QBrush(qg.QColor('#773b19')))
        self.painter2.setCompositionMode(qg.QPainter.CompositionMode_DestinationOver)
        self.painter2.drawRect(0, self.parent.height()-80, self.parent.width(), 80)
        self.painter2.setBrush(qg.QBrush(qg.QColor(0, 0, 0)))


        self.painter2.setBrush(qg.QBrush(qg.QColor(0, 0, 0, 0)))
        self.painter2.setCompositionMode(qg.QPainter.CompositionMode_Clear)
        self.painter2.setPen(qc.Qt.black)
        self.painter2.setBrush(qc.Qt.black)
        #print(len(self.collisions))
        for i in self.collisions:
            self.painter2.drawEllipse(i[0],i[1], 10, 10)


        #draw layer
        self.painter.drawPixmap(0, 0, self.ebene2)
        #self.painter2.drawRect(self.parent.width() / 2 - 10, self.parent.height() / 2 - 10, 20, 20)
        # self.painter2.drawEllipse(self.parent.width()/2,self.parent.height()/2,2,2)

    def mouseMoveEvent(self, e):
        self.m_x = e.x()
        self.m_y = e.y()
        alpha = self.a.pixel(self.m_x, self.m_y)#.alpha()
        self.parent.statusBar().showMessage(str(alpha))

class vector_2d:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __repr__(self):
        return str(self.x) + " " + str(self.y)

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
        self.diagonal=(parent.parent.width()**2+ parent.parent.height()**2)**(1/2)
        self.x=parent.m_x
        self.y=parent.m_y
        self.start_x=self.x
        self.start_y=self.y
        rng=random.uniform(0,2*math.pi)
        self.r_x=math.sin(rng)
        self.r_y=math.cos(rng)
        self.v_max = random.randint(2,25)
        self.v=1
        self.x+=self.r_x
        self.y+=self.r_y

    def initialize(self):
        self.x = self.parent.m_x
        self.y = self.parent.m_y
        self.start_x = self.x
        self.start_y = self.y
        rng = random.uniform(0, 2 * math.pi)
        self.r_x = math.sin(rng)
        self.r_y = math.cos(rng)
        self.v=1
        self.x += self.r_x
        self.y += self.r_y

    def velocity_upd(self):
        #abstand_x = self.x - self.parent.m_x
        #abstand_y = self.y - self.parent.m_y
        abstand_x = self.x - self.start_x
        abstand_y = self.y - self.start_y
        abstand=(abstand_x**2+abstand_y**2)**(1/2)
        koeff=2*abstand/self.diagonal
        self.v = self.v_max*koeff

    def show(self):


        self.velocity_upd()
        self.x += self.r_x * self.v
        self.y += self.r_y * self.v
        self.parent.painter.drawPoint(self.x, self.y)
        self.collide()

    def collide(self):
        # check alpha chanel
        if self.parent.a.pixel(self.x,self.y) != 0:
            x=round(self.x-self.r_x)
            y=round(self.y-self.r_y)
            self.parent.collisions.append([x,y])
            self.initialize()
            #print("collide!")

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())