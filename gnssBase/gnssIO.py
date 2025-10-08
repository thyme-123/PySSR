import re
import os
from datetime import *

from gnssBase import gnssTime


def formatString(x):
    value = "{:-.12e}".format(x)
    return "{:>19}".format(value)

def getSp3Header(satellites, mintime, epoch):
    header = []
    JD = gnssTime.day2JD(mintime)
    week, day = gnssTime.time2WeekDay(mintime)
    weekSecond = gnssTime.time2WeekSeconds(mintime)
    header.append("#dP{year:>4} {month:>2} {day:>2} {hour:>2} {minute:>2} {second:>11} {epoch:>7} ORBIT IGS20 IGU KMUS\n".format(
        year=mintime.year,
        month=mintime.month,
        day=mintime.day,
        hour=mintime.hour,
        minute=mintime.minute,
        second=mintime.second,
        epoch=epoch,
    ))
    header.append("## {week:>4} {weekSecond:>15}   300.00000000 {JD:>5} {JDS:>15}\n".format(
        week=week,
        weekSecond=weekSecond,
        JD=int(JD),
        JDS=JD-int(JD),
    ))
    satellitesNumber = len(satellites)
    satellites += ["   "] * (17 - satellitesNumber % 17)
    s = "+  {:0>3}   ".format(satellitesNumber)
    i = 0
    j = 0
    while i < len(satellites):
        s += satellites[i]
        i += 1
        if i % 17 == 0 and i != 0:
            s += "\n"
            header.append(s)
            s = "+        "
            j += 1
    for i in range(j):
        header.append("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    header.append("%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n")
    header.append("%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n")
    header.append("%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n")
    header.append("%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n")
    header.append("%i    0    0    0    0      0      0      0      0         0\n")
    header.append("%i    0    0    0    0      0      0      0      0         0\n")
    return header

def getClkHeader(mintime):
    header = []
    header.append("     2.00           C                                       RINEX VERSION / TYPE\n")
    header.append("SparseToClk         KMUS/NAV SERVICE    {year:4}{month:0>2}{day:0>2} {hour:0>2}{minute:0>2}{second:0>2}     PGM / RUN BY / DATE\n".format(
        year=mintime.year,
        month=mintime.month,
        day=mintime.day,
        hour=mintime.hour,
        minute=mintime.minute,
        second=mintime.second,
    ))
    header.append("     1    AS                                                # / TYPES OF DATA\n")
    header.append("                                                            END OF HEADER\n")
    return header

def writeRtSp3Header(f, t):
    JD = gnssTime.day2JD(t)
    week, day = gnssTime.time2WeekDay(t)
    weekSecond = gnssTime.time2WeekSeconds(t)
    f.write("#dP{year:>4} {month:>2} {day:>2} {hour:>2} {minute:>2} {second:>11} {epoch:>7} ORBIT IGS20 IGU KMUS\n".format(
        year=t.year,
        month=t.month,
        day=t.day,
        hour=t.hour,
        minute=t.minute,
        second=t.second,
        epoch=17280))
    f.write("## {week:>4} {weekSecond:>15}   300.00000000 {JD:>5} {JDS:>15}\n".format(
        week=week,
        weekSecond=weekSecond,
        JD=int(JD),
        JDS=JD-int(JD),
    ))
    f.write("+  108   G02G03G04G05G06G07G08G09G10G11G12G13G14G15G16G17G18\n")
    f.write("+        G19G20G22G23G24G25G26G27G28G29G30G31G32R01R02R03R04\n")
    f.write("+        R05R07R08R09R11R12R14R15R16R17R18R19R20R21R22R24E02\n")
    f.write("+        E03E04E05E06E07E08E09E10E13E15E16E21E23E24E25E26E27\n")
    f.write("+        E29E30E31E33E34E36C06C07C09C10C11C12C13C16C19C20C21\n")
    f.write("+        C22C23C24C25C26C27C28C29C30C32C33C34C35C36C37C38C39\n")
    f.write("+        C40C41C42C43C44C45  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n")
    f.write("%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n")
    f.write("%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n")
    f.write("%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n")
    f.write("%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n")
    f.write("%i    0    0    0    0      0      0      0      0         0\n")
    f.write("%i    0    0    0    0      0      0      0      0         0\n")
    pass

def wirteRtClkHeader(f, mintime):
    f.write("     2.00           C                                       RINEX VERSION / TYPE\n")
    f.write("SparseToClk         KMUS/NAV SERVICE    {year:4}{month:0>2}{day:0>2} {hour:0>2}{minute:0>2}{second:0>2}     PGM / RUN BY / DATE\n".format(
        year=mintime.year,
        month=mintime.month,
        day=mintime.day,
        hour=mintime.hour,
        minute=mintime.minute,
        second=mintime.second,
    ))
    f.write("     1    AS                                                # / TYPES OF DATA\n")
    f.write("                                                            END OF HEADER\n")


def formatSplit(string, start, length, type="float"):
    s = string[start:start + length]
    s = s.replace(" ","").replace("D", "E")
    if len(s) == 0 and type == "string":
        return ""
    elif len(s) == 0:
        return 0
    if type == "float":
        return float(s)
    elif type == "int":
        return int(float(s))
    elif type == "string":
        return s
    else:
        return ""

def readSSR(path):
    cData = {}
    sData = {}
    codeData = {}
    times = []
    with open(path, "r") as f:
        while True:
            line = f.readline()
            while "  " in line:
                line = line.replace("  ", " ")
            if line == "":
                break
            data1 = line.split(" ")
            if data1[1] == "ORBIT":
                year = int(data1[2])
                month = int(data1[3])
                day = int(data1[4])
                hour = int(data1[5])
                minute = int(data1[6])
                second = int(float(data1[7]))
                toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
                numberOfPRN = int(data1[9])
                if toc not in times:
                    times.append(toc)
                for _ in range(numberOfPRN):
                    line = f.readline()
                    while "  " in line:
                        line = line.replace("  ", " ")
                    data2 = line.split(" ")
                    PRN = data2[0]
                    IOD = float(data2[1])
                    DeltaOrbitRadial = float(data2[2])
                    DeltaOrbitAlongTrack = float(data2[3])
                    DeltaOrbitCrossTrack = float(data2[4])
                    DotOrbitDeltaRadial = float(data2[5])
                    DotOrbitDeltaAlongTrack = float(data2[6])
                    DotOrbitDeltaCrossTrack = float(data2[7])
                    if sData.get(PRN, -1) == -1:
                        sData[PRN] = {}
                    sData[PRN][toc] = {
                        "IOD": IOD,
                        "DeltaOrbitRadial": DeltaOrbitRadial,
                        "DeltaOrbitAlongTrack": DeltaOrbitAlongTrack,
                        "DeltaOrbitCrossTrack": DeltaOrbitCrossTrack,
                        "DotOrbitDeltaRadial": DotOrbitDeltaRadial,
                        "DotOrbitDeltaAlongTrack": DotOrbitDeltaAlongTrack,
                        "DotOrbitDeltaCrossTrack": DotOrbitDeltaCrossTrack,
                    }
            elif data1[1] == "CLOCK":
                year = int(data1[2])
                month = int(data1[3])
                day = int(data1[4])
                hour = int(data1[5])
                minute = int(data1[6])
                second = int(float(data1[7]))
                toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
                if toc not in times:
                    times.append(toc)
                numberOfPRN = int(data1[9])
                for _ in range(numberOfPRN):
                    line = f.readline()
                    while "  " in line:
                        line = line.replace("  ", " ")
                    data2 = line.split(" ")
                    PRN = data2[0]
                    IOD = float(data2[1])
                    DeltaClockC0 = float(data2[2])
                    DeltaClockC1 = float(data2[3])
                    DeltaClockC2 = float(data2[4])
                    if cData.get(PRN, -1) == -1:
                        cData[PRN] = {}
                    cData[PRN][toc] = {
                        "IOD": IOD,
                        "DeltaClockC0": DeltaClockC0,
                        "DeltaClockC1": DeltaClockC1,
                        "DeltaClockC2": DeltaClockC2,
                    }
            elif data1[1] == "CODE_BIAS":
                ear = int(data1[2])
                month = int(data1[3])
                day = int(data1[4])
                hour = int(data1[5])
                minute = int(data1[6])
                second = int(float(data1[7]))
                toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
                numberOfPRN = int(data1[9])
                for _ in range(numberOfPRN):
                    line = f.readline()
                    while "  " in line:
                        line = line.replace("  ", " ")
                    data2 = line.split(" ")
                    PRN = data2[0]
                    if codeData.get(PRN, -1) == -1:
                        codeData[PRN] = {}
                    codeData[PRN][toc] = {}
                    numberOfCode = int(data2[1])
                    index = 2
                    for __ in range(numberOfCode):
                        codeData[data2[index]] = float(data2[index+1])
                        index += 2
            else:
                continue
    return cData, sData, times


def readNav(path, rnxData=None):
    if not rnxData:
        rnxData = dict()
    times = []
    with open(path, "r") as f:
        line = f.readline()
        while True:
            if "END OF HEADER" in line:
                break
            else:
                line = f.readline()
        while True:
            line = f.readline()
            if line == "":
                break
            PRN = formatSplit(line, 0, 3, type="string")
            if PRN.startswith("G") or PRN.startswith("C") or PRN.startswith(
                    "E"):
                year = formatSplit(line, 4, 4, type="int")
                month = formatSplit(line, 9, 2, type="int")
                day = formatSplit(line, 12, 2, type="int")
                hour = formatSplit(line, 15, 2, type="int")
                minute = formatSplit(line, 18, 2, type="int")
                second = formatSplit(line, 21, 2, type="int")
                af0 = formatSplit(line, 23, 19, type="float")
                af1 = formatSplit(line, 42, 19, type="float")
                af2 = formatSplit(line, 61, 19, type="float")
                line = f.readline()  #2
                IOD = formatSplit(line, 4, 19, type="float")
                Crs = formatSplit(line, 23, 19, type="float")
                deltan = formatSplit(line, 42, 19, type="float")
                M0 = formatSplit(line, 61, 19, type="float")
                line = f.readline()  #3
                Cuc = formatSplit(line, 4, 19, type="float")
                e = formatSplit(line, 23, 19, type="float")
                Cus = formatSplit(line, 42, 19, type="float")
                sqrtA = formatSplit(line, 61, 19, type="float")
                line = f.readline()  #4
                toe = formatSplit(line, 4, 19, type="float")
                Cic = formatSplit(line, 23, 19, type="float")
                omega0 = formatSplit(line, 42, 19, type="float")
                Cis = formatSplit(line, 61, 19, type="float")
                line = f.readline()  #5
                i0 = formatSplit(line, 4, 19, type="float")
                Crc = formatSplit(line, 23, 19, type="float")
                omega = formatSplit(line, 42, 19, type="float")
                omegaDot = formatSplit(line, 61, 19, type="float")
                line = f.readline()  #6
                IDOT = formatSplit(line, 4, 19, type="float")
                dataSource = formatSplit(line, 23, 19, type="int")
                line = f.readline()
                TGD = formatSplit(line, 42, 19, type="float")
                line = f.readline()
                if "C" in PRN:
                    toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second+14)
                elif "R" in PRN:
                    toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute,
                                            second=second + 18)
                else:
                    toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
                if "E" in PRN and (not (dataSource & 0b100000000)):
                    if dataSource == 0:
                        pass
                    else:
                        continue
                if toc not in times:
                    times.append(toc)
                if rnxData.get(PRN, -1) == -1:
                    rnxData[PRN] = {}
                rnxData[PRN][toc] = {
                    "af0": af0,
                    "af1": af1,
                    "af2": af2,
                    "IOD": IOD,
                    "Crs": Crs,
                    "deltan": deltan,
                    "M0": M0,
                    "Cuc": Cuc,
                    "e": e,
                    "Cus": Cus,
                    "sqrtA": sqrtA,
                    "toe": toe,
                    "Cic": Cic,
                    "omega0": omega0,
                    "Cis": Cis,
                    "i0": i0,
                    "Crc": Crc,
                    "omega": omega,
                    "omegaDot": omegaDot,
                    "IDOT": IDOT,
                    "TGD": TGD,
                }
            elif PRN.startswith("R") or PRN.startswith("S"):
                year = formatSplit(line, 4, 4, type="int")
                month = formatSplit(line, 9, 2, type="int")
                day = formatSplit(line, 12, 2, type="int")
                hour = formatSplit(line, 15, 2, type="int")
                minute = formatSplit(line, 18, 2, type="int")
                second = formatSplit(line, 21, 2, type="int")
                tau = formatSplit(line, 23, 19, type="float")
                gamma = formatSplit(line, 42, 19, type="float")
                af2 = formatSplit(line, 61, 19, type="float")
                line = f.readline()
                x = formatSplit(line, 4, 19, type="float")
                vx = formatSplit(line, 23, 19, type="float")
                ax = formatSplit(line, 42, 19, type="float")
                healthy = formatSplit(line, 61, 19, type="float")
                line = f.readline()
                y = formatSplit(line, 4, 19, type="float")
                vy = formatSplit(line, 23, 19, type="float")
                ay = formatSplit(line, 42, 19, type="float")
                frequency1 = formatSplit(line, 61, 19, type="float")
                line = f.readline()
                z = formatSplit(line, 4, 19, type="float")
                vz = formatSplit(line, 23, 19, type="float")
                az = formatSplit(line, 42, 19, type="float")
                frequency2 = formatSplit(line, 61, 19, type="float")
                toc = gnssTime.gnssTime(year=year, month=month, day=day, hour=hour, minute=minute, second=second) + timedelta(seconds=18)
                if toc not in times:
                    times.append(toc)
                if rnxData.get(PRN, -1) == -1:
                    rnxData[PRN] = {}
                rnxData[PRN][toc] = {
                    "tau":tau,
                    "gamma": gamma,
                    "af2": af2,
                    "x": x,
                    "y": y,
                    "z": z,
                    "vx": vx,
                    "vy": vy,
                    "vz": vz,
                    "ax": ax,
                    "ay": ay,
                    "az": az,
                    "frequency1": frequency1,
                    "frequency2": frequency2,
                    "healthy": healthy,
                }
    return rnxData, times


def readSp3_system(path,ignore=[]):
    # 这个函数里有双差的钟差
    sp3Data_G = {}
    sp3Data_E = {}
    sp3Data_R = {}
    sp3Data_C = {}
    sp3Data_G["sum"] = {}
    sp3Data_E["sum"] = {}
    sp3Data_R["sum"] = {}
    sp3Data_C["sum"] = {}
    clkG, clkE, clkR, clkC, sumG, sumE, sumR, sumC = 0, 0, 0, 0, 0, 0, 0, 0
    year, month, day, hour, minute, second, sod = -1, -1, -1, -1, -1, -1, -1,
    with open(path, "r") as file:
        line = file.readline()
        while not line.startswith("*"):
            line = file.readline()
        while line != "" and ("EOF" not in line):
            while "  " in line:
                line = line.replace("  ", " ")
            data = line.split(" ")
            if data[0] == "*":
                if year != -1:
                    if clkG != 0:
                        sp3Data_G["sum"][date] = [-1, -1, -1, sumG / clkG, sod]
                    else:
                        sp3Data_G["sum"][date] = [-1, -1, -1, -1, sod]
                    if clkE != 0:
                        sp3Data_E["sum"][date] = [-1, -1, -1, sumE / clkE, sod]
                    else:
                        sp3Data_E["sum"][date] = [-1, -1, -1, -1, sod]
                    if clkR != 0:
                        sp3Data_R["sum"][date] = [-1, -1, -1, sumR / clkR, sod]
                    else:
                        sp3Data_R["sum"][date] = [-1, -1, -1, -1, sod]
                    if clkC != 0:
                        sp3Data_C["sum"][date] = [-1, -1, -1, sumC / clkC, sod]
                    else:
                        sp3Data_C["sum"][date] = [-1, -1, -1, -1, sod]
                    clkG, clkE, clkR, clkC, sumG, sumE, sumR, sumC = 0, 0, 0, 0, 0, 0, 0, 0
                year = int(data[1])
                month = int(data[2])
                day = int(data[3])
                hour = int(data[4])
                minute = int(data[5])
                second = float(data[6])
                sod = (hour * 60 + minute) * 60 + second  # 计算天内秒
                date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))
            else:
                prn = data[0][1:]
                if prn in ignore:
                    line = file.readline()
                    continue
                if data[4] == "999999.999999":
                    line = file.readline()
                    continue
                x = float(data[1])
                y = float(data[2])
                z = float(data[3])
                clk = float(data[4]) * pow(10, 3)
                if prn[0] == "G":
                    if sp3Data_G.get(prn, -1) == -1:
                        sp3Data_G[prn] = {}
                    sp3Data_G[prn][date] = [x, y, z, clk, sod]  # sod用来画图
                    sumG += clk
                    clkG += 1
                elif prn[0] == "E":
                    if sp3Data_E.get(prn, -1) == -1:
                        sp3Data_E[prn] = {}
                    sp3Data_E[prn][date] = [x, y, z, clk, sod]  # sod用来画图
                    sumE += clk
                    clkE += 1
                elif prn[0] == "R":
                    if sp3Data_R.get(prn, -1) == -1:
                        sp3Data_R[prn] = {}
                    sp3Data_R[prn][date] = [x, y, z, clk, sod]  # sod用来画图
                    sumR += clk
                    clkR += 1
                elif prn[0] == "C":
                    if sp3Data_C.get(prn, -1) == -1:
                        sp3Data_C[prn] = {}
                    sp3Data_C[prn][date] = [x, y, z, clk, sod]  # sod用来画图
                    sumC += clk
                    clkC += 1
            line = file.readline()
    if clkG != 0:
        sp3Data_G["sum"][date] = [-1, -1, -1, sumG / clkG, sod]
    else:
        sp3Data_G["sum"][date] = [-1, -1, -1, -1, sod]
    if clkE != 0:
        sp3Data_E["sum"][date] = [-1, -1, -1, sumE / clkE, sod]
    else:
        sp3Data_E["sum"][date] = [-1, -1, -1, -1, sod]
    if clkR != 0:
        sp3Data_R["sum"][date] = [-1, -1, -1, sumR / clkR, sod]
    else:
        sp3Data_R["sum"][date] = [-1, -1, -1, -1, sod]
    if clkC != 0:
        sp3Data_C["sum"][date] = [-1, -1, -1, sumC / clkC, sod]
    else:
        sp3Data_C["sum"][date] = [-1, -1, -1, -1, sod]
    return sp3Data_G, sp3Data_E, sp3Data_R, sp3Data_C

def readSp3(path):
    sp3Data = {}
    year, month, day, hour, minute, second, sod = -1, -1, -1, -1, -1, -1, -1,
    with open(path, "r") as file:
        line = file.readline()
        while not line.startswith("*"):
            line = file.readline()
        while line != "" and ("EOF" not in line):
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
                sod = (hour * 60 + minute) * 60 + second  #计算天内秒
                date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))
            else:
                prn = data[0][1:]
                x = float(data[1])
                y = float(data[2])
                z = float(data[3])
                clk = float(data[4]) * pow(10, 3)
                if clk >= 999999.999999 * pow(10, 3):
                    line = file.readline()
                    continue
                if sp3Data.get(prn, -1) == -1:
                    sp3Data[prn] = {}
                sp3Data[prn][date] = [x, y, z, clk, sod]  #sod用来画图
            line = file.readline()
    return sp3Data

def readATX(path):
    sattileList = {}
    with open(path,"r") as file:
        line = file.readline()
        while "END OF HEADER" not in line:
            line = file.readline()
        line = file.readline()
        prn = None
        validFROM = datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
        validUNTIL = datetime(year=9999, month=1, day=1, hour=0, minute=0, second=0)
        frequencyData = {}
        frequency = None
        while True:
            if not line:
                break
            if "START OF ANTENNA" in line:
                prn = None
                validFROM = datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
                validUNTIL = datetime(year=9999, month=1, day=1, hour=0, minute=0, second=0)
                frequencyData = {}
                frequency = None
            elif "VALID FROM" in line:
                year = formatSplit(line, 2, 4, type="int")
                month = formatSplit(line, 10, 2, type="int")
                day = formatSplit(line, 16, 2, type="int")
                hour = formatSplit(line, 22, 2, type="int")
                minute = formatSplit(line, 28, 2, type="int")
                second = formatSplit(line, 33, 2, type="float")
                validFROM = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))
            elif "VALID UNTIL" in line:
                year = formatSplit(line, 2, 4, type="int")
                month = formatSplit(line, 10, 2, type="int")
                day = formatSplit(line, 16, 2, type="int")
                hour = formatSplit(line, 22, 2, type="int")
                minute = formatSplit(line, 28, 2, type="int")
                second = formatSplit(line, 33, 2, type="float")
                validUNTIL = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))
            elif "START OF FREQUENCY" in line:
                frequency = formatSplit(line, 3, 3, type="string")
            elif "TYPE / SERIAL NO" in line:
                prn = formatSplit(line, 20, 3, type="string")
            elif "NORTH / EAST / UP" in line:
                n = formatSplit(line, 0, 10, type="float") / 1000
                e = formatSplit(line, 10, 10, type="float") / 1000
                u = formatSplit(line, 20, 10, type="float") / 1000
                frequencyData[frequency] = [n, e, u]
            elif "END OF ANTENNA" in line:
                if sattileList.get(prn,-1) == -1:
                    sattileList[prn] = []
                data = {
                    "validFROM": validFROM,
                    "validUNTIL": validUNTIL,
                    "frequencyData": frequencyData
                }
                sattileList[prn].append(data)
            line = file.readline()
    return sattileList

def writeSp3(path ,lines, outTime, satellites, epoch):
    sp3Headr = getSp3Header(satellites, outTime, epoch)
    with open(path,"w") as f:
        for line in sp3Headr:
            f.write(line)
        for line in lines:
            f.write(line)

def writeClk(path ,lines, mintime):
    clkHeader = getClkHeader(mintime)
    with open(path, "w") as f:
        for line in clkHeader:
            f.write(line)
        for line in lines:
            f.write(line)

def readSp3ALL(sp3PathList):
    sp3Data = {}
    for sp3path in sp3PathList:
        if not sp3path.endswith(".sp3"):
            continue
        with open(sp3path, "r") as f:
            print(sp3path)
            line = f.readline()
            while line and ("EOF" not in line):
                while not line.startswith("*"):
                    line = f.readline()
                while line != "" and ("EOF" not in line):
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
                        sod = (hour * 60 + minute) * 60 + second  # 计算天内秒
                        date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))
                    else:
                        prn = data[0][1:]
                        x = float(data[1])
                        y = float(data[2])
                        z = float(data[3])
                        clk = float(data[4]) * pow(10, 3)
                        if sp3Data.get(prn, -1) == -1:
                            sp3Data[prn] = {}
                        sp3Data[prn][date] = [x, y, z, clk, sod]  # sod用来画图
                    line = f.readline()
    return sp3Data