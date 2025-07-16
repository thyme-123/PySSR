import math
import struct

import pyrtcm

from gnssBase.gnssTime import *
from gnssBase.gnssSSR import *


def readBin(binary, length, start, type="int"):
    start_Byte = start[0]
    start_Bit = start[1]
    bitLength = start_Bit + length
    end_Byte = start_Byte + math.floor(bitLength / 8)
    end_Bit = bitLength % 8
    binary_data = binary[start_Byte: end_Byte + math.ceil(end_Bit / 8)]
    if end_Bit == 0:
        binary_data += b"\x00"
    mask = (1 << length) - 1
    data = (int.from_bytes(binary_data, byteorder='big', signed=False) >> (8 - end_Bit)) & mask
    start[0] = end_Byte
    start[1] = end_Bit
    if type == "int":
        singed = data >> (length - 1)  # 解析符号位
        mask_int = (1 << (length - 1)) - 1  # 获取数据位
        if singed == 1:
            return -1 * (((data & mask_int) ^ mask_int) + 1)  # 数据位转反码(data & mask_int),按位取反(data & mask_int) ^ mask_int),加一
        else:
            return data
    elif type == "uint":
        return data
    elif type == "sint":
        singed = data >> (length - 1)
        mask_int = (1 << (length - 1)) - 1
        return pow(-1, singed) * (data & mask_int)
    elif type == "bin":
        return data.to_bytes(length=math.ceil(length / 8), byteorder='big', signed=False)
    elif type == "float":
        b_data = data.to_bytes(length=math.ceil(length / 8), byteorder='big', signed=False)
        return struct.unpack('!f', b_data)[0]


def ephDecode(rtcmData=None, message=None):
    navData = {}
    if rtcmData.identity == "1019":
        prn = "G" + "{:0>2}".format(str(getattr(rtcmData, "DF009")))
        weekNumber = getattr(rtcmData, "DF076")
        SV = getattr(rtcmData, "DF077")
        code_L2 = getattr(rtcmData, "DF078")
        IODT = getattr(rtcmData, "DF079") * math.pi
        IODE = getattr(rtcmData, "DF071")
        toc = rtTime_gps2gpsTime(getattr(rtcmData, "DF081"))
        af2 = getattr(rtcmData, "DF082")
        af1 = getattr(rtcmData, "DF083")
        af0 = getattr(rtcmData, "DF084")
        IODC = getattr(rtcmData, "DF085")
        Crs = getattr(rtcmData, "DF086")
        Delta_n = getattr(rtcmData, "DF087") * math.pi
        M0 = getattr(rtcmData, "DF088") * math.pi
        Cuc = getattr(rtcmData, "DF089")
        e = getattr(rtcmData, "DF090")
        Cus = getattr(rtcmData, "DF091")
        sqrt_A = getattr(rtcmData, "DF092")
        toe = getattr(rtcmData, "DF093")
        Cic = getattr(rtcmData, "DF094")
        Omega0 = getattr(rtcmData, "DF095") * math.pi
        Cis = getattr(rtcmData, "DF096")
        i0 = getattr(rtcmData, "DF097") * math.pi
        Crc = getattr(rtcmData, "DF098")
        omega = getattr(rtcmData, "DF099") * math.pi
        OMEGADOT = getattr(rtcmData, "DF100") * math.pi
        t_GD = getattr(rtcmData, "DF101")
        SV_health = getattr(rtcmData, "DF102")
        L2_P_data_flag = getattr(rtcmData, "DF103")
        navData[prn] = {}
        navData[prn][toc] = {
            "af0": af0,
            "af1": af1,
            "af2": af2,
            "IOD": IODE,
            "Crs": Crs,
            "deltan": Delta_n,
            "M0": M0,
            "Cuc": Cuc,
            "e": e,
            "Cus": Cus,
            "sqrtA": sqrt_A,
            "toe": toe,
            "Cic": Cic,
            "omega0": Omega0,
            "Cis": Cis,
            "i0": i0,
            "Crc": Crc,
            "omega": omega,
            "omegaDot": OMEGADOT,
            "IDOT": IODT,
            "TGD": t_GD,
        }
    elif rtcmData.identity == "1020":
        prn = "R" + "{:0>2}".format(str(getattr(rtcmData, "DF038")))
        GLONASS_Frequency_Channel = getattr(rtcmData, "DF040")
        GLONASS_Almanac_Health = getattr(rtcmData, "DF104")
        GLONASS_almanac_health_availability = getattr(rtcmData, "DF105")
        GLONASS_P1 = getattr(rtcmData, "DF106")
        GLONASS_t0_bits = getattr(rtcmData, "DF107")
        GLONASS_MSb_B1 = getattr(rtcmData, "DF108")
        GLONASS_P2 = getattr(rtcmData, "DF109")
        GLONASS_t0_uint7 = getattr(rtcmData, "DF110")
        glotoc = rtTime_glo2gpsTime(GLONASS_t0_uint7 * 15)
        GLONASS_x0_first_derivative = getattr(rtcmData, "DF111")
        GLONASS_x0 = getattr(rtcmData, "DF112")
        GLONASS_x0_second_derivative = getattr(rtcmData, "DF113")
        GLONASS_y0_first_derivative = getattr(rtcmData, "DF114")
        GLONASS_y0 = getattr(rtcmData, "DF115")
        GLONASS_y0_second_derivative = getattr(rtcmData, "DF116")
        GLONASS_z0_first_derivative = getattr(rtcmData, "DF117")
        GLONASS_z0 = getattr(rtcmData, "DF118")
        GLONASS_z0_second_derivative = getattr(rtcmData, "DF119")
        GLONASS_P3 = getattr(rtcmData, "DF120")
        GLONASS_gamma0 = getattr(rtcmData, "DF121") * pow(2, -40)
        GLONASS_M_P = getattr(rtcmData, "DF122")
        GLONASS_M_l0_third_string = getattr(rtcmData, "DF123")
        GLONASS_tau0 = getattr(rtcmData, "DF124") * pow(2, -30) * -1
        GLONASS_M_Delta_tn = getattr(rtcmData, "DF125")
        GLONASS_En = getattr(rtcmData, "DF126")
        GLONASS_M_P4 = getattr(rtcmData, "DF127")
        GLONASS_M_FT = getattr(rtcmData, "DF128")
        GLONASS_M_NT = getattr(rtcmData, "DF129")
        GLONASS_M_M = getattr(rtcmData, "DF130")
        GLONASS_Additional_Data_Avail = getattr(rtcmData, "DF131")
        GLONASS_NA = getattr(rtcmData, "DF132")
        GLONASS_tau_c = getattr(rtcmData, "DF133")
        GLONASS_M_N4 = getattr(rtcmData, "DF134")
        GLONASS_M_tau_GPS = getattr(rtcmData, "DF135")
        GLONASS_M_In_fifth_string = getattr(rtcmData, "DF136")
        navData[prn] = {}
        navData[prn][glotoc] = {
            "tau": GLONASS_tau0,
            "gamma": GLONASS_gamma0,
            "af2": 0,
            "x": GLONASS_x0,
            "y": GLONASS_y0,
            "z": GLONASS_z0,
            "vx": GLONASS_x0_first_derivative,
            "vy": GLONASS_y0_first_derivative,
            "vz": GLONASS_z0_first_derivative,
            "ax": GLONASS_x0_second_derivative,
            "ay": GLONASS_y0_second_derivative,
            "az": GLONASS_z0_second_derivative,
            "frequency1": GLONASS_P1,
            "frequency2": GLONASS_P2,
            "healthy": GLONASS_Almanac_Health,
        }
    elif rtcmData.identity == "1045":
        prn = "E" + "{:0>2}".format(str(getattr(rtcmData, "DF252")))
        Galileo_Week_Number = getattr(rtcmData, "DF289")
        Galileo_IODnav = getattr(rtcmData, "DF290")
        Galileo_SV_SISA = getattr(rtcmData, "DF291")
        Galileo_IDOT = getattr(rtcmData, "DF292") * math.pi
        Galileo_toc = rtTime_gps2gpsTime(getattr(rtcmData, "DF293"))
        Galileo_af2 = getattr(rtcmData, "DF294")
        Galileo_af1 = getattr(rtcmData, "DF295")
        Galileo_af0 = getattr(rtcmData, "DF296")
        Galileo_Crs = getattr(rtcmData, "DF297")
        Galileo_Delta_n = getattr(rtcmData, "DF298") * math.pi
        Galileo_M0 = getattr(rtcmData, "DF299") * math.pi
        Galileo_Cuc = getattr(rtcmData, "DF300")
        Galileo_e = getattr(rtcmData, "DF301")
        Galileo_Cus = getattr(rtcmData, "DF302")
        Galileo_sqrt_A = getattr(rtcmData, "DF303")
        Galileo_toe = getattr(rtcmData, "DF304")
        Galileo_Cic = getattr(rtcmData, "DF305")
        Galileo_Omega0 = getattr(rtcmData, "DF306") * math.pi
        Galileo_Cis = getattr(rtcmData, "DF307")
        Galileo_i0 = getattr(rtcmData, "DF308") * math.pi
        Galileo_Crc = getattr(rtcmData, "DF309")
        Galileo_omega = getattr(rtcmData, "DF310") * math.pi
        Galileo_OMEGADOT = getattr(rtcmData, "DF311") * math.pi
        Galileo_BCD_EsdE1 = getattr(rtcmData, "DF312")
        Galileo_NAV_Signal_Health = getattr(rtcmData, "DF314")
        Galileo_NAV_Data_Validity = getattr(rtcmData, "DF315")
        navData[prn] = {}
        navData[prn][Galileo_toc] = {
            "af0": Galileo_af0,
            "af1": Galileo_af1,
            "af2": Galileo_af2,
            "IOD": Galileo_IODnav,
            "Crs": Galileo_Crs,
            "deltan": Galileo_Delta_n,
            "M0": Galileo_M0,
            "Cuc": Galileo_Cuc,
            "e": Galileo_e,
            "Cus": Galileo_Cus,
            "sqrtA": Galileo_sqrt_A,
            "toe": Galileo_toe,
            "Cic": Galileo_Cic,
            "omega0": Galileo_Omega0,
            "Cis": Galileo_Cis,
            "i0": Galileo_i0,
            "Crc": Galileo_Crc,
            "omega": Galileo_omega,
            "omegaDot": Galileo_OMEGADOT,
            "IDOT": Galileo_IDOT,
            "TGD": Galileo_BCD_EsdE1,
        }
    elif rtcmData.identity == "1046":
        prn = "E" + "{:0>2}".format(str(getattr(rtcmData, "DF252")))
        Galileo_week = getattr(rtcmData, "DF289")
        Galileo_iodnav = getattr(rtcmData, "DF290")
        Galileo_sisa = getattr(rtcmData, "DF286")
        Galileo_idot = getattr(rtcmData, "DF292") * math.pi
        Galileo_toc = rtTime_gps2gpsTime(getattr(rtcmData, "DF293"))
        Galileo_af2 = getattr(rtcmData, "DF294")
        Galileo_af1 = getattr(rtcmData, "DF295")
        Galileo_af0 = getattr(rtcmData, "DF296")
        Galileo_crs = getattr(rtcmData, "DF297")
        Galileo_delta_n = getattr(rtcmData, "DF298") * math.pi
        Galileo_m0 = getattr(rtcmData, "DF299") * math.pi
        Galileo_cuc = getattr(rtcmData, "DF300")
        Galileo_e = getattr(rtcmData, "DF301")
        Galileo_cus = getattr(rtcmData, "DF302")
        Galileo_sqrt_a = getattr(rtcmData, "DF303")
        Galileo_toe = getattr(rtcmData, "DF304")
        Galileo_cic = getattr(rtcmData, "DF305")
        Galileo_omega0 = getattr(rtcmData, "DF306") * math.pi # Right ascension at reference time
        Galileo_cis = getattr(rtcmData, "DF307")
        Galileo_i0 = getattr(rtcmData, "DF308") * math.pi  # Inclination angle at reference time
        Galileo_crc = getattr(rtcmData, "DF309")
        Galileo_omega = getattr(rtcmData, "DF310") * math.pi  # Argument of perigee
        Galileo_omegadot = getattr(rtcmData, "DF311") * math.pi  # Rate of right ascension
        Galileo_bgd_e5a_e1 = getattr(rtcmData, "DF312")  # E5a-E1 broadcast group delay
        Galileo_bgd_e5b_e1 = getattr(rtcmData, "DF313")  # E5b-E1 broadcast group delay
        Galileo_e5b_health = getattr(rtcmData, "DF316")
        Galileo_e5b_data_valid = getattr(rtcmData, "DF317")
        Galileo_e1b_health = getattr(rtcmData, "DF287")
        Galileo_e1b_data_valid = getattr(rtcmData, "DF288")
        navData[prn] = {}
        navData[prn][Galileo_toc] = {
            "af0": Galileo_af0,
            "af1": Galileo_af1,
            "af2": Galileo_af2,
            "IOD": Galileo_iodnav,
            "Crs": Galileo_crs,
            "deltan": Galileo_delta_n,
            "M0": Galileo_m0,
            "Cuc": Galileo_cuc,
            "e": Galileo_e,
            "Cus": Galileo_cus,
            "sqrtA": Galileo_sqrt_a,
            "toe": Galileo_toe,
            "Cic": Galileo_cic,
            "omega0": Galileo_omega0,
            "Cis": Galileo_cis,
            "i0": Galileo_i0,
            "Crc": Galileo_crc,
            "omega": Galileo_omega,
            "omegaDot": Galileo_omegadot,
            "IDOT": Galileo_idot,
            "TGD": Galileo_bgd_e5a_e1,
        }
    elif rtcmData.identity == "1042":
        prn = "C" + "{:0>2}".format(str(getattr(rtcmData, "DF488")))
        bds_week = getattr(rtcmData, "DF489")
        # Accuracy and clock parameters
        bds_urai = getattr(rtcmData, "DF490")  # User Range Accuracy Index
        bds_idot = getattr(rtcmData, "DF491") * math.pi  # Rate of inclination angle
        bds_aode = getattr(rtcmData, "DF492")  # Age of Data Ephemeris
        bds_toc = rtTime_gps2gpsTime(getattr(rtcmData, "DF493"))  # Clock data reference time
        bds_af2 = getattr(rtcmData, "DF494")  # Clock correction coefficient
        bds_af1 = getattr(rtcmData, "DF495")  # Clock correction coefficient
        bds_af0 = getattr(rtcmData, "DF496")  # Clock correction coefficient
        bds_aodc = getattr(rtcmData, "DF497")  # Age of Data Clock
        bds_crs = getattr(rtcmData, "DF498")  # Amplitude of sine harmonic correction
        bds_delta_n = getattr(rtcmData, "DF499") * math.pi  # Mean motion difference
        bds_m0 = getattr(rtcmData, "DF500")  * math.pi # Mean anomaly at reference time
        bds_cuc = getattr(rtcmData, "DF501")  # Amplitude of cosine harmonic correction
        bds_e = getattr(rtcmData, "DF502")  # Eccentricity
        bds_cus = getattr(rtcmData, "DF503")  # Amplitude of sine harmonic correction
        bds_sqrt_a = getattr(rtcmData, "DF504")  # Square root of semi-major axis
        bds_toe = getattr(rtcmData, "DF505")  # Ephemeris reference time
        bds_cic = getattr(rtcmData, "DF506")  # Amplitude of cosine harmonic correction
        bds_omega0 = getattr(rtcmData, "DF507") * math.pi  # Longitude of ascending node at reference time
        bds_cis = getattr(rtcmData, "DF508")  # Amplitude of sine harmonic correction
        bds_i0 = getattr(rtcmData, "DF509") * math.pi  # Inclination angle at reference time
        bds_crc = getattr(rtcmData, "DF510")  # Amplitude of cosine harmonic correction
        bds_omega = getattr(rtcmData, "DF511") * math.pi  # Argument of perigee
        bds_omegadot = getattr(rtcmData, "DF512") * math.pi  # Rate of right ascension
        bds_tgd1 = getattr(rtcmData, "DF513")  # B1I/B3I group delay differential
        bds_tgd2 = getattr(rtcmData, "DF514")  # B2I/B3I group delay differential
        bds_sv_health = getattr(rtcmData, "DF515")  # Satellite health status
        navData[prn] = {}
        navData[prn][bds_toc] = {
            "af0": bds_af0,
            "af1": bds_af1,
            "af2": bds_af2,
            "IOD": bds_aode,
            "Crs": bds_crs,
            "deltan": bds_delta_n,
            "M0": bds_m0,
            "Cuc": bds_cuc,
            "e": bds_e,
            "Cus": bds_cus,
            "sqrtA": bds_sqrt_a,
            "toe": bds_toe,
            "Cic": bds_cic,
            "omega0": bds_omega0,
            "Cis": bds_cis,
            "i0": bds_i0,
            "Crc": bds_crc,
            "omega": bds_omega,
            "omegaDot": bds_omegadot,
            "IDOT": bds_idot,
            "TGD": bds_tgd1,
        }
    return navData


def rtSp3Line(rnxData, sData, cData, startTime):
    lines = []
    satelliteList = sorted(rnxData.keys())
    lines.append("*  {year:4} {month:2} {day:2} {hour:2} {minute:2} {second:>11}\n".format(
        year=startTime.year,
        month=startTime.month,
        day=startTime.day,
        hour=startTime.hour,
        minute=startTime.minute,
        second="{:.8f}".format(startTime.second),
    ))
    for satellite in satelliteList:
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
            continue
        if (not satellite.startswith("C")) and (not satellite.startswith("R")):
            toc = selctToc(sData[satellite], rnxData[satellite], startTime, satellite)
        elif satellite.startswith("C"):
            toc = selctToc_BDS(sData[satellite], rnxData[satellite], startTime)
        elif satellite.startswith("R"):
            toc = selctToc_GLO(sData[satellite], rnxData[satellite], startTime)
        else:
            print(toc, startTime)
        if not toc:
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
            cdataTime = selectIOD_BDS(cData[satellite], startTime, toc)
        elif satellite.startswith("R"):
            cdataTime = selectIOD_GLO(cData[satellite], startTime, toc)
        else:
            cdataTime = selectIOD(cData[satellite], startTime, data["IOD"])
        if not cdataTime:
            continue
        cdata = cData[satellite][cdataTime]
        tsv2 = timeSub(startTime, cdataTime)
        clk_repair = clk + ((cdata["DeltaClockC0"] + cdata["DeltaClockC1"] / 1000 * tsv2 + cdata[
            "DeltaClockC2"] / 1000 * pow(
            tsv2, 2)) / c)
        if satellite not in sData:
            continue
        if satellite.startswith("C"):
            sdataTime = selectIOD_BDS(sData[satellite], startTime, toc)
        elif satellite.startswith("R"):
            sdataTime = selectIOD_GLO(sData[satellite], startTime, toc)
        else:
            sdataTime = selectIOD(sData[satellite], startTime, data["IOD"])
        if not sdataTime:
            continue
        sdata = sData[satellite][sdataTime]
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
        # clk_repair += 2*np.dot(rX.T[0],rDot.T[0])/299792458.0/299792458.0
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
        lines.append("P{PRN:3} {X:>13} {Y:>13} {Z:>13} {clk:>13}\n".format(PRN=satellite,
                                                                           X="{:.6f}".format(X_reapir[0][0] / 1000),
                                                                           Y="{:.6f}".format(X_reapir[1][0] / 1000),
                                                                           Z="{:.6f}".format(X_reapir[2][0] / 1000),
                                                                           clk="{:.6f}".format(
                                                                               clk_repair * pow(10, 6))))
    print(lines)


def ssrDecode(rtcmData, message=None):
    sdata = {}
    cdata = {}
    if rtcmData.identity == "1060":
        EpochTime = rtcmData.DF385
        toc = rtTime_gps2gpsTime(EpochTime)
        NumberOfSatellites = rtcmData.DF387
        for i in range(NumberOfSatellites):
            prn = "G" + "{:0>2}".format(str(getattr(rtcmData, "DF068_{:0>2}".format(i + 1))))
            IOD = getattr(rtcmData, "DF071_{:0>2}".format(i + 1))
            DeltaOrbitRadial = getattr(rtcmData, "DF365_{:0>2}".format(i + 1))
            DeltaOrbitAlongTrack = getattr(rtcmData, "DF366_{:0>2}".format(i + 1))
            DeltaOrbitCrossTrack = getattr(rtcmData, "DF367_{:0>2}".format(i + 1))
            DotOrbitDeltaRadial = getattr(rtcmData, "DF368_{:0>2}".format(i + 1))
            DotOrbitDeltaAlongTrack = getattr(rtcmData, "DF369_{:0>2}".format(i + 1))
            DotOrbitDeltaCrossTrack = getattr(rtcmData, "DF370_{:0>2}".format(i + 1))
            DeltaClockC0 = getattr(rtcmData, "DF376_{:0>2}".format(i + 1))
            DeltaClockC1 = getattr(rtcmData, "DF377_{:0>2}".format(i + 1))
            DeltaClockC2 = getattr(rtcmData, "DF378_{:0>2}".format(i + 1))
            if sdata.get(prn, -1) == -1:
                sdata[prn] = {}
            if cdata.get(prn, -1) == -1:
                cdata[prn] = {}
            sdata[prn][toc] = {
                "IOD": IOD,
                "DeltaOrbitRadial": DeltaOrbitRadial / 1000,
                "DeltaOrbitAlongTrack": DeltaOrbitAlongTrack / 1000,
                "DeltaOrbitCrossTrack": DeltaOrbitCrossTrack / 1000,
                "DotOrbitDeltaRadial": DotOrbitDeltaRadial,
                "DotOrbitDeltaAlongTrack": DotOrbitDeltaAlongTrack,
                "DotOrbitDeltaCrossTrack": DotOrbitDeltaCrossTrack,
            }
            cdata[prn][toc] = {
                "IOD": IOD,
                "DeltaClockC0": DeltaClockC0 / 1000,
                "DeltaClockC1": DeltaClockC1,
                "DeltaClockC2": DeltaClockC2,
            }
    elif rtcmData.identity == "1066":
        EpochTime = rtcmData.DF386
        toc = rtTime_ssrglo2gpsTime(EpochTime)
        NumberOfSatellites = rtcmData.DF387
        for i in range(NumberOfSatellites):
            prn = "R" + "{:0>2}".format(str(getattr(rtcmData, "DF384_{:0>2}".format(i + 1))))
            IOD = getattr(rtcmData, "DF392_{:0>2}".format(i + 1))
            DeltaOrbitRadial = getattr(rtcmData, "DF365_{:0>2}".format(i + 1))
            DeltaOrbitAlongTrack = getattr(rtcmData, "DF366_{:0>2}".format(i + 1))
            DeltaOrbitCrossTrack = getattr(rtcmData, "DF367_{:0>2}".format(i + 1))
            DotOrbitDeltaRadial = getattr(rtcmData, "DF368_{:0>2}".format(i + 1))
            DotOrbitDeltaAlongTrack = getattr(rtcmData, "DF369_{:0>2}".format(i + 1))
            DotOrbitDeltaCrossTrack = getattr(rtcmData, "DF370_{:0>2}".format(i + 1))
            DeltaClockC0 = getattr(rtcmData, "DF376_{:0>2}".format(i + 1))
            DeltaClockC1 = getattr(rtcmData, "DF377_{:0>2}".format(i + 1))
            DeltaClockC2 = getattr(rtcmData, "DF378_{:0>2}".format(i + 1))
            if sdata.get(prn, -1) == -1:
                sdata[prn] = {}
            if cdata.get(prn, -1) == -1:
                cdata[prn] = {}
            sdata[prn][toc] = {
                "IOD": IOD,
                "DeltaOrbitRadial": DeltaOrbitRadial / 1000,
                "DeltaOrbitAlongTrack": DeltaOrbitAlongTrack / 1000,
                "DeltaOrbitCrossTrack": DeltaOrbitCrossTrack / 1000,
                "DotOrbitDeltaRadial": DotOrbitDeltaRadial,
                "DotOrbitDeltaAlongTrack": DotOrbitDeltaAlongTrack,
                "DotOrbitDeltaCrossTrack": DotOrbitDeltaCrossTrack,
            }
            cdata[prn][toc] = {
                "IOD": IOD,
                "DeltaClockC0": DeltaClockC0 / 1000,
                "DeltaClockC1": DeltaClockC1,
                "DeltaClockC2": DeltaClockC2,
            }
    elif rtcmData.identity == "1243":
        start = [0, 0]  # start_Byte, start_Bit
        readBin(binary=message, length=24, start=start, type="uint")
        MessageNumber = readBin(binary=message, length=12, start=start, type="uint")
        EpochTime = readBin(binary=message, length=20, start=start, type="uint")
        SSRUpdateInterval = readBin(binary=message, length=4, start=start, type="uint")
        MultipleMessageIndicator = readBin(binary=message, length=1, start=start, type="uint")
        SatelliteReferenceDatum = readBin(binary=message, length=1, start=start, type="uint")
        IODSSR = readBin(binary=message, length=4, start=start, type="uint")
        SSRProviderID = readBin(binary=message, length=16, start=start, type="uint")
        SSRSolutionID = readBin(binary=message, length=4, start=start, type="uint")
        NumberOfSatellites = readBin(binary=message, length=6, start=start, type="uint")
        toc = rtTime_gps2gpsTime(EpochTime)
        for _ in range(NumberOfSatellites):
            prn = "E" + "{:0>2}".format(readBin(binary=message, length=6, start=start, type="uint"))
            IOD = readBin(binary=message, length=10, start=start, type="uint")
            DeltaOrbitRadial = readBin(binary=message, length=22, start=start, type="int") * 0.1 * pow(10, -3)
            DeltaOrbitAlongTrack = readBin(binary=message, length=20, start=start, type="int") * 0.4 * pow(10, -3)
            DeltaOrbitCrossTrack = readBin(binary=message, length=20, start=start, type="int") * 0.4 * pow(10, -3)
            DotOrbitDeltaRadial = readBin(binary=message, length=21, start=start, type="int") * 0.001
            DotOrbitDeltaAlongTrack = readBin(binary=message, length=19, start=start, type="int") * 0.004
            DotOrbitDeltaCrossTrack = readBin(binary=message, length=19, start=start, type="int") * 0.004
            DeltaClockC0 = readBin(binary=message, length=22, start=start, type="int") * 0.1 * pow(10, -3)
            DeltaClockC1 = readBin(binary=message, length=21, start=start, type="int") * 0.001 * pow(10, -3)
            DeltaClockC2 = readBin(binary=message, length=27, start=start, type="int") * 0.00002 * pow(10, -3)
            if sdata.get(prn, -1) == -1:
                sdata[prn] = {}
            if cdata.get(prn, -1) == -1:
                cdata[prn] = {}
            sdata[prn][toc] = {
                "IOD": IOD,
                "DeltaOrbitRadial": DeltaOrbitRadial,
                "DeltaOrbitAlongTrack": DeltaOrbitAlongTrack,
                "DeltaOrbitCrossTrack": DeltaOrbitCrossTrack,
                "DotOrbitDeltaRadial": DotOrbitDeltaRadial,
                "DotOrbitDeltaAlongTrack": DotOrbitDeltaAlongTrack,
                "DotOrbitDeltaCrossTrack": DotOrbitDeltaCrossTrack,
            }
            cdata[prn][toc] = {
                "IOD": IOD,
                "DeltaClockC0": DeltaClockC0,
                "DeltaClockC1": DeltaClockC1,
                "DeltaClockC2": DeltaClockC2,
            }
    elif rtcmData.identity == "1261":
        start = [0, 0]  # start_Byte, start_Bit
        readBin(binary=message, length=24, start=start, type="uint")
        MessageNumber = readBin(binary=message, length=12, start=start, type="uint")
        EpochTime = readBin(binary=message, length=20, start=start, type="uint")
        SSRUpdateInterval = readBin(binary=message, length=4, start=start, type="uint")
        MultipleMessageIndicator = readBin(binary=message, length=1, start=start, type="uint")
        SatelliteReferenceDatum = readBin(binary=message, length=1, start=start, type="uint")
        IODSSR = readBin(binary=message, length=4, start=start, type="uint")
        SSRProviderID = readBin(binary=message, length=16, start=start, type="uint")
        SSRSolutionID = readBin(binary=message, length=4, start=start, type="uint")
        NumberOfSatellites = readBin(binary=message, length=6, start=start, type="uint")
        toc = rtTime_dbs2gpsTime(EpochTime)
        for _ in range(NumberOfSatellites):
            prn = "C" + "{:0>2}".format(readBin(binary=message, length=6, start=start, type="uint"))
            TOEMOD = readBin(binary=message, length=10, start=start, type="uint")
            IOD = readBin(binary=message, length=8, start=start, type="uint")
            DeltaOrbitRadial = readBin(binary=message, length=22, start=start, type="int") * 0.1 * pow(10, -3)
            DeltaOrbitAlongTrack = readBin(binary=message, length=20, start=start, type="int") * 0.4 * pow(10, -3)
            DeltaOrbitCrossTrack = readBin(binary=message, length=20, start=start, type="int") * 0.4 * pow(10, -3)
            DotOrbitDeltaRadial = readBin(binary=message, length=21, start=start, type="int") * 0.001
            DotOrbitDeltaAlongTrack = readBin(binary=message, length=19, start=start, type="int") * 0.004
            DotOrbitDeltaCrossTrack = readBin(binary=message, length=19, start=start, type="int") * 0.004
            DeltaClockC0 = readBin(binary=message, length=22, start=start, type="int") * 0.1 * pow(10, -3)
            DeltaClockC1 = readBin(binary=message, length=21, start=start, type="int") * 0.001 * pow(10, -3)
            DeltaClockC2 = readBin(binary=message, length=27, start=start, type="int") * 0.00002 * pow(10, -3)
            if sdata.get(prn, -1) == -1:
                sdata[prn] = {}
            if cdata.get(prn, -1) == -1:
                cdata[prn] = {}
            sdata[prn][toc] = {
                "IOD": IOD,
                "DeltaOrbitRadial": DeltaOrbitRadial,
                "DeltaOrbitAlongTrack": DeltaOrbitAlongTrack,
                "DeltaOrbitCrossTrack": DeltaOrbitCrossTrack,
                "DotOrbitDeltaRadial": DotOrbitDeltaRadial,
                "DotOrbitDeltaAlongTrack": DotOrbitDeltaAlongTrack,
                "DotOrbitDeltaCrossTrack": DotOrbitDeltaCrossTrack,
            }
            cdata[prn][toc] = {
                "IOD": IOD,
                "DeltaClockC0": DeltaClockC0,
                "DeltaClockC1": DeltaClockC1,
                "DeltaClockC2": DeltaClockC2,
            }
    return sdata, cdata
