from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.DataAccesor import Data

class TableModel(QtCore.QAbstractTableModel):


    def __init__(self, header=[], data_list=[]):
        super(TableModel, self).__init__()
        self.data_list = data_list
        self.header = ['Number']
        #self.timer1 = QtCore.QTimer()
        Data.signal.startedCollecting.connect(self.getData)
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.insertRow)
        #self.timer1.start(1000)
        self.timer2.start(100)
        self.numOfRows = 15
        self.rowsInserted.connect(self.increaseRowByOne)
        self.onece = False


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.numOfRows

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
            return 1

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return None
        elif int_role != QtCore.Qt.DisplayRole:
            return None
        elif QModelIndex.row() >= len(self.data_list):
            return None
        return self.data_list[QModelIndex.row()]



    def headerData(self, col, orientation, int_role=None):
        if orientation == QtCore.Qt.Horizontal and int_role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def insertRow(self, p_int = 0, QModelIndex_parent=None, *args, **kwargs):
        rowNum = self.rowCount(QModelIndex_parent) -1
        colNum = self.columnCount(QModelIndex_parent) -1
        indx = self.index(rowNum, colNum, QtCore.QModelIndex())
        strr = self.data(indx,QtCore.Qt.DisplayRole)
        if (strr == None):
            return False
        newRow = 1
        self.beginInsertRows(QtCore.QModelIndex(), 1, 1)
        self.endInsertRows()
        return True



    # def insertData(self):
    #     #data = Data.getData()
    #     topLeft = self.createIndex(0,0)
    #     rowNum = self.rowCount()
    #     colNum = self.columnCount()
    #     bottomRight = self.createIndex(rowNum,colNum)
    #     self.dataChanged.emit(topLeft,bottomRight)

    def getData(self):
        self.data_list = Data.getData()


    def increaseRowByOne(self):
        self.numOfRows += 1






