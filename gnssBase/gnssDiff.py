import os
from datetime import *
from math import *
import math

import matplotlib.pyplot as plt
import numpy as np
from numpy import *

from gnssBase.gnssIO import *
from gnssBase.gnssPosition import *
from gnssBase.gnssTime import *

#bbox_to_anchor = (2.1, 0.5)
loc = 5
pointSize = 5
maxNcol = 27
width = 0.5
fontsize = 6

weight_wR = {
    "GPS": 0.98,
    "GLO": 0.98,
    "GAL": 0.98,
    "QZS": 0.99,
    "BDS_MEO": 0.98,
    "BDS_IGSO": 0.99,
    "BDS_GEO": 0.99
}

weight_w2AC = {
    "GPS": 1 / 49,
    "GLO": 1 / 45,
    "GAL": 1 / 61,
    "QZS": 1 / 126,
    "BDS_MEO": 1 / 54,
    "BDS_IGSO": 1 / 126,
    "BDS_GEO": 1 / 126
}

def RMS(data):
    return np.sqrt(np.sum(data * data)/(len(data)))

def compute_SISRE(diffR, diffA, diffC, diffCLK, prn):
    system = prn[0]
    wR = 0
    w2AC = 0
    arrayR = np.array(diffR, dtype=float)
    arrayA = np.array(diffA, dtype=float)
    arrayC = np.array(diffC, dtype=float)
    arrayClk = np.array(diffCLK, dtype=float)
    if system == "G":
        wR = weight_wR["GPS"]
        w2AC = weight_w2AC["GPS"]
    elif system == "R":
        wR = weight_wR["GLO"]
        w2AC = weight_w2AC["GLO"]
    elif system == "E":
        wR = weight_wR["GAL"]
        w2AC = weight_w2AC["GAL"]
    elif system == "C":
        if prn in ["C01", "C02", "C03", "C04", "C05", "C59", "C60", "C61", "C62"]:
            wR = weight_wR["BDS_GEO"]
            w2AC = weight_w2AC["BDS_GEO"]
        elif prn in ["C06", "C07", "C08", "C09", "C10", "C13", "C16", "C31", "C56", "C38", "C39", "C40"]:
            wR = weight_wR["BDS_IGSO"]
            w2AC = weight_w2AC["BDS_IGSO"]
        else:
            wR = weight_wR["BDS_MEO"]
            w2AC = weight_w2AC["BDS_MEO"]
    return np.sqrt(
        pow(RMS(wR * arrayR - arrayClk * pow(10, -9) * c), 2) - w2AC * (RMS(arrayA * arrayA) + RMS(arrayC * arrayC))
    )


def title2FileName(title):
    s = ""
    for i in title:
        if i in [".", "\\", "/", ";"]:
            continue
        else:
            s += i
    return s

def gnssPlotBar(data, prns, title, imgPath=None, noTitle=False, xlabel=None, ylabel=None, format="tiff", dpi=600):
    plt.clf()
    bbox_to_anchor = (1.25 + len(prns) // maxNcol * 0.2, 0.5)
    plt.figure(figsize=(0.38 * len(prns), 38 * 2 / 25.4))
    if not noTitle:
        plt.title(title)
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    for prn in prns:
        plt.bar(prn, np.std(data[prn]), label=prn)
    if not noTitle:
        plt.title(title)
    if imgPath != None and imgPath != "":
        imgFile = imgPath
        plt.savefig(imgFile, dpi=dpi, format=format, bbox_inches='tight')
    return

def gnssPlotScatter(times, data, prns, title, imgPath=None, noTitle=False, noLenged=False,
                    xlabel=None, ylabel=None, xlim=None, ylim=None, format="tiff", dpi=600):
    plt.clf()
    plt.rcdefaults()
    bbox_to_anchor = (1.05 + len(prns)//maxNcol * 0.2, 0.5)
    plt.figure(figsize=(6.45*4/2.54, 38*2/25.4))
    for prn in prns:
        plt.scatter(times[prn], data[prn], label=prn, s=pointSize)
    if not noTitle:
        plt.title(title)
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim((ylim))
    if not noLenged:
        plt.legend(bbox_to_anchor=bbox_to_anchor, loc=5, ncol=len(prns) // maxNcol + 1)
    if imgPath != None and imgPath != "":
        imgFile = imgPath
        plt.savefig(imgFile, dpi=dpi, format=format, bbox_inches='tight')
    else:
        plt.show()
    return

def gnssPlotScatter_dateTime(times, data, prns, title, imgPath=None, noTitle=False, noLenged=False,
                    xlabel=None, ylabel=None, xlim=None, ylim=None, format="tiff", dpi=600):
    plt.clf()
    plt.rcdefaults()
    bbox_to_anchor = (1.05 + len(prns) // maxNcol * 0.2, 0.5)
    plt.figure(figsize=(6.45 * 4 / 2.54, 38 * 2 / 25.4))
    for prn in prns:
        plt.scatter(times[prn], data[prn], label=prn, s=pointSize)
    plt.xticks(rotation=45)
    if not noTitle:
        plt.title(title)
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim((ylim))
    if not noLenged:
        plt.legend(bbox_to_anchor=bbox_to_anchor, loc=5, ncol=len(prns) // maxNcol + 1)
    if imgPath != None and imgPath != "":
        imgFile = imgPath
        plt.savefig(imgFile, dpi=dpi, format=format, bbox_inches='tight')
    else:
        plt.show()
    return


def findTimeLimit(times):
    minTime = 86400
    maxTime = 0
    for key in times.keys():
        if not times[key]:
            continue
        maxtime = max(times[key])
        mintime = min(times[key])
        if maxtime > maxTime:
            maxTime = maxtime
        if mintime < minTime:
            minTime = mintime
    return minTime, maxTime

def RMSE(data):
    return
    return np.sqrt(((predictions - targets) ** 2).mean())


def formatSplit(string, start, length, type="float"):
    if type == "float":
        return float(string[start:start + length])
    elif type == "int":
        return int(string[start:start + length])
    elif type == "string":
        return string[start:start + length]
    else:
        return ""


def getPosition(x1, y1, z1, x2, y2, z2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2))


def norm(a, n):
    sum = 0
    for x in range(0, n):
        sum += a[x] * a[x]
    return sqrt(sum)


def dot(a, b, n):
    sum = 0
    for x in range(0, n):
        sum += a[x] * b[x]
    return sum


def cross3(a, b):
    c = zeros(3)
    c[0] = a[1] * b[2] - a[2] * b[1]
    c[1] = a[2] * b[0] - a[0] * b[2]
    c[2] = a[0] * b[1] - a[1] * b[0]
    return c


def XYZ_to_RSW(rr, vv, xyz):
    rsw = np.zeros(3)
    along = vv / norm(vv, 3)
    # cross = np.cross(rr, vv)
    cross = cross3(rr, vv)
    cross /= norm(cross, 3)
    # radial = np.cross(along, cross)
    radial = cross3(along, cross)
    rsw[0] = dot(xyz, radial, 3)
    rsw[1] = dot(xyz, along, 3)
    rsw[2] = dot(xyz, cross, 3)
    return rsw


def findToc(navData, startTime):
    toc = datetime.datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
    for key in navData:
        if abs(timeDiff(startTime, key)) < abs(timeDiff(startTime, toc)):
            toc = key
    return toc


def gnssDiff(sp3Data, sp3TemplateData, parent, basePrn, system=None, navData=None, ignore=[]):
    prns = []
    times = {}
    diffX = {}
    diffY = {}
    diffZ = {}
    diffPosition = {}
    diffClk = {}
    diffR = {}
    diffS = {}
    diffW = {}
    minTime, maxTime = None, None
    for prn in sp3Data:
        if prn in ignore:
            continue
        if prn[0] != system:
            continue
        sp3Data_prn = sp3Data[prn]
        if sp3TemplateData.get(prn, -1) == -1:
            if parent != None:
                parent.printLogSignal.emit("lack {} data in templateSp3".format(prn))
            continue
        sp3TemplateData_prn = sp3TemplateData[prn]
        times[prn] = []
        diffX[prn] = []
        diffY[prn] = []
        diffZ[prn] = []
        diffPosition[prn] = []
        diffClk[prn] = []
        diffR[prn] = []
        diffS[prn] = []
        diffW[prn] = []
        prns.append(prn)
        for date in sp3Data[prn]:
            if sp3TemplateData_prn.get(date, -1) == -1:
                if parent != None:
                    parent.printLogSignal.emit("{prn} lack time {time} in templateSp3".format(prn=prn, time=date))
                continue
            sp3X = sp3Data_prn[date][0]
            sp3Y = sp3Data_prn[date][1]
            sp3Z = sp3Data_prn[date][2]
            sp3Clk = sp3Data_prn[date][3]
            sod = sp3Data_prn[date][4]
            templateX = sp3TemplateData_prn[date][0]
            templateY = sp3TemplateData_prn[date][1]
            templateZ = sp3TemplateData_prn[date][2]
            templateClk = sp3TemplateData_prn[date][3]
            if sp3TemplateData.get(basePrn, -1) == -1 and parent != None:
                parent.printLogSignal.emit("base {prn} lack in templateSp3".format(prn=basePrn, time=date))
                continue
            if sp3TemplateData[basePrn].get(date, -1) == -1 and parent != None:
                parent.printLogSignal.emit("base {prn} lack time {time} in templateSp3".format(prn=basePrn, time=date))
                continue
            templateBaseClk = sp3TemplateData[basePrn][date][3]
            if sp3Data.get(basePrn, -1) == -1 and parent != None:
                parent.printLogSignal.emit("base {prn} lack in Sp3".format(prn=basePrn, time=date))
                continue
            if sp3Data[basePrn].get(date, -1) == -1 and parent != None:
                parent.printLogSignal.emit("base {prn} lack time {time} in Sp3".format(prn=basePrn, time=date))
                continue
            sp3BaseClk = sp3Data[basePrn][date][3]
            times[prn].append(sod / 60)
            diffx = (sp3X - templateX) * pow(10, 3)
            diffy = (sp3Y - templateY) * pow(10, 3)
            diffz = (sp3Z - templateZ) * pow(10, 3)
            diffX[prn].append(diffx)
            diffY[prn].append(diffy)
            diffZ[prn].append(diffz)
            diffPosition[prn].append(getPosition(sp3X, sp3Y, sp3Z, templateX, templateY, templateZ) * pow(10, 3))
            if navData:
                if navData.get(prn, -1) == -1:
                    continue
                toc = findToc(navData[prn], date)
                X, Y, Z, clk, Vx, Vy, Vz = 0, 0, 0, 0, 0, 0, 0
                if system == "C":
                    X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(navData[prn][toc], date, toc)
                elif system == "R":
                    X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(navData[prn][toc], date, toc)
                else:
                    X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(navData[prn][toc], date, toc, prn)
                rr = np.array([X, Y, Z])
                vv = np.array([Vx, Vy, Vz])
                xyz = np.array([diffx, diffy, diffz])
                sp3R = XYZ_to_RSW(rr, vv, xyz)
                diffR[prn].append(sp3R[0])
                diffS[prn].append(sp3R[1])
                diffW[prn].append(sp3R[2])
                #diffClk[prn].append(sp3Clk - templateClk )
                diffClk[prn].append((sp3Clk - sp3BaseClk) - (templateClk - templateBaseClk) - sp3R[0] / c * pow(10, 9))
                #diffClk[prn].append((sp3Clk - sp3BaseClk) - (templateClk - templateBaseClk))
        minTime, maxTime = findTimeLimit(times)
    diff = {
        "X Position": diffX,
        "Y Position": diffY,
        "Z Position": diffZ,
        "3D Position": diffPosition,
        "CLK": diffClk,
        "R Position": diffR,
        "A Position": diffS,
        "C Position": diffW,
    }
    return prns, times, diff, minTime, maxTime

def process_clk(diffClk, diffClk_pre, diffR, times):
    sat_avg = {}
    for prn in diffClk:
        sat_avg[prn] = np.mean(diffClk[prn])
    clk_time = {
        "G": {},
        "R": {},
        "E": {},
        "C": {},
    }
    num_time = {
        "G": {},
        "R": {},
        "E": {},
        "C": {},
    }
    for prn in times:
        for i in range(len(times[prn])):
            t = times[prn][i]
            clk = diffClk[prn][i] - sat_avg[prn]
            clk_time[prn[0]][t] = clk_time[prn[0]].get(t, 0) + clk
            num_time[prn[0]][t] = num_time[prn[0]].get(t, 0) + 1
    for s in clk_time:
        for t in clk_time[s]:
            clk_time[s][t] = clk_time[s][t] / num_time[s][t]
    for prn in diffClk:
        for i in range(len(times[prn])):
            t = times[prn][i]
            clk = diffClk[prn][i]
            diffClk_pre[prn].append(clk - clk_time[prn[0]][t] - sat_avg[prn])
    return


def gnssDiff_bias(sp3Data, sp3TemplateData, parent, systems=[], navData=None, ignore=[], log=False, mod="sod"):
    assert mod in ["sod", "dateTime"]
    prns = []
    times_sod = {}
    times_date = {}
    diffX = {}
    diffY = {}
    diffZ = {}
    diffPosition = {}
    diffClk = {}
    diffClkRed = {}
    diffClk_pre = {}
    diffR = {}
    diffS = {}
    diffW = {}
    diffSISRE = {}
    logLine = []
    minTime, maxTime = None, None
    for prn in sp3Data:
        if prn in ignore:
            continue
        if prn[0] not in systems:
            continue
        if not sp3TemplateData.get(prn, None):
            if parent:
                parent.printLogSignal.emit(
                    "base {prn} lack in templateSp3".format(prn=prn))
            if log:
                logLine.append("base {prn} lack in templateSp3".format(prn=prn))
            continue
        sp3TemplateData_prn = sp3TemplateData[prn]
        sp3Data_prn = sp3Data[prn]
        times_sod[prn] = []
        times_date[prn] = []
        diffX[prn] = []
        diffY[prn] = []
        diffZ[prn] = []
        diffPosition[prn] = []
        diffClk[prn] = []
        diffClkRed[prn] = []
        diffClk_pre[prn] = []
        diffR[prn] = []
        diffS[prn] = []
        diffW[prn] = []
        diffSISRE[prn] = 0
        prns.append(prn)
        for date in sp3Data_prn:
            if not sp3TemplateData_prn.get(date, None):
                if log:
                    logLine.append("lack {} data in templateSp3\n".format(prn))
                if parent:
                    parent.printLogSignal.emit("lack {} data in templateSp3".format(prn))
                continue
            system = prn[0]
            sp3X = sp3Data_prn[date][0]
            sp3Y = sp3Data_prn[date][1]
            sp3Z = sp3Data_prn[date][2]
            sp3Clk = sp3Data_prn[date][3]
            sod = sp3Data_prn[date][4]
            templateX = sp3TemplateData_prn[date][0]
            templateY = sp3TemplateData_prn[date][1]
            templateZ = sp3TemplateData_prn[date][2]
            templateClk = sp3TemplateData_prn[date][3]
            times_sod[prn].append(sod)
            times_date[prn].append(date)
            diffx = (sp3X - templateX) * pow(10, 3)
            diffy = (sp3Y - templateY) * pow(10, 3)
            diffz = (sp3Z - templateZ) * pow(10, 3)
            diffX[prn].append(diffx)
            diffY[prn].append(diffy)
            diffZ[prn].append(diffz)
            diffPosition[prn].append(getPosition(sp3X, sp3Y, sp3Z, templateX, templateY, templateZ) * pow(10, 3))
            diffClk[prn].append(sp3Clk - templateClk)
            if navData:
                if navData.get(prn, -1) == -1:
                    continue
                toc = findToc(navData[prn], date)
                X, Y, Z, clk, Vx, Vy, Vz = 0, 0, 0, 0, 0, 0, 0
                if system == "C":
                    X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(navData[prn][toc], date, toc)
                elif system == "R":
                    X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(navData[prn][toc], date, toc)
                else:
                    X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(navData[prn][toc], date, toc, prn)
                rr = np.array([X, Y, Z])
                vv = np.array([Vx, Vy, Vz])
                xyz = np.array([diffx, diffy, diffz])
                sp3R = XYZ_to_RSW(rr, vv, xyz)
                diffR[prn].append(sp3R[0])
                diffS[prn].append(sp3R[1])
                diffW[prn].append(sp3R[2])
                diffClkRed[prn].append((sp3Clk - templateClk) - sp3R[0] / c * pow(10, 9))
    process_clk(diffClkRed, diffClk_pre, diffR, times_date)
    if navData:
        for prn in prns:
            diffSISRE[prn] = compute_SISRE(diffR[prn], diffS[prn], diffW[prn], diffClk[prn], prn)
    for prn in prns:
        for i in range(len(times_date[prn])):
            flag = diffx < 1 and diffy < 1 and diffz < 1 and diffClk[prn][-1] < 1
            if navData:
                flag = flag and diffR[prn][-1] < 1 and diffS[prn][-1] < 1 and diffW[prn][-1] < 1
            logLine.append("{prn} {time} {x} {y} {z} {R} {A} {C} {clk1} {clk2} {flag}\n".format(
                prn=prn,
                time=times_date[prn][i],
                x=diffX[prn][i],
                y=diffY[prn][i],
                z=diffZ[prn][i],
                R=diffR[prn][i] if navData else "NAN",
                A=diffS[prn][i] if navData else "NAN",
                C=diffW[prn][i] if navData else "NAN",
                clk1=diffClk[prn][i],
                clk2=diffClk_pre[prn][i],
                flag="" if flag else "*",
            ))
    if mod == "sod":
        minTime, maxTime = findTimeLimit(times_sod)
    else:
        minTime, maxTime = findTimeLimit(times_date)
    diff = {
        "X Position": diffX,
        "Y Position": diffY,
        "Z Position": diffZ,
        "3D Position": diffPosition,
        "CLK": diffClk,
        "CLK_pre": diffClk_pre,
        "R Position": diffR,
        "A Position": diffS,
        "C Position": diffW,
        "SISRE": diffSISRE,
    }
    if mod == "sod":
        return prns, times_sod, diff, minTime, maxTime, logLine
    return prns, times_date, diff, minTime, maxTime, logLine



def gnssDiff_all(sp3Data, sp3TemplateData, parent, basePrns,
                 systems=[], navData=None, ignore=[], log=False):
    prns = []
    times = {}
    diffX = {}
    diffY = {}
    diffZ = {}
    diffPosition = {}
    diffClk = {}
    diffClk_pre = {}
    diffR = {}
    diffS = {}
    diffW = {}
    diffSISRE = {}
    logLine = []
    minTime, maxTime = None, None
    for prn in sp3Data:
        print(prn)
        if prn in ignore:
            continue
        if prn[0] not in systems:
            continue
        system = prn[0]
        sp3Data_prn = sp3Data[prn]
        if sp3TemplateData.get(prn, -1) == -1:
            if parent:
                if log:
                    logLine.append("lack {} data in templateSp3\n".format(prn))
                parent.printLogSignal.emit("lack {} data in templateSp3".format(prn))
            continue
        sp3TemplateData_prn = sp3TemplateData[prn]
        times[prn] = []
        diffX[prn] = []
        diffY[prn] = []
        diffZ[prn] = []
        diffPosition[prn] = []
        diffClk[prn] = []
        diffClk_pre[prn] = []
        diffR[prn] = []
        diffS[prn] = []
        diffW[prn] = []
        diffSISRE[prn] = 0
        prns.append(prn)
        for date in sp3Data[prn]:
            if sp3TemplateData_prn.get(date, -1) == -1:
                if log:
                    logLine.append("{prn} lack time {time} in templateSp3".format(prn=prn, time=date))
                parent.printLogSignal.emit("{prn} lack time {time} in templateSp3".format(prn=prn, time=date))
                continue
            sp3X = sp3Data_prn[date][0]
            sp3Y = sp3Data_prn[date][1]
            sp3Z = sp3Data_prn[date][2]
            sp3Clk = sp3Data_prn[date][3]
            sod = sp3Data_prn[date][4]
            templateX = sp3TemplateData_prn[date][0]
            templateY = sp3TemplateData_prn[date][1]
            templateZ = sp3TemplateData_prn[date][2]
            templateClk = sp3TemplateData_prn[date][3]
            if sp3TemplateData.get(basePrns[system], -1) == -1:
                if log:
                    logLine.append("base {prn} lack in templateSp3".format(prn=basePrns[system], time=date))
                print("base {prn} lack in templateSp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack in templateSp3".format(prn=basePrns[system], time=date))
                continue
            if sp3TemplateData[basePrns[prn[0]]].get(date, -1) == -1:
                if log:
                    logLine.append("base {prn} lack time {time} in templateSp3".format(prn=basePrns[system], time=date))
                print("base {prn} lack time {time} in templateSp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack time {time} in templateSp3".format(prn=basePrns[system], time=date))
                continue
            templateBaseClk = sp3TemplateData[basePrns[system]][date][3]
            if sp3Data.get(basePrns[system], -1) == -1:
                if log:
                    logLine.append("base {prn} lack in Sp3".format(prn=basePrns[system], time=date))
                print("base {prn} lack in Sp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack in Sp3".format(prn=basePrns[system], time=date))
                continue
            if sp3Data[basePrns[system]].get(date, -1) == -1:
                if log:
                    logLine.append("base {prn} lack time {time} in Sp3".format(prn=basePrns[system], time=date))
                print("base {prn} lack time {time} in Sp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack time {time} in Sp3".format(prn=basePrns[system], time=date))
                continue
            sp3BaseClk = sp3Data[basePrns[system]][date][3]
            times[prn].append(sod)
            diffx = (sp3X - templateX) * pow(10, 3)
            diffy = (sp3Y - templateY) * pow(10, 3)
            diffz = (sp3Z - templateZ) * pow(10, 3)
            diffX[prn].append(diffx)
            diffY[prn].append(diffy)
            diffZ[prn].append(diffz)
            diffPosition[prn].append(getPosition(sp3X, sp3Y, sp3Z, templateX, templateY, templateZ) * pow(10, 3))
            if navData:
                if navData.get(prn, -1) == -1:
                    continue
                toc = findToc(navData[prn], date)
                X, Y, Z, clk, Vx, Vy, Vz = 0, 0, 0, 0, 0, 0, 0
                if system == "C":
                    X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(navData[prn][toc], date, toc)
                elif system == "R":
                    X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(navData[prn][toc], date, toc)
                else:
                    X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(navData[prn][toc], date, toc, prn)
                rr = np.array([X, Y, Z])
                vv = np.array([Vx, Vy, Vz])
                xyz = np.array([diffx, diffy, diffz])
                sp3R = XYZ_to_RSW(rr, vv, xyz)
                diffR[prn].append(sp3R[0])
                diffS[prn].append(sp3R[1])
                diffW[prn].append(sp3R[2])
                # diffClk[prn].append(sp3Clk - templateClk)
                diffClk[prn].append((sp3Clk - sp3BaseClk) - (templateClk - templateBaseClk))
                diffClk_pre[prn].append((sp3Clk - sp3BaseClk) - (templateClk - templateBaseClk) - sp3R[0] / c * pow(10, 9))
            if log:
                flag = diffx < 1 and diffy < 1 and diffz < 1 and diffClk[prn][-1] < 1
                if navData:
                    flag = flag and diffR[prn][-1] < 1 and diffS[prn][-1] < 1 and diffW[prn][-1] < 1
                logLine.append("{prn} {time} {x} {y} {z} {R} {A} {C} {clk1} {clk2} {flag}\n".format(
                    prn=prn,
                    time=date,
                    x=diffx,
                    y=diffy,
                    z=diffz,
                    R=diffR[prn][-1] if navData else "NAN",
                    A=diffS[prn][-1] if navData else "NAN",
                    C=diffW[prn][-1] if navData else "NAN",
                    clk1=sp3Clk - templateClk,
                    clk2=diffClk[prn][-1],
                    flag="" if flag else "*",
                ))
        if navData:
            diffSISRE[prn] = compute_SISRE(diffR[prn], diffS[prn], diffW[prn], diffClk[prn], prn)
            print(prn, diffSISRE)
        minTime, maxTime = findTimeLimit(times)
    diff = {
        "X Position": diffX,
        "Y Position": diffY,
        "Z Position": diffZ,
        "3D Position": diffPosition,
        "CLK": diffClk,
        "CLK_pre": diffClk_pre,
        "R Position": diffR,
        "A Position": diffS,
        "C Position": diffW,
        "SISRE": diffSISRE,
    }
    return prns, times, diff, minTime, maxTime, logLine

def gnssDiff_dateTIme(sp3Data, sp3TemplateData, parent, basePrns,
                 systems=[], navData=None, ignore=[]):
    prns = []
    times = {}
    diffX = {}
    diffY = {}
    diffZ = {}
    diffPosition = {}
    diffClk = {}
    diffR = {}
    diffS = {}
    diffW = {}
    minTime, maxTime = None, None
    for prn in sp3Data:
        if prn in ignore:
            continue
        if prn[0] not in systems:
            continue
        system = prn[0]
        sp3Data_prn = sp3Data[prn]
        if sp3TemplateData.get(prn, -1) == -1:
            if parent:
                parent.printLogSignal.emit("lack {} data in templateSp3".format(prn))
            continue
        sp3TemplateData_prn = sp3TemplateData[prn]
        times[prn] = []
        diffX[prn] = []
        diffY[prn] = []
        diffZ[prn] = []
        diffPosition[prn] = []
        diffClk[prn] = []
        diffR[prn] = []
        diffS[prn] = []
        diffW[prn] = []
        prns.append(prn)
        for date in sp3Data[prn]:
            if sp3TemplateData_prn.get(date, -1) == -1:
                if parent:
                    parent.printLogSignal.emit("{prn} lack time {time} in templateSp3".format(prn=prn, time=date))
                continue
            sp3X = sp3Data_prn[date][0]
            sp3Y = sp3Data_prn[date][1]
            sp3Z = sp3Data_prn[date][2]
            sp3Clk = sp3Data_prn[date][3]
            sod = sp3Data_prn[date][4]
            templateX = sp3TemplateData_prn[date][0]
            templateY = sp3TemplateData_prn[date][1]
            templateZ = sp3TemplateData_prn[date][2]
            templateClk = sp3TemplateData_prn[date][3]
            if sp3TemplateData.get(basePrns[system], -1) == -1:
                print("base {prn} lack in templateSp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack in templateSp3".format(prn=basePrns[system], time=date))
                continue
            if sp3TemplateData[basePrns[prn[0]]].get(date, -1) == -1:
                print("base {prn} lack time {time} in templateSp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack time {time} in templateSp3".format(prn=basePrns[system], time=date))
                continue
            templateBaseClk = sp3TemplateData[basePrns[system]][date][3]
            if sp3Data.get(basePrns[system], -1) == -1:
                print("base {prn} lack in Sp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack in Sp3".format(prn=basePrns[system], time=date))
                continue
            if sp3Data[basePrns[system]].get(date, -1) == -1:
                print("base {prn} lack time {time} in Sp3".format(prn=basePrns[system], time=date))
                if parent:
                    parent.printLogSignal.emit("base {prn} lack time {time} in Sp3".format(prn=basePrns[system], time=date))
                continue
            sp3BaseClk = sp3Data[basePrns[system]][date][3]
            times[prn].append(date)
            diffx = (sp3X - templateX) * pow(10, 3)
            diffy = (sp3Y - templateY) * pow(10, 3)
            diffz = (sp3Z - templateZ) * pow(10, 3)
            diffX[prn].append(diffx)
            diffY[prn].append(diffy)
            diffZ[prn].append(diffz)
            diffPosition[prn].append(getPosition(sp3X, sp3Y, sp3Z, templateX, templateY, templateZ) * pow(10, 3))
            if navData:
                if navData.get(prn, -1) == -1:
                    continue
                toc = findToc(navData[prn], date)
                X, Y, Z, clk, Vx, Vy, Vz = 0, 0, 0, 0, 0, 0, 0
                if system == "C":
                    X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(navData[prn][toc], date, toc)
                elif system == "R":
                    X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(navData[prn][toc], date, toc)
                else:
                    X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(navData[prn][toc], date, toc, prn)
                rr = np.array([X, Y, Z])
                vv = np.array([Vx, Vy, Vz])
                xyz = np.array([diffx, diffy, diffz])
                sp3R = XYZ_to_RSW(rr, vv, xyz)
                diffR[prn].append(sp3R[0])
                diffS[prn].append(sp3R[1])
                diffW[prn].append(sp3R[2])
                if sp3R[1]>1.5:
                    print(prn)
                #diffClk[prn].append(sp3Clk - templateClk )
                diffClk[prn].append((sp3Clk - sp3BaseClk) - (templateClk - templateBaseClk) - sp3R[0] / c * pow(10, 9))
                #diffClk[prn].append((sp3Clk - sp3BaseClk) - (templateClk - templateBaseClk))
        # minTime, maxTime = findTimeLimit(times)
    diff = {
        "X Position": diffX,
        "Y Position": diffY,
        "Z Position": diffZ,
        "3D Position": diffPosition,
        "CLK": diffClk,
        "R Position": diffR,
        "A Position": diffS,
        "C Position": diffW,
    }
    return prns, times, diff, minTime, maxTime