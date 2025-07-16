import os


import matplotlib.pyplot as plt
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMessageBox


from gnssBase.gnssIO import *
from gnssBase.gnssDiff import *
from gnssBase.gnssPosition import *


systems = ["G", "C", "R", "E"]
typList = {
    "tiff": "tif",
    "jpg": "jpg",
    "png": "png",
}


class PlotThread(QThread):

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        parent = self.parent()
        sp3InputPath = parent.sp3InputPathEdit.text()
        sp3TemplatePath = parent.sp3TemplatePathEdit.text()
        navPath = parent.navPathEdit.text()
        imgPath = parent.imgPathEdit.text()
        settingData = parent.settingWindow.getSettingData(parent.printLogSignal)
        baseSatelliteData = {}
        baseSatelliteList = settingData["baseSatellite"].split(",")
        ignore = settingData["ignore"].split(",")
        if not settingData["dpi"].isdigit():
            parent.printLogSignal.emit("dpi not int")
            return parent.endThread()
        dpi = int(settingData["dpi"])
        noTitle = settingData["noTitle"]
        noLenged = settingData["noLenged"]
        isLog = settingData["log"]
        logPath = settingData["logPath"]
        for baseSatellite in baseSatelliteList:
            if not baseSatellite:
                continue
            else:
                if baseSatellite[0] not in systems:
                    continue
                else:
                    if not baseSatellite[1:].isdigit():
                        continue
                    else:
                        baseSatelliteData[baseSatellite[0]] = baseSatellite
        if not imgPath:
            parent.printLogSignal.emit("no img path")
            return parent.endThread()
        if not os.path.isdir(imgPath):
            os.mkdir(imgPath)
        if not sp3InputPath:
            parent.printLogSignal.emit("no input sp3 file")
            return parent.endThread()
        if not sp3TemplatePath:
            parent.printLogSignal.emit("no template sp3 file")
            return parent.endThread()
        if not os.path.isfile(sp3InputPath):
            parent.printLogSignal.emit("input sp3 file is not exist")
            return parent.endThread()
        if not os.path.isfile(sp3TemplatePath):
            parent.printLogSignal.emit("template sp3 file is not exist")
            return parent.endThread()
        # sp3DataG, sp3DataE, sp3DataR, sp3DataC = readSp3_system(sp3InputPath)
        # sp3TemplateDataG, sp3TemplateDataE, sp3TemplateDataR, sp3TemplateDataC = readSp3_system(sp3TemplatePath)
        sp3Data = readSp3(sp3InputPath)
        sp3TemplateData = readSp3(sp3TemplatePath)
        # sp3DataDir = {
        #     "G": sp3DataG,
        #     "E": sp3DataE,
        #     "R": sp3DataR,
        #     "C": sp3DataC,
        # }
        # sp3TemplateDataDir = {
        #     "G": sp3TemplateDataG,
        #     "E": sp3TemplateDataE,
        #     "R": sp3TemplateDataR,
        #     "C": sp3TemplateDataC,
        # }
        navData = None
        if not navPath:
            navData = None
        elif not os.path.isfile(navPath):
            parent.printLogSignal.emit("nav file is not exist")
            navData = None
        else:
            navData, times = readNav(navPath)
        positonList = []
        for p in parent.positionHash:
            if parent.positionHash[p].isChecked():
                positonList.append(p)
        systemCheck = []
        for system in parent.systemHash:
            if parent.systemHash[system].isChecked():
                systemCheck.append(system)
        prns, times, diff, minTime, maxTime, logLines = gnssDiff_all(sp3Data, sp3TemplateData, parent, baseSatelliteData,
                                                           systemCheck, navData, log=isLog, ignore=ignore)
        if isLog:
            sp3Log = os.path.join(logPath, "plot.log")
            with open(sp3Log, "w") as f:
                for line in logLines:
                    f.write(line)
        sp3InputName = os.path.basename(sp3InputPath)
        sp3TemplateName = os.path.basename(sp3TemplatePath)
        baseTitle = "{} diff {} {}".format(sp3InputName, sp3TemplateName, "{}", "".join(systemCheck))
        for diffName in positonList:
            figTitle = baseTitle.format(diffName)
            typ = typList[settingData["imgFormat"]]
            imgpath = os.path.join(imgPath, "{}_{}.{}".format(diffName, "".join(systemCheck), typ))
            if diffName == "CLK":
                gnssPlotScatter(times, diff[diffName], prns, figTitle, imgpath, noTitle=noTitle, noLenged=noLenged,
                                xlabel="Times(second)",
                                ylabel="diff(ns)", xlim=[minTime, maxTime], format=settingData["imgFormat"], 
                                dpi=dpi)
                gnssPlotBar(diff[diffName], prns, "CLK STD {}".format("".join(systemCheck)), os.path.join(imgPath,
                                                                                                          "{}_STD {}.{}".format(
                                                                                                              diffName,
                                                                                                              "".join(systemCheck),
                                                                                                              typ)),
                            noTitle=noTitle, xlabel="PRN",
                            ylabel="std(ns)", format=settingData["imgFormat"],
                            dpi=dpi)
            else:
                gnssPlotScatter(times, diff[diffName], prns, figTitle, imgpath, noTitle=noTitle, noLenged=noLenged,
                                xlabel="Times(second)",
                                ylabel="diff(m)", xlim=[minTime, maxTime], format=settingData["imgFormat"],
                                dpi=dpi)

        # for system in parent.systemHash:
        #     if parent.systemHash[system].isChecked():
        #         sp3Data = sp3DataDir[system]
        #         sp3TemplateData = sp3TemplateDataDir[system]
        #         prns, times, diff, minTime, maxTime = gnssDiff(sp3Data, sp3TemplateData, parent,
        #                                                        baseSatelliteData[system], system, navData)
        #         sp3InputName = os.path.basename(sp3InputPath)
        #         sp3TemplateName = os.path.basename(sp3TemplatePath)
        #         baseTitle = "{} diff {} {}_{}".format(sp3InputName, sp3TemplateName, "{}", system)
        #         for diffName in positonList:
        #             if diff[diffName] == None:
        #                 continue
        #             else:
        #                 figTitle = baseTitle.format(diffName)
        #                 typ = typList[settingData["imgFormat"]]
        #                 imgpath = os.path.join(imgPath, "{}_{}.{}".format(diffName, system, typ))
        #                 if diffName == "CLK":
        #                     gnssPlotScatter(times, diff[diffName], prns, figTitle, imgpath, xlabel="Times(minute)",
        #                                     ylabel="diff(ns)", xlim=[minTime, maxTime], format=settingData["imgFormat"],
        #                                     dpi=dpi)
        #                 else:
        #                     gnssPlotScatter(times, diff[diffName], prns, figTitle, imgpath, xlabel="Times(minute)",
        #                                     ylabel="diff(m)", xlim=[minTime, maxTime], format=settingData["imgFormat"],
        #                                     dpi=dpi)
        return parent.endThread()
