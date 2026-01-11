import os
import sys

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import Slot

from window import MainWindow
from gnssBase.gnssSSR import repairSp3, repairClk
from gnssBase.gnssDiff import plotMain

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
        systemCheck = []
        plot_out = None
        positonList = []
        inputSp3 = []
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
            elif arg == "-plot_sys":
                mod = "sys"
            elif arg == "-plt_check":
                mod = "check"
            elif arg == "-sp3":
                mod = "sp3"
            elif arg == "-plot_out":
                mod = "plot_out"
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
                    elif mod == "sys":
                        systemList = arg.split(",")
                        for s in systemList:
                            if s in ["G", "R", "E", "C"]:
                                if s not in systemCheck:
                                    systemCheck.append(s)
                    elif mod == "check":
                        checkList = arg.split(",")
                        for c in checkList:
                            if c.upper() == "R":
                                positonList.append("R Position")
                            elif c.upper() == "A":
                                positonList.append("A Position")
                            elif c.upper() == "C":
                                positonList.append("C Position")
                            elif c.upper() == "X":
                                positonList.append("X Position")
                            elif c.upper() == "Y":
                                positonList.append("Y Position")
                            elif c.upper() == "Z":
                                positonList.append("Z Position")
                            elif c.upper() == "CLK":
                                positonList.append("CLK")
                    elif mod == "plot_out":
                        plot_out = arg
                    elif mod == "sp3":
                        inputSp3.append(arg)
        if outSp3:
            repairSp3(outSp3, navList, ssrPath, atxPath)
        if outClk:
            repairClk(outClk, navList, ssrPath)
        if (len(inputSp3) == 2) and plot_out and positonList and systemCheck:
            sp3Input = inputSp3[0]
            sp3TemplatePath = inputSp3[1]
            plotMain(sp3Input, sp3TemplatePath, positonList, navList, systemCheck, plot_out)
        return


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main_window()
    else:
        main(args)
