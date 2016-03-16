#
#RawDataManipulator.py
#
#A set of methods responsible for handling communication between the pressure plate sensors
#and the program.
#
#By Anthony Prom
#
import csv



def dataParse():

    with open('csvFile.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print row[1]
    print "All done"
    return

def pushToStorage():
    return

dataParse()