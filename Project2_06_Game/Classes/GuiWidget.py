import numpy as np
import scipy.interpolate as si
import sys
import time
import json
import qtawesome as qta

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

from Pane import Pane
from Path import Path
from Player import Player


class GuiWidget(qw.QWidget):
    """ Widgets and Buttons """
    def __init__(self, parent):
        qw.QWidget.__init__(self, parent)
        self.main_window = parent  # Main Window
        self.pane = Pane(self)
        self.player = Player(self.pane.width()//2, 0, self.pane.ebene_schlitten, self.pane.painter_schlitten, self.pane.ebene_pane, self.pane.track)
        self.run = True
        self.forward = True

        # button: new path
        b_new = qw.QPushButton('New path', self)
        b_new.setToolTip('Creates another path')
        b_new.clicked.connect(self.on_click_new_path)

        # button: clear everything
        b_clear = qw.QPushButton('Clear', self)
        b_clear.setToolTip('Clears everything')
        b_clear.clicked.connect(self.on_click_clear)

        # button: remove last change
        b_remove_step = qw.QPushButton('Undo', self)
        b_remove_step.setToolTip('Removes last change')
        b_remove_step.clicked.connect(self.on_click_undo)

        # button: center position
        b_move_to_center = qw.QPushButton('Center', self)
        b_move_to_center.setToolTip('Removes last change')
        b_move_to_center.clicked.connect(self.on_click_move_to_center)

        # button: start game
        self.b_game = qw.QPushButton('Play', self)
        self.b_game.setToolTip('Play')
        self.b_game.clicked.connect(self.on_click_game)

        styling_icon = qta.icon('fa5s.pause',
                                #active='fa5s.balance-scale',
                                color='black',
                                color_active='orange')

        self.b_pause = qw.QPushButton(styling_icon, "play/pause", self)
        self.b_pause.setToolTip('play/pause')
        self.b_pause.clicked.connect(self.on_click_play_pause)

        self.b_back = qw.QPushButton("slow backward", self)
        self.b_back.setToolTip('slow backward')
        self.b_back.clicked.connect(self.on_click_play_back)

        b_save = qw.QPushButton('Save', self)
        b_save.setToolTip('Save')
        b_save.clicked.connect(self.on_click_save)

        b_load = qw.QPushButton('Load', self)
        b_load.setToolTip('Load')
        b_load.clicked.connect(self.on_click_load)

        """b_plot = qw.QPushButton('Plot', self)
        b_plot.setToolTip('Plot a Graph')
        b_plot.clicked.connect(self.on_click_plot)"""

        # different colors/options for path
        self.cm_type = qw.QComboBox(self)
        self.cm_type.addItem("normal")
        self.cm_type.addItem("speed up")
        self.cm_type.addItem("slow down")
        self.cm_type.activated.connect(self.on_click_type)

        # different styles for buttons/elements in gui
        cm_style = qw.QComboBox(self)
        cm_style.setToolTip('choose a style')
        cm_style.addItem("Fusion")
        cm_style.addItem("Windows")
        cm_style.addItem("macintosh")
        #cm_style.addItem("Plastique")
        #cm_style.addItem("Cleanlooks")
        cm_style.addItem("windowsvista")
        cm_style.activated[str].connect(self.style_choice)

        # shows direct connection between control vertices
        self.b_show_cv = qw.QCheckBox('Show CV', self)
        self.b_show_cv.clicked.connect(lambda: self.on_click_show_cv(self.b_show_cv.checkState()))
        self.b_show_cv.setChecked(True)

        # tracking position
        self.b_show_tracking_position = qw.QLabel(f"Position: {self.pane.track_movement}")
        # tracking zoom
        self.b_show_tracking_zoom = qw.QLabel(f"Zoom: {self.pane.track_zoom}")

        #                    #
        # Layout begins here #
        #                    #

        hbox_pane_menu = qw.QHBoxLayout()  # pane und side menu
        vbox_side_menu = qw.QVBoxLayout()  # side menu order

        # creates menu order
        vbox_side_menu.addWidget(b_new)  # creates new path
        vbox_side_menu.addWidget(b_clear)  # clears everything
        vbox_side_menu.addWidget(b_remove_step)  # remove last step
        #vbox.addWidget(b_plot)
        vbox_side_menu.addWidget(self.cm_type)
        vbox_side_menu.addWidget(cm_style)
        vbox_side_menu.addWidget(self.b_show_cv)
        vbox_side_menu.addWidget(self.b_game)
        vbox_side_menu.addWidget(self.b_pause)
        vbox_side_menu.addWidget(self.b_back)
        vbox_side_menu.addWidget(b_save)
        vbox_side_menu.addWidget(b_load)

        vbox_side_menu.addStretch(1)

        vbox_side_menu.addWidget(b_move_to_center)
        vbox_side_menu.addWidget(self.b_show_tracking_zoom)
        vbox_side_menu.addWidget(self.b_show_tracking_position)

        # set position of pane and side menu
        hbox_pane_menu.addWidget(self.pane)

        side_menu = qw.QWidget()
        side_menu.setLayout(vbox_side_menu)
        side_menu.setFixedWidth(160)  # 80 with other resolution -> other unit than pixel?

        hbox_pane_menu.addWidget(side_menu)

        self.setLayout(hbox_pane_menu)

        #
        # Aktualisiert die globale Positionsverschiebung
        #

        self.timer = qc.QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(10)

        self.timer_4_game = qc.QTimer()
        self.timer_4_game.setInterval(10)
        self.timer_4_game.setSingleShot(True)
        self.timer_4_game.timeout.connect(self.game_loop)

    # function for button 'New Path'
    def on_click_new_path(self):
        if len(self.pane.current_cv) != 0:
            self.pane.paths.append(self.pane.current_path)
            self.pane.current_path = Path(qg.QPainterPath(), self.cm_type.currentText())
            #print(self.cm_type.currentText())
            #print(self.pane.current_path.color)
            self.pane.cvs.append(self.pane.current_cv)
            self.pane.current_cv = np.array([]).reshape(0, 2)

    # function for button 'Clear'
    def on_click_clear(self):
        self.pane.clear_all_surfaces()

    # function for button 'Undo'
    def on_click_undo(self):
        self.pane.undo()

    # function for box 'Show CV'
    def on_click_show_cv(self, value):
        """ value = True or False """
        self.pane.show_cv(value)

    def on_click_move_to_center(self):
        """ to move everything back to the start position """
        self.pane.move_to_center()

        #TODO: Wieso wird Pane erst nach den 2 Sekunden sichtbar aktualisiert und nicht mit update()-Aufruf?
        #time.sleep(2)
        #print("DEBUG: Haiho")

    # function for style options
    def style_choice(self, text):
        qw.QApplication.setStyle(qw.QStyleFactory.create(text))

    # functions for path color/function
    def on_click_type(self):
        text = self.cm_type.currentText()
        self.pane.current_path.changed_style(text)
        self.pane.plot()

    def resizeEvent(self, event):
        self.pane.resolution_of_surfaces()

    # starts endless while with the game
    def on_click_game(self):
        self.player = Player(self.pane.width()//2, 0, self.pane.ebene_schlitten, self.pane.painter_schlitten, self.pane.ebene_pane, self.pane.track)
        self.b_show_cv.setChecked(False)
        self.b_game.setText("Restart")
        #self.on_click_show_cv(self.b_show_cv.checkState())
        self.pane.update()
        #self.game_loop()


        self.timer_4_game.start()

    def game_loop(self):
        self.player.show()
        if self.run:
            self.player.next()
            self.pane.update_game()
            self.timer_4_game.start()

            #self.timer = qc.QTimer.singleShot(10, self.game_loop)
        #qc.QTimer.singleShot(20, self.game_loop)

    def on_click_play_pause(self):
        self.run = not self.run
        print("hi", self.run)
        if self.run:
            self.player.track = self.pane.track
            styling_icon = qta.icon('fa5s.pause', color='black', color_active='orange')
            self.timer_4_game.start()
        else:
            styling_icon = qta.icon('fa5s.play', color='black', color_active='orange')
            self.timer_4_game.stop()
        self.b_pause.setIcon(styling_icon)
        #self.game_loop()

    def on_click_play_back(self):
        self.forward = not self.forward
        #print("hi", self.run)
        if self.forward:
            #self.player.track = self.pane.track
            self.b_back.setText("backward")
            #self.player.time_direction = 1
            #self.player.g = self.player.g * (-1)
            self.player.time_speed = 0.01
            #styling_icon = qta.icon('fa5s.pause', color='black', color_active='orange')
        else:
            self.b_back.setText("forward")
            #self.player.time_control_point = time.time()
            #self.player.g = self.player.g * (-1)
            self.player.time_speed = 0.001
            #styling_icon = qta.icon('fa5s.play', color='black', color_active='orange')
        #self.b_pause.setIcon(styling_icon)
        #self.game_loop()

    def on_click_save(self):
        np.save('current_cv.npy', self.pane.current_cv)  # .npy extension is added if not given
        np.save('cvs.npy', self.pane.cvs)
        colors = []
        for i in range(len(self.pane.paths)):
            colors.append(self.pane.paths[i].color)
            print(self.pane.paths[i].color)

        with open('colors.txt', 'w') as filehandle:
            json.dump(colors, filehandle)

    def on_click_load(self):
        self.pane.track = []
        self.pane.current_cv = np.load('current_cv.npy')


        path = qg.QPainterPath()
        path.moveTo(self.pane.current_cv[0][0], self.pane.current_cv[0][1])
        for j in range(len(self.pane.current_cv)):
            x, y = self.pane.current_cv[j][0], self.pane.current_cv[j][1]
            self.pane.track.append([x, y])
            path.lineTo(x, y)
        self.pane.current_path = Path(path,"normal")

        temp = np.load('cvs.npy')
        self.pane.cvs = []
        for i in range(len(temp)):
            self.pane.cvs.append(temp[i])

        colors = []
        with open('colors.txt', 'r') as filehandle:
            colors = json.load(filehandle)


        for n in range(len(self.pane.cvs)):
            path = qg.QPainterPath()
            type = 5
            if colors[n] == 10:
                type = "normal"
            elif colors[n] == 13:
                type = "speed up"
            elif colors[n] == 5:
                type = "slow down"

            path.moveTo(self.pane.cvs[n][0][0], self.pane.cvs[n][0][1])
            for j in range(len(self.pane.cvs[n])):
                x, y = self.pane.cvs[n][j][0], self.pane.cvs[n][j][1]
                self.pane.track.append([x, y])
                path.lineTo(x, y)
            self.pane.paths.append(Path(path,type))


        print(self.pane.cvs, " \n len: ",len(self.pane.cvs))

        self.pane.update()
        self.pane.plot()
        self.pane.update()
        #self.pane.update()

    def update_gui(self):
        # tbd, how to update a function in GuiWidget from Pane? How to send a signal?
        self.b_show_tracking_position.setText(self.pane.display_tracking_position())
        self.b_show_tracking_zoom.setText(self.pane.display_tracking_zoom())



