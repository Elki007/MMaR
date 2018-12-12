from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from Point3D import Point3D


class Pane(qw.QLabel):
    """ Klasse der Malflaeche """

    def __init__(self, parent):
        """ creates Pane """
        super().__init__()
        self.parent = parent  # DrawWidget
        self.color = qc.Qt.white
        self.thickness = 3
        self.grid = False
        self.k = 24
        self.transposition = "rotation"
        # default value is false - means track mouse only when at least one button is pressed

        # background for black background with lines of grid/crystal if activated
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

        self.setObjectName("Pane")
        with open("stylesheet.css", "r") as style:  # reads stylesheets
            self.setStyleSheet(style.read())

        #self.create_bg()

        self.update()

    def __repr__(self):
        return str("Pane")

    def get_center_point(self):
        """ returns center coordinates from parent"""
        return self.parent.width()//2, (self.parent.height()-30)//2

    def create_bg(self):
        """ creates grid-/crystal lines if activated """

        # define center of grid/crystal graphic
        center_x, center_y = self.get_center_point()

        # defines painter of grid/crystal
        self.painter_bg.setPen(qg.QPen(qc.Qt.white, 0.5, qc.Qt.SolidLine))

        # creates Point3Ds for calculation of grid-/crystal-lines
        center = Point3D(center_x, center_y, 0)
        point_outside = Point3D(center_x, center_y - self.parent.width(), 0)

        # creates lines for as many 'k' (crystal-lines) are given
        for k in range(1, self.k+1):
            degree = k*360/self.k
            #crystal_vector = point_outside.make_vector(center)
            crystal_vector = center.make_vector(point_outside)
            b = crystal_vector.rotateZ(degree) + center
            if self.grid:
                self.painter_bg.drawLine(center.x, center.y, b.x, b.y)

        # TODO: why?
        #if self.grid:
        #    self.painter_bg.drawPoint(center_x, center_y)

    def transpose_rotation(self, x, y, k):
        """ rotates each point to a degree, dependent on k - quantity of grid lines """
        center_x, center_y = self.get_center_point()

        # TODO: defines... what?
        #self.painter_bg.setPen(qg.QPen(qc.Qt.white, 0.5, qc.Qt.SolidLine))

        center = Point3D(center_x, center_y, 0)
        any_point = Point3D(x, y, 0)
        degree = k * 360 / self.k
        point = center.make_vector(any_point)

        b = point.rotateZ(degree) + center

        return Point3D(b.x, b.y)

    def transpose_rotation_and_mirroring(self, x, y, k):
        """
        rotates and mirrors each point, dependent on position
        works with grid/crystal lines
        """

        center_x, center_y = self.get_center_point()

        center = Point3D(center_x, center_y)
        any_point = Point3D(x, y, 0)
        degree = k * 360 / self.k
        point = center.make_vector(any_point)

        if k % 2 == 0:
            b = point.rotateZ(degree)
            return Point3D(b.x + center.x, b.y + center.y)
        else:
            degree = (k+1) * 360 / self.k
            b = point.rotateZ(degree)
            return Point3D(b.y + center.x, b.x + center.y)

    def transpose_rotation_moved(self, x, y, k, factor=0.5):
        """
        moves and rotates each point, dependent on position
        works with grid/crystal lines
        """

        center_x, center_y = self.get_center_point()

        center = Point3D(center_x, center_y)
        degree = k * 360 / self.k
        any_point = Point3D(x, y)
        vector_to_center = center.make_vector(any_point)

        if k % 2 == 0:
            b = vector_to_center.rotateZ(degree)
            return Point3D(b.x + center.x, b.y + center.y)
        else:
            vector_to_center = vector_to_center * factor
            b = vector_to_center.rotateZ(degree)
            return Point3D(b.x + center.x, b.y + center.y)

    def update(self):
        """ draws something, is used if mouse will be clicked (and moved) """
        for i in range(self.k):
            if len(self.paths) == 0:
                return None
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
            if self.transposition == "rotation":
                b = self.transpose_rotation(x, y, i)
            elif self.transposition == "rotate and mirror":
                b = self.transpose_rotation_and_mirroring(x, y, i)
            elif self.transposition == "rotate and move":
                b = self.transpose_rotation_moved(x, y, i)
            #print("b: ", b.x, b.y)

            self.path[i].moveTo(b.x, b.y)
            self.path[i].lineTo(b.x+0.1, b.y+0.1)  # to draw a dot if it's just a click

        self.update()

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y() + 30

        for i in range(self.k):
            #self.path[i].lineTo(x,y)
            if self.transposition == "rotation":
                b = self.transpose_rotation(x, y, i)
            elif self.transposition == "rotate and mirror":
                b = self.transpose_rotation_and_mirroring(x, y, i)
            elif self.transposition == "rotate and move":
                b = self.transpose_rotation_moved(x, y, i)

            self.path[i].lineTo(b.x, b.y)
            #self.newPoint.emit(event.pos())
        self.update()


class DrawWidget(qw.QWidget):
    def __init__(self, parent):
        qw.QWidget.__init__(self, parent)
        self.parent = parent  # MainMenu
        self.setLayout(qw.QVBoxLayout())
        #self.layout().setSpacing(0)  # Zweck?

        self.draw = Pane(self)
        #label = qw.QLabel(self)
        #label.setFixedHeight(25)

        hbox = qw.QHBoxLayout()
        #hbox.maximumSize(25)
        gr1 = qw.QButtonGroup()

        """
        # creates the radio thickness buttons
        thickness_list = [1, 3, 5, 50, 1]
        for thickness in thickness_list:
            thick_button = qw.QRadioButton(str(thickness))
            thick_button.toggled.connect(lambda: self.btnstate(thick_button))
            gr1.addButton(thick_button)
            hbox.addWidget(thick_button)

            if thickness == 3:
                thick_button.setChecked(True)
        """

        self.setObjectName("DrawWidget")
        with open("stylesheet.css", "r") as style:  # reads stylesheets
            self.setStyleSheet(style.read())

        b_thickness1 = qw.QRadioButton("1")
        b_thickness1.toggled.connect(lambda: self.btnstate(b_thickness1))
        b_thickness2 = qw.QRadioButton("3")
        b_thickness2.toggled.connect(lambda: self.btnstate(b_thickness2))
        b_thickness3 = qw.QRadioButton("5")
        b_thickness3.toggled.connect(lambda: self.btnstate(b_thickness3))
        b_erase = qw.QPushButton("Erase")
        b_erase.setFixedSize(qc.QSize(60, 27))
        #b_newgame.setStyleSheet("size: 15 x 2")
        b_erase.clicked.connect(self.on_click_b_start)
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
        hbox.addWidget(b_erase)

        b_thickness2.setChecked(True)

        colorBox = qw.QComboBox(self)
        color_list = ["white", "red", "green", "blue", "cyan", "yellow"]
        for color in color_list:
            colorBox.addItem(color)

        colorBox.activated[str].connect(self.style_choice)

        transpose_box = qw.QComboBox(self)
        transpose_list = ["rotation", "rotate and mirror", "rotate and move"]
        for transposition in transpose_list:
            transpose_box.addItem(transposition)

        transpose_box.activated[str].connect(self.transpose_choice)

        kBox = qw.QComboBox(self)
        item_list = [1, 7, 8, 17, 18, 24] # 120]
        for number in item_list:
            kBox.addItem(f"{number}")

        kBox.activated[str].connect(self.k_choice)
        kBox.setCurrentText("24")

        hbox.addWidget(colorBox)
        hbox.addWidget(kBox)
        hbox.addWidget(transpose_box)
        hbox.addStretch(1)

        self.layout().addLayout(hbox)

        #label.setStyleSheet("QLabel { background-color : rgb(150,150,150); color : blue; }")
        #draw.newPoint.connect(lambda p: label.setText('Coordinates (%d, %d)' %(p.x(),p.y())))
        self.layout().addWidget(self.draw)

    def __repr__(self):
        return str("DrawWidget")

    def style_choice(self, text):
        """ changes color, e.g 'qc.Qt.green' """
        self.draw.color = eval("qc.Qt." + text)

    def k_choice(self, text):
        self.draw.k = int(text)

    def transpose_choice(self, text):
        """ changes transposition which is used """
        self.draw.transposition = text

    def on_click_grid(self):
        self.draw.grid = self.grid.isChecked()
        self.draw.ebene_background.fill(qg.QColor(0, 0, 0))
        self.draw.create_bg()
        self.draw.update()

    def on_click_b_start(self):
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
