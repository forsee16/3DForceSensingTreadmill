import random
import time
import threading
from numpy import sin

# A class that simulates a fake Arduino serial port

class Serial:

    name = 'COM1'
    port = 'COM1'
    timeout = 1
    parity = 'N'
    baudrate = 19200
    bytesize = 8
    stopbits = 1
    xonxoff = 0
    rtscts = 0
    _isOpen = False
    _data = ""

    ## init(): the constructor.  Many of the arguments have default values
    # and can be skipped when calling the constructor.
    # def __init__( self, port='COM1', baudrate = 19200, timeout=1,
    #               bytesize = 8, parity = 'N', stopbits = 1, xonxoff=0,
    #               rtscts = 0):
    #     self.name     = port
    #     self.port     = port
    #     self.timeout  = timeout
    #     self.parity   = parity
    #     self.baudrate = baudrate
    #     self.bytesize = bytesize
    #     self.stopbits = stopbits
    #     self.xonxoff  = xonxoff
    #     self.rtscts   = rtscts
    #     self._isOpen  = True
    #     #self._receivedData = ""
    #     self._data = ""


    ## isOpen()
    # returns True if the port to the Arduino is open.  False otherwise
    @classmethod
    def isOpen( klass ):
        return klass._isOpen

    ## open()
    # opens the port
    @classmethod
    def open( klass ):
        klass._isOpen = True

    ## close()
    # closes the port
    @classmethod
    def close( klass ):
        klass._isOpen = False

    ## write()
    # writes a string of characters to the Arduino
    @classmethod
    def write( klass, string ):
        #print( 'Arduino got: "' + string + '"' )
        klass._data += string

    ## read()
    # reads n characters from the fake Arduino. Actually n characters
    # are read from the string _data and returned to the caller.
    @classmethod
    def read( klass, n=1 ):
        s = klass._data[0:n]
        klass._data = klass._data[n:]
        #print( "read: now self._data = ", self._data )
        return s

    ## readline()
    # reads characters from the fake Arduino until a \n is found.
    @classmethod
    def readline( klass ):
        returnIndex = klass._data.index( "\n" )
        if returnIndex != -1:
            s = klass._data[0:returnIndex-1]
            klass._data = klass._data[returnIndex+1:]
            return s
        else:
            return ""

    ## __str__()
    # returns a string representation of the serial class
    @classmethod
    def __str__( klass ):
        return  "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % ( str(klass.isOpen), klass.port, klass.baudrate ) \
               + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)"\
               % ( klass.bytesize, klass.parity, klass.stopbits, klass.xonxoff,
                   klass.rtscts )


    ## a function that starts writing random numbers to port by invoking writeRandom() in a new thread (as not to block other functions)
    @classmethod
    def start(klass):
        klass.open()
        threading._start_new_thread(klass.writeRandom, ())



    ## writes random numbers between 0 and 10 to port every 1/50 second
    @classmethod
    def writeRandom(klass):
        i = 1.0
        while i < 500: ## collects data for 10 seconds then closes port
            num = random.random()*20
            #num = i
            #num = sin(i*.1)*20
            i += 1
            klass.write(str(num) + "\n")
            time.sleep(1/50)
        klass.close()




