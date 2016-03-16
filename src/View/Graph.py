from __future__ import unicode_literals
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


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