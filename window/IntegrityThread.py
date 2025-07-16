import os

from PySide6.QtCore import QThread

from SSR.ssrClass import *
from SSR.sp3Class import *
from SSR.ssrDefine import *

class IntegrityThread(QThread):

    def __init__(self, path, outPath, mod=0, parent=None):
        super().__init__(parent)
        self.path = path
        self.outPath = outPath
        self.mod = mod


    def run(self):
        parent = self.parent()
        settingData = parent.settingWindow.getSettingData()
        if not settingData["dpi"].isdigit():
            parent.printLogSignal.emit("dpi not int")
            return parent.endThread()
        dpi = int(settingData["dpi"])
        noTitle = settingData["noTitle"]
        suf = os.path.splitext(os.path.split(self.path)[1])[1]
        if suf.lower() == ".ssr":
            if not parent.timeStepEdit.text().isdigit():
                return
            step = int(parent.timeStepEdit.text())
            ssrData = SSR_CLSSS(self.path)
            ssrData.plotIntegrity(outPath=self.outPath, noTitle=noTitle, xlabel="time", ylabel="prn", format=settingData["imgFormat"],
                                  mod=self.mod, dpi=dpi)
            ssrData.plotIntegrityPercentage(outPath=self.outPath, noTitle=noTitle, xlabel="prn", ylabel="percentage",
                                            format=settingData["imgFormat"], timeStep=step, dpi=dpi)
        elif suf.lower() == ".sp3":
            sp3Data = SP3_CLASS(self.path)
            sp3Data.plotIntegrity(self.outPath, noTitle=noTitle, xlabel="time", ylabel="prn", format=settingData["imgFormat"], dpi=dpi)
            sp3Data.plotIntegrityPercentage(self.outPath, noTitle=noTitle, xlabel="time", ylabel="prn",
                                  format=settingData["imgFormat"], dpi=dpi)
        else:
            return
        return