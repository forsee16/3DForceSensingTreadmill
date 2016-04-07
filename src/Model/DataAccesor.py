from src.Input.fakeSerial import Serial
from collections import deque
from PyQt5.QtCore import pyqtSignal, QObject
import time

## inheriting from QObject allows the class to emit signals that indicate model has started collecting data
class Signal(QObject):

    startedCollecting = pyqtSignal()

# class is static so that the table and graph classes have access to the same data
class Data():

    bufferSize = 100
    dataBuffer = deque([0.0] * bufferSize) # using deque becuase inserting and removing performace is much better than lists
    signal = Signal()


    @classmethod
    def startCollecting(klass):
        if not Serial.isOpen():
            Serial.start() ## opens up a fake serial port and starts writing random data to it
            time.sleep(1/100000) ## give time for the port to start up befre emmiting the sginal
            klass.signal.startedCollecting.emit() ## emit signal to indicate that model started collecting data


    @classmethod
    def getData(klass):
        data = Serial.readline()
        klass.add(data)
        return klass.dataBuffer

    @classmethod
    def getBufferSize(klass):
        return klass.bufferSize

    # add plot points to buffer
    @classmethod
    def addToBuf(klass, buf, val):
        if len(buf) < klass.bufferSize:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    @classmethod
    def add(klass, data):
        klass.addToBuf(klass.dataBuffer, data)


