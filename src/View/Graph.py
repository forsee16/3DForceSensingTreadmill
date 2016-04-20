import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from collections import deque
from src.Model.DataAccesor import Data
import time
import csv
import numpy

class MplCanvas(FigureCanvas): ## MathPlotLib canvas for plotting the graphs
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4):
        fig = Figure(figsize=(width, height), facecolor= "white")
        self.axes = fig.add_subplot(1,1,1)


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
        self.canvas = MplCanvas(self, width=7, height=4)
        self.navi_toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(self.navi_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)
        self.line, = self.canvas.axes.plot([], [], lineWidth=2)
        self.xlabel = "Time (s)"
        self.ylabel = "Force (kg)"
        self.xlimit = (0,20)
        self.ylimit = (0,200)
        self.refreshRate = 0.03
        self.canvas.axes.set_xlim(self.xlimit)
        self.canvas.axes.set_ylim(self.ylimit)
        self.canvas.axes.set_xlabel(self.xlabel)
        self.canvas.axes.set_ylabel(self.ylabel)
        self.ani = ControlFuncAnimation(self.canvas.figure, self.update_graph, init_func=self.init, blit=True, interval=30)


    # init first frame of graph to empty
    def init(self):
        self.line.set_data([], [])
        return self.line,

    # this function gets called by FuncAnimation at specified intervals (specified in the ControlFuncAnimation)
    def update_graph(self, i):
        Data.updateBuffers()
        data = Data.graphDataBuffer
        xdata = numpy.array(range(len(data)))*self.refreshRate
        self.line.set_data(xdata, data)
        if(xdata[-1] >= 20): ## stop collecting at 20 seconds
            temp = self.line,
            self.stop()
            return temp
        return self.line,


    #start plotting points
    def start(self):
        Data.reset()
        Data.startCollecting()
        self.ani._start()

    #stop plotting
    def stop(self):
        self.ani._stop()
        Data.closePort()
        data = Data.graphDataBuffer
        self.canvas.axes.lines.remove(self.line)
        self.line, = self.canvas.axes.plot(numpy.array(range(len(data)))*self.refreshRate, data, lineWidth=2)
        self.canvas.axes.set_xlabel(self.xlabel)
        self.canvas.axes.set_ylabel(self.ylabel)
        self.canvas.axes.set_xlim(self.xlimit)
        self.canvas.axes.set_ylim(self.ylimit)
        self.canvas.draw()

    def loadData(self):
        x=deque()
        y=deque()
        even=True
        with open('force.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                if(even):
                    y.appendleft( float(row[0]))
                even = not even


        counter =0
        counterVal = 0

        while(counter<len(y)):
            x.append(counterVal)
            counterVal = counterVal +0.120
            counter = counter +1
        self.line, = self.canvas.axes.plot(x,y, lineWidth=2)
        self.canvas.axes.set_xlabel(self.xlabel)
        self.canvas.axes.set_ylabel(self.ylabel)
        self.canvas.axes.set_xlim(self.xlimit)
        self.canvas.axes.set_ylim(self.ylimit)
        self.canvas.draw()
        Data.tableDataBuffer = y
        Data.timeBuffer = x
        Data.signal.loadData.emit()


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