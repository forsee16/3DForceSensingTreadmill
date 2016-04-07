#!/usr/bin/python

class EventListener:
    """A collection a listeners for the view"""

    #Instance variables that will contain the model and view that
    #this controller will be controlling
    model = None
    view = None
    table = None
    typeOfGraph = 0


    # initialize the controller
    def __init__(self):
        self.model = DataModel(0, 0, 0, 0, 0)
        #self.view =
        #self.view.AddListener(self) #Pass controller to view here

    # user has changed the time frame
    def onSelectTimeFrame(self, start, end):
        for currentBox in range(0, self.view.box.length):
            #changed boxes in the range to yellow and ones out of the range to white
            if currentBox in range(start, end):
                self.view.box[currentBox].color = "yellow"
            else:
                self.view.box[currentBox].color = "white"
        #tell the model that the range has been changed so the data can be updated
        self.model.selectTimeFrame(start, end)

    # Graph's will have types: ForceX, ForceY, ForceZ, Power, and Energy
    def onSelectTypeOfGraph(self, type):
        self.model.changeType(type)
        if type=="ForceX":
            self.typeOfGraph = 0
        elif type == "ForceY":
            self.typeOfGraph=1
        elif type == "ForceZ":
            self.typeOfGraph=2
        elif type == "Pressure":
            self.typeOfGraph=3
        elif type == "Moment":
            self.typeOfGraph=4
        elif type == "Power":
            self.typeOfGraph=5
        elif type == "Energy":
            self.typeOfGraph=6

        updateGraph()

    def onNewCurrentData(self):
        self.model.getCurrentData()
        # append the new data value to table
        updateTable()
        updateGraph()

    #def updateGraph(self, data):

    #def updateTable(self):


    #The user changes the csv table being used
    def onSelectCSV(self, file):
        self.model.changeFile(file)
        self.table = self.model.getOldData()
        #what kind of Table does Abdullah want this in



ev = EventListener()