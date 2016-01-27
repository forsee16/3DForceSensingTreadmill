class GraphData(graph):

    #__init__
    # #__init__
    #Description: Creates a new graph
    #
    #Parameters:
    #   inputData - a list of input data for the graph
    ##
    def __init__(self, inputForce, inputCenterOPressure, inputMoment, inputPower, intputEnergy):
        self.force = inputForce
        self.centerOfPressure = inputCenterOPressure
        self.moment = inputMoment
        self.power = inputPower
        self.energy = inputEnergy




    # Probably should be storing all the stuff in an array that we can keep accessing.  Needs to be central.

    ##
    #updateForce
    #
    #Description: called each time we get new data from the input
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def updateForce(self, force):
        self.force = force

    def updatePressure(self, pressure):
        self.centerOfPressure = pressure

    def updateMoment(self, moment):
        self.moment = moment

    def updatePower(self, power):
        self.power = power

    def updateEnergy(self, energy):
        self.energy = energy