import sys
from PyQt5 import QtWidgets
from src.logic_layer.main_window_logic import MainWindowLogic
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowLogic(MainWindow)
    ui.process()
    MainWindow.show()
    sys.exit(app.exec_())