import sys
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import font_manager as fm


class MSAPlottingBoard(QFrame):
    def __init__(self, property, controller, ihm_factor=1, width=0, height=0, background_color="", global_font_color="", global_font=None):
        super(MSAPlottingBoard, self).__init__()

        # 2 mean the plotting board will work on windows level and color level configuration for image in 2d
        # 3 mean the plotting board will work on interactive volume rendering configuration for image in 3d
        self.property = property
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.width = width
        self.height = height
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.pos = None
        self.RADIUS = 10
        self.grayScale = [0, 69, 180, 255]
        self.windowLevel = [0, 0, 1, 1]
        self.setAcceptDrops(True)

        self.font1 = {'family': 'Times New Roman',
                      'color': 'red',
                      'weight': 'normal',
                      'size': 6, }

        self.font2 = {'family': 'Times New Roman',
                      'weight': 'normal',
                      'size': 4, }

        self.pos_x = 0
        self.pos_y = 0

        self.windowFirstPointEnable = False
        self.windowSecondPointEnable = False

        self.setFixedSize(self.width, self.height)
        # a figure instance to plot on
        self.figure = plt.figure()

        self.figure.patch.set_facecolor('#333333')

        self.canvas = FigureCanvas(self.figure)
        image_processing_bar = QLabel()
        image_processing_bar.setFixedHeight(self.height * 0.1)

        # set the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(image_processing_bar)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.cpt = 0
        self.mouseLeftButtonPressed = False
        self.mouseLeftButtonDoubleClicked = False

        self.color = ['r-', 'y-', 'b-', 'g-', 'w-', 'm-']
        # self.color = ['red', 'yellow', 'blue', 'green', 'white', 'magenta']

        self.enterEvent = self.figure.canvas.mpl_connect('figure_enter_event',     self.enter_figure)
        self.leaveEvent = self.figure.canvas.mpl_connect('figure_leave_event',     self.leave_figure)
        self.clickEvent = self.figure.canvas.mpl_connect('button_press_event',     self.on_click)
        self.releaseEvent = self.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.motionEvent = self.figure.canvas.mpl_connect('motion_notify_event',   self.on_move)
        self.scrollEvent = self.figure.canvas.mpl_connect('scroll_event',          self.on_scroll)

    def on_scroll(self, event):
        pass
        # print("scroll")

    def on_move(self, event):
        pass
        # print(event.button, event.x, event.y, event.xdata, event.ydata)

    def on_click(self, event):
        if event.dblclick:
            print("double click", event)
            self.mouseLeftButtonDoubleClicked = True

            self.mouseLeftButtonDoubleClicked = False
        else:
            self.mouseLeftButtonPressed = True
            print("click", event)

        # print(event.button, event.x, event.y, event.xdata, event.ydata)

    def on_release(self, event):
        print("release", event)
        self.mouseLeftButtonPressed = False
        pass
        # print(event.button, event.x, event.y, event.xdata, event.ydata)

    def enter_figure(self, event):
        self.setCursor(Qt.CrossCursor)

    def leave_figure(self, event):
        self.setCursor(Qt.ArrowCursor)

    def disconnect_event(self):
        self.canvas.mpl_disconnect(self.enterEvent)
        self.canvas.mpl_disconnect(self.leaveEvent)
        self.canvas.mpl_disconnect(self.clickEvent)
        self.canvas.mpl_disconnect(self.releaseEvent)
        self.canvas.mpl_disconnect(self.motionEvent)
        self.canvas.mpl_disconnect(self.scrollEvent)

    def do_plot_distance_flow(self, count, sequences):
        abssisa = []
        for sequence in sequences:
            abssisa.append([n for n in range(1, len(sequence) + 1)])

        self.clear()

        histo_plot = self.figure.subplots()
        #histo_plot.set_axis_on()

        if self.ihm_factor == 2:
            histo_plot.patch.set_facecolor('#434343')
        elif self.ihm_factor == 1:
            histo_plot.patch.set_facecolor('#333333')

        compteur = 0
        plots = []
        max_y = 0
        for x in range(len(sequences)):
            temp, = histo_plot.plot(abssisa[x], sequences[x], self.color[x], label="candi." + str(compteur), linewidth=0.5, ms=1)
            if len(sequences[x]) > 1:
                if max(sequences[x]) > max_y:
                    max_y = max(sequences[x])

            plots.append(temp)
            compteur += 1

        legend = plt.legend(handles=plots, prop=self.font2)
        # 设置坐标刻度值的大小以及刻度值的字体
        plt.tick_params(labelsize=3)
        labels = histo_plot.get_xticklabels() + histo_plot.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        [label.set_fontsize(6) for label in labels]

        plt.xlabel('frame index', fontdict=self.font1)
        plt.ylabel('distance', fontdict=self.font1)
        histo_plot.spines['bottom'].set_linewidth(0.5)
        histo_plot.spines['bottom'].set_color("#0C6D56")
        histo_plot.spines['left'].set_linewidth(0.5)
        histo_plot.spines['left'].set_color("#0C6D56")
        histo_plot.spines['top'].set_linewidth(0.5)
        histo_plot.spines['top'].set_color("#0C6D56")
        histo_plot.spines['right'].set_linewidth(0.5)
        histo_plot.spines['right'].set_color("#0C6D56")
        histo_plot.tick_params(axis='y', width=0.5, colors='#ECDEDE')
        histo_plot.tick_params(axis='x', width=0.5, colors='#ECDEDE')

        plt.grid(axis="y", linestyle='-')

        if max_y > 60:
            histo_plot.set_yticks(np.arange(int(max_y*0.2), max_y, 30))
            histo_plot.vlines(36, 0, max_y, color="red")
        else:
            histo_plot.set_yticks(np.arange(20, 60, 20))
            histo_plot.vlines(36, 0, 60, color="red")
        histo_plot.set_xticks(np.arange(0, count, 10))

        self.update()

    def set_background_color_string(self, color_string):
        self.setStyleSheet("background-color:" + color_string)

    def set_background_color(self, r, g, b):
        self.setStyleSheet("background-color:rgb(" + str(r) + "," + str(g) + "," + str(b) + ");")

    def clear(self):
        self.figure.clear()

    def update(self):
        self.canvas.draw()

    def plot(self, grayscale, frequency, extreme_pts):
        self.clear()

        histo_plot = self.figure.add_axes([0, 0, 1, 1])
        histo_plot.set_axis_on()

        if self.ihm_factor == 2:
            histo_plot.patch.set_facecolor('#434343')
        elif self.ihm_factor == 1:
            histo_plot.patch.set_facecolor('#2F2F2F')

        histo_plot.plot(grayscale, frequency, 'green')

        i = 0
        for pts in extreme_pts:
            # print "extreme_pts: ", '(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')'
            if i % 3 == 0:
                histo_plot.annotate('(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')',
                                    (grayscale[pts], frequency[pts]),
                                    arrowprops=dict(arrowstyle='->'),
                                    xytext=(grayscale[pts], frequency[pts] + 100000))
            elif i % 3 == 1:
                histo_plot.annotate('(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')',
                                    (grayscale[pts], frequency[pts]),
                                    arrowprops=dict(arrowstyle='->'),
                                    xytext=(grayscale[pts], frequency[pts] + 150000))
            elif i % 3 == 2:
                histo_plot.annotate('(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')',
                                    (grayscale[pts], frequency[pts]),
                                    arrowprops=dict(arrowstyle='->'),
                                    xytext=(grayscale[pts], frequency[pts] + 200000))

            i += 1

        self.update()
        self.cpt += 1

    def plot(self, grayscale, frequency):
        self.figure.clear()

        histo_plot = self.figure.add_axes([0, 0, 1, 1])
        histo_plot.set_axis_on()

        if self.ihm_factor == 2:
            histo_plot.patch.set_facecolor('#434343')
        elif self.ihm_factor == 1:
            histo_plot.patch.set_facecolor('#2F2F2F')

        histo_plot.plot(grayscale, frequency, 'green')

        """
         i = 0
        for pts in extreme_pts:
            # print "extreme_pts: ", '(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')'
            if i % 3 == 0:
                histo_plot.annotate('(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')',
                                    (grayscale[pts], frequency[pts]), arrowprops=dict(arrowstyle='->'),
                                    xytext=(grayscale[pts], frequency[pts] + 100000))
            elif i % 3 == 1:
                histo_plot.annotate('(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')',
                                    (grayscale[pts], frequency[pts]),
                                    arrowprops=dict(arrowstyle='->'),
                                    xytext=(grayscale[pts], frequency[pts] + 150000))
            elif i % 3 == 2:
                histo_plot.annotate('(' + str(grayscale[pts]) + ',' + str(frequency[pts]) + ')',
                                    (grayscale[pts], frequency[pts]),
                                    arrowprops=dict(arrowstyle='->'),
                                    xytext=(grayscale[pts], frequency[pts] + 200000))

            i += 1
        """

        self.canvas.draw()
        self.cpt += 1

    def plot_points(self, pts):

        x = []
        y = []

        for pt in pts:
            x.append(pt[0])
            y.append(pt[1])

        # calculate polynomial
        z = np.polyfit(x, y, 3)
        f = np.poly1d(z)

        # calculate new x's and y's
        x_new = np.linspace(x[0], x[-1], 50)
        y_new = f(x_new)

        self.figure.clear()

        histo_plot = self.figure.add_subplot(111, axisbg=(50.0 / 255, 50.0 / 255, 50.0 / 255))
        histo_plot.plot(x, y)
        # histo_plot.spines['right'].set_color('none')
        # histo_plot.spines['top'].set_color('none')
        # histo_plot.xaxis.set_ticks_position('bottom')
        # histo_plot.set_xticks([60, 120])
        # histo_plot.set_xlim([0, 160])
        # histo_plot.set_xticklabels(['Level\n', 'Window\n'])

        # histo_plot.set_yticks([60, 120])
        # histo_plot.set_ylim([0, 160])
        # histo_plot.set_yticklabels(['Threshold\n', 'balabala\n'])

        # for tick in histo_plot.xaxis.get_major_ticks():
        #     tick.label.set_fontsize(10)
        #     # specify integer or one of preset strings, e.g.
        #     # tick.label.set_fontsize('x-small')
        #     tick.label.set_rotation('horizontal')
        #
        # for tick in histo_plot.yaxis.get_major_ticks():
        #     tick.label.set_fontsize(10)
        #     # specify integer or one of preset strings, e.g.
        #     # tick.label.set_fontsize('x-small')
        #     tick.label.set_rotation('vertical')
        #
        # plt.annotate(
        #     'peak\nvalley',
        #     xy=(120, 3000), arrowprops=dict(arrowstyle='->'), xytext=(200, 6000))

        histo_plot.grid()

        self.canvas.draw()
        self.cpt += 1

    def on_right_button_press_event(self, event):
        # x, y = event.xdata, event.ydata
        if self.windowFirstPointEnable:
            self.grayScale[1] = self.pos_x
            self.windowLevel[1] = self.pos_y

        elif self.windowSecondPointEnable:
            self.grayScale[2] = self.pos_x
            self.windowLevel[2] = self.pos_y

    def on_motion(self, event):
        self.pos_x, self.pos_y = event.xdata, event.ydata

        if self.pos_x is not None:

            if self.pos_x == self.grayScale[1]:
                dist1 = math.fabs(self.pos_y - self.windowLevel[1])
                if dist1 == 0:
                    self.windowFirstPointEnable = not self.windowFirstPointEnable
                    self.setCursor(QCursor(Qt.CrossCursor))
                else:
                    self.windowFirstPointEnable = False
                    self.setCursor(QCursor(Qt.ArrowCursor))

            elif self.pos_x == self.grayScale[2]:
                dist2 = math.fabs(self.pos_y - self.windowLevel[2])
                if dist2 == 0:
                    self.windowSecondPointEnable = not self.windowSecondPointEnable
                    self.setCursor(QCursor(Qt.CrossCursor))
                else:
                    self.windowFirstPointEnable = False
                    self.setCursor(QCursor(Qt.ArrowCursor))
            else:

                temp_w1 = self.pos_x - self.grayScale[1]
                temp_h1 = self.pos_y - self.windowLevel[1]
                dist3 = math.sqrt(math.fabs(temp_w1) ** 2 + math.fabs(temp_h1) ** 2)

                temp_w2 = self.pos_x - self.grayScale[2]
                temp_h2 = self.pos_y - self.windowLevel[2]
                dist4 = math.sqrt(math.fabs(temp_w2) ** 2 + math.fabs(temp_h2) ** 2)

                if dist3 < self.RADIUS:
                    self.windowFirstPointEnable = not self.windowFirstPointEnable
                    self.setCursor(QCursor(Qt.CrossCursor))
                elif dist4 < self.RADIUS:
                    self.windowSecondPointEnable = not self.windowFirstPointEnable
                    self.setCursor(QCursor(Qt.CrossCursor))
                else:
                    self.windowFirstPointEnable = False
                    self.windowSecondPointEnable = False
                    self.setCursor(QCursor(Qt.ArrowCursor))

    def update_background_color(self, color_string):
        self.setStyleSheet("background-color: " + color_string)