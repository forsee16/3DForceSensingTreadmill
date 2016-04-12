import random
import time
import threading
from numpy import sin

# A class that simulates a fake Arduino serial port

class Serial:

    isOpen = False
    _data = ""
    timerCounter = 1

    ## close()
    # closes the port
    @classmethod
    def close(klass):
        klass.isOpen = False
        klass.timerCounter = 0

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


    ## a function that starts writing random numbers to port by invoking writeRandom() in a new thread (as not to block other functions)
    @classmethod
    def start(klass):
        klass.isOpen = True
        threading._start_new_thread(klass.writeRandom, ())

    ## writes random numbers between 0 and 10 to port every 1/50 second
    @classmethod
    def writeRandom(klass):
        while klass.timerCounter < 500: ## collects data for 10 seconds then closes port
            num = random.random()*20
            #num = sin(klass.counter*.1)*20
            klass.timerCounter += 1
            klass.write(str(num) + "\n")
            time.sleep(1/50)
        klass.close()




