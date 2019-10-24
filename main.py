from GUIClass import *
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.showMaximized()
    sys.exit(app.exec_())