from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.DataAccesor import Data
from collections import deque

class TableModel(QtCore.QAbstractTableModel):


    def __init__(self, header=[]):
        super(TableModel, self).__init__()
        self.header = ['Time(s)', 'Force (kg)']
        self.numOfRows = 10
        self.dataUpdatTimer = QtCore.QTimer()
        self.dataUpdatTimer.timeout.connect(self.updateData)
        self.dataUpdatTimer.timeout.connect(self.insertRow)
        self.data_list = deque()
        self.time_list = deque()
        Data.signal.startedCollecting.connect(self.startDataUpdateTimer)
        Data.signal.resetTable.connect(self.resetTable)


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.numOfRows

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
            return 2

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return None
        elif int_role != QtCore.Qt.DisplayRole:
            return None
        elif QModelIndex.row() >= len(self.data_list):
            return None
        #print(self.data_list)
        #point = self.data_list[int]
        if(QModelIndex.column() == 0):
            return self.time_list[QModelIndex.row()]
        else:
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
        if (strr == None): ## check last row is non empty before adding new ones
            return False
        newRow = 1
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.endInsertRows()
        self.increaseRowByOne()
        return True



    def updateData(self):
        self.data_list = Data.tableDataBuffer
        self.time_list = Data.timeBuffer
        topLeft = self.createIndex(0,0)
        rowNum = self.numOfRows
        colNum = self.columnCount()
        bottomLeft = self.createIndex(rowNum,rowNum)
        self.dataChanged.emit(bottomLeft, bottomLeft)

    def increaseRowByOne(self):
        self.numOfRows += 1

    def startDataUpdateTimer(self):
        #self.getData()
        self.dataUpdatTimer.start(1/20)

    def resetTable(self):
        self.dataUpdatTimer.stop()
        self.numOfRows = 10
        self.data_list.clear()
        self.beginResetModel()
        self.endResetModel()





