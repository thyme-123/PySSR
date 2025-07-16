import datetime
import os
from datetime import timedelta

import numpy as np
from PySide6.QtCore import QThread

from gnssBase.gnssTime import *
from gnssBase.gnssSSR import *
from gnssBase.gnssRT import *
from gnssBase.gnssIO import *
from ntrip.ntrip import *


class ssrThread(QThread):

    def __init__(self, mount, url, port, username, password, parent=None):
        super().__init__(parent)
        self.mount = mount
        self.url = url
        self.port = port
        self.username = username if username else None
        self.password = password if password else None
        self.ntripStream = NtripStream(parent, url=url, mount=mount, port=port, userName=username, passWord=password)
        self.isRun = False
        return

    def run(self):
        iterate = self.ntripStream.run()
        self.isRun = True
        print("ssr Start")
        while self.isRun:
            data, message = next(iterate)
            sData, cData = ssrDecode(data, message)
            self.parent().upDataSSR(sData, cData)
        print("ssr end")
        self.ntripStream.stop()
        return

    def stop(self):
        self.isRun = False


class ephThread(QThread):

    def __init__(self, mount, url, port, username, password, parent=None):
        super().__init__(parent)
        self.mount = mount
        self.url = url
        self.port = port
        self.username = username if username else None
        self.password = password if password else None
        self.ntripStream = NtripStream(parent, url=url, mount=mount, port=port, userName=username, passWord=password)
        self.isRun = False

    def run(self):
        iterate = self.ntripStream.run()
        self.isRun = True
        while self.isRun:
            data, message = next(iterate)
            ephData = ephDecode(data)
            self.parent().upDataEPH(ephData)
        self.ntripStream.stop()
        return

    def stop(self):
        self.isRun = False


class rtRepairThread(QThread):

    def __init__(self, outPath, parent=None):
        super().__init__(parent)
        self.isRun = False
        self.outPath = outPath
        return

    def run(self):
        self.isRun = True
        mount = self.parent().mountSSR
        while self.isRun:
            nowUT = getUTDay()
            week, day = time2WeekDay(nowUT)
            day_week = week
            day_day = day
            fClkPath = os.path.join(self.outPath, "kus{}{}.clk".format(week, day))
            fSp3Path = os.path.join(self.outPath, "kus{}{}.sp3".format(week, day))
            fSsrPath = os.path.join(self.outPath, "kus{}{}.ssr".format(week, day))
            with open(fClkPath, "w") as fClk:
                with open(fSp3Path, "w") as fSp3:
                    with open(fSsrPath, "w") as fSsr:
                        # fClk = open(fClkPath, "w")
                        # fSp3 = open(fSp3Path, "w")
                        wirteRtClkHeader(fClk, nowUT)
                        writeRtSp3Header(fSp3, nowUT)
                        fSp3.flush()
                        os.fsync(fSp3.fileno())
                        fClk.flush()
                        os.fsync(fClk.fileno())
                        print("write header")
                        while self.isRun:
                            sData = self.parent().ssrData_S
                            cData = self.parent().ssrData_C
                            rnxData = self.parent().ephData
                            nowUT = getUTDay()
                            startTime = nowUT
                            lines_sp3 = []
                            lines_clk = []
                            lines_ssrS = []
                            lines_ssrC = []
                            while startTime.second % 5 != 0:
                                startTime -= timedelta(seconds=1)
                            lines_sp3.append("*  {year:4} {month:2} {day:2} {hour:2} {minute:2} {second:>11}\n".format(
                                year=startTime.year,
                                month=startTime.month,
                                day=startTime.day,
                                hour=startTime.hour,
                                minute=startTime.minute,
                                second="{:.8f}".format(startTime.second),
                            ))
                            # print(sorted(list(rnxData.keys())))
                            # print(rnxData)
                            # print(sData.keys())
                            # print(cData.keys())
                            for satellite in sorted(list(rnxData.keys())):
                                timeDifftoc = 0
                                if satellite.startswith("C"):
                                    pass
                                if satellite.startswith("E"):
                                    timeDifftoc = 60 * 60 * 6
                                else:
                                    timeDifftoc = 60 * 60 * 6
                                # keys = sorted(list(rnxData[satellite].keys()))
                                # for index in range(len(keys)):
                                #     if keys[index] >= startTime:
                                #         break
                                # toc = keys[index]
                                toc = None
                                if satellite not in sData:
                                    continue
                                if (not satellite.startswith("C")) and (not satellite.startswith("R")):
                                    toc = selctToc_rt(sData[satellite], rnxData[satellite], startTime, satellite)
                                elif satellite.startswith("C"):
                                    toc = selctToc_BDS_rt(sData[satellite], rnxData[satellite], startTime)
                                elif satellite.startswith("R"):
                                    toc = selctToc_GLO_rt(sData[satellite], rnxData[satellite], startTime)
                                if not toc:
                                    self.parent().updataErrorSatellite(satellite)
                                    continue
                                if abs(timeSub(startTime, toc)) > timeDifftoc:
                                    continue
                                data = rnxData[satellite][toc]
                                if satellite.startswith("C"):
                                    X, Y, Z, clk, Vx, Vy, Vz = DBSPosition(data, startTime, toc, prn=satellite)
                                elif satellite.startswith("R"):
                                    X, Y, Z, clk, Vx, Vy, Vz = glonassPosition(data, startTime, toc)
                                else:
                                    X, Y, Z, clk, Vx, Vy, Vz = GPSPosition(data, startTime, toc, prn=satellite)
                                if satellite not in cData:
                                    continue
                                if satellite.startswith("C"):
                                    cdataTime = selectIOD_BDS_rt(cData[satellite], startTime, toc)
                                elif satellite.startswith("R"):
                                    cdataTime = selectIOD_GLO_rt(cData[satellite], startTime, toc)
                                else:
                                    cdataTime = selectIOD_rt(cData[satellite], startTime, data["IOD"])
                                if not cdataTime:
                                    continue
                                cdata = cData[satellite][cdataTime]
                                tsv2 = timeSub(startTime, cdataTime)
                                clk_repair = clk + (
                                            (cdata["DeltaClockC0"] + cdata["DeltaClockC1"] / 1000 * tsv2 + cdata[
                                                "DeltaClockC2"] / 1000 * pow(
                                                tsv2, 2)) / c)
                                lines_ssrC.append(
                                    "{prn:3} {iod:>11} {DeltaClockC0:>10} {DeltaClockC1:>10} {DeltaClockC2:>10}\n".format(
                                        prn=satellite,
                                        iod=cdata["IOD"],
                                        DeltaClockC0="{:.4f}".format(cdata["DeltaClockC0"]),
                                        DeltaClockC1="{:.4f}".format(cdata["DeltaClockC1"]),
                                        DeltaClockC2="{:.4f}".format(cdata["DeltaClockC2"]),
                                    )
                                )
                                if satellite not in sData:
                                    continue
                                if satellite.startswith("C"):
                                    sdataTime = selectIOD_BDS_rt(sData[satellite], startTime, toc)
                                elif satellite.startswith("R"):
                                    sdataTime = selectIOD_GLO_rt(sData[satellite], startTime, toc)
                                else:
                                    sdataTime = selectIOD_rt(sData[satellite], startTime, data["IOD"])
                                if not sdataTime:
                                    continue
                                sdata = sData[satellite][sdataTime]
                                lines_ssrS.append(
                                    "{prn:3} {iod:>11} {DeltaOrbitRadial:>10} {DeltaOrbitAlongTrack:>10} {DeltaOrbitCrossTrack:>10}    {DotOrbitDeltaRadial:>10} {DotOrbitDeltaAlongTrack:>10} {DotOrbitDeltaCrossTrack:>10}\n".format(
                                        prn=satellite,
                                        iod=sdata["IOD"],
                                        DeltaOrbitRadial="{:.4f}".format(sdata["DeltaOrbitRadial"]),
                                        DeltaOrbitAlongTrack="{:.4f}".format(sdata["DeltaOrbitAlongTrack"]),
                                        DeltaOrbitCrossTrack="{:.4f}".format(sdata["DeltaOrbitCrossTrack"]),
                                        DotOrbitDeltaRadial="{:.4f}".format(sdata["DotOrbitDeltaRadial"]),
                                        DotOrbitDeltaAlongTrack="{:.4f}".format(sdata["DotOrbitDeltaAlongTrack"]),
                                        DotOrbitDeltaCrossTrack="{:.4f}".format(sdata["DotOrbitDeltaCrossTrack"]),
                                    ))
                                tsv = timeSub(startTime, sdataTime)
                                DeltaOrbitRadial = sdata["DeltaOrbitRadial"]
                                DeltaOrbitAlongTrack = sdata["DeltaOrbitAlongTrack"]
                                DeltaOrbitCrossTrack = sdata["DeltaOrbitCrossTrack"]
                                DotOrbitDeltaRadial = sdata["DotOrbitDeltaRadial"] / 1000
                                DotOrbitDeltaAlongTrack = sdata["DotOrbitDeltaAlongTrack"] / 1000
                                DotOrbitDeltaCrossTrack = sdata["DotOrbitDeltaCrossTrack"] / 1000
                                DeltaO = np.array(
                                    [[DeltaOrbitRadial], [DeltaOrbitAlongTrack], [DeltaOrbitCrossTrack]]) + np.array(
                                    [[DotOrbitDeltaRadial], [DotOrbitDeltaAlongTrack], [DotOrbitDeltaCrossTrack]]) * tsv
                                rX = np.array([[X], [Y], [Z]])
                                rDot = np.array([[Vx], [Vy], [Vz]])
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
                                if np.nan in  X_reapir:
                                    continue
                                lines_sp3.append("P{PRN:3} {X:>13} {Y:>13} {Z:>13} {clk:>13}\n".format(PRN=satellite,
                                                                                                       X="{:.6f}".format(
                                                                                                           X_reapir[0][
                                                                                                               0] / 1000),
                                                                                                       Y="{:.6f}".format(
                                                                                                           X_reapir[1][
                                                                                                               0] / 1000),
                                                                                                       Z="{:.6f}".format(
                                                                                                           X_reapir[2][
                                                                                                               0] / 1000),
                                                                                                       clk="{:.6f}".format(
                                                                                                           clk_repair * pow(
                                                                                                               10, 6))))
                                lines_clk.append(
                                    "AS {PRN:3}  {year:>4} {month:>2} {day:>2} {hour:>2} {minute:>2} {second:>9}  1   {clk:>19}\n".format(
                                        PRN=satellite,
                                        year=startTime.year,
                                        month=startTime.month,
                                        day=startTime.day,
                                        hour=startTime.hour,
                                        minute=startTime.minute,
                                        second="{:.6f}".format(startTime.second),
                                        clk="{:.12e}".format(clk_repair)))
                            fSsr.write(
                                "> ORBIT {year:4} {month:0>2} {day:0>2} {hour:0>2} {minute:0>2} {second:0>4} 2 {numberOfSsr} {mount}\n".format(
                                    year=startTime.year,
                                    month=startTime.month,
                                    day=startTime.day,
                                    hour=startTime.hour,
                                    minute=startTime.minute,
                                    second="{:.1f}".format(startTime.second),
                                    numberOfSsr=len(lines_ssrS),
                                    mount=mount,
                                ))
                            for line_ssrS in lines_ssrS:
                                fSsr.write(line_ssrS)
                            fSsr.write(
                                "> CLOCK {year:4} {month:0>2} {day:0>2} {hour:0>2} {minute:0>2} {second:0>4} 2 {numberOfSsr} {mount}\n".format(
                                    year=startTime.year,
                                    month=startTime.month,
                                    day=startTime.day,
                                    hour=startTime.hour,
                                    minute=startTime.minute,
                                    second="{:.1f}".format(startTime.second),
                                    numberOfSsr=len(lines_ssrC),
                                    mount=mount,
                                ))
                            for line_ssrC in lines_ssrC:
                                fSsr.write(line_ssrC)
                            fSsr.flush()
                            os.fsync(fSsr.fileno())
                            for sp3line in lines_sp3:
                                fSp3.write(sp3line)
                            fSp3.flush()
                            os.fsync(fSp3.fileno())
                            for clkline in lines_clk:
                                fClk.write(clkline)
                            fClk.flush()
                            os.fsync(fClk.fileno())
                            week, day = time2WeekDay(startTime)
                            if week != day_week or day != day_day:
                                break
                            QThread.sleep(5)
        return

    def stop(self):
        self.isRun = False


class RTThread(QThread):

    def __init__(self, mountEPH, mountSSR, url, port, username, password, outPath, parent=None):
        super().__init__(parent)
        self.mountSSR = mountSSR
        self.outPath = outPath
        self.ephData = {}
        self.ssrData_S = {}
        self.ssrData_C = {}
        self.errorSatellite = []
        self.ephThread = ephThread(mountEPH, url, port, username, password, self)
        self.ssrThread = ssrThread(mountSSR, url, port, username, password, self)
        self.repairThread = rtRepairThread(outPath, self)
        self.ephT = None
        self.ephF = None
        print("init")
        return

    def updataErrorSatellite(self, satellite):
        self.errorSatellite.append(satellite)

    def run(self):
        print(1)
        self.ephThread.start()
        print(2)
        self.ssrThread.start()
        print(3)
        self.repairThread.start()
        return

    def stop(self):
        self.repairThread.stop()
        self.ephThread.stop()
        self.ssrThread.stop()

    def upDataEPH(self, ephData):
        if not ephData:
            return
        prn = list(ephData.keys())[0]
        tocNew = list(ephData[prn].keys())[0]
        if self.ephData.get(prn, -1) == -1:
            self.ephData[prn] = {}
        print(tocNew, prn, self.ephData[prn].get(tocNew, -1),self.ephData[prn])
        tocDelList = []
        for toc in self.ephData[prn]:
            if abs(timeDiff(toc, tocNew)) > 4 * 60 * 60:
                tocDelList.append(toc)
        for toc in tocDelList:
            del (self.ephData[prn][toc])
        if (self.ephData[prn].get(tocNew, -1) == -1 and (prn[0] == "G" or prn[0] == "E")) or (self.ephData[prn].get(tocNew + timedelta(seconds=14), -1) == -1 and prn[0] == "C") or (self.ephData[prn].get(tocNew + timedelta(seconds=18), -1) == -1 and prn[0] == "R") or (prn in self.errorSatellite):
            if prn in self.errorSatellite:
                self.errorSatellite.remove(prn)
            if prn[0] == "C":
                self.ephData[prn][tocNew + timedelta(seconds=14)] = ephData[prn][tocNew].copy()
            elif prn[0] == "R":
                self.ephData[prn][tocNew + timedelta(seconds=18)] = ephData[prn][tocNew].copy()
            else:
                self.ephData[prn][tocNew] = ephData[prn][tocNew].copy()
        # if (self.ephData[prn].get(tocNew, -1) == -1 and (prn[0] == "G" or prn[0] == "E")) or (
        #         self.ephData[prn].get(tocNew + timedelta(seconds=14), -1) == -1 and prn[0] == "C") or (
        #         self.ephData[prn].get(tocNew + timedelta(seconds=18), -1) == -1 and prn[0] == "R") or (
        #         prn in self.errorSatellite):
            if self.ephT == None or getTimetamp(self.ephT) < getTimetamp(getDay(tocNew)):
                self.ephT = getDay(tocNew)
                week, day = time2WeekDay(tocNew)
                self.ephF = open(os.path.join(self.outPath, "kus{}{}.{}p".format(week, day, tocNew.year % 100)), "w")
                self.ephF.write("     3.05           N: GNSS NAV DATA    M: Mixed            RINEX VERSION / TYPE\n")
                self.ephF.write(
                    "                                        {year:4}{month:0>2}{day:0>2} {hour:0>2}{minute:0>2}{second:0>2} UTC PGM / RUN BY / DATE\n".format(
                        year=tocNew.year,
                        month=tocNew.month,
                        day=tocNew.day,
                        hour=tocNew.hour,
                        minute=tocNew.minute,
                        second=int(tocNew.second),
                    ))
                self.ephF.write("                                                            END OF HEADER\n")
            if prn.startswith("R"):
                self.ephF.write(
                    "{prn:3} {year:4} {month:0>2} {day:0>2} {hour:0>2} {minute:0>2} {second:0>2}{af0:>19}{af1:>19}{af2:>19}\n".format(
                        prn=prn,
                        year=tocNew.year,
                        month=tocNew.month,
                        day=tocNew.day,
                        hour=tocNew.hour,
                        minute=tocNew.minute,
                        second=int(tocNew.second),
                        af0="{:.12e}".format(ephData[prn][tocNew]["tau"]),
                        af1="{:.12e}".format(ephData[prn][tocNew]["gamma"]),
                        af2="{:.12e}".format(ephData[prn][tocNew]["af2"]),
                    ))
                self.ephF.write(
                    "    {x:>19}{vx:>19}{ax:>19}{health:>19}\n".format(
                        x="{:.12e}".format(ephData[prn][tocNew]["x"]),
                        vx="{:.12e}".format(ephData[prn][tocNew]["vx"]),
                        ax="{:.12e}".format(ephData[prn][tocNew]["ax"]),
                        health="{:.12e}".format(ephData[prn][tocNew]["healthy"]),

                    ))
                self.ephF.write(
                    "    {y:>19}{vy:>19}{ay:>19}{f1:>19}\n".format(
                        y="{:.12e}".format(ephData[prn][tocNew]["y"]),
                        vy="{:.12e}".format(ephData[prn][tocNew]["vy"]),
                        ay="{:.12e}".format(ephData[prn][tocNew]["ay"]),
                        f1="{:.12e}".format(ephData[prn][tocNew]["frequency1"]),
                    ))
                self.ephF.write(
                    "    {z:>19}{vz:>19}{az:>19}{f2:>19}\n".format(
                        z="{:.12e}".format(ephData[prn][tocNew]["z"]),
                        vz="{:.12e}".format(ephData[prn][tocNew]["vz"]),
                        az="{:.12e}".format(ephData[prn][tocNew]["az"]),
                        f2="{:.12e}".format(ephData[prn][tocNew]["frequency2"]),
                    ))
            else:
                self.ephF.write(
                    "{prn:3} {year:4} {month:0>2} {day:0>2} {hour:0>2} {minute:0>2} {second:0>2}{af0:>19}{af1:>19}{af2:>19}\n".format(
                        prn=prn,
                        year=tocNew.year,
                        month=tocNew.month,
                        day=tocNew.day,
                        hour=tocNew.hour,
                        minute=tocNew.minute,
                        second=int(tocNew.second),
                        af0="{:.12e}".format(ephData[prn][tocNew]["af0"]),
                        af1="{:.12e}".format(ephData[prn][tocNew]["af1"]),
                        af2="{:.12e}".format(ephData[prn][tocNew]["af2"]),
                    ))
                self.ephF.write(
                    "    {IOD:>19}{Crs:>19}{deltan:>19}{M0:>19}\n".format(
                        IOD="{:.12e}".format(ephData[prn][tocNew]["IOD"]),
                        Crs="{:.12e}".format(ephData[prn][tocNew]["Crs"]),
                        deltan="{:.12e}".format(ephData[prn][tocNew]["deltan"]),
                        M0="{:.12e}".format(ephData[prn][tocNew]["M0"]),
                    ))
                self.ephF.write(
                    "    {Cuc:>19}{e:>19}{Cus:>19}{sqrtA:>19}\n".format(
                        Cuc="{:.12e}".format(ephData[prn][tocNew]["Cuc"]),
                        e="{:.12e}".format(ephData[prn][tocNew]["e"]),
                        Cus="{:.12e}".format(ephData[prn][tocNew]["Cus"]),
                        sqrtA="{:.12e}".format(ephData[prn][tocNew]["sqrtA"]),
                    ))
                self.ephF.write(
                    "    {toe:>19}{Cic:>19}{omega0:>19}{Cis:>19}\n".format(
                        toe="{:.12e}".format(ephData[prn][tocNew]["toe"]),
                        Cic="{:.12e}".format(ephData[prn][tocNew]["Cic"]),
                        omega0="{:.12e}".format(ephData[prn][tocNew]["omega0"]),
                        Cis="{:.12e}".format(ephData[prn][tocNew]["Cis"]),
                    ))
                self.ephF.write(
                    "    {i0:>19}{Crc:>19}{omega:>19}{omegaDot:>19}\n".format(
                        i0="{:.12e}".format(ephData[prn][tocNew]["i0"]),
                        Crc="{:.12e}".format(ephData[prn][tocNew]["Crc"]),
                        omega="{:.12e}".format(ephData[prn][tocNew]["omega"]),
                        omegaDot="{:.12e}".format(ephData[prn][tocNew]["omegaDot"]),
                    ))
                self.ephF.write(
                    "    {IDOT:>19}{a:>19}{b:>19}{c:>19}\n".format(
                        IDOT="{:.12e}".format(ephData[prn][tocNew]["IDOT"]),
                        a="{:.12e}".format(0),
                        b="{:.12e}".format(0),
                        c="{:.12e}".format(0),
                    ))
                self.ephF.write(
                    "    {a:>19}{b:>19}{TGD:>19}{c:>19}\n".format(
                        a="{:.12e}".format(0),
                        b="{:.12e}".format(0),
                        TGD="{:.12e}".format(ephData[prn][tocNew]["TGD"]),
                        c="{:.12e}".format(0),
                    ))
                self.ephF.write(
                    "    {a:>19}{b:>19}\n".format(
                        a="{:.12e}".format(0),
                        b="{:.12e}".format(0),
                    ))
            self.ephF.flush()
            os.fsync(self.ephF.fileno())
        #
        # if prn in self.errorSatellite:
        #     self.errorSatellite.remove(prn)
        # if prn[0] == "C":
        #     self.ephData[prn][tocNew + timedelta(seconds=14)] = ephData[prn][tocNew].copy()
        # elif prn[0] == "R":
        #     self.ephData[prn][tocNew + timedelta(seconds=18)] = ephData[prn][tocNew].copy()
        # else:
        #     self.ephData[prn][tocNew] = ephData[prn][tocNew].copy()


    def upDataSSR(self, sData, cData):
        if not sData:
            return
        prnList = list(sData.keys())
        for prn in prnList:
            tocNew = list(sData[prn].keys())[0]
            if self.ssrData_S.get(prn, -1) == -1:
                self.ssrData_S[prn] = {}
            tocDelList = []
            for toc in self.ssrData_S[prn]:
                if abs(timeDiff(toc, tocNew)) > 20:
                    tocDelList.append(toc)
            for toc in tocDelList:
                del (self.ssrData_S[prn][toc])
            self.ssrData_S[prn][tocNew] = sData[prn][tocNew].copy()
        if not cData:
            return
        prnList = list(cData.keys())
        for prn in prnList:
            tocNew = list(cData[prn].keys())[0]
            if self.ssrData_C.get(prn, -1) == -1:
                self.ssrData_C[prn] = {}
            tocDelList = []
            for toc in self.ssrData_C[prn]:
                if abs(timeDiff(toc, tocNew)) > 15:
                    tocDelList.append(toc)
            for toc in tocDelList:
                del (self.ssrData_C[prn][toc])
            self.ssrData_C[prn][tocNew] = cData[prn][tocNew].copy()
