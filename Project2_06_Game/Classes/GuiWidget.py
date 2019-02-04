import numpy as np
import scipy.interpolate as si
import sys
from datetime import date
import time

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
        self.player = Player(0, 0, self.pane.ebene_pane, self.pane.track)
        self.run = True

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
        b_game = qw.QPushButton('Play', self)
        b_game.setToolTip('Play')
        b_game.clicked.connect(self.on_click_game)

        b_pause = qw.QPushButton('play/pause', self)
        b_pause.setToolTip('play/pause')
        b_pause.clicked.connect(self.on_click_play_pause)

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
        vbox_side_menu.addWidget(b_game)
        vbox_side_menu.addWidget(b_pause)

        vbox_side_menu.addStretch(1)

        vbox_side_menu.addWidget(b_move_to_center)
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
        for i in range(len(self.pane.cvs)):
            self.pane.cvs[i] -= self.pane.track_movement
        self.pane.current_cv -= self.pane.track_movement
        self.pane.track_movement -= self.pane.track_movement

        if len(self.pane.cvs) > 0:
            self.pane.draw_path_between_cv(only_old=True)
        if len(self.pane.current_cv) > 0:
            self.pane.draw_path_between_cv(only_current=True)

        self.pane.plot()
        self.pane.update()

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
        self.player = Player(self.pane.width()//2, 0, self.pane.ebene_pane,self.pane.track)
        #self.b_show_cv.setChecked(False)
        #self.on_click_show_cv(self.b_show_cv.checkState())
        self.pane.update()
        self.game_loop()

    def game_loop(self):
        self.player.show(self.pane.ebene_schlitten, self.pane.painter_schlitten)
        self.player.next()
        self.pane.update_game()
        if self.run:
            self.timer = qc.QTimer.singleShot(40, self.game_loop)
        #qc.QTimer.singleShot(20, self.game_loop)

    def on_click_play_pause(self):
        self.run = not self.run
        print("hi")

    def update_gui(self):
        # tbd, how to update a function in GuiWidget from Pane? How to send a signal?
        self.b_show_tracking_position.setText(f"Position: ({self.pane.track_movement[0]},{self.pane.track_movement[1]})")


