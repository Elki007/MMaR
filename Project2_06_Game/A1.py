import numpy as np
import scipy.interpolate as si
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class App(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Aufgabe 1: Spline Kurven'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Aufgabe 1: Spline Kurven')
        self.setCentralWidget(DrawWidget(self))
        self.setMinimumHeight(qw.QDesktopWidget().height() // 2)
        self.setMinimumWidth(qw.QDesktopWidget().width() // 2)
        self.show()


class DrawWidget(qw.QWidget):
    def __init__(self, parent):
        qw.QWidget.__init__(self, parent)
        self.main_window = parent  # Main Window
        self.pane = Pane(self)
        # vmtl. obsolet durch resizeEvent in Pane
        sizePolicy = qw.QSizePolicy(qw.QSizePolicy.Ignored, qw.QSizePolicy.Ignored)
        self.pane.setSizePolicy(sizePolicy)
        #self.pane.setScaledContents(True)

        hbox = qw.QHBoxLayout()
        vbox = qw.QVBoxLayout()

        b_new = qw.QPushButton('New path', self)
        b_new.setToolTip('New path')
        b_new.clicked.connect(self.on_click_new_path)

        b_clear = qw.QPushButton('Clear', self)
        b_clear.setToolTip('Clear the Graph')
        b_clear.clicked.connect(self.on_click_clear)

        b_clear_pane = qw.QPushButton('Undo', self)
        b_clear_pane.setToolTip('remove last change')
        b_clear_pane.clicked.connect(self.on_click_undo)

        """b_plot = qw.QPushButton('Plot', self)
        b_plot.setToolTip('Plot a Graph')
        b_plot.clicked.connect(self.on_click_plot)"""

        self.cm_type = qw.QComboBox(self)
        self.cm_type.addItem("normal")
        self.cm_type.addItem("speed up")
        self.cm_type.addItem("slow down")
        self.cm_type.activated.connect(self.on_click_type)

        cm_style = qw.QComboBox(self)
        cm_style.setToolTip('choose a style')
        cm_style.addItem("Fusion")
        cm_style.addItem("Windows")
        cm_style.addItem("macintosh")
        #m_style.addItem("Plastique")
        #cm_style.addItem("Cleanlooks")
        cm_style.addItem("windowsvista")
        cm_style.activated[str].connect(self.style_choice)

        b_show_cv = qw.QCheckBox('Show CV', self)
        b_show_cv.clicked.connect(lambda: self.on_click_show_cv(b_show_cv.checkState()))
        b_show_cv.setChecked(True)

        vbox.addWidget(b_new)
        vbox.addWidget(b_clear)
        vbox.addWidget(b_clear_pane)
        #vbox.addWidget(b_plot)
        vbox.addWidget(self.cm_type)
        vbox.addWidget(cm_style)
        vbox.addWidget(b_show_cv)

        vbox.addStretch(1)

        hbox.addWidget(self.pane)

        hack = qw.QWidget()
        hack.setLayout(vbox)
        hack.setFixedWidth(160)  # 80 with other resolution -> other unit than pixel?

        hbox.addWidget(hack)

        self.setLayout(hbox)

    def on_click_clear(self):
        self.pane.clear_all_surfaces()

    def on_click_plot(self):
        self.pane.plot()

    def on_click_new_path(self):
        if len(self.pane.current_cv) != 0:
            self.pane.paths.append(self.pane.current_path)
            self.pane.current_path = Path(qg.QPainterPath(), self.cm_type.currentText())
            print(self.pane.current_path.color)
            self.pane.cvs.append(self.pane.current_cv)
            self.pane.current_cv = np.array([]).reshape(0, 2)

    def on_click_undo(self):
        self.pane.undo()

    def on_click_show_cv(self, value):
        """ value = True or False """
        self.pane.show_cv(value)

    def style_choice(self, text):
        qw.QApplication.setStyle(qw.QStyleFactory.create(text))

    def on_click_type(self):
        text = self.cm_type.currentText()
        self.pane.current_path.changed_style(text)
        self.pane.plot()

    def on_click_hight(self, text):
        self.pane.hight = int(text)
        self.pane.resolution_of_surfases()

    def on_click_width(self, text):
        self.pane.width = int(text)
        self.pane.resolution_of_surfases()

    def resizeEvent(self, event):
        self.pane.resolution_of_surfases()


class Path:
    def __init__(self, path, type):
        self.path = path
        self.type = type
        self.color = qc.Qt.cyan
        self.changed_style(type)

    def changed_style(self, text):
        self.type = text
        if text == "normal":
            self.color = qc.Qt.cyan
        elif text == "speed up":
            self.color = qc.Qt.darkRed
        elif text == "slow down":
            self.color = qc.Qt.gray
        elif text == "ignore":
            self.color = qc.Qt.green


class Pane(qw.QLabel):
    """ Paint surface class """
    def __init__(self, parent):
        """ creates Pane """
        super().__init__()
        self.parent = parent  # App - Main window
        main_window = parent.main_window
        self.style = "normal"
        self.color = qc.Qt.red
        self.thickness = 3
        self.grid = False

        # background for black background with lines of grid/crystal if activated
        self.ebene_pane = qg.QPixmap(self.width(), self.height())
        self.ebene_cv = qg.QPixmap(self.width(), self.height())
        self.ebene_schlitten = qg.QPixmap(self.width(), self.height())
        self.ebene_total = qg.QPixmap(self.width(), self.height())

        self.fill_all_default()     # cleans all surfaces
        self.set_all_painters()     # create all painters

        self.paths = []
        self.cvs = []
        self.current_path = Path(qg.QPainterPath(), "normal")

        self.painter_cv.setPen(qg.QPen(self.color, 3, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.current_path.path)

        self.current_cv = np.array([]).reshape(0, 2)
        self.showCV = True

        self.update()

    def resolution_of_surfases(self):
        self.end_all_painters()

        self.ebene_pane = qg.QPixmap(self.width(), self.height())
        self.ebene_cv = qg.QPixmap(self.width(), self.height())
        self.ebene_schlitten = qg.QPixmap(self.width(), self.height())
        self.ebene_total = qg.QPixmap(self.width(), self.height())

        #print(self.width(), self.h)
        self.fill_all_default()

        self.set_all_painters()

        self.update()
        self.plot()

    def fill_all_default(self):
        self.ebene_pane.fill(qg.QColor(0, 0, 0))
        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_schlitten.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))

    def set_all_painters(self):
        self.painter_cv = qg.QPainter(self.ebene_cv)
        self.painter_cv.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_pane = qg.QPainter(self.ebene_pane)
        self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_schlitten = qg.QPainter(self.ebene_schlitten)
        self.painter_total = qg.QPainter(self.ebene_total)

    def end_all_painters(self):
        self.painter_cv.end()
        self.painter_pane.end()
        self.painter_schlitten.end()
        self.painter_total.end()

    def clear_all_surfaces(self):
        self.end_all_painters()
        self.fill_all_default()
        self.set_all_painters()

        self.paths = []
        self.current_path.path = qg.QPainterPath()

        self.cvs = []
        self.current_cv = np.array([]).reshape(0, 2)
        self.update()

    def undo(self):
        if len(self.current_cv) == 0:
            if len(self.cvs) != 0:
                self.current_cv = self.cvs[-1]
                self.cvs = self.cvs[:-1]
                self.paths = self.paths[:-1]

        if len(self.current_cv) != 0:
            self.current_cv = self.current_cv[:-1]
            if len(self.current_cv) != 0:
                self.current_path.path = qg.QPainterPath()
                self.current_path.path.moveTo(self.current_cv[0][0],self.current_cv[0][1])
                for i in range(len(self.current_cv)):
                    self.current_path.path.lineTo(self.current_cv[i][0], self.current_cv[i][1])
            self.update()
            self.plot()

    def show_cv(self, value):
        """ value = True or False """
        self.showCV = value
        self.update()

    def update(self):
        """ draws everything """
        """ draws control points (vertexes) and Paths """

        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))

        if self.showCV:
            path = self.current_path.path
            color = qc.Qt.blue
            thickness = 1
            self.painter_cv.setPen(qg.QPen(color, thickness, qc.Qt.SolidLine))
            # draw actual path
            self.painter_cv.drawPath(path)
            # draw old paths
            for i in range(len(self.paths)):
                path = self.paths[i].path
                self.painter_cv.drawPath(path)

            # draw old paths
            for j in range(len(self.cvs)):
                for i in range(self.cvs[j].shape[0]):
                    self.painter_cv.setPen(qg.QPen(color, 6, qc.Qt.SolidLine))
                    self.painter_cv.drawPoint(self.cvs[j][i][0], self.cvs[j][i][1])
            # draw actual path
            for i in range(self.current_cv.shape[0]):
                self.painter_cv.setPen(qg.QPen(color, 6, qc.Qt.SolidLine))
                self.painter_cv.drawPoint(self.current_cv[i][0],self.current_cv[i][1])

        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))  # wird woanders wiederholt/überschrieben
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        self.painter_total.drawPixmap(0, 0, self.ebene_cv)
        self.painter_total.drawPixmap(0, 0, self.ebene_schlitten)
        self.setPixmap(self.ebene_total)
        #print("drawing all")

    def plot(self):
        self.painter_pane.end()
        self.ebene_pane.fill(qg.QColor(0, 0, 0))
        self.painter_pane = qg.QPainter(self.ebene_pane)
        self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)

        # bspline -> Bezier
        def bspline(cv, n=100, degree=3):
            """ Calculate n samples on a bspline

                cv :      Array of control vertices
                n  :      Number of samples to return
                degree:   Curve degree
            """
            cv = np.asarray(cv)
            count = len(cv)

            degree = np.clip(degree, 1, count-1)

            # Calculate knot vector
            kv = None
            kv = np.clip(np.arange(count+degree+1)-degree, 0, count-degree)

            # Calculate query range
            u = np.linspace(False, (count-degree), n)

            # Calculate result
            return np.array(si.splev(u, (kv, cv.T, degree))).T

        for i in range(len(self.cvs)):
            p = bspline(self.cvs[i], n=len(self.cvs[i])*10)
            x, y = p.T
            path = qg.QPainterPath()

            path.moveTo(x[0],y[0])
            for j in range(len(x)):
                path.lineTo(x[j],y[j])

            self.painter_pane.setPen(qg.QPen(self.paths[i].color, 3, qc.Qt.SolidLine))
            self.painter_pane.drawPath(path)

        # actual path, if it is not empty!
        if len(self.current_cv) != 0:
            p = bspline(self.current_cv, n=len(self.current_cv)*10) # n - amount of interpolated points
            x, y = p.T
            path = qg.QPainterPath()

            path.moveTo(x[0], y[0])
            for j in range(len(x)):
                path.lineTo(x[j], y[j])

            self.painter_pane.setPen(qg.QPen(self.current_path.color, 3, qc.Qt.SolidLine))
            self.painter_pane.drawPath(path)

        self.update()


        #print(self.current_cv)
        #p = bspline(self.test_cv, n=100)
        #x, y = p.T
        #print(x,y)

    def mousePressEvent(self, event):
        #print("click")
        x = event.pos().x()
        y = event.pos().y()
        if self.current_path.path.isEmpty():
            self.current_path.path.moveTo(x, y)
            self.current_path.path.lineTo(x+0.1, y+0.1)
        self.current_path.path.lineTo(x, y)

        self.current_cv = np.r_[self.current_cv, [[x, y]]]
        #print(self.current_cv, self.current_cv[:, 0] )

        self.update()
        self.plot()


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())

