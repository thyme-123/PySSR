import datetime
import os

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMessageBox


from gnssBase.gnssIO import *
from gnssBase.gnssSSR import *


class RepairThread(QThread):

    def __init__(self,parent=None):
        super().__init__(parent)

    def run(self):
        parent = self.parent()
        settingData = parent.settingWindow.getSettingData(parent.printLogSignal)
        log = settingData["log"]
        logPath = settingData["logPath"]
        navPathList = parent.navPathEdit.text().split(";")
        ssrPath = parent.ssrPathEdit.text()
        atxPath = parent.atxPathEdit.text()
        settingData = self.parent()
        if not navPathList:
            parent.printLogSignal.emit("no nav file")
            return parent.endThread()
        if not ssrPath and (not parent.ssrCheck.isChecked()):
            parent.printLogSignal.emit("no ssr file")
            return parent.endThread()
        for navPath in navPathList:
            if not os.path.isfile(navPath):
                parent.printLogSignal.emit("no nav file")
                return parent.endThread()
        if not os.path.isfile(ssrPath) and (not parent.ssrCheck.isChecked()):
            parent.printLogSignal.emit("no ssr file")
            return parent.endThread()
        sp3Path = parent.sp3PathEdit.text()
        clkPath = parent.clkPathEdit.text()
        parent.printLogSignal.emit("start read rnx file {}".format(navPath))
        rnxData = {}
        times = None
        for navPath in navPathList:
            rnxData, times = readNav(navPath, rnxData)
        cData, sData = None, None
        parent.printLogSignal.emit("end read rnx file {}".format(navPath))
        if not parent.ssrCheck.isChecked():
            parent.printLogSignal.emit("start read ssr file {}".format(ssrPath))
            cData, sData, times = readSSR(ssrPath)
            parent.printLogSignal.emit("end read ssr file {}".format(ssrPath))
        atxData = None
        if os.path.isfile(atxPath):
            atxData = readATX(atxPath)
        while True:
            if not sp3Path:
                parent.printLogSignal.emit("no out sp3 path,skip processing")
                break
            parent.printLogSignal.emit("start write sp3file {}".format(sp3Path))
            logLines = []
            if parent.ssrCheck.isChecked():
                lines, outTime, satellites, epoch = noSp3Line(rnxData, times)
            else:
                lines, outTime, satellites, epoch, logLines = sp3Lines(rnxData, times, cData, sData, atxData, mod=False, log=log)
            writeSp3(sp3Path, lines, outTime, satellites, epoch)
            if log:
                sp3Log = os.path.join(logPath, "sp3.log")
                with open(sp3Log, "w") as f:
                    for line in logLines:
                        f.write(line)
            parent.printLogSignal.emit("end write sp3file {}".format(sp3Path))
            break
        while True:
            logLines = []
            if not clkPath:
                parent.printLogSignal.emit("no out clk path,skip processing")
                break
            parent.printLogSignal.emit("start write clk file {}".format(clkPath))
            if parent.ssrCheck.isChecked():
                lines, ansTime = noClkLine(rnxData,times)
            else:
                lines, ansTime, logLines = clkLines(rnxData, times, cData, log=log)
            writeClk(clkPath, lines, ansTime)
            if log:
                clkLog = os.path.join(logPath, "clk.log")
                with open(clkLog, "w") as f:
                    for line in logLines:
                        f.write(line)
            parent.printLogSignal.emit("end write sp3file {}".format(clkPath))
            break
        return parent.endThread()