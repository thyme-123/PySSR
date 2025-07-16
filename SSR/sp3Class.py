import os

from datetime import datetime

import matplotlib.pyplot as plt

class SP3_CLASS:

    def __init__(self, path=None):
        self.data = {}
        self.path = path
        self.fileName = None
        if path:
            self.read(path)

    def read(self, path):
        self.fileName = os.path.basename(path)
        year, month, day, hour, minute, second, sod = -1, -1, -1, -1, -1, -1, -1
        with open(path, "r") as f:
            line = f.readline()
            while not line.startswith("*"):
                line = f.readline()
            while line and ("EOF" not in line):
                while "  " in line:
                    line = line.replace("  ", " ")
                data = line.split(" ")
                if data[0] == "*":
                    year = int(data[1])
                    month = int(data[2])
                    day = int(data[3])
                    hour = int(data[4])
                    minute = int(data[5])
                    second = float(data[6])
                    sod = (hour * 60 + minute) * 60 + second
                    date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))
                else:
                    prn = data[0][1:]
                    if self.data.get(prn, -1) == -1:
                        self.data[prn] = []
                    self.data[prn].append(date)
                line = f.readline()

    def plotIntegrity(self, outPath, title="", noTitle=False, xlabel=None, ylabel=None, format="tiff", dpi=600):
        plt.clf()
        prnList = sorted(list(self.data.keys()))
        plt.figure(figsize=(6.45 * 4 / 3, 0.4 * len(prnList)))
        y1 = []
        y2 = []
        n = 1
        for prn in prnList:
            y1.append(n)
            y2.append(prn)
            plt.scatter(self.data[prn], [n] * len(self.data[prn]), s=0.3)
            n += 1
        plt.yticks(y1, y2, fontsize=10)
        if not noTitle:
            plt.title(title)
        if xlabel != None:
            plt.xlabel(xlabel)
        if ylabel != None:
            plt.ylabel(ylabel)
        if not noTitle:
            plt.title(title)
        if outPath != None and outPath != "":
            outFile = os.path.join(outPath, self.fileName + "_sp3_Integrity.{}".format(format))
            plt.savefig(outFile, dpi=dpi, format=format, bbox_inches='tight')

    def plotIntegrityPercentage(self, outPath, title="", noTitle=False, xlabel=None, ylabel=None, format="tiff", dpi=600):
        plt.clf()
        prnList = sorted(list(self.data.keys()))
        plt.figure(figsize=(0.30 * len(prnList), 38 * 2 / 25.4))
        step = 86400 / (5 * 60)
        for prn in prnList:
            plt.bar(prn, len(self.data[prn]) / step)
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
            outFile = os.path.join(outPath, self.fileName + "_sp3_IntegrityPercentage.{}".format(format))
            plt.savefig(outFile, dpi=dpi, format=format, bbox_inches='tight')