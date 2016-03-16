import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Controller.EventListener import EventListener
from View.MainUI import MainUI


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())