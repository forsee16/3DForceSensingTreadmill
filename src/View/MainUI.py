from __future__ import unicode_literals
import random
import matplotlib
matplotlib.use('Qt5Agg')
from numpy import arange, sin, pi
from PyQt5 import QtCore, QtGui, QtWidgets
from src.View.Graph import AnimationWidget
from src.View.Table import TableModel






class MainUI:
    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1048, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralWidgetLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralWidgetLayout.setObjectName("centralWidgetLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_1.addWidget(self.tableView)
        self.horizontalLayout.addLayout(self.verticalLayout_1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2, 5)
        self.centralWidgetLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1048, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        ########################

        hbox = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("start")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("stop")
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setObjectName("load")




        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.load_button)
        self.verticalLayout_2.addLayout(hbox) ## add horizontal layoyt (includes 3 buttons) on the vertical layout on the right

        self.graph = AnimationWidget()
        self.verticalLayout_2.addWidget(self.graph) ## add graph to vertical layout on the right
        self.start_button.clicked.connect(self.graph.start)
        self.stop_button.clicked.connect(self.graph.stop)
        model = TableModel()
        self.tableView.setModel(model)






        #######################

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.start_button.setText(_translate("MainWindow", "start"))
        self.stop_button.setText(_translate("MainWindow", "stop"))
        self.load_button.setText(_translate("MainWindow", "load"))

