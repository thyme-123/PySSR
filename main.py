import os
import sys

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import Slot

from window import MainWindow
from gnssBase.gnssSSR import repairSp3, repairClk

BASE = os.path.abspath('.')


def main_window():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow.MainWindow()
    mainWindow.show()
    return sys.exit(app.exec())

def main(args):
    if "-nw" not in args:
        return main_window()
    else:
        navList = []
        ssrPath = None
        atxPath = None
        mod = None
        outSp3 = None
        outClk = None
        for arg in args:
            if arg == "-nav":
                mod = "nav"
            elif arg == "-ssr":
                mod = "ssr"
            elif arg == "-atx":
                mod = "atx"
            elif arg == "-out":
                mod = "out"
            elif arg == "-nw":
                mod = None
            else:
                if not mod:
                    continue
                else:
                    if mod == "nav":
                        navList.append(arg)
                    elif mod == "ssr":
                        ssrPath = arg
                    elif mod == "atx":
                        atxPath = arg
                    elif mod == "out":
                        if arg.lower().endswith(".clk"):
                            outClk = arg
                        elif arg.lower().endswith(".sp3"):
                            outSp3 = arg
        if outSp3:
            repairSp3(outSp3, navList, ssrPath, atxPath)
        if outClk:
            repairClk(outClk, navList, ssrPath)
        return


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main_window()
    else:
        main(args)
