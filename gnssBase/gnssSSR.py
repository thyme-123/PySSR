import datetime
from math import *
from datetime import *

import numpy as np

from gnssBase.gnssIO import *
from gnssBase.gnssTime import *
from gnssBase.gnssPosition import *

c = 299792458


def selectIOD_rt(data, startTime, iod):
    toc = None
    keys = data.keys()
    keyList = []
    for key in keys:
        if data[key]["IOD"] == iod:
            keyList.append(key)
    for key in keyList:
        if ((not toc) or abs(timeSub(startTime, key)) < abs(timeSub(startTime, toc))) and (
                abs(timeSub(startTime, key)) < 10):
            toc = key
    return toc

def selectIOD_BDS_rt(data, startTime, toc_bds):
    toc = None
    keys = data.keys()
    keyList = []
    IOD = (time2WeekSeconds(toc_bds - timedelta(seconds=14)) / 720) % 240
    for key in keys:
        if IOD == data[key]["IOD"]:
            keyList.append(key)
    for key in keyList:
        if ((not toc) or abs(timeSub(startTime, key)) < abs(timeSub(startTime, toc))) and (
                abs(timeSub(startTime, key)) < 10):
            toc = key
    return toc

def selectIOD_GLO_rt(data, startTime, toc_glo):
    toc = None
    keys = data.keys()
    keyList = []
    #IOD = (time2WeekSeconds(toc_bds - timedelta(seconds=14)) / 720) % 240
    tMos = toc_glo - timedelta(seconds=18) + timedelta(seconds=3*3600)
    IOD = getDaySec(tMos) // 900
    for key in keys:
        if IOD == data[key]["IOD"]:
            keyList.append(key)
    for key in keyList:
        if ((not toc) or abs(timeSub(startTime, key)) < abs(timeSub(startTime, toc))) and (
                abs(timeSub(startTime, key)) < 10):
            toc = key
    return toc

def selctToc_BDS_rt(sData, rnxData, startTime):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 5:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        iod = (time2WeekSeconds(t - timedelta(seconds=14)) / 720) % 240
        if iod == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t

def selctToc_rt(sData, rnxData, startTime, prn=None):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 5:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        if rnxData[t]["IOD"] == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t

def selctToc_GLO_rt(sData, rnxData, startTime):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 10:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        tMos = t - timedelta(seconds=18) + timedelta(seconds=3 * 3600)
        IOD = getDaySec(tMos) // 900
        if IOD == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t

def selctToc_GLO(sData, rnxData, startTime):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 5:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        tMos = t - timedelta(seconds=18) + timedelta(seconds=3 * 3600)
        IOD = getDaySec(tMos) // 900
        if IOD == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t

def selectIOD(data, startTime, iod):
    toc = None
    keys = data.keys()
    keyList = []
    for key in keys:
        if data[key]["IOD"] == iod:
            keyList.append(key)
    for key in keyList:
        if ((not toc) or abs(timeSub(startTime, key)) < abs(timeSub(startTime, toc))) and (
                abs(timeSub(startTime, key)) < 5):
            toc = key
    return toc


def selectIOD_BDS(data, startTime, toc_bds):
    toc = None
    keys = data.keys()
    keyList = []
    IOD = (time2WeekSeconds(toc_bds - timedelta(seconds=14)) / 720) % 240
    for key in keys:
        if IOD == data[key]["IOD"]:
            keyList.append(key)
    for key in keyList:
        if ((not toc) or abs(timeSub(startTime, key)) < abs(timeSub(startTime, toc))) and (
                abs(timeSub(startTime, key)) < 5):
            toc = key
    return toc

def selectIOD_GLO(data, startTime, toc_glo):
    toc = None
    keys = data.keys()
    keyList = []
    #IOD = (time2WeekSeconds(toc_bds - timedelta(seconds=14)) / 720) % 240
    tMos = toc_glo - timedelta(seconds=18) + timedelta(seconds=3*3600)
    IOD = getDaySec(tMos) // 900
    for key in keys:
        if IOD == data[key]["IOD"]:
            keyList.append(key)
    for key in keyList:
        if ((not toc) or abs(timeSub(startTime, key)) < abs(timeSub(startTime, toc))) and (
                abs(timeSub(startTime, key)) < 5):
            toc = key
    return toc

def selctToc_GLO(sData, rnxData, startTime):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 5:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        tMos = t - timedelta(seconds=18) + timedelta(seconds=3 * 3600)
        IOD = getDaySec(tMos) // 900
        if IOD == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t


def selctToc_BDS(sData, rnxData, startTime):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 5:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        iod = (time2WeekSeconds(t - timedelta(seconds=14)) / 720) % 240
        if iod == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t


def selctToc(sData, rnxData, startTime, prn=None):
    toc = None
    for t in sData:
        if ((not toc) or (abs(timeSub(toc, startTime)) < abs(timeSub(t, startTime)))) and abs(
                timeSub(t, startTime)) < 5:
            toc = t
    if toc == None:
        return None
    ans_t = None
    for t in rnxData:
        if rnxData[t]["IOD"] == sData[toc]["IOD"]:
            if ans_t == None:
                ans_t = t
            else:
                if abs(timeSub(t, startTime)) < abs(timeSub(ans_t, startTime)):
                    ans_t = t
    return ans_t


def noSp3Line(rnxData, times):
    mintime = min(times)
    lines = []
    satellites = []
    startTime = datetime.datetime(1980, 1, 6)
    while startTime < mintime:
        startTime += datetime.timedelta(seconds=86400)
    outTime = startTime
    epoch = 0
    for _ in range(24 * 12):  # 24小时,每5分钟
        print(startTime)
        lines.append("*  {year:4} {month:2} {day:2} {hour:2} {minute:2} {second:>11}\n".format(
            year=startTime.year,
            month=startTime.month,
            day=startTime.day,
            hour=startTime.hour,
            minute=startTime.minute,
            second="{:.8f}".format(startTime.second),
        ))
        for satellite in rnxData:
            if satellite not in satellites:
                satellites.append(satellite)
            keys = sorted(list(rnxData[satellite].keys()))
            for index in range(len(keys)):
                if keys[index] >= startTime:
                    break
            toc = keys[index]
            data = rnxData[satellite][toc]
            if satellite.startswith("C"):
                X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(data, startTime, toc, prn=satellite)
            elif satellite.startswith("R") or satellite.startswith("S"):
                X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(data, startTime, toc)
            else:
                X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(data, startTime, toc, prn=satellite)
            if satellite == "C02":
                pass
            lines.append("P{PRN:3} {X:>13} {Y:>13} {Z:>13} {clk:>13}\n".format(PRN=satellite,
                                                                               X="{:.6f}".format(X / 1000),
                                                                               Y="{:.6f}".format(Y / 1000),
                                                                               Z="{:.6f}".format(Z / 1000),
                                                                               clk="{:.6f}".format(
                                                                                   clk * pow(10, 6))))
        startTime += datetime.timedelta(seconds=5 * 60)
        epoch += 1
    satellites = sorted(satellites)
    return lines, outTime, satellites, epoch


def noClkLine(rnxData, times):
    mintime = min(times)
    lines = []
    startTime = datetime.datetime(1980, 1, 6)
    while startTime < mintime:
        startTime += datetime.timedelta(seconds=86400)
    outTime = startTime
    for _ in range(24 * 60 * 2):  # 24小时,每30秒
        print(startTime)
        for satellite in rnxData:
            keys = sorted(list(rnxData[satellite].keys()))
            for index in range(len(keys)):
                if keys[index] >= startTime:
                    break
            toc = keys[index]
            data = rnxData[satellite][toc]
            if satellite.startswith("C"):
                X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(data, startTime, toc, prn=satellite)
            elif satellite.startswith("R"):
                X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(data, startTime, toc)
            elif satellite.startswith("G") or satellite.startswith("E"):
                X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(data, startTime, toc, prn=satellite)
            else:
                continue
            lines.append(
                "AS {PRN:3}  {year:>4} {month:>2} {day:>2} {hour:>2} {minute:>2} {second:>9}  1   {clk:>19}\n".format(
                    PRN=satellite,
                    year=startTime.year,
                    month=startTime.month,
                    day=startTime.day,
                    hour=startTime.hour,
                    minute=startTime.minute,
                    second="{:.6f}".format(startTime.second),
                    clk="{:.12e}".format(clk)))
        startTime += datetime.timedelta(seconds=30)
    return lines, outTime


def sp3Lines(rnxData, times, cData, sData, atxData=None, mod=False, log=False):
    mintime = min(times)
    lines = []
    logLines = []
    satellites = []
    startTime = datetime.datetime(1980, 1, 6)
    while startTime < mintime:
        startTime += datetime.timedelta(seconds=86400)
    outTime = startTime
    epoch = 0
    for _ in range(24 * 12):  # 24小时,每5分钟
        print(startTime)
        lines.append("*  {year:4} {month:2} {day:2} {hour:2} {minute:2} {second:>11}\n".format(
            year=startTime.year,
            month=startTime.month,
            day=startTime.day,
            hour=startTime.hour,
            minute=startTime.minute,
            second="{:.8f}".format(startTime.second),
        ))
        if log:
            logLines.append("> {year:4} {month:2} {day:2} {hour:2} {minute:2} {second:>11}\n".format(
                year=startTime.year,
                month=startTime.month,
                day=startTime.day,
                hour=startTime.hour,
                minute=startTime.minute,
                second="{:.8f}".format(startTime.second),
            ))
        linesTemp = []
        for satellite in rnxData:
            timeDifftoc = 0
            if satellite.startswith("E"):
                timeDifftoc = 60 * 60 * 6
            else:
                timeDifftoc = 60 * 60 * 6
            keys = sorted(list(rnxData[satellite].keys()))
            for index in range(len(keys)):
                if keys[index] >= startTime:
                    break
            toc = keys[index]
            if satellite not in sData:
                if log:
                    logLines.append("{prn} not in ssr,skip\n".format(prn=satellite))
                continue
            if (not satellite.startswith("C")) and (not satellite.startswith("R")):
                toc = selctToc(sData[satellite], rnxData[satellite], startTime, satellite)
            elif satellite.startswith("C"):
                if not mod:
                    toc = selctToc_BDS(sData[satellite], rnxData[satellite], startTime)
                else:
                    toc = selctToc(sData[satellite], rnxData[satellite], startTime, satellite)
            elif satellite.startswith("R"):
                toc = selctToc_GLO(sData[satellite], rnxData[satellite], startTime)
            else:
                print(toc, startTime)
            if not toc:
                if log:
                    logLines.append("{prn} not it nav,skip\n".format(prn=satellite))
                continue
            if abs(timeSub(startTime, toc)) > timeDifftoc:
                if log:
                    logLines.append("{prn} startTime and toc diff too big,skip\n".format(prn=satellite))
                continue
            data = rnxData[satellite][toc]
            if satellite.startswith("C"):
                X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(data, startTime, toc, prn=satellite, mod=mod)
            elif satellite.startswith("R"):
                X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(data, startTime, toc)
            else:
                X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(data, startTime, toc, prn=satellite)
            if satellite not in cData:
                if log:
                    logLines.append("{prn} not in ssr,skip\n".format(prn=satellite))
                continue
            if satellite.startswith("C"):
                cdataTime = selectIOD_BDS(cData[satellite], startTime, toc)
            elif satellite.startswith("R"):
                cdataTime = selectIOD_GLO(cData[satellite], startTime, toc)
            else:
                cdataTime = selectIOD(cData[satellite], startTime, data["IOD"])
            if not cdataTime:
                if log:
                    logLines.append("{prn} not in ssr,skip".format(prn=satellite))
                continue
            cdata = cData[satellite][cdataTime]
            tsv2 = timeSub(startTime, cdataTime)
            clk_repair = clk + ((cdata["DeltaClockC0"] + cdata["DeltaClockC1"] / 1000 * tsv2 + cdata[
                "DeltaClockC2"] / 1000 * pow(
                tsv2, 2)) / c)
            if satellite not in sData:
                if log:
                    logLines.append("{prn} not in ssr,skip\n".format(prn=satellite))
                continue
            if satellite.startswith("C"):
                sdataTime = selectIOD_BDS(sData[satellite], startTime, toc)
            elif satellite.startswith("R"):
                sdataTime = selectIOD_GLO(sData[satellite], startTime, toc)
            else:
                sdataTime = selectIOD(sData[satellite], startTime, data["IOD"])
            if not sdataTime:
                if log:
                    logLines.append("{prn} IOD mismatch\n".format(prn=satellite))
                continue
            sdata = sData[satellite][sdataTime]
            if log:
                logLines.append("{prn} {startTime} NavTime:{toc} ssrOrbTime:{sTime} ssrClkTime:{cTime}\n".format(prn=satellite,
                                                                                            startTime=startTime,
                                                                                            toc=toc,
                                                                                            sTime=sdataTime,
                                                                                            cTime=cdataTime))
            tsv = timeSub(startTime, sdataTime)
            DeltaOrbitRadial = sdata["DeltaOrbitRadial"]
            DeltaOrbitAlongTrack = sdata["DeltaOrbitAlongTrack"]
            DeltaOrbitCrossTrack = sdata["DeltaOrbitCrossTrack"]
            DotOrbitDeltaRadial = sdata["DotOrbitDeltaRadial"] / 1000
            DotOrbitDeltaAlongTrack = sdata["DotOrbitDeltaAlongTrack"] / 1000
            DotOrbitDeltaCrossTrack = sdata["DotOrbitDeltaCrossTrack"] / 1000
            DeltaO = np.array([[DeltaOrbitRadial], [DeltaOrbitAlongTrack], [DeltaOrbitCrossTrack]]) + np.array(
                [[DotOrbitDeltaRadial], [DotOrbitDeltaAlongTrack], [DotOrbitDeltaCrossTrack]]) * tsv
            rX = np.array([[X], [Y], [Z]])
            rDot = np.array([[Vx], [Vy], [Vz]])
            #clk_repair += 2*np.dot(rX.T[0],rDot.T[0])/299792458.0/299792458.0
            e_along = rDot / np.linalg.norm(rDot)
            e_cross = np.cross(rX.T, rDot.T).T / (np.linalg.norm(np.cross(rX.T, rDot.T).T))
            e_radial = np.cross(e_along.T, e_cross.T).T
            DeltaX = np.zeros((3, 3))
            DeltaX[0][0] = e_radial[0]
            DeltaX[1][0] = e_radial[1]
            DeltaX[2][0] = e_radial[2]
            DeltaX[0][1] = e_along[0]
            DeltaX[1][1] = e_along[1]
            DeltaX[2][1] = e_along[2]
            DeltaX[0][2] = e_cross[0]
            DeltaX[1][2] = e_cross[1]
            DeltaX[2][2] = e_cross[2]
            X_reapir = rX - DeltaX @ DeltaO
            if atxData:
                if atxData.get(satellite, -1) != -1:
                    neuList1 = None
                    neuList2 = None
                    for atxdata in atxData[satellite]:
                        validFROM = atxdata["validFROM"]
                        validUNTIL = atxdata["validUNTIL"]
                        frequencyData = atxdata["frequencyData"]
                        if timeSub(validUNTIL, startTime) > 0:
                            if satellite[0] == "G":
                                frequency1 = "G01"
                                frequency2 = "G02"
                                frq = [1, 2]
                            elif satellite[0] == "E":
                                frequency1 = "E01"
                                frequency2 = "E05"
                                frq = [1, 5]
                            elif satellite[0] == "R":
                                frequency1 = "R01"
                                frequency2 = "R02"
                                frq = [1, 2]
                            elif satellite[0] == "C":
                                frequency1 = "C02"
                                frequency2 = "C07"
                                frq = [2, 7]
                            if frequencyData.get(frequency1, -1) == -1 or frequencyData.get(frequency2, -1) == -1:
                                continue
                            neuList1 = frequencyData[frequency1]
                            neuList2 = frequencyData[frequency2]
                    if neuList1 != None:
                        dx, dy, dz = satposs(satellite, startTime, rX.T[0], neuList1, neuList2, frq)
                        X_reapir[0][0] -= dx
                        X_reapir[1][0] -= dy
                        X_reapir[2][0] -= dz
            if satellite not in satellites:
                satellites.append(satellite)
            linesTemp.append("P{PRN:3} {X:>13} {Y:>13} {Z:>13} {clk:>13}\n".format(PRN=satellite,
                                                                               X="{:.6f}".format(X_reapir[0][0] / 1000),
                                                                               Y="{:.6f}".format(X_reapir[1][0] / 1000),
                                                                               Z="{:.6f}".format(X_reapir[2][0] / 1000),
                                                                               clk="{:.6f}".format(
                                                                                   clk_repair * pow(10, 6))))
        linesTemp = sorted(linesTemp)
        for line in linesTemp:
            lines.append(line)
        epoch += 1
        startTime += timedelta(seconds=5 * 60)
    return lines, outTime, satellites, epoch, logLines

def clkLines(rnxData, times, cData, mod=False, log=False):
    mintime = min(times)
    startTime = datetime.datetime(1980, 1, 6)
    while startTime < mintime:
        startTime += datetime.timedelta(seconds=86400)
    ansTime = startTime
    lines = []
    logLines = []
    for _ in range(24 * 60 * 2):  # 24小时,每30秒
        print(startTime)
        if log:
            logLines.append("> {year:4} {month:2} {day:2} {hour:2} {minute:2} {second:>11}\n".format(
                year=startTime.year,
                month=startTime.month,
                day=startTime.day,
                hour=startTime.hour,
                minute=startTime.minute,
                second="{:.8f}".format(startTime.second),
            ))
        for satellite in rnxData:
            timeDifftoc = 0
            if satellite.startswith("E"):
                timeDifftoc = 60 * 60 * 6
            else:
                timeDifftoc = 60 * 60 * 6
            keys = sorted(list(rnxData[satellite].keys()))
            for index in range(len(keys)):
                if keys[index] >= startTime:
                    break
            toc = keys[index]
            if satellite not in cData:
                if log:
                    logLines.append("{prn} not in ssr,skip\n".format(prn=satellite))
                continue
            if (not satellite.startswith("C")) and (not satellite.startswith("R")):
                toc = selctToc(cData[satellite], rnxData[satellite], startTime, satellite)
            elif satellite.startswith("C"):
                toc = selctToc_BDS(cData[satellite], rnxData[satellite], startTime)
            elif satellite.startswith("R"):
                toc = selctToc_GLO(cData[satellite], rnxData[satellite], startTime)
            if not toc:
                if log:
                    logLines.append("{prn} not toc,skip\n".format(prn=satellite))
                continue
            if abs(timeSub(startTime, toc)) > timeDifftoc:
                if log:
                    logLines.append("{prn} startTime and toc diff too big,skip\n".format(prn=satellite))
                continue
            if satellite not in cData:
                if log:
                    logLines.append("{prn} not in ssr,skip\n".format(prn=satellite))
                continue
            data = rnxData[satellite][toc]
            if satellite.startswith("C"):
                X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(data, startTime, toc, prn=satellite, mod=mod)
            elif satellite.startswith("R"):
                X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(data, startTime, toc)
            else:
                X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(data, startTime, toc, prn=satellite)
            if satellite.startswith("C"):
                cdataTime = selectIOD_BDS(cData[satellite], startTime, toc)
            elif satellite.startswith("R"):
                cdataTime = selectIOD_GLO(cData[satellite], startTime, toc)
            else:
                cdataTime = selectIOD(cData[satellite], startTime, data["IOD"])
            if not cdataTime:
                if log:
                    logLines.append("{prn} IOD mismatch\n".format(prn=satellite))
                continue
            if log:
                logLines.append("{prn} {startTime} NavTime:{toc} ssrClkTime:{cTime}\n".format(prn=satellite,
                                                                                            startTime=startTime,
                                                                                            toc=toc,
                                                                                            cTime=cdataTime))
            cdata = cData[satellite][cdataTime]
            tsv2 = timeSub(startTime, cdataTime)
            clk_repair = clk + ((cdata["DeltaClockC0"] + cdata["DeltaClockC1"] / 1000 * tsv2 + cdata[
                "DeltaClockC2"] / 1000 * pow(
                tsv2, 2)) / c)
            rX = np.array([[X], [Y], [Z]])
            rDot = np.array([[Vx], [Vy], [Vz]])
            #clk_repair += 2.0 * (X * xDot + Y * yDot + Z * zDot) / c / c
            lines.append(
                "AS {PRN:3}  {year:>4} {month:>2} {day:>2} {hour:>2} {minute:>2} {second:>9}  1   {clk:>19}\n".format(
                    PRN=satellite,
                    year=startTime.year,
                    month=startTime.month,
                    day=startTime.day,
                    hour=startTime.hour,
                    minute=startTime.minute,
                    second="{:.6f}".format(startTime.second),
                    clk="{:.12e}".format(clk_repair)))
        startTime += timedelta(seconds=30)
    return lines, ansTime, logLines

def repairSp3(outPath ,navPath, ssrPath, atxPath=None):
    pass

def repairClk(outPath ,navPath, ssrPath, atxPath=None):
    pass
