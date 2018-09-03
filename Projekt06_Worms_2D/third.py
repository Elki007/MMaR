import sys
import random
import math
from datetime import datetime, timedelta
import numpy as np
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg



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

        self.setCentralWidget(MainMenu(self))

        self.show()



class MainMenu(qw.QWidget):
    def __init__(self, parent):
        qw.QWidget.__init__(self)
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
        self.parent.statusBar().hide()

    def on_click_b_hs(self):
        self.parent.statusBar().clearMessage()
        self.parent.statusBar().hide()
        #self.parent.setCentralWidget(Test(self.parent))

    def keyPressEvent(self, e):
        if e.key() == qc.Qt.Key_D:
            print("d")
        elif e.key() == qc.Qt.Key_A:
            print("a")


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

        self.canvas.fill(qg.QColor(0, 0, 0, 0))

        self.painter = qg.QPainter(self.canvas)
        self.painter2 = qg.QPainter(self.ebene2)


        ####################################################################################
        ####################################################################################
        ####################################################################################
        ####################################################################################
        ####################################################################################
        #default value is false - means track mouse only when at least one button is pressed
        self.setMouseTracking(True)
        self.grabKeyboard() #OMG 2 hours later!

        #self.player = Player(self,qc.Qt.darkGreen, qc.Qt.red, "Max")

        self.point = []
        self.point.append(Point(self))

        self.players=[]
        self.bullets = []

        self.players.append(Player(self,qc.Qt.darkGreen, qc.Qt.red, "Max",len(self.players)))
        self.bullets.append(None)

        self.players.append(Player(self,qc.Qt.darkCyan, qc.Qt.red, "Misha",len(self.players)))
        self.bullets.append(None)

        self.victory=False
        self.current_player = 0
        self.timer_begin = True
        self.r_start=datetime.now().time()


        self.time_for_round=10
        self.left = self.time_for_round

        self.initUI()

    def initUI(self):

        self.Run()

    def Run(self):
        try:
            #print("a")
            self.painter.setBrush(qg.QBrush(qg.QColor(33, 191, 243)))  # '#5DBCD2'
            self.painter.drawRect(-1, -1, self.parent.width() + 1, self.parent.height() + 1)

            alive=0
            for i in self.players:
                if i.hp>0:
                    alive+=1
            if alive == 1:
                for i in self.players:
                    if i.hp > 0:
                        self.painter.setPen(qc.Qt.black)
                        self.painter.setFont(qg.QFont('Helvetica', 12))
                        self.painter.drawText(200, 50, i.name +" won!")
                        self.victory=True
            else:
                self.time()

            #self.painter.setPen(qg.QPen.setWidthF(5))

            #self.painter.setPen(qg.QPen.setWidthF(1))
            self.update_const()

            for i in range(len(self.players)):
                self.players[i].paint()
                if self.bullets[i] != None:
                    self.bullets[i].paint()

            self.a = self.ebene2.toImage()
            self.setPixmap(self.canvas)
        finally:
            if self.victory ==False:
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
            #i[0,1] - x,y is a colliding point
            #i[2] is an explosion radius
            #drawEllipse uses x,y as a top left coordintes, that's why we need to perform some calc.
            self.painter2.drawEllipse(i[0]-i[2]/2, i[1]-i[2]/2, i[2], i[2])


        #draw layer
        self.painter.drawPixmap(0, 0, self.ebene2)
        #self.painter2.drawRect(self.parent.width() / 2 - 10, self.parent.height() / 2 - 10, 20, 20)
        # self.painter2.drawEllipse(self.parent.width()/2,self.parent.height()/2,2,2)



    def mouseMoveEvent(self, e):
        self.m_x = e.x()
        self.m_y = e.y()
        alpha = self.a.pixel(self.m_x, self.m_y)#.alpha()
        #self.parent.statusBar().showMessage(str(alpha))

    def mousePressEvent(self, e):
        #print("lclick", self.gun.v/10)
        if self.bullets[self.current_player] == None:
            self.bullets[self.current_player] = Bullet(self,self.current_player)

    def keyPressEvent(self, e):
        if e.key() == qc.Qt.Key_D:
            # if a slope is not vertical
            if self.a.pixel(self.players[self.current_player].x + 1, self.players[self.current_player].y - 6) == 0:
                self.players[self.current_player].x += 1
            #print("d")
        elif e.key() == qc.Qt.Key_A:
            # if a slope is not vertical
            if self.a.pixel(self.players[self.current_player].x - 1, self.players[self.current_player].y - 6) == 0:
                self.players[self.current_player].x -= 1
            #print("a")

    def time(self):
        if self.timer_begin == True:
            self.r_start = datetime.now()
            self.timer_begin=False

        time_pass= datetime.now()-self.r_start
        show =self.time_for_round - time_pass.seconds

        if show <0:
            self.timer_begin = True
            if self.current_player +1 >= len(self.players):
                self.current_player = 0
            else:
                self.current_player += 1

        self.painter.setPen(qc.Qt.black)
        self.painter.setFont(qg.QFont('Helvetica', 12))
        self.painter.drawText(50, 50, str(self.players[self.current_player].name) + ", it's your turn! Time left: " + str(show))

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

class Bullet:
    def __init__(self, parent,player_i):
        self.parent = parent
        self.i=player_i
        self.x = parent.players[self.i].x+parent.players[self.i].v[0]
        self.y = parent.players[self.i].y+parent.players[self.i].v[1]
        # self.v is gun direction
        # multiplying direction we will get power
        # 0.1 for direction and self.v[1]+=0.02 is perfect for a cannon

        self.weight = 1
        self.damage = self.weight * 20
        self.power = 0.11 / self.weight
        self.gravity = 0.02 * self.weight
        self.explosion = 10
        self.v = self.power*parent.players[self.i].v

    def paint(self):
        self.parent.painter.setPen(qg.QPen(qg.QColor(0, 0, 0), 2, qc.Qt.SolidLine))
        self.parent.painter.drawPoint(self.x, self.y)
        self.collide()
        self.x += self.v[0]
        self.y += self.v[1]
        self.v[1]+=self.gravity#0.01 smth very light

    def collide(self):
        # check alpha chanel
        if self.parent.a.pixel(self.x,self.y) != 0:
            while self.parent.a.pixel(self.x,self.y) != 0:
                self.x -= self.v[0]/100
                self.y -= self.v[1]/100
            x=round(self.x)
            y=round(self.y)
            self.parent.collisions.append([x,y, self.explosion])
            self.parent.bullets[self.i] = None

            ####first implement - we are looking only at ground
            for i in self.parent.players:
                if abs(i.x-x) < i.w/2 + self.explosion/2:
                    #abs(i.x - x) - i.w # distance to body
                    koeff = 1-(abs(i.x - x) - i.w/2)/(self.explosion/2) #dmg.koeff
                    if koeff > 1: koeff=1
                    i.hp -= self.damage*koeff
                    #if i.hp<0:
                        #print("dead!")
                        #del self.parent.players[i.i]

                    #print(koeff)


class Player:
    def __init__(self, parent, color, gun_color,name,i):
        self.parent = parent
        self.name = name
        self.i=i
        self.x = random.randint(50,400)
        self.y = 200
        self.len = 20
        self.color = color
        self.hp = 100
        self.w=25
        self.h=12
        self.g_color = gun_color
        #self.v is
        self.v = np.array([1,1])

    def paint(self):
        ##body
        if self.hp<0:
            self.color = qc.Qt.gray
            self.g_color = qc.Qt.gray
        self.parent.painter.setPen(qg.QPen(self.color, 2, qc.Qt.SolidLine))
        self.parent.painter.setBrush(qg.QBrush(self.color))
        self.parent.painter.drawRect(self.x-self.w/2,self.y-self.h/2,self.w,self.h)

        ##hp bar
        percent=self.hp/100
        color=qc.Qt.green
        if self.hp<40:
            color=qc.Qt.red
        elif self.hp<80:
            color=qc.Qt.yellow
        if self.hp > 0:
            self.parent.painter.setPen(qg.QPen(color, 2, qc.Qt.SolidLine))
            self.parent.painter.setBrush(qg.QBrush(color))

        self.parent.painter.drawRect(self.x - self.w / 2, self.y + self.h + 2, self.w*percent, 2)

        ##gun
        ###do not update self.v if it is not your turn!
        if self.parent.current_player == self.i:
            v = np.array([self.parent.m_x-self.x,self.parent.m_y-self.y])
            if np.linalg.norm(v)!=0:
                self.v= v / np.linalg.norm(v)
                self.v*=self.len

        self.parent.painter.setPen(qg.QPen(self.g_color, 2, qc.Qt.SolidLine))
        self.parent.painter.drawLine(self.x, self.y, self.x+self.v[0], self.y+self.v[1])

        ###check if on ground
        self.on_ground()

    def on_ground(self):
        # check alpha chanel
        if self.parent.a.pixel(self.x, self.y) == 0:
                self.y += 1
        # if we will move a player and it hits the ground
        elif self.parent.a.pixel(self.x, self.y-1) != 0:
            self.y -=1



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