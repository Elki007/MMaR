import sys,random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
import configparser

class Board(QFrame):
    ScoreSignal = pyqtSignal(str)

    BoardWidth = 20
    BoardHeight = 20

    speed = 500
    print("speed: ", speed)
    score = 0

    scale = 30  # one cell scale

    ######
    snake_cords = [
        [1, 0],
        [0, 0],
        [-1, 0]
    ]

    direct = 1  # Direction
    newdirect = 1
    ######
    num = 10

    apples_cords = [[random.randint(0, 20), random.randint(0, 20)] for i in range(num)]


    def __init__(self, parent):
        super().__init__(parent)

        print("self: ", self)
        print("parent: ", parent)
        #print(parent.player_str)

        self.initBoard()
        self.setNewParamets(parent)


    def __repr__(self):
        return "Board"

    def __str__(self):
        return "Board"


    def setNewParamets(self, parent):
        ScoreSignal = pyqtSignal(str)
        #self.ScoreSignal = ScoreSignal
        #self.player_str = parent.player_str
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.player_value = config.get('SectionOne', 'player')
        self.border_value = config.get('SectionOne', "Border")
        self.acceleration_value = config.get('SectionOne', "Acceleration")
        self.speed_value = config.get('SectionOne', "Speed")
        self.maxSpeed_value = config.get('SectionOne', "Maximum speed")
        self.stepSpeed_value = config.get('SectionOne', "Step Speed")
        self.length_value = config.get('SectionOne', "length")
        self.fruitPrbbl_value = config.get('SectionOne', "Fruit probability")
        self.fruitMaxLife_value = config.get('SectionOne', "Fruit maximum lifespan")
        self.fruitMinLife_value = config.get('SectionOne', "Fruit minimum lifespan")
        self.fieldWidth_value = config.get('SectionOne', "Field width")
        self.fieldHigh_value = config.get('SectionOne', "Field high")
        self.scale_value = config.get('SectionOne', "Field zoom")


        speed = 500
        #print("new speed: ",speed)
        #self.speed = speed
        score = 0
        #self.score = score
        self.scale = int(self.scale_value)  # one cell scale
        self.BoardWidth = int(self.fieldWidth_value)
        self.BoardHeight = int(self.fieldHigh_value)


        #self.scale = scale
        ######
        snake_cords = [
            [1, 0],
            [0, 0],
            [-1, 0]
        ]
        self.snake_cords = snake_cords
        print("new snake_cords: ", snake_cords)
        direct = 0  # Direction
        #self.direct = direct
        ######
        self.num = int(self.fruitPrbbl_value)
        #self.num = num

        apples_cords = [[random.randint(0, self.BoardWidth), random.randint(0, self.BoardHeight)] for i in range(self.num)]
        self.apples_cords = apples_cords

    def initBoard(self):

        self.timer = QBasicTimer()
        self.timerOn = False

    def timerEvent(self, event):
        self.snake_step()

    def snake_step(self):
        #######update direction#####

        #print(self.timer)
        scords = self.snake_cords
        acords = self.apples_cords

        for i in range(len(scords)-1,0,-1):
            scords[i][0] = scords[i - 1][0]
            scords[i][1] = scords[i - 1][1]

        if self.newdirect != - self.direct:
            self.direct = self.newdirect
        if self.direct == 1:
            scords[0][0] += 1
        elif self.direct == -1:
            scords[0][0] -= 1
        elif self.direct == 2:
            scords[0][1] -= 1
        else:
            scords[0][1] += 1


        #### if snake cross itselfs####
        if scords[0] in scords[1:]:
            scords.pop(len(scords)-1)

        for i in acords:
            if scords[0] == i:
                acords.pop(acords.index(i))
                scords.append([scords[-1][0], scords[-1][1]])
                self.apple_update()
                self.score += 1
                break
        #########################################################
        ############boarders for snake##########################
        if scords[0][0] == self.BoardWidth+1:#21:
            scords[0][0] = 0
        elif scords[0][0] == -1:
            scords[0][0] = self.BoardWidth

        if scords[0][1] == self.BoardHeight+1:
            scords[0][1] = 0
        elif scords[0][1] == -1:
            scords[0][1] = self.BoardHeight

        self.ScoreSignal.emit(self.player_value  + " score: " + str(self.score))

        self.speed_update()

        self.game_over()

        self.update()

    def apple_update(self):
        if len(self.apples_cords) < self.num:
            cord = [random.randint(0,self.BoardWidth),random.randint(0,self.BoardHeight)]
            while cord in self.apples_cords or cord in self.snake_cords:
                cord = [random.randint(0, self.BoardWidth), random.randint(0, self.BoardHeight)]
            self.apples_cords.append(cord)

    def start(self):

        self.timer.start(Board.speed, self)
        self.timerOn = True

    def pause(self):

        if self.timerOn:
            self.timer.stop()
            self.ScoreSignal.emit('Paused, current Score: ' + str(self.score))
        else:
            self.timer.start(Board.speed, self)

        self.timerOn = not self.timerOn



    def paintEvent(self, QP):
        QP = QPainter()
        QP.begin(self)
        self.drawSnake(QP)
        self.drawApples(QP)
        self.drawBoard(QP)
        QP.end()

    def drawSnake(self, QP):
        QP.setBrush(QColor(0, 128, 0))
        #print(self.snake_cords)
        for i in self.snake_cords:
            #QP.drawRect(i[0]*self.scale,i[1]*self.scale, self.scale, self.scale)
            QP.drawEllipse(i[0] * self.scale, i[1] * self.scale, self.scale, self.scale)


    def drawApples(self, QP):
        QP.setBrush(QColor(200, 0, 0))
        #painter = QPainter(self)
        pixmap = QPixmap("apple.png")
        #print("im here")
        for i in self.apples_cords:
            #QP.drawRect(i[0] * self.scale, i[1] * self.scale, self.scale, self.scale)
            QP.drawPixmap(i[0]* self.scale, i[1]* self.scale, self.scale, self.scale, pixmap)



    def drawBoard(self, QP):
        #pen = QPen(QColor(0, 0, 0), 2, Qt.SolidLine)
        QP.drawLine(0, 0, 0, (self.BoardHeight+1)*self.scale)
        QP.drawLine((self.BoardWidth+1)*self.scale, 0, (self.BoardWidth+1)*self.scale, (self.BoardHeight+1)*self.scale)
        QP.drawLine(0, 0, (self.BoardWidth+1)*self.scale, 0)
        QP.drawLine(0, (self.BoardHeight+1)*self.scale, (self.BoardWidth+1)*self.scale, (self.BoardHeight+1)*self.scale)

    def speed_update(self):
        Board.speed = 1500//len(self.snake_cords)
        self.start()

    def game_over(self):
        if len(self.snake_cords) == 2:
            self.timer.stop()
            self.timerOn = False
            self.ScoreSignal.emit("Game Over! " + self.player_value + ", you got " + str(self.score) + " apples")

