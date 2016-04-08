from src.Input.fakeSerial import Serial
from collections import deque
from PyQt5.QtCore import pyqtSignal, QObject
import time


## inheriting from QObject allows the class to emit signals that indicate model has started collecting data
class Signal(QObject):
    startedCollecting = pyqtSignal()
    doneCollecting = pyqtSignal()


# class is static so that the table and graph classes have access to the same data
class Data():
    # bufferSize = 500
    ## deque(iterable, maxlen)
    dataBuffer = deque(
        [0.0])  # using deque becuase appending and removing performace is O(1) comparaed to lists performance O(n)
    signal = Signal()
    count = 0

    @classmethod
    def startCollecting(klass):
        if not Serial.isOpen():
            Serial.start()  ## opens up a fake serial port and starts writing random data to it (#port only collects for 10 seconds)
            time.sleep(1 / 100)  ## give time for the port to start up befre emmiting the sginal
            klass.signal.startedCollecting.emit()  ## emit signal to indicate that model started collecting data

    @classmethod
    def getData(klass):
        if (Serial._isOpen):
            data = Serial.readline()
            klass.addToBuf(klass.dataBuffer, data)
        else:
            klass.signal.doneCollecting.emit() ## emit signal so that graph class knows when to stop plotting
        return klass.dataBuffer

    # @classmethod
    # def getBufferSize(klass):
    #     return klass.bufferSize

    # add plot points to buffer
    @classmethod
    def addToBuf(klass, buf, val):
        buf.appendleft(val)
        klass.count += 1


        # print(buf)

        # # add data
        # @classmethod
        # def add(klass, data):
        #     klass.addToBuf(klass.dataBuffer, data)
