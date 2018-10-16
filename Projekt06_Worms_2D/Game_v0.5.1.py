'''
To use "import skfmm" you have to install the plugin "scikit-fmm"

If you get the error: "Microsoft Visual C++ 14.0 is required" you have to install the Build-Tools
https://visualstudio.microsoft.com/de/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15

At "Workloads" -> Buildtools (4,81 GB)
'''

# TODO: Distribution of files to separate e.g. logic and graphic

import sys
import random
import math
import numpy as np
from datetime import datetime, timedelta
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg


# Benötigt für Abstand zur Oberfläche (as advised), tbd
# import skfmm
# import matplotlib as plt
# from PyQt5.QtGui import QImage
# from matplotlib import cm


# Settings for the window in general
class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(480)
        self.setMinimumWidth(600)
        self.zoom = 1
        self.init_ui()

    def init_ui(self):
        self.statusBar().showMessage('online')
        # self.setGeometry(300, 300, 250, 150)  # Wozu ist das?
        self.setWindowTitle('Worms 2D')
        self.setCentralWidget(MainMenu(self))

        # self.center()  # Wozu ist das?

        self.show()

    def center(self):  ##### screen center  # Wozu ist das?
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# Settings for main menu - first displayed menu
class MainMenu(qw.QWidget):
    def __init__(self, parent):
        qw.QWidget.__init__(self)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Menu items
        b_newgame = qw.QPushButton("New Game")
        b_highscore = qw.QPushButton("High score")  # tbd
        b_settings = qw.QPushButton("Settings")  # tbd
        b_credits = qw.QPushButton("Credits")  # tbd
        b_exit = qw.QPushButton("Exit")

        # Menu actions
        b_newgame.clicked.connect(self.on_click_b_newgame)
        # b_newgame.connect = parent.setCentralWidget(qw.QPushButton("inside Game"))
        b_highscore.clicked.connect(self.on_click_b_highscore)
        b_settings.clicked.connect(self.on_click_b_settings)
        b_credits.clicked.connect(self.on_click_b_credits)
        b_exit.clicked.connect(self.on_click_b_exit)

        # Layout of menu
        hbox = qw.QHBoxLayout()
        vbox = qw.QVBoxLayout()

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        vbox.addStretch(1)
        vbox.addWidget(b_newgame)
        # vbox.addWidget(b_highscore)
        # vbox.addWidget(b_settings)
        # vbox.addWidget(b_credits)
        vbox.addWidget(b_exit)
        vbox.addStretch(1)

        self.setLayout(hbox)

    # Functions for clicked menu items
    def on_click_b_newgame(self):
        # print('PyQt5 button click')
        self.parent.setCentralWidget(qw.QPushButton("inside Game"))
        self.parent.setCentralWidget(GameWindow(self.parent))
        self.parent.statusBar().clearMessage()
        self.parent.statusBar().hide()

    def on_click_b_highscore(self):
        self.parent.statusBar().clearMessage()
        # self.parent.statusBar().hide()
        # self.parent.setCentralWidget(Test(self.parent))

    def on_click_b_settings(self):
        pass

    def on_click_b_credits(self):
        pass

    def on_click_b_exit(selfs):
        sys.exit(app.exec_())


# Settings for the window with the actual game
class GameWindow(qw.QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # default value is false - means track mouse only when at least one button is pressed
        self.setMouseTracking(True)
        self.grabKeyboard()

        # Ingame menu for weapon choice - direct images to click
        weapon_title = qw.QPushButton("Weapons")
        weapon_title.setDisabled(True)
        weapon_title.setStyleSheet("color: black")
        self.weapon01 = qw.QPushButton()
        self.weapon01.setIcon(qg.QIcon('w_cannon01.png'))
        self.weapon01.setStyleSheet("background-color: blue")
        self.weapon02 = qw.QPushButton()
        self.weapon02.setIcon(qg.QIcon('w_rifle01.png'))
        self.weapon02.setStyleSheet("background-color: lightgrey")
        self.weapon03 = qw.QPushButton()
        self.weapon03.setIcon(qg.QIcon('w_bomb01.png'))
        self.weapon03.setStyleSheet("background-color: lightgrey")

        # Action for Button clicked for weapon choice
        self.weapon01.clicked.connect(self.on_click_weapon01)
        self.weapon02.clicked.connect(self.on_click_weapon02)
        self.weapon03.clicked.connect(self.on_click_weapon03)

        # Layout for weapon choice
        weapon_menu_layout = qw.QHBoxLayout()
        weapon_menu = qw.QVBoxLayout()
        weapon_items = qw.QHBoxLayout()

        weapon_menu.addWidget(weapon_title)
        weapon_menu.addLayout(weapon_items)
        weapon_menu.addStretch(1)

        weapon_items.addWidget(self.weapon01)
        weapon_items.addWidget(self.weapon02)
        weapon_items.addWidget(self.weapon03)

        weapon_menu_layout.addStretch(1)
        weapon_menu_layout.addLayout(weapon_menu)
        weapon_menu_layout.setSpacing(0)

        self.setLayout(weapon_menu_layout)

        # refers to class Bullet with default 0
        self.weapon_choice = 0

        # mouse coordinates
        self.mouse_x = 0
        self.mouse_y = 0

        # an array of changes to original surface
        self.collisions_to_surface = []

        # generic surface
        self.ebene0_generic_surface = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                                 self.parent.height() * self.parent.zoom)  # oder QImage
        # first layer background
        self.ebene1_background = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                            self.parent.height() * self.parent.zoom)  # oder QImage
        # second layer only surface
        self.ebene2_surface = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                         self.parent.height() * self.parent.zoom)  # oder QImage
        # objects
        self.ebene3_object = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                        self.parent.height() * self.parent.zoom)  # oder QImage
        # interface
        self.ebene4_interface = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                           self.parent.height() * self.parent.zoom)  # oder QImage
        # smoke
        # TODO: smoke can go through surface - it's "power smoke" at the moment
        self.ebene5_smoke = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                       self.parent.height() * self.parent.zoom)  # oder QImage
        # wind
        # TODO: wind only effects smoke atm, right factor for bullets needs to be found and implemented
        self.ebene6_wind = qg.QPixmap(self.parent.width() * self.parent.zoom,
                                      self.parent.height() * self.parent.zoom)  # oder QImage

        # make 'em transparent (alpha channel = 0) 4th number in parameters
        self.ebene0_generic_surface.fill(qg.QColor(0, 0, 0, 0))
        self.ebene1_background.fill(qg.QColor(0, 0, 0, 0))
        self.ebene2_surface.fill(qg.QColor(0, 0, 0, 0))
        self.ebene3_object.fill(qg.QColor(0, 0, 0, 0))
        self.ebene4_interface.fill(qg.QColor(0, 0, 0, 0))
        self.ebene5_smoke.fill(qg.QColor(0, 0, 0, 0))
        self.ebene6_wind.fill(qg.QColor(0, 0, 0, 0))

        # Generate Surface
        self.surface_sinus_count = 20  # how many functions will be overlayed to create surface
        self.surface_factor = 3  # results of function will be multiplied with
        self.surface_distance_from_top = 0.5 * self.parent.height()  # how far from top is y=0 of the generated surface
        self.surface_color = [255, 191, 102]  # color of top of surface (default: brownish [255, 191, 102])

        # array of x-coordinates
        self.surface = self.surface_generator()

        # Generate Wind
        self.wind_factor = 3  # strength of wind

        # 2d-array of wind power coordinates
        self.wind_map = self.wind_generator()

        # 2d-array: True for surface, False for air/no surface
        self.surface_true_false = self.surface_true_false_generator()

        # Qt5 tools to paint
        self.painter0_generic_surface = qg.QPainter(self.ebene0_generic_surface)
        self.painter1_background = qg.QPainter(self.ebene1_background)
        self.painter2_surface = qg.QPainter(self.ebene2_surface)
        self.painter3_object = qg.QPainter(self.ebene3_object)
        self.painter4_interface = qg.QPainter(self.ebene4_interface)
        self.painter5_smoke = qg.QPainter(self.ebene5_smoke)
        self.painter6_wind = qg.QPainter(self.ebene6_wind)

        # draw dynamic surface - 2 Versions (Maxims and advised (with scikit-fmm and matplotlib)) (just one needed)
        # advised version (tbd)
        """
        # begin of Maxims test?
        #self.alpha = 0
        #self.map = np.zeros([self.parent.width(), self.parent.height()], dtype=np.bool)

        map_dist = skfmm.distance(self.surface_true_false)  # Distanzen zur 0 (also False)
        map_dist = map_dist / np.max(map_dist)  # Normieren auf 0,1

        world = plt.cm.copper_r(map_dist)  # Mit Matplotlib in Farben Konvertieren

        world[:, :, 3] = self.surface_true_false  # Nicht-Land auf Transparent setzen (True = 1, False = 0)
        world = np.asarray(world * 255, np.uint8)  # Konvertierung in ein 8-Bit Array, das in ein QImage konvertiert werden kann

        #mapmap = qg.QImage(world, self.parent.height(), self.parent.width(), qg.QImage.Format_Indexed8)
        """

        # version of Maxim (depends only on height)
        for j in range(self.parent.width()):
            self.surf_color_R, self.surf_color_G, self.surf_color_B = self.surface_color
            for i in range(self.parent.height()):
                if self.surface_true_false[i][j]:
                    self.painter0_generic_surface.setPen(
                        qg.QColor(self.surf_color_R, self.surf_color_G, self.surf_color_B))
                    self.painter0_generic_surface.drawPoint(j, i)
                    if self.surf_color_R >= 4: self.surf_color_R -= 4
                    if self.surf_color_G >= 4: self.surf_color_G -= 4
                    if self.surf_color_B >= 4: self.surf_color_B -= 4

        # it is possible to check an alpha channel only if QPixmap is converted toImage
        # update_surface() damit die Oberfläche für die Spielerposition zur Verfügung steht
        self.update_surface()
        self.ebene2_surface_image = self.ebene2_surface.toImage()
        self.ebene3_object_image = self.ebene3_object.toImage()

        # TODO: Bei mehr als 2 Spielern: Tote können weiterspielen und bspw. unten aus dem Bildschirm fallen
        # Array mit allen Spielernamen
        self.player_names = ["Max", "Misha"]

        self.bullet_shot_allowed = False
        self.players = []
        self.bullets = []
        self.hits = []
        self.explosions = []

        for i in range(len(self.player_names)):
            self.players.append(
                Player(self, qc.Qt.darkGreen, qg.QColor(104, 156, 56), self.player_names[i], len(self.players)))
            self.bullets.append(None)

        # flag to stop the Game
        self.victory = False

        # game settings
        self.time_for_round = 10
        self.time_between_rounds = 4
        self.game_speed = 5
        self.gravity = 0.01

        # timer settings
        self.current_player = 0
        self.timer_begin = True
        self.r_start = datetime.now().time()
        self.timer_between_rounds_begin = False
        self.time_between_start = 0

        # movement flags
        self.movement_right = False
        self.movement_left = False

        self.init_ui()

    # creates array with x-coordinates, based on overlayed functions
    # ?highest amplitude of single sinus: sqrt(1/0.001) -> ~32
    def surface_generator(self):
        w = np.linspace(start=0.001, stop=0.05, num=self.surface_sinus_count)
        x_coordinates = range(self.parent.width())
        surface_random_one = np.random.uniform(0, 2 * math.pi, self.surface_sinus_count)
        surface_random_two = np.random.uniform(-1, 1, self.surface_sinus_count)

        surface = []
        for i in x_coordinates:
            res = 0
            for j in range(self.surface_sinus_count):
                res += (1 / math.sqrt(w[j])) * math.sin(w[j] * i + surface_random_one[j]) * surface_random_two[j]
            surface.append((res * self.surface_factor) + self.surface_distance_from_top)
        return surface

    # creates array with x- and y-coordinates, based on overlayed functions
    def wind_generator(self):
        x_coordinates = range(self.parent.width())
        y_coordinates = range(self.parent.height())

        w = 0.006
        wind_random_one = np.random.uniform(0, 2 * math.pi)
        wind_random_two = np.random.uniform(0, 2 * math.pi)

        wind = []
        for i in y_coordinates:
            res = []
            for j in x_coordinates:
                # res.append(w * math.sin(w * j + wind_random_one) * math.sin(w * i + wind_random_two) * self.wind_factor)
                res.append(math.sin(w * j + wind_random_one) * math.sin(w * i + wind_random_two) * self.wind_factor)
            wind.append(res)

        #print("Maximalwert:", max([max(inner_array) for inner_array in wind]))
        #print("Minimalwert:", min([min(inner_array) for inner_array in wind]))

        return wind

    # creates array with true/false to show surface
    def surface_true_false_generator(self):
        surface_true_false = []
        for i in range(self.parent.height()):
            tmp = []
            for j in range(self.parent.width()):
                tmp.append(True) if i > self.surface[j] else tmp.append(False)
            surface_true_false.append(tmp)
        return surface_true_false

    def on_click_weapon01(self):
        self.weapon_choice = 0
        self.weapon01.setStyleSheet("background-color: blue")
        self.weapon02.setStyleSheet("background-color: lightgrey")
        self.weapon03.setStyleSheet("background-color: lightgrey")

    def on_click_weapon02(self):
        self.weapon_choice = 1
        self.weapon01.setStyleSheet("background-color: lightgrey")
        self.weapon02.setStyleSheet("background-color: blue")
        self.weapon03.setStyleSheet("background-color: lightgrey")

    def on_click_weapon03(self):
        self.weapon_choice = 2
        self.weapon01.setStyleSheet("background-color: lightgrey")
        self.weapon02.setStyleSheet("background-color: lightgrey")
        self.weapon03.setStyleSheet("background-color: blue")

    def init_ui(self):
        self.run()

    def run(self):
        try:
            # renew layer 3,4
            self.ebene3_object.fill(qg.QColor(0, 0, 0, 0))
            self.ebene4_interface.fill(qg.QColor(0, 0, 0, 0))

            # we do not fill this layer because we want to show last particles with less effort
            self.painter5_smoke.setBrush(qg.QBrush(qg.QColor(150, 150, 150, 0)))
            # self.painter5.setPen(qc.Qt.black)
            # self.painter5.setBrush(qc.Qt.black)
            self.painter5_smoke.setCompositionMode(qg.QPainter.CompositionMode_Clear)
            self.painter5_smoke.drawRect(0, 0, self.parent.width(), self.parent.height())

            # sky
            self.painter1_background.setBrush(qg.QBrush(qg.QColor(33, 191, 243)))  # '#5DBCD2'
            self.painter1_background.drawRect(-1, -1, self.parent.width() + 1, self.parent.height() + 1)

            # after sky we draw second layer - surface
            self.update_surface()
            self.ebene2_surface_image = self.ebene2_surface.toImage()

            alive = 0
            for each in self.players:
                if each.hp > 0:
                    alive += 1
            # Still a problem, when the current or next player is removed?
            # Probably needs flags (at playercounter)
            """
            for i in range(len(self.players)):
                if self.players[i].hp <= 50:
                    self.players.pop(i)
            """
            if alive == 1:
                for each in self.players:
                    if each.hp > 0:
                        self.painter4_interface.setPen(qc.Qt.black)
                        self.painter4_interface.setFont(qg.QFont('Helvetica', 12))
                        self.painter4_interface.drawText(200, 50, each.name + " won!")
                        self.victory = True
            elif alive == 0:
                self.painter4_interface.setPen(qc.Qt.black)
                self.painter4_interface.setFont(qg.QFont('Helvetica', 12))
                self.painter4_interface.drawText(200, 50, "Well played! Nobody alive!")
                self.victory = True
            else:
                self.time()

            # movement and shooting not allowed between rounds
            if not self.timer_between_rounds_begin:
                self.movement()
                if self.bullet_shot_allowed:
                    self.bullets[self.current_player] = Bullet(self, self.current_player)
            self.bullet_shot_allowed = False

            for i in range(len(self.players)):
                self.players[i].paint()

            # layer 3 is for objects, so bullets can proof if layer is not transparent
            self.ebene3_object_image = self.ebene3_object.toImage()

            for i in range(len(self.players)):
                if self.bullets[i] is not None:
                    self.bullets[i].paint()

            for i in range(len(self.hits) - 1, -1, -1):
                self.hits[i].paint()
                if self.hits[i].destruct:
                    del self.hits[i]

            for i in range(len(self.explosions) - 1, -1, -1):
                self.explosions[i].paint()
                if self.explosions[i].destruct:
                    del self.explosions[i]

            # test why does the frame sets to pen color?
            self.painter1_background.setPen(qc.Qt.black)
            self.painter2_surface.setPen(qc.Qt.black)
            self.painter3_object.setPen(qc.Qt.black)
            self.painter4_interface.setPen(qc.Qt.black)

            # self.painter2.drawPixmap(0, 0, self.ebene3)
            self.painter1_background.drawPixmap(0, 0, self.ebene2_surface)
            self.painter1_background.drawPixmap(0, 0, self.ebene3_object)
            self.painter1_background.drawPixmap(0, 0, self.ebene4_interface)
            self.painter1_background.drawPixmap(0, 0, self.ebene5_smoke)
            self.setPixmap(self.ebene1_background)

        finally:
            if not self.victory:
                qc.QTimer.singleShot(self.game_speed, self.run)
            else:
                buttonReply = qw.QMessageBox.question(self, 'Worms 2D', "Would you like to play again?",
                                                      qw.QMessageBox.Yes | qw.QMessageBox.No, qw.QMessageBox.No)
                if buttonReply == qw.QMessageBox.Yes:
                    # print('Yes clicked.')
                    self.parent.setCentralWidget(MainMenu(self.parent))
                    self.parent.setCentralWidget(GameWindow(self.parent))
                else:
                    # print('No clicked.')
                    self.parent.setCentralWidget(MainMenu(self.parent))

    def update_surface(self):
        # connect paint methods to layers
        # surface
        self.painter2_surface.setBrush(qg.QBrush(qg.QColor('#743b29')))
        self.painter2_surface.setCompositionMode(qg.QPainter.CompositionMode_DestinationOver)

        # new
        self.painter2_surface.drawPixmap(0, 0, self.ebene0_generic_surface)
        # old
        # self.painter2.drawRect(0, self.parent.height()-80, self.parent.width(), 80)

        # collisions
        self.painter2_surface.setBrush(qg.QBrush(qg.QColor(0, 0, 0, 0)))
        self.painter2_surface.setCompositionMode(qg.QPainter.CompositionMode_Clear)
        self.painter2_surface.setPen(qc.Qt.black)
        self.painter2_surface.setBrush(qc.Qt.black)
        # print(len(self.collisions))
        for i in self.collisions_to_surface:
            # i[0,1] - x,y is a colliding point
            # i[2] is an explosion radius
            # drawEllipse uses x,y as a top left coordintes, that's why we need to perform some calc.
            self.painter2_surface.drawEllipse(i[0] - i[2] / 2, i[1] - i[2] / 2, i[2], i[2])

    def mouseMoveEvent(self, event):
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        # alpha = self.ebene2_surface_image.pixel(self.m_x, self.m_y)  # .alpha()
        # alpha2 = self.ebene3_object_image.pixel(self.m_x, self.m_y)  # .alpha()
        # self.parent.statusBar().showMessage(str(self.f(self.m_x)))
        # self.parent.statusBar().showMessage("a: "+str(alpha)+" b: "+str(alpha2))

    def mousePressEvent(self, e):
        # print("lclick", self.gun.v/10)
        if self.bullets[self.current_player] == None:
            # print(self.weapon.currentIndex())
            self.bullet_shot_allowed = True

    # Pressing A, D, Left or Right switches the status of self.movement_left or *_right to True
    def keyPressEvent(self, event):
        if (event.key() == qc.Qt.Key_D or event.key() == qc.Qt.Key_Right) and not event.isAutoRepeat():
            self.movement_right = True
        elif (event.key() == qc.Qt.Key_A or event.key() == qc.Qt.Key_Left) and not event.isAutoRepeat():
            self.movement_left = True

    # Releasing any Key switches both movement values to False
    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.movement_right = False
            self.movement_left = False

    # Dependent on status from self.movement_left and *_right the tank is moving
    def movement(self):
        if self.movement_right:
            # if not an end of a screen
            if self.players[self.current_player].x_player + self.players[
                self.current_player].tank_width != self.parent.width():
                # if a slope is not vertical
                if self.ebene2_surface_image.pixel(self.players[self.current_player].x_player + 4,
                                                   self.players[self.current_player].y_player - 5) == 0:
                    self.players[self.current_player].x_player += 0.5
                    # print(self.players[self.current_player].rotation, " ", self.players[self.current_player].left_point)
        if self.movement_left:
            # if not an end of a screen
            if self.players[self.current_player].x_player - self.players[self.current_player].tank_width != 0:
                # if a slope is not vertical
                if self.ebene2_surface_image.pixel(self.players[self.current_player].x_player - 4,
                                                   self.players[self.current_player].y_player - 5) == 0:
                    self.players[self.current_player].x_player -= 0.5

    def time(self):
        if self.timer_between_rounds_begin:
            time_pass_between_rounds = datetime.now() - self.time_between_start
            show_between = self.time_between_rounds - time_pass_between_rounds.seconds

            if show_between < 0:
                self.timer_between_rounds_begin = False

            self.painter4_interface.setPen(qc.Qt.black)
            self.painter4_interface.setFont(qg.QFont('Helvetica', 12))
            if show_between > 1:
                self.painter4_interface.drawText(50, 50, str(self.players[self.current_player].name) +
                                                 ", it's your turn in " + str(show_between) + " seconds!")
            elif show_between > 0:
                self.painter4_interface.drawText(50, 50, str(self.players[self.current_player].name) +
                                                 ", it's your turn in " + str(show_between) + " second!!")
            else:
                self.painter4_interface.drawText(50, 50, str(self.players[self.current_player].name) +
                                                 "! Go for it!")

        else:
            if self.timer_begin:
                self.r_start = datetime.now()
                self.timer_begin = False

            time_pass_round = datetime.now() - self.r_start
            show = self.time_for_round - time_pass_round.seconds

            if show < 0:
                self.timer_begin = True

                if self.current_player + 1 >= len(self.players):
                    self.current_player = 0
                else:
                    self.current_player += 1

                self.timer_between_rounds_begin = True
                self.time_between_start = datetime.now()

            self.painter4_interface.setPen(qc.Qt.black)
            self.painter4_interface.setFont(qg.QFont('Helvetica', 12))
            self.painter4_interface.drawText(50, 50, str(self.players[self.current_player].name) +
                                             ", it's your turn! Time left: " + str(show))


class Hit:
    def __init__(self, parent, x, y, dmg, koeff, crit):
        self.parent = parent
        self.x = x
        self.y = y - 30  # not in a Tank, but slightly above
        self.y_start = self.y
        self.y_end = 100  # how long should we display dmg
        self.dmg = dmg
        self.koeff = koeff
        self.crit = crit
        self.destruct = False

    def paint(self):
        # if we showed this hit long enough, by this attr we can delete it.
        # print("i'm drawing")
        if (self.y_start - self.y) / self.y_end > 0.9:  # 90% of self.y_end is covered - next is too slow.
            self.destruct = True

        if self.crit:
            test = "Critical! "
            self.parent.painter4_interface.setFont(
                qg.QFont('CorpoS', 14, weight=qg.QFont.Bold, italic=qg.QFont.StyleItalic))
        else:
            test = ""
            self.parent.painter4_interface.setFont(qg.QFont('Helvetica', 12))

        if self.koeff == 1:
            self.parent.painter4_interface.setPen(qg.QPen(qc.Qt.red, 2, qc.Qt.SolidLine))

            self.parent.painter4_interface.drawText(self.x, self.y, test + str(self.dmg))
        elif self.koeff > 0.5:
            self.parent.painter4_interface.setPen(qg.QPen(qc.Qt.yellow, 2, qc.Qt.SolidLine))
            self.parent.painter4_interface.drawText(self.x, self.y, test + str(self.dmg))
        else:
            self.parent.painter4_interface.setPen(qg.QPen(qc.Qt.green, 2, qc.Qt.SolidLine))
            self.parent.painter4_interface.drawText(self.x, self.y, test + str(self.dmg))

        self.y -= 1.5 - (self.y_start - self.y) / self.y_end


class Bullet:
    def __init__(self, parent, player_number):
        self.parent = parent
        self.criticat = False
        if random.randint(0, 10) == 1: self.criticat = True
        self.player_number = player_number

        # which weapon and where will the bullet start (factor 1.2: little distance to tank cannon)
        self.weapon = parent.weapon_choice
        self.x_bullet = parent.players[self.player_number].x_player + 1.2 * \
                        parent.players[self.player_number].gun_vector[0]
        self.y_bullet = parent.players[self.player_number].y_player + 1.2 * \
                        parent.players[self.player_number].gun_vector[1]

        # Cannon
        if self.weapon == 0:
            self.weight = 10
            self.power = 0.25

            self.damage = 20
            self.explosion = 10

        # Rifle
        elif self.weapon == 1:
            self.weight = 2
            self.power = 0.4

            self.damage = 1
            self.explosion = 1

        # Grenade
        elif self.weapon == 2:
            self.weight = 10
            self.power = 0.15

            self.damage = 40
            self.explosion = 50

        self.gravity = self.parent.gravity * self.weight
        # direction and speed of bullet
        self.bullet_velocity = self.power * parent.players[self.player_number].gun_vector

    def paint(self):
        self.parent.painter3_object.setPen(qg.QPen(qg.QColor(0, 0, 0), 2, qc.Qt.SolidLine))
        self.parent.painter3_object.drawPoint(self.x_bullet, self.y_bullet)

        self.x_bullet += self.bullet_velocity[0]
        self.y_bullet += self.bullet_velocity[1]
        self.collide()
        self.bullet_velocity[1] += self.gravity  # 0.01 smth very light

    def collide(self):
        # check alpha channel - check if there's surface - anything but 0: surface, 0: Air
        # If something hit anything but air on ebene2_surface
        if self.parent.ebene2_surface_image.pixel(self.x_bullet, self.y_bullet) != 0:
            # checks in little steps where the bullet hits the top of the surface
            while self.parent.ebene2_surface_image.pixel(self.x_bullet, self.y_bullet) != 0:
                self.x_bullet -= self.bullet_velocity[0] / 10
                self.y_bullet -= self.bullet_velocity[1] / 10

            # rounded position of bullet
            x_bullet, y_bullet = round(self.x_bullet), round(self.y_bullet)
            self.parent.collisions_to_surface.append([x_bullet, y_bullet, self.explosion])
            self.parent.bullets[self.player_number] = None

            #########right place to initialize smoke#####
            self.parent.explosions.append(Explosion(self, 1))

            ####first implement - we are looking only at ground
            for each in self.parent.players:
                if abs(each.x_player - x_bullet) < each.tank_width_rotated / 2 + self.explosion / 2:
                    if abs(each.y_player - y_bullet) < each.tank_height_rotated / 2 + self.explosion / 2:
                        koeff = 1 - (abs(each.x_player - x_bullet) - each.tank_width_rotated / 2) / (
                                    self.explosion / 2)  # dmg.koeff
                        if koeff > 1: koeff = 1
                        if self.criticat:
                            dmg = float(round(1.5 * self.damage * koeff, 1))
                        else:
                            dmg = float(round(self.damage * koeff, 1))
                            each.hp -= dmg
                        # print(dmg)
                        self.parent.hits.append(
                            Hit(self.parent, each.x_player, each.y_player, dmg, koeff, self.criticat))

        # If something hit anything but air on ebene3_object
        elif self.parent.ebene3_object_image.pixel(self.x_bullet, self.y_bullet) != 0:
            # If it went through it goes back to the top
            while self.parent.ebene3_object_image.pixel(self.x_bullet, self.y_bullet) != 0:
                self.x_bullet -= self.bullet_velocity[0] / 10
                self.y_bullet -= self.bullet_velocity[1] / 10

            # rounded position of bullet
            x_bullet, y_bullet = round(self.x_bullet), round(self.y_bullet)
            self.parent.collisions_to_surface.append([x_bullet, y_bullet, self.explosion])
            self.parent.bullets[self.player_number] = None
            #########right place to initialize smoke#####
            self.parent.explosions.append(Explosion(self, 0))

            for each in self.parent.players:
                if abs(each.x_player - x_bullet) <= each.tank_pixmap.width() / 2 + self.explosion / 2:
                    # distance from hitbox compared to rotated height and explosion radius
                    # "+5" because of some rounding issues - sometimes it didn't recognised the tank
                    if abs(each.y_player - y_bullet) <= each.tank_height_rotated / 2 + self.explosion / 2 + 5:
                        koeff = 1 - (abs(each.x_player - x_bullet) - each.tank_width_rotated / 2) / (
                                    self.explosion / 2)  # dmg.koeff
                        if koeff > 1: koeff = 1
                        # koeff=1
                        if self.criticat:
                            dmg = float(round(1.5 * self.damage * koeff, 1))
                        else:
                            dmg = float(round(self.damage * koeff, 1))
                        each.hp -= dmg
                        # print(dmg)
                        self.parent.hits.append(
                            Hit(self.parent, each.x_player, each.y_player, dmg, koeff, self.criticat))


class Player:
    def __init__(self, parent, color, gun_color, name, number):
        self.parent = parent
        self.name = name
        self.number = number  # place in players array

        self.tank_scaled_to_width = 30
        self.tank_image = qg.QImage("tankwithout01.png")
        self.tank_pixmap = qg.QPixmap.fromImage(self.tank_image)
        self.tank_pixmap = self.tank_pixmap.scaledToWidth(self.tank_scaled_to_width)

        # original width and height without rotation
        self.tank_width = self.tank_scaled_to_width  # length of tank_pixmap
        self.tank_height = self.tank_scaled_to_width * 0.6  # height of tank_pixmap
        # width and height within rotation
        self.tank_width_rotated = self.tank_pixmap.width()
        self.tank_height_rotated = self.tank_pixmap.height()
        self.start_position_distance = 80
        # x- and y-coordinates, prevent nearly same start positions
        # describes center position of tank image
        self.x_player = self.start_position_x()
        self.y_player = self.start_position_y()
        self.corr = 10  # offset from ground (there's an ugly difference from plain and gradient)
        self.weight = 500
        self.len = 15  # length of tank cannon (painted version)
        self.color = color  # color of tank (painted version - outdated)
        self.hp_max = 300
        self.hp = self.hp_max
        self.gun_color = gun_color  # color of gun
        self.gun_vector = np.array([1, 1])
        self.vector = 0
        self.left_point = [0, 0]
        self.right_point = [0, 0]
        self.tank_rotation = 0

    # calculation of x-coordinate fpr start position, each player has a distance
    # of self.start_position_distance between each other if it needs more than
    # 50 tries to get an x_coordinate, self.start_position_distance will be ignored
    def start_position_x(self):
        if len(self.parent.players) > 0:
            position_not_found = True
            not_found_termination = 0
            while position_not_found:
                if not_found_termination > 50:
                    print("Problem bei der Ermittlung der Startposition bei einem Abstand von",
                          self.start_position_distance, "bei Spieler", self.number, "(" + self.name + ").")
                    break
                not_found_termination += 1
                start_position = random.randint(self.tank_width, self.parent.parent.width() - self.tank_width)
                position_not_found = False
                for each in self.parent.players:
                    if (each.x_player - self.start_position_distance) < start_position < (
                            each.x_player + self.start_position_distance):
                        position_not_found = True
                        break
        else:
            start_position = random.randint(self.tank_width, self.parent.parent.width() - self.tank_width)
        return start_position

    # calculation of y-coordinate (height) for start position
    # begins at top and draws closer to surface
    def start_position_y(self):
        y_coordinate = 0
        while self.parent.ebene2_surface_image.pixel(self.x_player, y_coordinate) == 0:
            y_coordinate += 10
        while self.parent.ebene2_surface_image.pixel(self.x_player, y_coordinate) != 0:
            y_coordinate -= 2
        return y_coordinate - 10

    def paint(self):
        ##body
        if self.hp <= 0:
            self.color = qc.Qt.gray
            self.gun_color = qc.Qt.gray
        self.parent.painter3_object.setPen(qg.QPen(self.color, 2, qc.Qt.SolidLine))
        self.parent.painter3_object.setBrush(qg.QBrush(self.color))
        # debugger view - hitbox (allerdings auf gleicher Ebene -> dient nur zur Fehlerbeseitigung)
        # self.parent.painter3_object.drawRect(self.x_player - self.tank_length / 2, self.y_player - self.tank_height / 2,self.tank_length,self.tank_height)

        tank_pixmap = self.tank_pixmap

        self.left_point = [self.x_player - self.tank_width / 4, self.y_player + self.corr]
        self.right_point = [self.x_player + self.tank_width / 4, self.y_player + self.corr]

        if self.parent.ebene2_surface_image.pixel(self.left_point[0], self.left_point[1]) == 0:
            while self.parent.ebene2_surface_image.pixel(self.left_point[0], self.left_point[1]) == 0:
                self.left_point[1] += 1
        else:
            while self.parent.ebene2_surface_image.pixel(self.left_point[0], self.left_point[1]) != 0:
                self.left_point[1] -= 1

        if self.parent.ebene2_surface_image.pixel(self.right_point[0], self.right_point[1]) == 0:
            while self.parent.ebene2_surface_image.pixel(self.right_point[0], self.right_point[1]) == 0:
                self.right_point[1] += 1
        else:
            while self.parent.ebene2_surface_image.pixel(self.right_point[0], self.right_point[1]) != 0:
                self.right_point[1] -= 1

        self.vector = np.array([self.right_point[0] - self.left_point[0], self.right_point[1] - self.left_point[1]])

        if np.linalg.norm(self.vector) != 0:
            self.vector = self.vector / np.linalg.norm(self.vector)

        self.tank_rotation = round(90 - math.acos(self.vector[1]) / math.pi * 180)

        # print(self.rotation)
        tank_transform = qg.QTransform().rotate(self.tank_rotation)
        tank_pixmap = tank_pixmap.transformed(tank_transform, qc.Qt.SmoothTransformation)
        self.tank_height_rotated = tank_pixmap.height()
        self.tank_width_rotated = tank_pixmap.width()

        # if self.number == 0:
        # print("tank_rotation:", self.tank_rotation)
        # print("tank_transform_dx:", tank_transform.dx())
        # print("tank_transform_dy:", tank_transform.dy())
        # print("tank_pixmap.width():", tank_pixmap.width())
        # print("tank_pixmap.height():", tank_pixmap.height())

        self.parent.painter3_object.drawPixmap(self.x_player - self.tank_width / 2,
                                               self.y_player - self.tank_height / 2 + 1, tank_pixmap)
        # self.parent.painter4.setBrush(qg.QBrush(qc.Qt.red))
        # self.parent.painter3.drawLine(self.left_point[0],self.left_point[1],self.right_point[0],self.right_point[1])

        ##name
        self.parent.painter4_interface.setPen(qg.QPen(qc.Qt.black, 2, qc.Qt.SolidLine))
        self.parent.painter4_interface.setFont(qg.QFont('Helvetica', 12))
        self.parent.painter4_interface.drawText(self.x_player - self.tank_width / 2, self.y_player - self.tank_height,
                                                self.name)

        ##hp bar
        percent = self.hp / self.hp_max
        color = qc.Qt.green
        if percent < 0.4:
            color = qc.Qt.red
        elif percent < 0.80:
            color = qc.Qt.yellow
        if self.hp > 0:
            self.parent.painter4_interface.setPen(qg.QPen(color, 2, qc.Qt.SolidLine))
            self.parent.painter4_interface.setBrush(qg.QBrush(color))
            self.parent.painter4_interface.drawRect(self.x_player - self.tank_width / 2,
                                                    self.y_player - self.tank_height + 2, self.tank_width * percent, 2)
        else:
            self.parent.painter4_interface.setPen(qg.QPen(qc.Qt.red, 2, qc.Qt.SolidLine))
            self.parent.painter4_interface.setFont(qg.QFont('Helvetica', 12))
            self.parent.painter4_interface.drawText(self.x_player - self.tank_width / 2,
                                                    self.y_player + self.tank_height + 12, "dead")

        ##gun
        ###do not update self.gun_vector if it is not your turn!
        if self.parent.current_player == self.number:
            gun_vector = np.array([self.parent.mouse_x - self.x_player, self.parent.mouse_y - self.y_player])
            if np.linalg.norm(gun_vector) != 0:
                self.gun_vector = gun_vector / np.linalg.norm(gun_vector)
                self.gun_vector *= self.len

        self.parent.painter3_object.setPen(qg.QPen(self.gun_color, 2, qc.Qt.SolidLine))
        self.parent.painter3_object.drawLine(self.x_player, self.y_player, self.x_player + self.gun_vector[0],
                                             self.y_player + self.gun_vector[1])

        # DEBUG-Ausgabe der Position des aktuellen Spielers
        # TODO: Hitbox/Transformation ist noch nicht optimal (nicht abhängig von der Transformation)
        # TODO: Panzerkanone wird noch immer gezeichnet, statt durch die Grafik angezeigt zu werden
        """
        if self.parent.current_player == self.number:
            print("self.x_player: ", self.x_player)
            print("self.y_player: ", self.y_player)
            print("\n\n")
        """

        ###check if on ground
        self.on_ground()

    def on_ground(self):
        if self.y_player + self.corr >= self.parent.height() - 2:
            self.hp = 0
            self.y_player += 4 * self.tank_height
        else:
            # check alpha chanel
            if self.parent.ebene2_surface_image.pixel(self.x_player, self.corr + self.y_player + 2) == 0:
                self.y_player += 2
            # if we will move a player and it hits the ground
            elif self.parent.ebene2_surface_image.pixel(self.x_player, self.corr + self.y_player - 1) != 0:
                self.y_player -= 1


class Explosion:
    def __init__(self, parent, ground):
        self.parent = parent
        self.x_explosion = parent.x_bullet
        self.y_explosion = parent.y_bullet

        ###make smoke depend on current gun
        self.amount = 0
        if self.parent.weapon == 0:
            self.amount = random.randint(20, 50)
        elif self.parent.weapon == 1:
            self.amount = random.randint(2, 5)
        elif self.parent.weapon == 2:
            self.amount = random.randint(100, 150)

        self.opacity = 100
        self.timer = 300
        self.destruct = False
        self.smoke = []
        self.parts = []

        for i in range(self.amount):
            self.smoke.append(Part(self, 1))
        if ground == 1:
            for i in range(round(self.amount)):
                self.parts.append(Part(self, 0))

    def paint(self):
        delete = -1
        if self.timer > 0:
            for i in range(self.amount):
                self.smoke[i].paint()
            for i in range(len(self.parts) - 1, -1, -1):
                self.parts[i].paint()
                if self.parent.parent.ebene3_object_image.pixel(self.parts[i].x_part, self.parts[i].y_part) != 0:
                    for each in self.parent.parent.players:
                        x_parts = round(self.parts[i].x_part)
                        y_parts = round(self.parts[i].y_part)
                        # print(x,y)

                        if abs(each.x_player - x_parts) <= each.tank_width_rotated:
                            if abs(each.y_player - y_parts) <= each.tank_height_rotated:
                                critical = False
                                if random.randint(1, 10) == 1:
                                    critical = True
                                koeff = 1
                                if critical:
                                    dmg = float(round(15 * 0.1 * koeff, 1))
                                else:
                                    dmg = float(round(0.1 * koeff, 1))
                                each.hp -= dmg
                                self.parent.parent.hits.append(
                                    Hit(self.parent.parent, each.x_player, each.y_player, dmg, koeff, critical))

                    # self.parent.parent.collisions.append([x, y, self.parts[i].explosion])
                    del self.parts[i]
                elif self.parent.parent.ebene2_surface_image.pixel(self.parts[i].x_part, self.parts[i].y_part) != 0:
                    if self.parent.parent.ebene2_surface_image.pixel(
                            self.parts[i].x_part - self.parts[i].part_vector[0],
                            self.parts[i].y_part - self.parts[i].part_vector[1]) == 0:
                        while self.parent.parent.ebene2_surface_image.pixel(self.parts[i].x_part,
                                                                            self.parts[i].y_part) != 0:
                            self.parts[i].x_part -= self.parts[i].part_vector[0] / 10
                            self.parts[i].y_part -= self.parts[i].part_vector[1] / 10
                    x_part, y_part = round(self.parts[i].x_part), round(self.parts[i].y_part)
                    self.parent.parent.collisions_to_surface.append([x_part, y_part, self.parts[i].explosion_size])
                    del self.parts[i]
            self.timer -= 1
            self.opacity -= 0.3

        else:
            self.destruct = True


class Part:
    def __init__(self, parent, smoke):
        self.parent = parent
        self.smoke = smoke
        color = [qg.QColor(214, 143, 76), qg.QColor(175, 108, 40), qg.QColor(132, 72, 13), qg.QColor(81, 53, 25),
                 qg.QColor(40, 28, 16)]
        self.color = color[random.randint(0, len(color) - 1)]

        self.gravity = self.parent.parent.gravity
        self.part_vector = [0, 0]
        if self.smoke == 1:
            self.weight = random.uniform(-0.01, -0.001)
            self.part_vector = [0, random.uniform(-0.5, 0)]
            self.x_part = random.randint(round(parent.x_explosion - self.parent.parent.explosion / 2),
                                         round(parent.x_explosion + self.parent.parent.explosion / 2))
            self.y_part = random.randint(round(self.parent.y_explosion), round(
                self.parent.y_explosion + math.sqrt(
                    abs((self.parent.parent.explosion / 2) ** 2 - (self.x_part - parent.x_explosion) ** 2))))

        else:
            self.x_part = self.parent.x_explosion
            self.y_part = self.parent.y_explosion
            self.weight = random.uniform(0.1, 0.3)
            self.part_vector = [random.uniform(-1, 1), -1]
        self.smoke_size = 4  # for smoke
        self.explosion_size = 2  # for particles

    def paint(self):
        if self.parent.opacity > 0:
            opacity = self.parent.opacity
        else:
            opacity = 0
        if self.smoke == 1:
            self.color = qg.QColor(150, 150, 150, opacity)
            self.x_part += self.part_vector[0]
            self.y_part += self.part_vector[1]
            self.part_vector[1] += self.weight * self.gravity
            self.part_vector[0] += self.weight * 2 * 0  # effect of "wind" on smoke appears here

            if 0 < int(self.y_part) < self.parent.parent.parent.height() and 0 < int(self.x_part) < self.parent.parent.parent.width():
                #print(self.parent.parent.parent.wind_map[int(self.y_part)][int(self.x_part)])
                #print(int(self.y_part), ",", int(self.x_part))
                self.part_vector[0] += self.weight * self.parent.parent.parent.wind_map[int(self.y_part)][int(self.x_part)]
            else:
                #print("Out of bound:", self.x_part, ",", self.y_part)
                self.part_vector[0] += self.weight * 2 * 0

            self.parent.parent.parent.painter5_smoke.setCompositionMode(qg.QPainter.CompositionMode_DestinationOver)
            self.parent.parent.parent.painter5_smoke.setPen(self.color)
            self.parent.parent.parent.painter5_smoke.setBrush(self.color)
            self.parent.parent.parent.painter5_smoke.drawEllipse(self.x_part - self.smoke_size / 2,
                                                                 self.y_part - self.smoke_size / 2, self.smoke_size,
                                                                 self.smoke_size)
        else:
            self.x_part += self.part_vector[0]
            self.y_part += self.part_vector[1]
            self.part_vector[1] += self.weight * self.gravity

            self.parent.parent.parent.painter1_background.setPen(
                qg.QPen(self.color, self.explosion_size, qc.Qt.SolidLine))
            self.parent.parent.parent.painter1_background.drawPoint(self.x_part, self.y_part)
            # self.parent.parent.parent.painter.setBrush(self.color)
            # self.parent.parent.parent.painter.drawEllipse(self.x - self.d / 4, self.y - self.d / 4, self.d/2, self.d/2)


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
