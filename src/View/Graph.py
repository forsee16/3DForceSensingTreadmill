import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from collections import deque
from src.Model.DataAccesor import Data


class MplCanvas(FigureCanvas): ## MathPlotLib canvas for plotting the graphs
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class AnimationWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        vbox = QtWidgets.QVBoxLayout()
        self.canvas = MplCanvas(self, width=7, height=4, dpi=100)
        self.navi_toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(self.navi_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)

        self.line, = self.canvas.axes.plot([], [], animated=True, lw=2)
        self.canvas.axes.set_xlim(0, 100)
        self.canvas.axes.set_ylim(-20, 20)
        self.bufferSize = Data.getBufferSize() # how much of the graph is displayed
        self.ani = ControlFuncAnimation(self.canvas.figure, self.update_graph, init_func=self.init, fargs=(self.line,), blit=True, interval=25)

    # init first frame of graph to empty
    def init(self):
        self.line.set_data([], [])
        return self.line,


    # this function gets called by FuncAnimation at specified intervals (specified in the ControlFuncAnimation)
    # frame is an int which starts at 0
    def update_graph(self, frame, a0):
        #x = np.linspace(0, 20, 1000)
        #y = np.sin(x - 0.01 *frame) #
        #data = self.readSerial() # data read from the serial port
        data = Data.getData()
        self.line.set_data(range(self.bufferSize), data) # x is unchanging
        return self.line,

    #start plotting points
    def start(self):
        Data.startCollecting()
        self.ani._start()

    #stop plotting
    def stop(self):
        self.ani._stop()

    def plot(self):
        pass


class ControlFuncAnimation(animation.FuncAnimation):
    """ This is a slight modification to the animation class to allow pausing
    starting and stopping."""
    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
            save_count=None, auto_start=False, **kwargs):
        self.fig = fig # fig is an instance of the MplCanvas class
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