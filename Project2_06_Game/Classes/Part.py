import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import random, math


class Part:
    def __init__(self, player):
        self.parent = player
        self.painter = player.painter
        self.color = qg.QColor(255-random.randint(0,50), 255-random.randint(0,50), 255-random.randint(0,50))

        self.gravity = player.g * 0.03
        self.part_vector = [0, 0]

        self.x_part = self.parent.x
        self.y_part = self.parent.y
        self.weight = random.uniform(0.1, 0.3)
        self.part_vector = [random.uniform(-1, 1), -1]

        self.explosion_size = 2  # for particles

    def paint(self):
        self.x_part += self.part_vector[0]
        self.y_part += self.part_vector[1]
        self.part_vector[1] += (self.gravity * self.weight).y
        # TODO: transformation
        self.painter.setPen(
            qg.QPen(self.color, self.explosion_size, qc.Qt.SolidLine))
        self.painter.drawPoint(self.x_part, self.y_part)
