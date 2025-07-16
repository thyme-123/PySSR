import os
from datetime import datetime

import matplotlib.pyplot as plt

from SSR.ssrDefine import *


INTEGRITY_S = {
    "G": PLOT_SSR_S_INTEGRITY_G,
    "R": PLOT_SSR_S_INTEGRITY_R,
    "E": PLOT_SSR_S_INTEGRITY_E,
    "C": PLOT_SSR_S_INTEGRITY_C,
}


INTEGRITY_C = {
    "G": PLOT_SSR_C_INTEGRITY_G,
    "R": PLOT_SSR_C_INTEGRITY_R,
    "E": PLOT_SSR_C_INTEGRITY_E,
    "C": PLOT_SSR_C_INTEGRITY_C,
}

def getSystem(prn):
    return prn[0]


class SSR_CLSSS:

    def __init__(self, path=None):
        self.dataS = {}
        self.dataC = {}
        self.prnS = []
        self.prnC = []
        self.isRead = False
        self.fileName = None
        if path:
            self.read(path)

    def read(self, path):
        self.fileName = os.path.basename(path)
        ns = 1
        nc = 1
        prn2ns = {}
        prn2nc = {}
        with open(path, "r") as f:
            line = f.readline()
            while line:
                while "  " in line:
                    line = line.replace("  ", " ")
                data = line.split(" ")
                if data[1] == "ORBIT":
                    year = int(data[2])
                    month = int(data[3])
                    day = int(data[4])
                    hour = int(data[5])
                    minute = int(data[6])
                    second = int(float(data[7]))
                    t = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
                    numberOfSatellite = int(data[9])
                    for _ in range(numberOfSatellite):
                        line = f.readline()
                        while "  " in line:
                            line = line.replace("  ", " ")
                        data = line.split(" ")
                        prn = data[0]
                        IOD = int(data[1])
                        R = float(data[2])
                        A = float(data[3])
                        C = float(data[4])
                        VR = float(data[5])
                        VA = float(data[6])
                        VC = float(data[7])
                        if self.dataS.get(prn, -1) == -1:
                            prn2ns[prn] = ns
                            ns += 1
                            self.dataS[prn] = {
                                "times": [],
                                "IOD": [],
                                "R": [],
                                "A": [],
                                "C": [],
                                "VR": [],
                                "VA": [],
                                "VC": [],
                                "NS": [],
                            }
                        self.dataS[prn]["times"].append(t)
                        self.dataS[prn]["IOD"].append(IOD)
                        self.dataS[prn]["R"].append(R)
                        self.dataS[prn]["A"].append(A)
                        self.dataS[prn]["C"].append(C)
                        self.dataS[prn]["VR"].append(VR)
                        self.dataS[prn]["VA"].append(VA)
                        self.dataS[prn]["VC"].append(VC)
                        self.dataS[prn]["NS"].append(prn2ns[prn])
                elif data[1] == "CLOCK":
                    year = int(data[2])
                    month = int(data[3])
                    day = int(data[4])
                    hour = int(data[5])
                    minute = int(data[6])
                    second = int(float(data[7]))
                    t = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
                    numberOfSatellite = int(data[9])
                    for _ in range(numberOfSatellite):
                        line = f.readline()
                        while "  " in line:
                            line = line.replace("  ", " ")
                        data = line.split(" ")
                        prn = data[0]
                        IOD = int(data[1])
                        C0 = float(data[2])
                        C1 = float(data[3])
                        C2 = float(data[4])
                        if self.dataC.get(prn, -1) == -1:
                            prn2nc[prn] = nc
                            nc += 1
                            self.dataC[prn] = {
                                "times": [],
                                "IOD": [],
                                "C0": [],
                                "C1": [],
                                "C2": [],
                                "NC": [],
                            }
                        self.dataC[prn]["times"].append(t)
                        self.dataC[prn]["IOD"].append(IOD)
                        self.dataC[prn]["C0"].append(C0)
                        self.dataC[prn]["C1"].append(C1)
                        self.dataC[prn]["C2"].append(C2)
                        self.dataC[prn]["NC"].append(prn2nc[prn])
                line = f.readline()
        self.isRead = True

    def plotIntegrity(self, outPath, title="", noTitle=False, xlabel=None, ylabel=None, format="tiff", dpi=600, mod=0):
        assert self.isRead, "SSR_CLASS not read ssr"
        if mod & PLOT_SSR_S_INTEGRITY:
            plt.clf()
            font_family = 'Arial'
            font_size = 13
            plt.rcParams['font.family'] = font_family
            plt.rcParams['font.size'] = font_size
            prnList = sorted(list(self.dataS.keys()))
            plt.figure(figsize=(6.45 * 4, 0.2 * len(prnList)))
            y1 = []
            y2 = []
            n = 1
            maxTime = max(self.dataS[prnList[0]]["times"])
            minTime = min(self.dataS[prnList[0]]["times"])
            for prn in prnList:
                if mod & INTEGRITY_S[getSystem(prn)]:
                    y1.append(n)
                    y2.append(prn)
                    plt.scatter(self.dataS[prn]["times"], [n] * len(self.dataS[prn]["times"]), s=0.2)
                    maxTime = max(maxTime, max(self.dataS[prn]["times"]))
                    minTime = min(minTime, min(self.dataS[prn]["times"]))
                    n += 1
            plt.yticks(y1, y2, fontsize=10)
            plt.xlim(minTime, maxTime)
            plt.ylim(0, n + 1)
            if not noTitle:
                plt.title(title)
            if xlabel != None:
                plt.xlabel(xlabel)
            if ylabel != None:
                plt.ylabel(ylabel)
            if not noTitle:
                plt.title(title)
            if outPath != None and outPath != "":
                outFile = os.path.join(outPath, self.fileName + "_S_Integrity.{}".format(format))
                plt.savefig(outFile, dpi=dpi, format=format, bbox_inches='tight')
        if mod & PLOT_SSR_C_INTEGRITY:
            plt.clf()
            font_family = 'Arial'
            font_size = 13
            plt.rcParams['font.family'] = font_family
            plt.rcParams['font.size'] = font_size
            prnList = sorted(list(self.dataS.keys()))
            plt.figure(figsize=(6.45 * 4, 0.2 * len(prnList)))
            y1 = []
            y2 = []
            maxTime = max(self.dataS[prnList[0]]["times"])
            minTime = min(self.dataS[prnList[0]]["times"])
            n = 1
            for prn in prnList:
                if mod & INTEGRITY_C[getSystem(prn)]:
                    y1.append(n)
                    y2.append(prn)
                    plt.scatter(self.dataC[prn]["times"], [n] * len(self.dataS[prn]["times"]), s=0.2)
                    maxTime = max(maxTime, max(self.dataS[prn]["times"]))
                    minTime = min(minTime, min(self.dataS[prn]["times"]))
                    n += 1
            plt.yticks(y1, y2, fontsize=10)
            plt.xlim(minTime, maxTime)
            plt.ylim(0, n + 1)
            if not noTitle:
                plt.title(title)
            if xlabel != None:
                plt.xlabel(xlabel)
            if ylabel != None:
                plt.ylabel(ylabel)
            if not noTitle:
                plt.title(title)
            if outPath != None and outPath != "":
                outFile = os.path.join(outPath, self.fileName + "_C_Integrity.{}".format(format))
                plt.savefig(outFile, dpi=dpi, format=format, bbox_inches='tight')

    def plotPRNS(self, prn, outPath, mod=0):
        plt.clf()
        outFile = os.path.join(outPath, self.fileName + "_" + prn + "_S.png")
        fig = plt.figure(figsize=(6.45 * 4 / 2.54, 38 * 2 / 25.4))
        ax1 = fig.add_subplot()
        if mod & PLOT_SSR_S_R:
            ax1.scatter(self.dataS[prn]["times"], self.dataS[prn]["R"], s=0.1)
        if mod & PLOT_SSR_S_A:
            ax1.scatter(self.dataS[prn]["times"], self.dataS[prn]["A"], s=0.1)
        if mod & PLOT_SSR_S_C:
            ax1.scatter(self.dataS[prn]["times"], self.dataS[prn]["C"], s=0.1)
        if mod & PLOT_SSR_IOD:
            ax2 = ax1.twinx()
            ax2.scatter(self.dataS[prn]["times"], self.dataS[prn]["IOD"], s=0.1, color="#000000")
            ax2.legend(["IOD"])
        ax1.legend(["R","A","C"])
        plt.savefig(outFile)

    def plotPRNC(self, prn, outPath, mod=0):
        plt.clf()
        outFile = os.path.join(outPath, self.fileName + "_" + prn + "_C.png")
        fig = plt.figure(figsize=(6.45 * 4 / 2.54, 38 * 2 / 25.4))
        ax1 = fig.add_subplot()
        if mod & PLOT_SSR_C_0:
            ax1.scatter(self.dataC[prn]["times"], self.dataC[prn]["C0"], s=0.1)
        if mod & PLOT_SSR_IOD:
            ax2 = ax1.twinx()
            ax2.scatter(self.dataC[prn]["times"], self.dataC[prn]["IOD"], s=0.1, color="#000000")
            ax2.legend(["IOD"])
        ax1.legend(["C0"])
        plt.savefig(outFile)

    def plotIntegrityPercentage(self, outPath, timeStep=10, title="", noTitle=False, xlabel=None, ylabel=None, format="tiff", dpi=600):
        assert self.isRead, "SSR_CLASS not read ssr"
        plt.clf()
        font_family = 'Arial'
        font_size = 12
        plt.rcParams['font.family'] = font_family
        plt.rcParams['font.size'] = font_size
        prnList = sorted(list(self.dataS.keys()))
        plt.figure(figsize=(0.38 * len(prnList), 38 * 2 / 25.4))
        step = 86400 / timeStep
        for prn in prnList:
            plt.bar(prn, len(self.dataS[prn]["times"]) / step)
        plt.yticks([i / 10 for i in range(0, 11)], ["{i}%".format(i=i * 10) for i in range(0, 11)], fontsize=10)
        if not noTitle:
            plt.title(title)
        if xlabel != None:
            plt.xlabel(xlabel)
        if ylabel != None:
            plt.ylabel(ylabel)
        if not noTitle:
            plt.title(title)
        if outPath != None and outPath != "":
            outFile = os.path.join(outPath, self.fileName + "_S_IntegrityPercentage.{}".format(format))
            plt.savefig(outFile, dpi=dpi, format=format, bbox_inches='tight')
        plt.clf()
        prnList = sorted(list(self.dataC.keys()))
        plt.figure(figsize=(0.38 * len(prnList), 38 * 2 / 25.4))
        step = 86400 / timeStep
        i = 1
        for prn in prnList:
            plt.bar(i, len(self.dataC[prn]["times"]) / step)
            i += 1
        plt.xlim(0, i)
        plt.xticks(list(range(1, i)), prnList)
        plt.yticks([i/10 for i in range(0, 11)], ["{i}%".format(i=i * 10) for i in range(0, 11)], fontsize=10)
        if not noTitle:
            plt.title(title)
        if xlabel != None:
            plt.xlabel(xlabel)
        if ylabel != None:
            plt.ylabel(ylabel)
        if not noTitle:
            plt.title(title)
        if outPath != None and outPath != "":
            outFile = os.path.join(outPath, self.fileName + "_C_IntegrityPercentage.{}".format(format))
            plt.savefig(outFile, dpi=dpi, format=format, bbox_inches='tight')

