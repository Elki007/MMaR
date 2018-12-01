from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from Point3D import Point3D


class Pane(qw.QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.color = qc.Qt.white
        self.thickness = 3
        self.grid = False
        self.k = 24
        # default value is false - means track mouse only when at least one button is pressed
        print(parent.parent)
        print(self)
        print(self.width(), self.height())
        print(parent.parent)
        print(parent.width(), parent.height())
        self.ebene_background = qg.QPixmap(parent.parent.width(), parent.parent.height())
        self.ebene_background.fill(qg.QColor(0, 0, 0))

        self.ebene_pane = qg.QPixmap(parent.parent.width(), parent.parent.height())
        self.ebene_pane.fill(qg.QColor(0, 0, 0, 0))

        self.ebene_total = qg.QPixmap(parent.parent.width(), parent.parent.height())
        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))


        self.painter_bg = qg.QPainter(self.ebene_background)
        self.painter_pane = qg.QPainter(self.ebene_pane)
        self.painter_total = qg.QPainter(self.ebene_total)

        self.paths = []
        self.path = []
        for i in range(self.k):
            self.paths.append([])
            self.path.append([])

        #self.create_bg()

        self.update()

    def __repr__(self):
        return str("Pane")

    def create_bg(self):
        #print(self.parent)
        center_x = self.parent.width()//2
        center_y = (self.parent.height()-30)//2
        #print(center_x,center_y)


        self.painter_bg.setPen(qg.QPen(qc.Qt.white, 0.5, qc.Qt.SolidLine))
        #self.painter_bg.drawLine(0, 0, 100, 100)
        center = Point3D(center_x, center_y, 0)
        a = Point3D(center_x, center_y - 2000, 0)
        for k in range(1,self.k+1):
            degree = k*360/self.k
            point = a.make_vector(center)
            b = point.rotateZ(degree) + center
            if self.grid:
                self.painter_bg.drawLine(center.x, center.y, b.x, b.y)

        if self.grid:
            self.painter_bg.drawPoint(center_x,center_y)

    def transpose(self,x,y,k):
        center_x = self.parent.width() // 2
        center_y = (self.parent.height() - 30) // 2
        self.painter_bg.setPen(qg.QPen(qc.Qt.white, 0.5, qc.Qt.SolidLine))

        center = Point3D(center_x, center_y, 0)
        a = Point3D(x, y, 0)
        degree = k * 360 / self.k
        point = a.make_vector(center)
        if self.k%2 == 0:
            b = point.rotateZ(degree) + center
        else:
            b = - point.rotateZ(degree) + center
        c = Point3D(b.x,b.y,b.z)
        return c

    def update(self):
        for i in range(self.k):
            if len(self.paths) == 0:
                return
            if len(self.paths[i]) != 0:
                path = self.paths[i][-1][0]
                thickness = self.paths[i][-1][1]
                self.painter_pane.setPen(qg.QPen(self.color, thickness, qc.Qt.SolidLine))
                self.painter_pane.drawPath(path)

        """if len(self.paths2) != 0:
            path = self.paths2[-1][0]
            thickness = self.paths2[-1][1]
            self.painter_pane.setPen(qg.QPen(qc.Qt.gray, thickness, qc.Qt.SolidLine))
            self.painter_pane.drawPath(path)"""

        '''for i in range(len(self.paths)):
            path = self.paths[i][0]
            thickness = self.paths[i][1]
            self.painter_pane.setPen(qg.QPen(qc.Qt.gray, thickness, qc.Qt.SolidLine))
            self.painter_pane.drawPath(path)'''

        self.painter_total.drawPixmap(0, 0, self.ebene_background)
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        self.setPixmap(self.ebene_total)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y() + 30
        for i in range(self.k):
            self.path[i] = qg.QPainterPath()
            #self.path2 = qg.QPainterPath()

            self.paths[i].append([self.path[i], self.thickness])
            #self.paths2.append([self.path2, self.thickness])

            #self.path[i].moveTo(x, y)
            #print("original: ",x,y)
            b = self.transpose(x,y,i)
            #print("b: ", b.x, b.y)

            self.path[i].moveTo(b.x, b.y)

        self.update()

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y() + 30
        for i in range(self.k):
            #self.path[i].lineTo(x,y)
            b = self.transpose(x, y, i)
            self.path[i].lineTo(b.x, b.y)
            #self.newPoint.emit(event.pos())
        self.update()


class DrawWidget(qw.QWidget):
    def __init__(self,parent):
        qw.QWidget.__init__(self, parent)
        self.parent = parent
        self.setLayout(qw.QVBoxLayout())
        self.layout().setSpacing(0)

        self.draw = Pane(self)
        #label = qw.QLabel(self)
        #label.setFixedHeight(25)

        hbox = qw.QHBoxLayout()
        #hbox.maximumSize(25)
        gr1 = qw.QButtonGroup()
        b_thickness1 = qw.QRadioButton("1")
        b_thickness1.toggled.connect(lambda: self.btnstate(b_thickness1))
        b_thickness2 = qw.QRadioButton("3")
        b_thickness2.toggled.connect(lambda: self.btnstate(b_thickness2))
        b_thickness3 = qw.QRadioButton("5")
        b_thickness3.toggled.connect(lambda: self.btnstate(b_thickness3))
        b_newgame = qw.QPushButton("Erase")
        b_newgame.setFixedSize(qc.QSize(60,27))
        #b_newgame.setStyleSheet("size: 15 x 2")
        b_newgame.clicked.connect(self.on_click_b_newgame)
        gr1.addButton(b_thickness1)
        gr1.addButton(b_thickness2)
        gr1.addButton(b_thickness3)

        hbox.addWidget(b_thickness1)
        hbox.addWidget(b_thickness2)
        hbox.addWidget(b_thickness3)

        self.grid = qw.QCheckBox("Grid")
        self.grid.clicked.connect(self.on_click_grid)
        print(self.grid.isChecked())

        hbox.addWidget(self.grid)
        hbox.addWidget(b_newgame)


        b_thickness2.setChecked(True)

        colorBox = qw.QComboBox(self)
        colorBox.addItem("white")
        colorBox.addItem("red")
        colorBox.addItem("green")
        colorBox.addItem("blue")
        colorBox.addItem("cyan")
        colorBox.addItem("yellow")
        colorBox.activated[str].connect(self.style_choise)

        kBox = qw.QComboBox(self)
        kBox.addItem("1")
        kBox.addItem("7")
        kBox.addItem("8")
        kBox.addItem("17")
        kBox.addItem("18")
        kBox.addItem("24")
        kBox.activated[str].connect(self.k_choise)
        kBox.setCurrentText("24")

        hbox.addWidget(colorBox)
        hbox.addWidget(kBox)
        hbox.addStretch(1)

        self.layout().addLayout(hbox)

        #label.setStyleSheet("QLabel { background-color : rgb(150,150,150); color : blue; }")
        #draw.newPoint.connect(lambda p: label.setText('Coordinates (%d, %d)' %(p.x(),p.y())))
        self.layout().addWidget(self.draw)

    def __repr__(self):
        return str("DrawWidget")

    def style_choise(self,text):
        if text == "red":
            self.draw.color = qc.Qt.red
        elif text == "white":
            self.draw.color = qc.Qt.white
        elif text == "green":
            self.draw.color = qc.Qt.green
        elif text == "blue":
            self.draw.color = qc.Qt.blue
        elif text == "cyan":
            self.draw.color = qc.Qt.cyan
        elif text == "yellow":
            self.draw.color = qc.Qt.yellow

    def k_choise(self, text):
        if text == "1":
            self.draw.k = 1
        elif text == "7":
            self.draw.k = 7
        elif text == "8":
            self.draw.k = 8
        elif text == "17":
            self.draw.k = 17
        elif text == "18":
            self.draw.k = 18
        elif text == "24":
            self.draw.k = 24

    def on_click_grid(self):
        self.draw.grid = self.grid.isChecked()
        self.draw.ebene_background.fill(qg.QColor(0, 0, 0))
        self.draw.create_bg()
        self.draw.update()


    def on_click_b_newgame(self):
        self.draw.ebene_pane.fill(qg.QColor(0, 0, 0, 0))
        self.draw.ebene_background.fill(qg.QColor(0, 0, 0))

        self.draw.paths = []
        #self.draw.paths2 = []

        self.draw.path = []
        #self.draw.path2 = qg.QPainterPath()
        for i in range(self.draw.k):
            self.draw.paths.append([])
            self.draw.path.append([])

        self.draw.create_bg()
        self.draw.update()

    def btnstate(self, b):
        self.draw.thickness = int(b.text())