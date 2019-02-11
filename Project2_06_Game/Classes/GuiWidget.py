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
        self.player = Player(self, self.pane.width()//2, 0, self.pane, self)
        self.pane.player_created(self.player)  # So pane can track every new Player object (easier this way)
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
        self.b_game = qw.QPushButton('Start', self)
        self.b_game.setToolTip('Start')
        self.b_game.clicked.connect(self.on_click_game)

        styling_icon = qta.icon('fa5s.pause',
                                #active='fa5s.balance-scale',
                                color='black',
                                color_active='orange')

        self.b_pause = qw.QPushButton(styling_icon, "", self)
        self.b_pause.setToolTip('play/pause')
        self.b_pause.clicked.connect(self.on_click_play_pause)

        styling_icon = qta.icon('fa5s.step-forward',
                                # active='fa5s.balance-scale',
                                color='black',
                                color_active='orange')

        self.b_sf = qw.QPushButton(styling_icon,"", self)
        self.b_sf.setToolTip('step forward')
        self.b_sf.clicked.connect(self.on_click_step_forward)

        styling_icon = qta.icon('fa5s.step-backward',
                                # active='fa5s.balance-scale',
                                color='black',
                                color_active='orange')

        self.b_sb = qw.QPushButton(styling_icon, "", self)
        self.b_sb.setToolTip('step backward')
        self.b_sb.clicked.connect(self.on_click_step_backward)

        styling_icon = qta.icon('fa5s.backward',
                                # active='fa5s.balance-scale',
                                color='black',
                                color_active='orange')

        self.b_back = qw.QPushButton(styling_icon, "", self)
        self.b_back.setToolTip('backward')
        self.b_back.clicked.connect(self.on_click_backward)

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

        # enters the edit mode and disable show_cv
        self.b_edit_mode = qw.QCheckBox('Edit Mode', self)
        self.b_edit_mode.clicked.connect(lambda: self.on_click_edit_mode(self.b_edit_mode.checkState()))
        self.b_edit_mode.setChecked(False)

        # tracking player position
        self.b_show_tracking_player = qw.QCheckBox('Tracking Player', self)
        self.b_show_tracking_player.clicked.connect(lambda: self.on_click_tracking_player(self.b_show_tracking_player.checkState()))
        self.b_show_tracking_player.setChecked(False)

        # tracking position
        self.b_show_tracking_position = qw.QLabel(self.pane.display_tracking("position"))
        # tracking zoom
        self.b_show_tracking_zoom = qw.QLabel(self.pane.display_tracking("zoom"))

        #                    #
        # Layout begins here #
        #                    #

        hbox_pane_menu = qw.QHBoxLayout()  # pane und side menu
        vbox_side_menu = qw.QVBoxLayout()  # side menu order

        hbox_time_menu = qw.QHBoxLayout()  # time menu

        mini_hbox_checkboxes = qw.QHBoxLayout()
        mini_hbox_checkboxes.addWidget(self.b_show_cv)
        mini_hbox_checkboxes.addWidget(self.b_edit_mode)

        hbox_time_menu = qw.QHBoxLayout()  # time menu
        hbox_time_menu.addWidget(self.b_back)
        hbox_time_menu.addWidget(self.b_sb)
        hbox_time_menu.addWidget(self.b_pause)
        hbox_time_menu.addWidget(self.b_sf)
        # creates menu order
        vbox_side_menu.addWidget(b_new)  # creates new path
        vbox_side_menu.addWidget(b_clear)  # clears everything
        vbox_side_menu.addWidget(b_remove_step)  # remove last step
        #vbox.addWidget(b_plot)
        vbox_side_menu.addWidget(self.cm_type)
        vbox_side_menu.addWidget(cm_style)
        vbox_side_menu.addLayout(mini_hbox_checkboxes)
        vbox_side_menu.addStretch(1)
        vbox_side_menu.addWidget(self.b_game)
        vbox_side_menu.addWidget(self.b_show_tracking_player)
        vbox_side_menu.addLayout(hbox_time_menu)
        vbox_side_menu.addStretch(1)
        vbox_side_menu.addWidget(b_save)
        vbox_side_menu.addWidget(b_load)

        vbox_side_menu.addStretch(10)

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
        self.pane.create_new_path(self.cm_type.currentText())

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

    # function for box 'Edit Mode'
    def on_click_edit_mode(self, value):
        """ value = True or False """
        self.pane.edit_mode(value)
        if value:
            self.on_click_show_cv(False)
            self.b_show_cv.setDisabled(True)
        else:
            self.b_show_cv.setDisabled(False)
            self.on_click_show_cv(self.b_show_cv.checkState())

    def on_click_tracking_player(self, value):
        """ value = True or False """
        self.pane.tracking_player(value)

    def on_click_move_to_center(self):
        """ to move everything back to the start position """
        self.pane.move_to_center()
        # TODO: Wieso wird Pane erst nach den 2 Sek aktualisiert und nicht mit dem internen update()-Aufruf?
        # Wie lässt sich das ändern?
        #time.sleep(2)
        #print("DEBUG: Haiho")

    # function for style options
    def style_choice(self, text):
        qw.QApplication.setStyle(qw.QStyleFactory.create(text))

    # functions for path color/function
    def on_click_type(self):
        text = self.cm_type.currentText()
        self.pane.change_path_style(text)
        self.pane.plot()
        self.pane.update()

    def resizeEvent(self, event):
        self.pane.resolution_of_surfaces()

    # starts endless while with the game
    def on_click_game(self):
        self.player = Player(self, 20, 200, self.pane, self) #self.pane.width()//2
        self.pane.player_created(self.player)  # So pane can track every new Player object (easier this way)
        self.b_show_cv.setChecked(False)
        self.b_game.setText("Restart")
        #self.on_click_show_cv(self.b_show_cv.checkState())
        self.pane.update()
        #self.game_loop()


        self.timer_4_game.start()

    def game_loop(self):
        self.player.show()
        if self.run:
            if self.forward:
                self.player.next()
            else:
                self.player.prev()
            #self.pane.update_game()  # test for tracking_player
            self.pane.update()
            self.timer_4_game.start()

            #self.timer = qc.QTimer.singleShot(10, self.game_loop)
        #qc.QTimer.singleShot(20, self.game_loop)

    def on_click_play_pause(self):
        self.run = not self.run
        if self.run:
            print("resume")
            styling_icon = qta.icon('fa5s.pause', color='black', color_active='orange')
            self.timer_4_game.start()
        else:
            print("pause")
            styling_icon = qta.icon('fa5s.play', color='black', color_active='orange')
            self.timer_4_game.stop()
        self.b_pause.setIcon(styling_icon)
        #self.game_loop()

    def on_click_step_forward(self):
        self.timer_4_game.stop()
        self.player.show()
        self.player.next()
        #self.pane.update_game()  # test for tracking_player
        self.pane.update()

    def on_click_step_backward(self):
        self.timer_4_game.stop()
        self.player.show()
        self.player.prev()
        #self.pane.update_game()  # test for tracking_player
        self.pane.update()

    def on_click_backward(self):
        #self.timer_4_game.stop()
        self.forward = not self.forward
        if self.forward:
            styling_icon = qta.icon('fa5s.backward', color='black', color_active='orange')
        else:
            styling_icon = qta.icon('fa5s.forward', color='black', color_active='orange')
        self.b_back.setIcon(styling_icon)

        #self.timer_4_game.start()

    def on_click_save(self):
        """ Saves all paths """
        save_paths = self.pane.save_all_paths()
        np.save('something_.npy', save_paths)

    def on_click_load(self):
        """ Load all saved paths """
        # TODO: Nur paths updated, bspw. self.pane.track fehlt
        # self.pane.track = []  # not reimplemented

        load_paths = np.load('something_.npy')
        self.pane.load_all_paths(load_paths)

    def update_gui(self):
        self.b_show_tracking_position.setText(self.pane.display_tracking("position"))
        self.b_show_tracking_zoom.setText(self.pane.display_tracking("zoom"))



