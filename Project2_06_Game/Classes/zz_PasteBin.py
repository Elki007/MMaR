"""
Nur eine Datei, um Code zwischenzulagern, falls es noch einmal wichtig werden könnte

"""

# Von Pane
def mouseMoveEvent(self, QMouseEvent):
    """ Shows plotted data on the fly by left click and drag the cvs by right clicks - 1st version """
    x = QMouseEvent.pos().x()
    y = QMouseEvent.pos().y()

    if QMouseEvent.buttons() == qc.Qt.LeftButton:
        self.current_cv[-1] = x, y
    elif QMouseEvent.buttons() == qc.Qt.RightButton:
        self.current_cv += x - self.mousePressedCoords[0], y - self.mousePressedCoords[1]
        for i in range(len(self.cvs)):
            self.cvs[i] += x - self.mousePressedCoords[0], y - self.mousePressedCoords[1]
        self.mousePressedCoords = [x, y]

    self.update()
    self.plot()