import csv
class DataModel:

    # #__init__
    #Description: Creates a new data model
    #
    #Parameters:
    #   inputData - a list of input data for the graph
    ##
    def __init__(self, inputForce, inputCenterOfPressure, inputMoment, inputPower, inputEnergy):
        self.force = inputForce
        self.centerOfPressure = inputCenterOfPressure
        self.moment = inputMoment
        self.power = inputPower
        self.energy = inputEnergy
        self.currentData = []
        self.oldData = [[]]
        with open("force.csv", 'wb') as forceFile:
            self.forceWriter = csv.writer(forceFile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open("pressure.csv", 'wb') as pressureFile:
            self.pressureWriter = csv.writer(pressureFile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open("power.csv", 'wb') as powerFile:
            self.powerWriter = csv.writer(powerFile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open("moment.csv", 'wb') as momentFile:
            self.momentWriter = csv.writer(momentFile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open("energy.csv", 'wb') as energyFile:
            self.energyWriter = csv.writer(energyFile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def createDataArray(self):
        self.currentData.append(self, self.force)
        self.currentData.append(self, self.centerOfPressure)
        self.currentData.append(self, self.moment)
        self.currentData.append(self, self.power)
        self.currentData.append(self, self.energy)


    # Probably should be storing all the stuff in an array that we can keep accessing.  Needs to be central.

    ##
    #updateForce
    #
    #Description: called each time we get new data from the input
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def updateForce(self, force):
        self.force = force
        self.currentData.insert(0, force)
        self.oldData[0].append(force)
        self.forceWriter.writerow(force)

    def getForce(self):
        return self.dataArray[0]

    def updatePressure(self, pressure):
        self.centerOfPressure = pressure
        self.currentData.insert(1, pressure)
        self.oldData[1].append(pressure)
        self.pressureWriter.writerow(pressure)

    def getPressure(self):
        return self.dataArray[1]

    def updateMoment(self, moment):
        self.moment = moment
        self.currentData.insert(2, moment)
        self.oldData[2].append(moment)
        self.momentWriter.writerow(moment)

    def getMoment(self):
        return self.currentData[2]

    def updatePower(self, power):
        self.power = power
        self.currentData.insert(3, power)
        self.oldData[3].append(power)
        self.powerWriter.writerow(power)

    def getPower(self):
        return self.currentData[3]

    def updateEnergy(self, energy):
        self.energy = energy
        self.currentData.insert(4, energy)
        self.oldData[4].append(energy)
        self.energyWriter.writerow(energy)

    def getEnergy(self):
        return self.currentData[4]

    def getCurrentData(self):
        return self.currentData

    def getOldData(self):
        return self.oldData

    def getTableModel(self):

