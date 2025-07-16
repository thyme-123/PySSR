import os
import sys

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import Slot

from window import MainWindow

BASE = os.path.abspath('.')


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow.MainWindow()
    mainWindow.show()
    return sys.exit(app.exec())


if __name__ == "__main__":
    main()
