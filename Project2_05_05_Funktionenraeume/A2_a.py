import numpy as np
import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class App(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Aufgabe 2: Spline Kurven'
        self.setMinimumHeight(qw.QDesktopWidget().height() // 3)
        self.setMinimumWidth(qw.QDesktopWidget().width() // 3)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Aufgabe 2: Spline Kurven')
        self.setCentralWidget(DrawWidget(self))
        self.show()


class DrawWidget(qw.QWidget):
    def __init__(self, parent):
        qw.QWidget.__init__(self, parent)
        self.main_window = parent  # Main Window
        self.pane = Pane(self)
        sizePolicy = qw.QSizePolicy(qw.QSizePolicy.Ignored, qw.QSizePolicy.Ignored)
        self.pane.setSizePolicy(sizePolicy)
        # self.pane.setScaledContents(True)

        hbox = qw.QHBoxLayout()
        vbox = qw.QVBoxLayout()

        b_A2_c = qw.QPushButton('A2_c', self)
        b_A2_c.setToolTip('A2_c')
        b_A2_c.clicked.connect(self.pane.A2_main_c)

        b_A2_b = qw.QPushButton('A2_b', self)
        b_A2_b.setToolTip('A2_b')
        b_A2_b.clicked.connect(self.pane.A2_main_b)

        b_A2_b_np = qw.QPushButton('A2_b_np', self)
        b_A2_b_np.setToolTip('A2_b')
        b_A2_b_np.clicked.connect(self.pane.A2_main_b_np)

        b_clear = qw.QPushButton('Clear', self)
        b_clear.setToolTip('Clear the Graph')
        b_clear.clicked.connect(self.on_click_clear)

        b_clear_pane = qw.QPushButton('Undo', self)
        b_clear_pane.setToolTip('remove last change')
        b_clear_pane.clicked.connect(self.on_click_undo)

        """b_plot = qw.QPushButton('Plot', self)
        b_plot.setToolTip('Plot a Graph')
        b_plot.clicked.connect(self.on_click_plot)"""

        """self.cm_type = qw.QComboBox(self)
        self.cm_type.addItem("normal")
        self.cm_type.addItem("speed up")
        self.cm_type.addItem("slow down")
        self.cm_type.activated.connect(self.on_click_type)

        cm_style = qw.QComboBox(self)
        cm_style.setToolTip('choose a style')
        cm_style.addItem("Fusion")
        cm_style.addItem("Windows")
        cm_style.addItem("macintosh")
        # m_style.addItem("Plastique")
        # cm_style.addItem("Cleanlooks")
        cm_style.addItem("windowsvista")
        cm_style.activated[str].connect(self.style_choice)

        b_show_cv = qw.QCheckBox('Show CV', self)
        b_show_cv.clicked.connect(lambda: self.on_click_show_cv(b_show_cv.checkState()))
        b_show_cv.setChecked(True)"""

        vbox.addWidget(b_A2_b)
        vbox.addWidget(b_A2_b_np)
        vbox.addWidget(b_A2_c)
        vbox.addWidget(b_clear)
        vbox.addWidget(b_clear_pane)
        # vbox.addWidget(b_plot)
        # vbox.addWidget(self.cm_type)
        # vbox.addWidget(cm_style)
        # vbox.addWidget(b_show_cv)

        vbox.addStretch(1)

        hbox.addWidget(self.pane)

        hack = qw.QWidget()
        hack.setLayout(vbox)
        hack.setFixedWidth(110)

        hbox.addWidget(hack)

        self.setLayout(hbox)

    def on_click_clear(self):
        self.pane.clear_all_surfaces()

    def on_click_plot(self):
        self.pane.plot()

    def on_click_new_path(self):
        if len(self.pane.current_cv) != 0:
            self.pane.paths.append(self.pane.current_path)
            self.pane.current_path = qg.QPainterPath()

            self.pane.cvs.append(self.pane.current_cv)
            self.pane.current_cv = np.array([]).reshape(0, 2)

    def on_click_undo(self):
        self.pane.undo()

    def on_click_show_cv(self, value):
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

        self.y_at = self.height() // 2

        self.fill_all_default()  # cleans all surfaces
        self.set_all_painters()  # create all painters

        self.paths = []
        self.cvs = []
        self.current_path = qg.QPainterPath()

        self.painter_cv.setPen(qg.QPen(self.color, 3, qc.Qt.SolidLine))
        self.painter_cv.drawPath(self.current_path)

        self.current_cv = np.array([]).reshape(0, 2)
        self.A2b = np.array([]).reshape(0, 2)
        self.showCV = True

        self.update()

    def resolution_of_surfases(self):
        self.end_all_painters()

        self.ebene_pane = qg.QPixmap(self.width(), self.height())
        self.ebene_cv = qg.QPixmap(self.width(), self.height())
        self.ebene_schlitten = qg.QPixmap(self.width(), self.height())
        self.ebene_total = qg.QPixmap(self.width(), self.height())

        self.y_at = self.height() // 2

        # print(self.width(), self.h)
        self.fill_all_default()

        self.set_all_painters()

        self.update()
        #self.plot()

    def fill_all_default(self):
        self.ebene_pane.fill(qg.QColor(0, 0, 0))
        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_schlitten.fill(qg.QColor(0, 0, 0, 0))
        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))

    def set_all_painters(self):
        self.painter_cv = qg.QPainter(self.ebene_cv)
        #self.painter_cv.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_pane = qg.QPainter(self.ebene_pane)
        #self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_schlitten = qg.QPainter(self.ebene_schlitten)
        self.painter_total = qg.QPainter(self.ebene_total)

        self.painter_pane.setPen(qg.QPen(qc.Qt.white, 1, qc.Qt.SolidLine))
        self.painter_pane.drawLine(0, self.y_at, self.width(), self.y_at)

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
        self.current_path = qg.QPainterPath()

        self.cvs = []
        self.current_cv = np.array([]).reshape(0, 2)
        self.A2b = np.array([]).reshape(0, 2)
        self.update()

    def undo(self):
        self.paths = self.paths[:-1]
        self.update()

    def undo2(self):
        if len(self.current_cv) == 0:
            if len(self.cvs) != 0:
                self.current_cv = self.cvs[-1]
                self.cvs = self.cvs[:-1]
                self.paths = self.paths[:-1]

        if len(self.current_cv) != 0:
            self.current_cv = self.current_cv[:-1]
            if len(self.current_cv) != 0:
                self.current_path = qg.QPainterPath()
                self.current_path.moveTo(self.current_cv[0][0], self.current_cv[0][1])
                for i in range(len(self.current_cv)):
                    self.current_path.lineTo(self.current_cv[i][0], self.current_cv[i][1])
        self.update()
        #self.plot()

    def show_cv(self, value):
        self.showCV = value
        self.update()

    def update(self):
        """ draws control points (vertexes) and Paths """
        self.ebene_cv.fill(qg.QColor(0, 0, 0, 0))

        if self.showCV:
            path = self.current_path
            color = qc.Qt.blue
            thickness = 1
            self.painter_cv.setPen(qg.QPen(color, thickness, qc.Qt.SolidLine))
            # draw actual path
            self.painter_cv.drawPath(path)
            # draw old paths
            for i in range(len(self.paths)):
                path = self.paths[i]
                self.painter_cv.drawPath(path)

            # draw old paths
            """for j in range(len(self.cvs)):
                for i in range(self.cvs[j].shape[0]):
                    self.painter_cv.setPen(qg.QPen(color, 6, qc.Qt.SolidLine))
                    self.painter_cv.drawPoint(self.cvs[j][i][0], self.cvs[j][i][1])
            # draw actual path
            for i in range(self.current_cv.shape[0]):
                self.painter_cv.setPen(qg.QPen(color, 6, qc.Qt.SolidLine))
                self.painter_cv.drawPoint(self.current_cv[i][0], self.current_cv[i][1])"""

        if self.A2b.size >1:
            for x in range(self.A2b.size-1):
                #self.painter_cv.drawPoint(x,self.A2b[x])
                self.painter_cv.drawLine(x, self.A2b[x], x+1, self.A2b[x+1])

        self.ebene_total.fill(qg.QColor(0, 0, 0, 0))
        self.painter_total.drawPixmap(0, 0, self.ebene_pane)
        self.painter_total.drawPixmap(0, 0, self.ebene_cv)
        self.painter_total.drawPixmap(0, 0, self.ebene_schlitten)
        self.setPixmap(self.ebene_total)


    def plot(self):
        self.painter_pane.end()
        self.ebene_pane.fill(qg.QColor(0, 0, 0))
        self.painter_pane = qg.QPainter(self.ebene_pane)
        #self.painter_pane.setRenderHint(qg.QPainter.Antialiasing, True)
        self.painter_pane.setPen(qg.QPen(qc.Qt.white, 1, qc.Qt.SolidLine))
        self.painter_pane.drawLine(0, self.y_at, self.width(), self.y_at)

        def p_1(t):
            return 1 / 6 * t ** 3

        def p_2(t):
            return 1 / 6 * (1 + 3 * t + 3 * t ** 2 - 3 * t ** 3)

        def p_3(t):
            return 1 / 6 * (4 - 6 * t ** 2 + 3 * t ** 3)

        def p_4(t):
            return 1 / 6 * (1 - 3 * t + 3 * t ** 2 - t ** 3)

        def b(t):
            if t <= 0:
                return 0
            elif t <= 1:
                return p_1(t)
            elif t <= 2:
                return p_2(t - 1)
            elif t <= 3:
                return p_3(t - 2)
            elif t <= 4:
                return p_4(t - 3)
            else:
                return 0

        def b_sp(t, i):
            return b(t - i)

        def change_color(color):
            if color % 2 == 1:
                return qc.Qt.green
            else:
                return qc.Qt.darkCyan

        def test(x, y, color):
            path = qg.QPainterPath()

            break_j = 0
            farbe = change_color(color[0])
            self.painter_pane.setPen(qg.QPen(farbe, 3, qc.Qt.SolidLine))
            path.moveTo(x[0], y[0])
            for j in range(len(x)):
                path.lineTo(x[j], y[j])
                if j + 1 != len(color):
                    if color[j] != color[j + 1]:
                        break_j = j + 1
                        break
            self.painter_pane.drawPath(path)
            if break_j != 0:
                # print(f"len(x):{len(x)}, len(color):{len(color)}, break_j:{break_j}")
                return test(x[break_j:], y[break_j:], color[break_j:])

        def spline(cv):
            """
            :param cv: Control vertexes
            :return: x and y array for spline-curve
            """
            k = len(cv)  # Amount of CV
            if k < 4:
                print("insufficient control points")
                return False

            t_min, t_max = 1, k - 2  # Axe for shifted basis functions
            x = []
            y = []
            color = []
            color_temp = 0
            color_temp_v2 = 1
            t = t_min
            while t <= t_max:
                subsum_x = 0
                subsum_y = 0
                for i in range(0, k):
                    b = b_sp(t, i - 2)
                    # if b > 0.66:
                    #    color_temp = i
                    subsum_x += cv[i][0] * b
                    # print(f"P_x:{cv[i][0]} b_sp({t},{i}):{b}")
                    subsum_y += cv[i][1] * b
                if color_temp_v2 + 1 <= t:
                    color_temp_v2 += 1
                x.append(subsum_x)
                y.append(subsum_y)
                color.append(color_temp_v2)

                t += 0.01

            # print("x:", x)
            # print("y:", y)
            # print("color: ", color)
            return x, y, color

        def bspline(cv, n=100, degree=3):
            """ Calculate n samples on a bspline
                cv :      Array of control vertices
                n  :      Number of samples to return
                degree:   Curve degree
            """
            cv = np.asarray(cv)
            count = len(cv)

            degree = np.clip(degree, 1, count - 1)

            # Calculate knot vector
            kv = None
            kv = np.clip(np.arange(count + degree + 1) - degree, 0, count - degree)

            # Calculate query range
            u = np.linspace(False, (count - degree), n)

            # Calculate result
            # return np.array(si.splev(u, (kv,cv.T,degree))).T

        self.painter_pane.setPen(qg.QPen(qc.Qt.red, 3, qc.Qt.SolidLine))

        for i in range(len(self.cvs)):
            # p = bspline(self.cvs[i], n=len(self.cvs[i])*10)
            # x, y = p.T
            temp = spline(self.cvs[i])
            if temp:
                x, y, color = temp[0], temp[1], temp[2]
                test(x, y, color)

        # actual path, if it is not empty!
        if len(self.current_cv) != 0:
            # p = bspline(self.current_cv, n=len(self.current_cv)*10) # n - amount of interpolated points
            # x, y = p.T
            temp = spline(self.current_cv)
            if temp:
                x, y, color = temp[0], temp[1], temp[2]
                # if len(x) > 10:
                # x, y = x[5:], y[5:]
                # x, y = x[:-5], y[:-5]
                # print(x)
                test(x, y, color)

        self.update()

    def get_n(self):
        return self.current_cv[:,0].size

    def get_t(self):
        n = self.get_n()
        return np.linspace(0, 2*np.pi, 2*n + 1)

    def get_f_Ti(self, t):
        x = self.current_cv[:, 0]
        y = self.current_cv[:, 1] - self.y_at
        x_vals = np.linspace(0, self.width(), self.width() + 1)
        y_interp = np.interp(x_vals, x, y)

        return y_interp[int(self.width() * t / (2 * np.pi))]


    def lambda_m_sin(self, m):
        n = self.get_n()
        t = self.get_t()

        subsum = 0
        for i in range(n):
            subsum += np.sin(m * t[i]) * self.get_f_Ti(t[i])
        return 1/n * 2 * np.pi * subsum

    def lambda_m_cos(self, m):
        n = self.get_n()
        t = self.get_t()

        subsum = 0
        for i in range(n):
            subsum += np.cos(m * t[i]) * self.get_f_Ti(t[i])
        return 1/n * 2 * np.pi * subsum


    def A2_main_b(self):
        self.paths.append(self.current_path)

        if self.current_cv[:,0].size >1 :
            if self.current_cv[-1][0] == self.width():
                #print(self.lambda_m_sin(2))
                path = qg.QPainterPath()

                first = True
                for t in self.get_t():
                    y = 0

                    for m in range(self.get_n()):
                        y += self.lambda_m_sin(m) * np.sin(m * t) + self.lambda_m_cos(m) * np.cos(m * t)

                    y += self.height()//2
                    if first:
                        path.moveTo(int(t / (2*np.pi)*self.width()), y)
                        path.lineTo(int(t / (2*np.pi)*self.width()) + 0.1, y + 0.1)
                    else:
                        path.lineTo(int(t / (2 * np.pi) * self.width()), y)
                    first = False
                    #print(y)
                self.paths.append(path)

        self.update()

    def A2_main_b_np(self):
        self.paths.append(self.current_path)

        x = self.current_cv[:, 0]
        y = self.current_cv[:, 1] - self.y_at
        x_vals = np.linspace(0, self.width(), self.width() + 1)
        y_interp = np.interp(x_vals, x, y)
        y_fft = np.fft.fft(y_interp)

        path = qg.QPainterPath()
        path.moveTo(x_vals[0],y_fft[0]+self.height()//2)
        for i in range(len(y_fft)):
            path.lineTo(x_vals[i], y_fft[i]+self.height()//2)

        self.paths.append(path)
        self.update()


    def A2_main_c(self):
        self.paths.append(self.current_path)

        if self.current_cv[:,0].size >1 :
            if self.current_cv[-1][0] == self.width():
                #print(self.lambda_m_sin(2))
                for m in range(5,7):
                    path = qg.QPainterPath()
                    first = True
                    for t in self.get_t():
                        y = self.lambda_m_sin(m) * np.sin(m * t) + self.height()/5
                        if first:
                            path.moveTo(int(t / (2*np.pi)*self.width()),y)
                            path.lineTo(int(t / (2*np.pi)*self.width()) + 0.1, y + 0.1)
                        else:
                            path.lineTo(int(t / (2 * np.pi) * self.width()), y)
                        first = False
                    self.paths.append(path)
        self.update()



    #def plot_A2(self):




    def mousePressEvent(self, event):
        # print("click")
        x = event.pos().x()
        y = event.pos().y()
        if self.current_path.isEmpty():
            if x < 10:
                x = 0
            else:
                return
            self.current_path.moveTo(x, y)
            self.current_path.lineTo(x + 0.1, y + 0.1)
            self.current_cv = np.r_[self.current_cv, [[x, y]]]
            #self.fun_A2_a()

        if self.current_cv[-1][0] < x:
            if x > self.width()-10:
                x = self.width()
            self.current_path.lineTo(x, y)
            self.current_cv = np.r_[self.current_cv, [[x, y]]]
            #self.fun_A2_a()
            # print(f"last:{self.current_cv[-1]}, current:{x}")
        # print(self.current_cv, self.current_cv[:, 0] )

        #print(self.A2b)
        self.update()
        # self.plot()


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
