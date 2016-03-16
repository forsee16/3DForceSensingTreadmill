from __future__ import unicode_literals
import random
import datetime
import time
import matplotlib
from matplotlib.backend_bases import TimerBase as tb
from matplotlib.backend_bases import Event
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from numpy import arange, sin, pi
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.animation as animation

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass




class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        #self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        pass

    def update_figure(self, i):
        pass

    def init(self):
        pass



class AnimationWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        vbox = QtWidgets.QVBoxLayout()
        self.canvas = MyMplCanvas(self, width=7, height=4, dpi=100)
        self.navi_toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(self.navi_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)

        self.x = np.linspace(0, 5, 400)
        self.p = 0.0
        self.y = np.sin(self.x + self.p)
        #self.y = np.linspace(0, 1, 400)
        self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, lw=2)

        self.ani = ControlFuncAnimation(self.canvas.figure, self.update_line, blit=True, interval=25)

    def update_line(self, i):
        self.p += 0.1
        y = np.sin(self.x + self.p)
        #y = self.y = np.linspace(0, 1, 400)
        self.line.set_ydata(y)
        return [self.line]

    def on_start(self):
        self.ani._start()


    def on_stop(self):
        self.ani._stop()


class MainUI:
    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1048, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralWidgetLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralWidgetLayout.setObjectName("centralWidgetLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_1.addWidget(self.tableView)
        self.horizontalLayout.addLayout(self.verticalLayout_1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.centralWidgetLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1048, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        ########################



        hbox = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("start")
        self.start_button.adjustSize()
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("stop")


        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        self.verticalLayout_2.addLayout(hbox)

        test = AnimationWidget()
        self.verticalLayout_2.addWidget(test)
        self.start_button.clicked.connect(test.on_start)
        self.stop_button.clicked.connect(test.on_stop)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.start_button.setText(_translate("MainWindow", "start"))
        self.stop_button.setText(_translate("MainWindow", "stop"))

class ControlFuncAnimation(animation.FuncAnimation):
    """ This is a slight modification to the animation class to allow pausing
    starting and stopping.

    .. todo::
        improve documentation
    """
    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
            save_count=None, auto_start=False, **kwargs):
        self.fig = fig #This should be done.
        animation.FuncAnimation.__init__(self, fig, func, frames=frames,
                                         init_func=init_func, fargs=fargs,
                                         save_count=save_count, **kwargs)

        self._started = False #Set to false _start will start animation
        if not auto_start:
            self._fig.canvas.mpl_disconnect(self._first_draw_id)
            self._first_draw_id = None

    def _start(self, *args):
        if not self._started:
            if self.event_source is None:
                self.event_source = self.fig.canvas.new_timer()
                self.event_source.interval = self._interval
            animation.FuncAnimation._start(self)
            self._started = True

    def _stop(self, *args):
        if self.event_source:
            animation.FuncAnimation._stop(self, *args)
        self._started = False

