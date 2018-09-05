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

        self.center()

        self.show()

    def center(self):   ##### screen center
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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


class GameWindow(qw.QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.grabKeyboard()

        tank = qg.QImage("tank2.png")
        tank.scaled(50, 50)
        qtank = qg.QPixmap.fromImage(tank)
        self.tank = qtank.scaledToWidth(30)

        self.items = qw.QDockWidget("Weapon", self)

        self.weapon = qw.QComboBox()
        self.weapon.addItem("Cannon")
        self.weapon.addItem("Rifle gun")
        self.weapon.addItem("Bomb")

        self.items.setWidget(self.weapon)
        self.items.setFloating(False)
        #move to the right top
        self.items.setGeometry(520, 0, 0, 0)
        # disable close, dock buttons
        self.items.setFeatures(qw.QDockWidget.DockWidgetMovable)

        #mouse coordinates
        self.m_x=0
        self.m_y=0

        self.alpha=0
        self.map = np.zeros([self.parent.width(),self.parent.height()], dtype=np.bool)

        #an array of changes to original surface
        self.collisions=[]

        #generic surface
        self.ebene0 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage
        # first layer background
        self.ebene1 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage
        #second layer only surface
        self.ebene2 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage

        #objects
        self.ebene3 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage

        #interface
        self.ebene4 = qg.QPixmap(self.parent.width() * self.parent.z,
                                 self.parent.height() * self.parent.z)  # oder QImage

        # make 'em transparent (alpha channel = 0) 4th number in parameters
        self.ebene0.fill(qg.QColor(0, 0, 0, 0))
        self.ebene1.fill(qg.QColor(0, 0, 0, 0))
        self.ebene2.fill(qg.QColor(0, 0, 0, 0))
        self.ebene3.fill(qg.QColor(0, 0, 0, 0))
        self.ebene4.fill(qg.QColor(0, 0, 0, 0))

        #it is possible to check an alpha channel only if QPixmap is converted toImage
        self.a = self.ebene2.toImage()
        self.b = self.ebene2.toImage()

        #Generated Surface
        self.w=np.linspace(0.001,0.05,20)
        #self.x=np.linspace(0,self.width(),10)
        self.x=range(0,self.parent.width(),1)
        self.x_poly = range(self.parent.width())
        self.f_x = []
        self.rand_a = random.uniform(0,math.pi)
        self.rand_b = np.float64(random.uniform(-1,1))

        for i in self.x:
            #print(self.f(i))
            self.f_x.append(2*self.f(i))

        z = np.polyfit(self.x, self.f_x, 7)
        f = np.poly1d(z)
        self.ground2 = f(self.x_poly)

        self.ground2 = self.f_x
        #print(self.ground)
        #print(self.ground2)

        a=[]
        for i in range(self.parent.height()):
            b=[]
            for j in range(self.parent.width()):
                if i > self.ground2[j]+300:
                    b.append(True)
                else:
                    b.append(False)
            a.append(b)

        #self.ebene1.fill(qg.QColor(0, 0, 0, 0))

        #Qt5 tools to paint
        self.painter0 = qg.QPainter(self.ebene0)
        self.painter = qg.QPainter(self.ebene1)
        self.painter2 = qg.QPainter(self.ebene2)
        self.painter3 = qg.QPainter(self.ebene3)
        self.painter4 = qg.QPainter(self.ebene4)


        #draw dynamic surfase
        for j in range(self.parent.width()):
            self.surf_color_R = 255
            self.surf_color_G = 191
            self.surf_color_B = 102
            for i in range(self.parent.height()):
                if a[i][j]==True:
                    self.painter0.setPen(qg.QColor(self.surf_color_R, self.surf_color_G, self.surf_color_B))
                    self.painter0.drawPoint(j,i)
                    if self.surf_color_R >= 4 : self.surf_color_R -= 4
                    if self.surf_color_G >= 4 : self.surf_color_G -= 4
                    if self.surf_color_B >= 4 : self.surf_color_B -= 4

        #default value is false - means track mouse only when at least one button is pressed
        self.setMouseTracking(True)
        self.grabKeyboard() #OMG 2 hours later!

        self.players=[]
        self.bullets = []
        self.hits = []

        self.players.append(Player(self,qc.Qt.darkGreen, qc.Qt.red, "Max",len(self.players)))
        self.bullets.append(None)

        self.players.append(Player(self,qc.Qt.darkCyan, qc.Qt.red, "Misha",len(self.players)))
        self.bullets.append(None)

        #flag to stop the Game
        self.victory=False
        # game settings
        self.time_for_round = 10
        self.game_speed = 16
        self.gravity = 0.01

        #timer settings
        self.current_player = 0
        self.timer_begin = True
        self.r_start=datetime.now().time()

        self.initUI()

    def initUI(self):

        self.Run()

    def Run(self):
        try:
            #renew layer 3,4
            self.ebene3.fill(qg.QColor(0, 0, 0, 0))
            self.ebene4.fill(qg.QColor(0, 0, 0, 0))


            #sky
            self.painter.setBrush(qg.QBrush(qg.QColor(33, 191, 243)))  # '#5DBCD2'
            self.painter.drawRect(-1, -1, self.parent.width() + 1, self.parent.height() + 1)


            #after sky we draw second layer - surface
            self.update_surface()
            self.a = self.ebene2.toImage()

            alive=0
            for i in self.players:
                if i.hp>0:
                    alive+=1
            if alive == 1:
                for i in self.players:
                    if i.hp > 0:
                        self.painter4.setPen(qc.Qt.black)
                        self.painter4.setFont(qg.QFont('Helvetica', 12))
                        self.painter4.drawText(200, 50, i.name +" won!")
                        self.victory=True
            elif alive == 0:
                self.painter4.setPen(qc.Qt.black)
                self.painter4.setFont(qg.QFont('Helvetica', 12))
                self.painter4.drawText(200, 50, "Well played! Nobody alive!")
                self.victory = True
            else:
                self.time()

            for i in range(len(self.players)):
                self.players[i].paint()
            #layer 3 is for objects, so we will find there is it not transparent
            self.b = self.ebene3.toImage()


            for i in range(len(self.players)):
                if self.bullets[i] != None:
                    self.bullets[i].paint()

            for i in range(len(self.hits)-1,-1,-1):
                self.hits[i].paint()
                if self.hits[i].destruct == True:
                    del self.hits[i]

            #test why does the frame sets to pen color?
            self.painter.setPen(qc.Qt.black)
            self.painter2.setPen(qc.Qt.black)
            self.painter3.setPen(qc.Qt.black)
            self.painter4.setPen(qc.Qt.black)

            #self.painter2.drawPixmap(0, 0, self.ebene3)
            self.painter.drawPixmap(0, 0, self.ebene2)
            self.painter.drawPixmap(0, 0, self.ebene3)
            self.painter.drawPixmap(0, 0, self.ebene4)
            self.setPixmap(self.ebene1)

        finally:
            if self.victory ==False:
                qc.QTimer.singleShot(self.game_speed, self.Run)
            else:
                buttonReply = qw.QMessageBox.question(self, 'Worms 2D', "Would you like to play again?",
                                                   qw.QMessageBox.Yes | qw.QMessageBox.No, qw.QMessageBox.No)
                if buttonReply == qw.QMessageBox.Yes:
                    #print('Yes clicked.')
                    self.parent.setCentralWidget(MainMenu(self.parent))
                    self.parent.setCentralWidget(GameWindow(self.parent))

                else:
                    #print('No clicked.')
                    self.parent.setCentralWidget(MainMenu(self.parent))

    def update_surface(self):
        #connect paint methods to layers
        # surface

        self.painter2.setBrush(qg.QBrush(qg.QColor('#743b29')))
        self.painter2.setCompositionMode(qg.QPainter.CompositionMode_DestinationOver)

        #new
        self.painter2.drawPixmap(0, 0, self.ebene0)
        #old
        #self.painter2.drawRect(0, self.parent.height()-80, self.parent.width(), 80)

        #collisions
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



    def mouseMoveEvent(self, e):
        self.m_x = e.x()
        self.m_y = e.y()
        alpha = self.a.pixel(self.m_x, self.m_y)#.alpha()
        alpha2 = self.b.pixel(self.m_x, self.m_y)  # .alpha()
        #self.parent.statusBar().showMessage(str(self.f(self.m_x)))
        #self.parent.statusBar().showMessage("a: "+str(alpha)+" b: "+str(alpha2))

    def mousePressEvent(self, e):
        #print("lclick", self.gun.v/10)
        if self.bullets[self.current_player] == None:
            #print(self.weapon.currentIndex())
            self.bullets[self.current_player] = Bullet(self,self.current_player)

    def keyPressEvent(self, e):
        if e.key() == qc.Qt.Key_D:
            #if not an end of a screen
            if self.players[self.current_player].x+self.players[self.current_player].w != self.parent.width():
                # if a slope is not vertical
                if self.a.pixel(self.players[self.current_player].x + 4, self.players[self.current_player].y - 5) == 0:
                    self.players[self.current_player].x += 1
                    print(self.players[self.current_player].rotation, " ", self.players[self.current_player].left_point)
                #print("d")
        elif e.key() == qc.Qt.Key_A:
            # if not an end of a screen
            if self.players[self.current_player].x - self.players[self.current_player].w != 0:
                # if a slope is not vertical
                if self.a.pixel(self.players[self.current_player].x - 4, self.players[self.current_player].y - 5) == 0:
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

        self.painter4.setPen(qc.Qt.black)
        self.painter4.setFont(qg.QFont('Helvetica', 12))
        self.painter4.drawText(50, 50, str(self.players[self.current_player].name) + ", it's your turn! Time left: " + str(show))

    def f(self, x):
        res=np.float64(0)
        for i in range(len(self.w)):
            w=np.float64(self.w[i])
            res += 1 / (math.sqrt(w)) * math.sin(w * x + self.rand_a) * self.rand_b
            #res += 1/(math.sqrt(w))* math.sin(w*x+random.uniform(0,math.pi))*np.float64(random.uniform(-1,1))
        return 2*res

class Hit:
    def __init__(self, parent,x,y,dmg,koeff,crit):
        self.parent = parent
        self.x = x
        self.y = y - 30 # not in a Tank, but slightly above
        self.y_start = self.y
        self.y_end = 100 # how long should we display dmg
        self.dmg = dmg
        self.koeff = koeff
        self.crit = crit
        self.destruct=False

    def paint(self):
        #if we showed this hit enought long, by this attr we can delete it.
        #print("i'm drawing")
        if (self.y_start-self.y)/self.y_end > 0.9: # 90% of self.y_end is covered - next is too slow.
            self.destruct=True

        if self.crit==True:
            test="Critical! "
            self.parent.painter4.setFont(qg.QFont('CorpoS', 14, weight=qg.QFont.Bold, italic=qg.QFont.StyleItalic))
        else:
            test=""
            self.parent.painter4.setFont(qg.QFont('Helvetica', 12))

        if self.koeff==1:
            self.parent.painter4.setPen(qg.QPen(qc.Qt.red, 2, qc.Qt.SolidLine))

            self.parent.painter4.drawText(self.x,self.y, test+str(self.dmg))
        elif self.koeff >0.5:
            self.parent.painter4.setPen(qg.QPen(qc.Qt.yellow, 2, qc.Qt.SolidLine))
            self.parent.painter4.drawText(self.x, self.y, test+str(self.dmg))
        else:
            self.parent.painter4.setPen(qg.QPen(qc.Qt.green, 2, qc.Qt.SolidLine))
            self.parent.painter4.drawText(self.x, self.y, test+str(self.dmg))

        self.y -= 1.5-(self.y_start-self.y)/self.y_end

class Bullet:
    def __init__(self, parent,player_i):
        self.parent = parent
        self.criticat = False
        if random.randint(0,10)==1: self.criticat = True
        self.i=player_i
        self.weapon= parent.weapon.currentIndex()
        self.x = parent.players[self.i].x+parent.players[self.i].v[0]
        self.y = parent.players[self.i].y+parent.players[self.i].v[1]
        # self.v is gun direction



        #Cannon
        if self.weapon == 0:
            self.weight = 10
            self.power = 0.25

            self.damage = 20
            self.explosion = 10

        #Rifle
        elif self.weapon == 1:
            self.weight = 1
            self.power = 0.4

            self.damage = 1
            self.explosion = 1

        #Grenede
        elif self.weapon == 2:
            self.weight = 10
            self.power = 0.15

            self.damage = 40
            self.explosion = 50

        self.gravity = self.parent.gravity * self.weight

        self.v = self.power*parent.players[self.i].v

    def paint(self):
        self.parent.painter3.setPen(qg.QPen(qg.QColor(0, 0, 0), 2, qc.Qt.SolidLine))
        self.parent.painter3.drawPoint(self.x, self.y)

        self.x += self.v[0]
        self.y += self.v[1]
        self.collide()
        self.v[1]+=self.gravity#0.01 smth very light

    def collide(self):
        # check alpha chanel
        if self.parent.a.pixel(self.x,self.y) != 0:
            if self.parent.a.pixel(self.x - self.v[0], self.y - self.v[1]) == 0:
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
                    if abs(i.y-y) < i.h/2+self.explosion/2:
                        #abs(i.x - x) - i.w # distance to body
                        koeff = 1-(abs(i.x - x) - i.w/2)/(self.explosion/2) #dmg.koeff
                        if koeff > 1: koeff=1
                        if self.criticat==True:
                            dmg = float(round(1.5*self.damage*koeff,1))
                        else:
                            dmg = float(round(self.damage * koeff, 1))
                        i.hp -= dmg
                        #print(dmg)
                        self.parent.hits.append(Hit(self.parent, i.x, i.y, dmg, koeff, self.criticat))

        elif self.parent.b.pixel(self.x,self.y) != 0:
            if self.parent.b.pixel(self.x - self.v[0], self.y - self.v[1]) == 0:
                while self.parent.a.pixel(self.x,self.y) != 0:
                    self.x -= self.v[0]/100
                    self.y -= self.v[1]/100
            x=round(self.x)
            y=round(self.y)
            self.parent.collisions.append([x,y, self.explosion])
            self.parent.bullets[self.i] = None

            for i in self.parent.players:
                if abs(i.x-x) <= i.w/2 + self.explosion/2:
                    if abs(i.y-y) <= i.h/2 + self.explosion/2:
                        abs(i.x - x) - i.w # distance to body
                        koeff = 1 - (abs(i.x - x) - i.w / 2) / (self.explosion / 2)  # dmg.koeff
                        if koeff > 1: koeff = 1
                        #koeff=1
                        if self.criticat==True:
                            dmg = float(round(1.5*self.damage * koeff,1))
                        else:
                            dmg = float(round(self.damage * koeff, 1))
                        i.hp -= dmg
                        #print(dmg)
                        self.parent.hits.append(Hit(self.parent, i.x, i.y, dmg, koeff, self.criticat))

class Player:
    def __init__(self, parent, color, gun_color,name,i):
        self.parent = parent
        self.name = name
        self.i=i
        self.x = random.randint(50,400)
        self.y = 1
        self.corr=10 # offset from ground
        self.weight=500
        self.len = 15
        self.color = color
        self.hp_max = 300
        self.hp = self.hp_max
        self.w=30
        self.h=12
        self.g_color = gun_color
        #self.v is
        self.v = np.array([1,1])
        self.vector=0
        self.left_point =[0,0]
        self.right_point=[0,0]

    def paint(self):
        ##body
        if self.hp<=0:
            self.color = qc.Qt.gray
            self.g_color = qc.Qt.gray
        self.parent.painter3.setPen(qg.QPen(self.color, 2, qc.Qt.SolidLine))
        self.parent.painter3.setBrush(qg.QBrush(self.color))
        #self.parent.painter3.drawRect(self.x - self.w / 2, self.y - self.h / 2,self.w,self.h)

        pixmap = self.parent.tank
        self.rotation = 0

        self.left_point=[self.x-self.w/4,self.y+self.corr]
        self.right_point=[self.x+self.w/4,self.y+self.corr]

        if self.parent.a.pixel(self.left_point[0], self.left_point[1]) == 0:
            while self.parent.a.pixel(self.left_point[0], self.left_point[1]) == 0:
                self.left_point[1]+=1
        else:
            while self.parent.a.pixel(self.left_point[0], self.left_point[1]) != 0:
                self.left_point[1]-=1

        if self.parent.a.pixel(self.right_point[0], self.right_point[1]) == 0:
            while self.parent.a.pixel(self.right_point[0], self.right_point[1]) == 0:
                self.right_point[1]+=1
        else:
            while self.parent.a.pixel(self.right_point[0], self.right_point[1]) != 0:
                self.right_point[1]-=1

        self.vector=np.array([self.right_point[0]-self.left_point[0],self.right_point[1]-self.left_point[1]])


        if np.linalg.norm(self.vector) != 0:
            self.vector = self.vector / np.linalg.norm(self.vector)

        self.rotation=round(90-math.acos(self.vector[1])/math.pi*180)

        #print(self.rotation)
        transform = qg.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, qc.Qt.SmoothTransformation)

        self.parent.painter3.drawPixmap(self.x - self.w / 2, self.y - self.h / 2+1, pixmap)
        #self.parent.painter4.setBrush(qg.QBrush(qc.Qt.red))
        #self.parent.painter3.drawLine(self.left_point[0],self.left_point[1],self.right_point[0],self.right_point[1])


        ##name
        self.parent.painter4.setPen(qg.QPen(qc.Qt.black, 2, qc.Qt.SolidLine))
        self.parent.painter4.setFont(qg.QFont('Helvetica', 12))
        self.parent.painter4.drawText(self.x-self.w/2, self.y-self.h, self.name)

        ##hp bar
        percent=self.hp/self.hp_max
        color=qc.Qt.green
        if percent<0.4:
            color=qc.Qt.red
        elif percent<0.80:
            color=qc.Qt.yellow
        if self.hp > 0:
            self.parent.painter4.setPen(qg.QPen(color, 2, qc.Qt.SolidLine))
            self.parent.painter4.setBrush(qg.QBrush(color))
            self.parent.painter4.drawRect(self.x - self.w / 2, self.y - self.h + 2, self.w*percent, 2)
        else:
            self.parent.painter4.setPen(qg.QPen(qc.Qt.red, 2, qc.Qt.SolidLine))
            self.parent.painter4.setFont(qg.QFont('Helvetica', 12))
            self.parent.painter4.drawText(self.x - self.w / 2, self.y + self.h + 12, "dead")

        ##gun
        ###do not update self.v if it is not your turn!
        if self.parent.current_player == self.i:
            v = np.array([self.parent.m_x-self.x,self.parent.m_y-self.y])
            if np.linalg.norm(v)!=0:
                self.v= v / np.linalg.norm(v)
                self.v*=self.len

        self.parent.painter3.setPen(qg.QPen(self.g_color, 2, qc.Qt.SolidLine))
        self.parent.painter3.drawLine(self.x, self.y, self.x+self.v[0], self.y+self.v[1])

        ###check if on ground
        self.on_ground()

    def on_ground(self):
        if self.y+self.corr >= self.parent.height()-2:
            self.hp=0
            self.y += 4*self.h
        else:
            # check alpha chanel
            if self.parent.a.pixel(self.x, self.corr+self.y+2) == 0:
                    self.y += 2
            # if we will move a player and it hits the ground
            elif self.parent.a.pixel(self.x, self.corr+self.y-1) != 0:
                self.y -= 1




if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())