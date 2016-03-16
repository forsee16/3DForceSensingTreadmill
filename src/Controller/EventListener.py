#!/usr/bin/python

class EventListener:
    """A collection a listeners for the view"""

    #Instance variables that will contain the model and view that
    #this controller will be controlling
    model = None
    view = None


    #initialize the controller
    def __init__(self, modelToInitialize, viewToInitialize):

        model = modelToInitialize
        view = viewToInitialize
        view.AddListener(self) #Pass controller to view here

    #user has changed the time frame
    def onSelectTimeFrame(self, start, end):
        for currentBox in range(0, self.view.box.length):
            #changed boxes in the range to yellow and ones out of the range to white
            if currentBox in range(start, end):
                self.view.box[currentBox].color = "yellow";
            else:
                self.view.box[currentBox].color = "white";
        #tell the model that the range has been changed so the data can be updated
        self.model.selectTimeFrame(start, end)

    # Graph's will have types: ForceX, ForceY, ForceZ, Power, and Energy
    def onSelectTypeOfGraph(self, type):
        self.model.changeType(type)

    #def updateGraph(self, data):

    #def updateTable(self, data):

    #The user changes the csv table being used
    def onSelectCSV(self, file):
        self.model.selectCSV(file)


