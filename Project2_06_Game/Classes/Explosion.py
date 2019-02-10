import random
from Part import Part


class Explosion:
    def __init__(self, parent):
        self.parent = parent
        self.x_explosion = parent.x
        self.y_explosion = parent.y

        ###make smoke depend on current gun
        self.amount = random.randint(10, 50)

        self.timer = 300
        self.destruct = False
        self.smoke = []
        self.parts = []

        for i in range(self.amount):
            self.smoke.append(Part(parent))

    def paint(self):
        if self.timer > 0:
            for i in range(self.amount):
                self.smoke[i].paint()
            for i in range(len(self.parts) - 1, -1, -1):
                self.parts[i].paint()

            self.timer -= 1

        else:
            self.destruct = True
