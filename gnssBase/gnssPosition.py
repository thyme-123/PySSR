import datetime
from math import *

import numpy as np

from gnssBase.gnssTime import *
from gnssBase.satData import *

a = 6378137.0
f = (1.0 / 298.257223563)
e2 = f * (2-f)
c = 299792458

AU = 149597870691.0
D2R = (3.1415926535897932 / 180.0)
AS2R = ((3.1415926535897932 / 180.0) / 3600.0)

frequency = {
        "G": {1: FREQ1, 2: FREQ2, 5: FREQ5},
        "R": {3: FREQ3_GLO, 1: 0, 2: 0},
        "E": {1: FREQ1, 5: FREQ5, 6: FREQ6, 7: FREQ7, 8: FREQ8,},
        "C": {1: FREQ_B1_BDS3, 2: FREQ1_CMP, 5: FREQ_B2a_BDS3, 6: FREQ_B3_BDS3, 7: FREQ_B2b_BDS3, 8: FREQ_B2_BDS3},
    }

fc = [
    [134.96340251, 1717915923.2178,  31.8792,  0.051635, -0.00024470],
    [357.52910918,  129596581.0481,  -0.5532,  0.000136, -0.00001149],
    [ 93.27209062, 1739527262.8478, -12.7512, -0.001037,  0.00000417],
    [297.85019547, 1602961601.2090,  -6.3706,  0.006593, -0.00003169],
    [125.04455501,   -6962890.2665,   7.4722,  0.007702, -0.00005939],
]

nut = [
  [   0,   0,   0,   0,   1, -6798.4, -171996, -174.2, 92025,   8.9],
  [   0,   0,   2,  -2,   2,   182.6,  -13187,   -1.6,  5736,  -3.1],
  [   0,   0,   2,   0,   2,    13.7,   -2274,   -0.2,   977,  -0.5],
  [   0,   0,   0,   0,   2, -3399.2,    2062,    0.2,  -895,   0.5],
  [   0,  -1,   0,   0,   0,  -365.3,   -1426,    3.4,    54,  -0.1],
  [   1,   0,   0,   0,   0,    27.6,     712,    0.1,    -7,   0.0],
  [   0,   1,   2,  -2,   2,   121.7,    -517,    1.2,   224,  -0.6],
  [   0,   0,   2,   0,   1,    13.6,    -386,   -0.4,   200,   0.0],
  [   1,   0,   2,   0,   2,     9.1,    -301,    0.0,   129,  -0.1],
  [   0,  -1,   2,  -2,   2,   365.2,     217,   -0.5,   -95,   0.3],
  [  -1,   0,   0,   2,   0,    31.8,     158,    0.0,    -1,   0.0],
  [   0,   0,   2,  -2,   1,   177.8,     129,    0.1,   -70,   0.0],
  [  -1,   0,   2,   0,   2,    27.1,     123,    0.0,   -53,   0.0],
  [   1,   0,   0,   0,   1,    27.7,      63,    0.1,   -33,   0.0],
  [   0,   0,   0,   2,   0,    14.8,      63,    0.0,    -2,   0.0],
  [  -1,   0,   2,   2,   2,     9.6,     -59,    0.0,    26,   0.0],
  [  -1,   0,   0,   0,   1,   -27.4,     -58,   -0.1,    32,   0.0],
  [   1,   0,   2,   0,   1,     9.1,     -51,    0.0,    27,   0.0],
  [  -2,   0,   0,   2,   0,  -205.9,     -48,    0.0,     1,   0.0],
  [  -2,   0,   2,   0,   1,  1305.5,      46,    0.0,   -24,   0.0],
  [   0,   0,   2,   2,   2,     7.1,     -38,    0.0,    16,   0.0],
  [   2,   0,   2,   0,   2,     6.9,     -31,    0.0,    13,   0.0],
  [   2,   0,   0,   0,   0,    13.8,      29,    0.0,    -1,   0.0],
  [   1,   0,   2,  -2,   2,    23.9,      29,    0.0,   -12,   0.0],
  [   0,   0,   2,   0,   0,    13.6,      26,    0.0,    -1,   0.0],
  [   0,   0,   2,  -2,   0,   173.3,     -22,    0.0,     0,   0.0],
  [  -1,   0,   2,   0,   1,    27.0,      21,    0.0,   -10,   0.0],
  [   0,   2,   0,   0,   0,   182.6,      17,   -0.1,     0,   0.0],
  [   0,   2,   2,  -2,   2,    91.3,     -16,    0.1,     7,   0.0],
  [  -1,   0,   0,   2,   1,    32.0,      16,    0.0,    -8,   0.0],
  [   0,   1,   0,   0,   1,   386.0,     -15,    0.0,     9,   0.0],
  [   1,   0,   0,  -2,   1,   -31.7,     -13,    0.0,     7,   0.0],
  [   0,  -1,   0,   0,   1,  -346.6,     -12,    0.0,     6,   0.0],
  [   2,   0,  -2,   0,   0, -1095.2,      11,    0.0,     0,   0.0],
  [  -1,   0,   2,   2,   1,     9.5,     -10,    0.0,     5,   0.0],
  [   1,   0,   2,   2,   2,     5.6,      -8,    0.0,     3,   0.0],
  [   0,  -1,   2,   0,   2,    14.2,      -7,    0.0,     3,   0.0],
  [   0,   0,   2,   2,   1,     7.1,      -7,    0.0,     3,   0.0],
  [   1,   1,   0,  -2,   0,   -34.8,      -7,    0.0,     0,   0.0],
  [   0,   1,   2,   0,   2,    13.2,       7,    0.0,    -3,   0.0],
  [  -2,   0,   0,   2,   1,  -199.8,      -6,    0.0,     3,   0.0],
  [   0,   0,   0,   2,   1,    14.8,      -6,    0.0,     3,   0.0],
  [   2,   0,   2,  -2,   2,    12.8,       6,    0.0,    -3,   0.0],
  [   1,   0,   0,   2,   0,     9.6,       6,    0.0,     0,   0.0],
  [   1,   0,   2,  -2,   1,    23.9,       6,    0.0,    -3,   0.0],
  [   0,   0,   0,  -2,   1,   -14.7,      -5,    0.0,     3,   0.0],
  [   0,  -1,   2,  -2,   1,   346.6,      -5,    0.0,     3,   0.0],
  [   2,   0,   2,   0,   1,     6.9,      -5,    0.0,     3,   0.0],
  [   1,  -1,   0,   0,   0,    29.8,       5,    0.0,     0,   0.0],
  [   1,   0,   0,  -1,   0,   411.8,      -4,    0.0,     0,   0.0],
  [   0,   0,   0,   1,   0,    29.5,      -4,    0.0,     0,   0.0],
  [   0,   1,   0,  -2,   0,   -15.4,      -4,    0.0,     0,   0.0],
  [   1,   0,  -2,   0,   0,   -26.9,       4,    0.0,     0,   0.0],
  [   2,   0,   0,  -2,   1,   212.3,       4,    0.0,    -2,   0.0],
  [   0,   1,   2,  -2,   1,   119.6,       4,    0.0,    -2,   0.0],
  [   1,   1,   0,   0,   0,    25.6,      -3,    0.0,     0,   0.0],
  [   1,  -1,   0,  -1,   0, -3232.9,      -3,    0.0,     0,   0.0],
  [  -1,  -1,   2,   2,   2,     9.8,      -3,    0.0,     1,   0.0],
  [   0,  -1,   2,   2,   2,     7.2,      -3,    0.0,     1,   0.0],
  [   1,  -1,   2,   0,   2,     9.4,      -3,    0.0,     1,   0.0],
  [   3,   0,   2,   0,   2,     5.5,      -3,    0.0,     1,   0.0],
  [  -2,   0,   2,   0,   2,  1615.7,      -3,    0.0,     1,   0.0],
  [   1,   0,   2,   0,   0,     9.1,       3,    0.0,     0,   0.0],
  [  -1,   0,   2,   4,   2,     5.8,      -2,    0.0,     1,   0.0],
  [   1,   0,   0,   0,   2,    27.8,      -2,    0.0,     1,   0.0],
  [  -1,   0,   2,  -2,   1,   -32.6,      -2,    0.0,     1,   0.0],
  [   0,  -2,   2,  -2,   1,  6786.3,      -2,    0.0,     1,   0.0],
  [  -2,   0,   0,   0,   1,   -13.7,      -2,    0.0,     1,   0.0],
  [   2,   0,   0,   0,   1,    13.8,       2,    0.0,    -1,   0.0],
  [   3,   0,   0,   0,   0,     9.2,       2,    0.0,     0,   0.0],
  [   1,   1,   2,   0,   2,     8.9,       2,    0.0,    -1,   0.0],
  [   0,   0,   2,   1,   2,     9.3,       2,    0.0,    -1,   0.0],
  [   1,   0,   0,   2,   1,     9.6,      -1,    0.0,     0,   0.0],
  [   1,   0,   2,   2,   1,     5.6,      -1,    0.0,     1,   0.0],
  [   1,   1,   0,  -2,   1,   -34.7,      -1,    0.0,     0,   0.0],
  [   0,   1,   0,   2,   0,    14.2,      -1,    0.0,     0,   0.0],
  [   0,   1,   2,  -2,   0,   117.5,      -1,    0.0,     0,   0.0],
  [   0,   1,  -2,   2,   0,  -329.8,      -1,    0.0,     0,   0.0],
  [   1,   0,  -2,   2,   0,    23.8,      -1,    0.0,     0,   0.0],
  [   1,   0,  -2,  -2,   0,    -9.5,      -1,    0.0,     0,   0.0],
  [   1,   0,   2,  -2,   0,    32.8,      -1,    0.0,     0,   0.0],
  [   1,   0,   0,  -4,   0,   -10.1,      -1,    0.0,     0,   0.0],
  [   2,   0,   0,  -4,   0,   -15.9,      -1,    0.0,     0,   0.0],
  [   0,   0,   2,   4,   2,     4.8,      -1,    0.0,     0,   0.0],
  [   0,   0,   2,  -1,   2,    25.4,      -1,    0.0,     0,   0.0],
  [  -2,   0,   2,   4,   2,     7.3,      -1,    0.0,     1,   0.0],
  [   2,   0,   2,   2,   2,     4.7,      -1,    0.0,     0,   0.0],
  [   0,  -1,   2,   0,   1,    14.2,      -1,    0.0,     0,   0.0],
  [   0,   0,  -2,   0,   1,   -13.6,      -1,    0.0,     0,   0.0],
  [   0,   0,   4,  -2,   2,    12.7,       1,    0.0,     0,   0.0],
  [   0,   1,   0,   0,   2,   409.2,       1,    0.0,     0,   0.0],
  [   1,   1,   2,  -2,   2,    22.5,       1,    0.0,    -1,   0.0],
  [   3,   0,   2,  -2,   2,     8.7,       1,    0.0,     0,   0.0],
  [  -2,   0,   2,   2,   2,    14.6,       1,    0.0,    -1,   0.0],
  [  -1,   0,   0,   0,   2,   -27.3,       1,    0.0,    -1,   0.0],
  [   0,   0,  -2,   2,   1,  -169.0,       1,    0.0,     0,   0.0],
  [   0,   1,   2,   0,   1,    13.1,       1,    0.0,     0,   0.0],
  [  -1,   0,   4,   0,   2,     9.1,       1,    0.0,     0,   0.0],
  [   2,   1,   0,  -2,   0,   131.7,       1,    0.0,     0,   0.0],
  [   2,   0,   0,   2,   0,     7.1,       1,    0.0,     0,   0.0],
  [   2,   0,   2,  -2,   1,    12.8,       1,    0.0,    -1,   0.0],
  [   2,   0,  -2,   0,   1,  -943.2,       1,    0.0,     0,   0.0],
  [   1,  -1,   0,  -2,   0,   -29.3,       1,    0.0,     0,   0.0],
  [  -1,   0,   0,   1,   1,  -388.3,       1,    0.0,     0,   0.0],
  [  -1,  -1,   0,   2,   1,    35.0,       1,    0.0,     0,   0.0],
  [   0,   1,   0,   1,   0,    27.3,       1,    0.0,     0,   0.0]
]

def Rx(x):
    return np.array([[1,0,0],
                    [0,np.cos(x),-1*np.sin(x)],
                    [0,np.sin(x),np.cos(x)]])

def Ry(x):
    return np.array([[cos(x),0,sin(x)],
                   [0,1,0],
                   [-sin(x),0,cos(x)]])

def Rz(x):
    return np.array([[np.cos(x),-1 * np.sin(x),0],
                   [np.sin(x),np.cos(x),0],
                   [0,0,1]])

def rotX(x):
    return np.array([[1, 0, 0],
                     [0, np.cos(x), np.sin(x)],
                     [0, -1 * np.sin(x), np.cos(x)]])

def rotZ(x):
    return np.array([[np.cos(x), np.sin(x), 0],
                     [-1 * np.sin(x), np.cos(x), 0],
                     [0, 0, 1]])

def norm(arr):
    r = 0
    for i in arr:
        r += pow(i, 2)
    return arr/r

def xyz2blh(x,y,z):
    R0 = sqrt(pow(x,2)+pow(y,2))
    R1 = sqrt(pow(x,2)+pow(y,2)+pow(z,2))
    L = atan2(y,x)
    N = a
    H = R1 -a
    B = atan2(z*(N+H),R0*(N*(1-e2)+H))
    deltaH = 0
    deltaB = 0
    while(abs(deltaH-H)>pow(10,-3) and abs(deltaB - B)>pow(10,-9)):
        deltaH = H
        deltaB = B
        N = a/sqrt(1-e2*pow(sin(B),2))
        H = R0/cos(B)-N
        B = atan2(z*(N+H),R0*(N*(1-e2)+H))
    return L,B,H

def xyz2enu(x1,y1,z1,x2,y2,z2):
    L,B,H = xyz2blh(x1,y1,z1)
    sinL = sin(L)
    cosL = cos(L)
    sinB = sin(B)
    cosB = cos(B)
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    E = -1*sinL*dx+cosL*dy
    N = -1*sinB*cosL*dx - sinB*sinL*dy + cosB*dz
    U = cosB*cosL*dx + cosB*sinL*dy + sinB*dz
    return E,N,U

def neu2xyz(e,n,u,x1,y1,z1):
    L, B, H = xyz2blh(x1, y1, z1)
    sinL = sin(L)
    cosL = cos(L)
    sinB = sin(B)
    cosB = cos(B)
    dx = -1 * sinL * e - sinB * cosL * n + cosB * cosL * u
    dy = cosL * e - sinB * sinL * n + cosB * sinL * u
    dz = cosB * n + sinB * u
    return dx, dy, dz

def getLam(s,frq):
    lam = []
    for f in frq:
        lam.append(frequency[s][f]/c)
    return lam

def eci2ecef(utct,rs):
    #ep2000 = datetime(2000, 1, 1, 12, 0, 0)
    ep2000 = datetime.datetime(2000, 1, 1, 12, 0, 0)
    gpst = utc2gpst(utct)
    t = (timeDiff(gpst, ep2000) + 19.0 + 32.184) / 86400.0 / 36525.0
    f = [0, 0, 0, 0, 0]
    tt = [pow(t,i) for i in range(1,5)]
    for i in range(5):
        f[i] = fc[i][0] * 3600.0
        for j in range(4):
            f[i] += fc[i][j+1] * tt[j]
        f[i] = fmod(f[i] * AS2R, 2*pi)
    # f = []
    # for i in range(5):
    #     f.append(fc[i][0] * 3600)
    #     for j in range(1,4):
    #         f[i] += fc[i][j] * pow(t, j)
    #     f[i] = fmod(f[i] * AS2R, 2.0 * pi)
    ze = (2306.2181 * t + 0.30188 * pow(t,2) + 0.017998 * pow(t,3)) * AS2R
    th = (2004.3109 * t - 0.42665 * pow(t,2) - 0.041833 * pow(t,3)) * AS2R
    z = (2306.2181 * t + 1.09468 * pow(t,2) + 0.018203 * pow(t,3)) * AS2R
    eps = (84381.448 - 46.8150 * t - 0.00059 * pow(t,2) + 0.001813 * pow(t,3)) * AS2R
    R1 = Rz(-z)
    R2 = Ry(th)
    R3 = Rz(-ze)
    P = np.dot(np.dot(R1, R2),R3)
    dpsi = 0
    deps = 0
    for i in range(106):
        ang = 0
        for j in range(5):
            ang += nut[i][j] * f[j]
        dpsi += (nut[i][6] + nut[i][7] * t) * sin(ang)
        deps += (nut[i][8] + nut[i][9] * t) * cos(ang)
    dpsi *= 1E-4 * AS2R
    deps *= 1E-4 * AS2R
    R1 = Rx(-eps - deps)
    R2 = Rz(-dpsi)
    R3 = Rx(eps)
    N = np.dot(np.dot(R1, R2), R3)
    sect = utct
    sec = sect.hour * 3600 + sect.minute * 60 + sect.second
    #sec = timeDiff(utct,datetime(1970,1,1))
    day = datetime.datetime(sect.year,sect.month,sect.day)
    t1 = timeDiff(day, ep2000) / 86400.0 / 36525.0
    t2 = t1 * t1
    t3 = t2 * t1
    gmst0 = 24110.54841 + 8640184.812866 * t1 + 0.093104 * t2 - 6.2E-6 * t3
    gmst = gmst0 + 1.002737909350795 * sec
    gmst_ = fmod(gmst, 86400.0) * pi / 43200.0
    gast = gmst_ + dpsi * cos(eps)
    gast += (0.00264 * sin(f[4]) + 0.000063 * sin(2.0 * f[4])) * AS2R
    R1 = Ry(-1 * 0)
    R2 = Rx(-1 * 0)
    R3 = Rz(gast)
    W = np.dot(R1, R2)
    R = np.dot(W,R3)
    NP = np.dot(N, P)
    U_ = np.dot(R, NP)
    #return np.dot(U_,rs.T)
    return np.dot(U_.T,rs)

def sumPosition(t):
    sum_eci = np.array([0,0,0],dtype=np.float64)
    tu = gpst2utc(t)
    # astronomical arguments
    #temp = timeDiff(tu, datetime(2000, 1, 1, 12, 0, 0))
    # tk = timeDiff(tu,datetime(2000, 1, 1, 12, 0, 0)) / 86400.0 / 36525.0
    temp = timeDiff(tu, datetime.datetime(2000, 1, 1, 12, 0, 0))
    tk = timeDiff(tu,datetime.datetime(2000, 1, 1, 12, 0, 0)) / 86400.0 / 36525.0
    f = [0, 0, 0, 0, 0]
    tt = [pow(tk,i) for i in range(1,5)]
    for i in range(5):
        f[i] = fc[i][0] * 3600.0
        for j in range(4):
            f[i] += fc[i][j+1] * tt[j]
        f[i] = fmod(f[i] * AS2R, 2*pi)
    # end
    # obliquity of the ecliptic
    eps = 23.439291 - 0.0130042 * tk
    sine = sin(eps * D2R)
    cose = cos(eps * D2R)
    # end

    # sun position in eci
    Ms = 357.5277233 + 35999.05034 * tk
    ls = 280.460 + 36000.770 * tk + 1.914666471 * sin(Ms * D2R) + 0.019994643 * sin(2.0 * Ms * D2R)
    rs = AU * (1.000140612 - 0.016708617 * cos(Ms * D2R) - 0.000139589 * cos(2.0 * Ms * D2R))
    sinl = sin(ls * D2R)
    cosl = cos(ls * D2R)
    sum_eci[0] = rs * cosl
    sum_eci[1] = rs * cose * sinl
    sum_eci[2] = rs * sine * sinl
    # end
    sum_ecef = eci2ecef(tu,sum_eci)
    return sum_ecef

def satposs(prn, gtime, rx, neu1, neu2=None, frq=None):
    system = prn[0]
    dant = [0, 0, 0]
    lam0, lam1 = 0, 0
    if system == "G":
        lam0, lam1 = getLam(system, frq)
    elif system == "E":
        lam0, lam1 = getLam(system, frq)
    rsun = sumPosition(gtime)
    ez = -1 * rx / np.linalg.norm(rx)
    es = rsun - rx
    es = es / np.linalg.norm(es)
    ey = np.cross(ez, es)
    ey = ey / np.linalg.norm(ey)
    ex = np.cross(ey, ez)
    ex = ex / np.linalg.norm(ex)
    gamma = pow(lam0,2) / pow(lam1,2)
    # C1 = gamma / (gamma - 1.0)
    # C2 = -1.0 / (gamma - 1.0)
    C1 = 1
    C2 = 0
    dant1 = 0
    dant2 = 0
    for i in range(3):
        dant1 = neu1[0] * ex[i] + neu1[1] * ey[i] + neu1[2] * ez[i]
        dant2 = neu2[0] * ex[i] + neu2[1] * ey[i] + neu2[2] * ez[i]
        dant[i] = C1 * dant1 + C2 * dant2
    return dant

def GPSPosition(data, startTime, toc, prn):
    # if prn != None:
    #     print(prn)
    c = 299792458
    PI = pi
    radv = 7.2921151467e-5
    GM = 3.986005e14
    if prn.startswith("E"):
        GM = 3.986004418E14
    F = -4.442807633e-10
    limit = 0.0000000000001
    tsv = timeSub(startTime, toc)
    # if prn.startswith("E"):
    #     print(prn,tsv,startTime,toc)
    #print(prn,tsv,startTime,toc)
    # n0 = sqrt(GM) / pow(data["sqrtA"], 3)
    n0 = sqrt(GM) / pow(data["sqrtA"], 3)
    n = n0 + data["deltan"]
    M = data["M0"] + n * tsv
    E = M
    EK = E
    iteration = 0
    maxIteration = 1000
    tk = timeSub(startTime, toc)
    # while iteration<maxIteration:
    while abs(E - M - data["e"] * sin(E)) > limit and iteration<maxIteration:
        E = E - (E - M - data["e"] * sin(E)) / (1 - data["e"] * cos(E))
        iteration += 1
    f = atan2((sqrt(1 - data["e"] ** 2) * sin(E)), (cos(E) - data["e"]))
    u_ = data["omega"] + f
    u = u_ + data["Cuc"] * cos(2 * u_) + data["Cus"] * sin(2 * u_)
    r = pow(data["sqrtA"], 2) * (1 - data["e"] * cos(E)) + data["Crc"] * cos(2 * u_) + data["Crs"] * sin(
        2 * u_)
    i = data["i0"] + data["Cic"] * cos(2 * u_) + data["Cis"] * sin(2 * u_) + data["IDOT"] * tsv
    x = r * cos(u)
    y = r * sin(u)
    L = data["omega0"] + (data["omegaDot"] - radv) * tsv - radv * data["toe"]
    X = x * cos(L) - y * cos(i) * sin(L)
    Y = x * sin(L) + y * cos(i) * cos(L)
    Z = y * sin(i)
    tdiff = timeSub(startTime, toc)
    clk = (data["af0"] + data["af1"] * tdiff + data["af2"] * pow(tdiff, 2))
    sin2u0 = sin(2 * u_)
    cos2u0 = cos(2 * u_)
    sinom = sin(L)
    cosom = cos(L)
    sini = sin(i)
    cosi = cos(i)
    tanv2 = tan(f / 2)
    dEdM = 1 / (1 - data["e"] * cos(E))
    dotv = sqrt((1.0 + data["e"]) / (1.0 - data["e"])) / cos(E / 2) / cos(E / 2) / (
            1 + tanv2 * tanv2) * dEdM * n
    dotu = dotv + (data["Cuc"] * sin2u0 + data["Cus"] * cos2u0) * 2 * dotv
    dotom = data["omegaDot"] - radv
    doti = data["IDOT"] + (data["Cic"] * sin2u0 + data["Cis"] * cos2u0) * 2 * dotv
    dotr = pow(data["sqrtA"], 2) * data["e"] * sin(E) * dEdM * n + (
            data["Crc"] * -1 * sin2u0 + data["Crs"] * cos2u0) * 2 * dotv
    dotx = dotr * cos(u) - r * sin(u) * dotu
    doty = dotr * sin(u) + r * cos(u) * dotu
    xDot = cosom * dotx - cosi * sinom * doty - x * sinom * dotom - y * cosi * cosom * dotom + y * sini * sinom * doti
    yDot = sinom * dotx + cosi * cosom * doty + x * cosom * dotom - y * cosi * sinom * dotom - y * sini * cosom * doti
    zDot = sini * doty + y * cosi * doti
    return X, Y, Z, clk, xDot, yDot, zDot


def DBSPosition(data, startTime, toc, prn=None, mod=False):
    c = 299792458
    PI = pi
    limit = 0.000000000000001
    if mod:
        limit = 0.0001
    gmBDS = 398.6004418e12
    omegaBDS = 7292115.0000e-11
    a0 = pow(data["sqrtA"],2)
    n0 = sqrt(gmBDS / pow(a0,3))
    tk = timeSub(startTime,toc)
    n = n0 + data["deltan"]
    M = data["M0"] + n * tk
    E = M
    EK = E
    iteration = 0
    maxIteration = 1000
    # while iteration<maxIteration:
    while abs(E - M - data["e"] * sin(E)) > limit and iteration < maxIteration:
        # E = E + (M + data["e"] * sin(E) - E) / (1 - data["e"] * cos(E))
        E = E - (E - M - data["e"] * sin(E)) / (1 - data["e"] * cos(E))
        iteration += 1
    e = data["e"]
    v = atan2(sqrt(1 - e * e) * sin(E), cos(E) - e)
    u0 = v + data["omega"]
    sin2u0 = sin(2 * u0)
    cos2u0 = cos(2 * u0)
    r = a0 * (1 - e * cos(E)) + data["Crc"] * cos2u0 + data["Crs"] * sin2u0
    i = data["i0"] + data["IDOT"] * tk + data["Cic"] * cos2u0 + data["Cis"] * sin2u0
    u = u0 + data["Cuc"] * cos2u0 + data["Cus"] * sin2u0
    xp = r * cos(u)
    yp = r * sin(u)
    toesec = time2WeekSeconds(toc) - 14
    sinom = 0
    cosom = 0
    sini = 0
    cosi = 0
    tanv2 = tan(v / 2)
    dEdM = 1 / (1 - data["e"] * cos(E))
    dotv = sqrt((1.0 + data["e"]) / (1.0 - data["e"])) / cos(E / 2) / cos(E / 2) / (1 + tanv2 * tanv2) * dEdM * n
    dotu = dotv + (-1 * data["Cuc"] * sin2u0 + data["Cus"] * cos2u0) * 2 * dotv
    doti = data["IDOT"] + (-1 * data["Cic"] * sin2u0 + data["Cis"] * cos2u0) * 2 * dotv
    dotr = a0 * data["e"] * sin(E) * dEdM * n + (-1 * data["Crc"] * sin2u0 + data["Crs"] * cos2u0) * 2 * dotv
    dotx = dotr * cos(u) - r * sin(u) * dotu
    doty = dotr * sin(u) + r * cos(u) * dotu
    iMaxGEO = 10.0 / 180.0 * PI
    X, Y, Z, clk, xDot, yDot, zDot = 0, 0, 0, 0, 0, 0, 0,
    if data["i0"] > iMaxGEO:
        OM = data["omega0"] + (data["omegaDot"] - omegaBDS) * tk - omegaBDS * toesec
        sinom = sin(OM)
        cosom = cos(OM)
        sini = sin(i)
        cosi = cos(i)
        X = xp * cosom - yp * cosi * sinom
        Y = xp * sinom + yp * cosi * cosom
        Z = yp * sini
        dotom = data["omegaDot"] - 7292115.1467e-11
        xDot = cosom * dotx - cosi * sinom * doty - xp * sinom * dotom - yp * cosi * cosom * dotom + yp * sini * sinom * doti
        yDot = sinom * dotx + cosi * cosom * doty + xp * cosom * dotom - yp * cosi * sinom * dotom - yp * sini * cosom * doti
        zDot = sini * doty + yp * cosi * doti
    else:
        OM = data["omega0"] + data["omegaDot"] * tk - omegaBDS * toesec
        ll = omegaBDS * tk
        sinom = sin(OM)
        cosom = cos(OM)
        sini = sin(i)
        cosi = cos(i)
        xx = xp * cosom - yp * cosi * sinom
        yy = xp * sinom + yp * cosi * cosom
        zz = yp * sini
        X1 = np.array([[xx],[yy],[zz]])
        RX = rotX(-5.0 / 180.0 * PI)
        RZ = rotZ(ll)
        X2 = RZ @ RX @ X1
        X = X2[0][0]
        Y = X2[1][0]
        Z = X2[2][0]
        dotom = data["omegaDot"]
        vx = cosom * dotx - cosi * sinom * doty - xp * sinom * dotom - yp * cosi * cosom * dotom + yp * sini * sinom * doti
        vy = sinom * dotx + cosi * cosom * doty + xp * cosom * dotom - yp * cosi * sinom * dotom - yp * sini * cosom * doti
        vz = sini * doty + yp * cosi * doti
        V = np.array([[vx], [vy], [vz]])
        C = cos(ll)
        S = sin(ll)
        UU = np.array([[-S,  C, 0],
                       [-C, -S, 0],
                       [ 0,  0, 0]])
        RdotZ = omegaBDS * UU
        VV = RZ @ RX @ V + RdotZ @ RX @ X1
        xDot = VV[0][0]
        yDot = VV[1][0]
        zDot = VV[2][0]
    clk = data["af0"] + data["af1"] * tk + data["af2"] * pow(tk, 2)
    return X, Y, Z, clk, xDot, yDot, zDot

def runge_kutta_4(xi, yi, dx, acc, der):
    # Compute k1, k2, k3, k4
    k1 = der(xi, yi, acc) * dx
    k2 = der(xi + dx / 2.0, yi + k1 / 2.0, acc) * dx
    k3 = der(xi + dx / 2.0, yi + k2 / 2.0, acc) * dx
    k4 = der(xi + dx, yi + k3, acc) * dx

    # Update the state vector
    yf = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

    return yf

def glo_deriv(tt, xv, acc):
    # State vector components
    rr = xv[:3]  # First 3 elements are position
    vv = xv[3:6]  # Next 3 elements are velocity

    # Constants
    gmWGS = 398.60044e12
    AE = 6378136.0
    OMEGA = 7292115.e-11
    C20 = -1082.6257e-6

    # Calculate intermediate terms
    rho = np.linalg.norm(rr)
    t1 = -gmWGS / (rho ** 3)
    t2 = 1.5 * C20 * (gmWGS * AE ** 2) / (rho ** 5)
    t3 = OMEGA ** 2
    t4 = 2.0 * OMEGA
    z2 = rr[2] ** 2

    # Vector of derivatives
    va = np.zeros(6)
    va[0] = vv[0]
    va[1] = vv[1]
    va[2] = vv[2]
    va[3] = (t1 + t2 * (1.0 - 5.0 * z2 / (rho ** 2)) + t3) * rr[0] + t4 * vv[1] + acc[0]
    va[4] = (t1 + t2 * (1.0 - 5.0 * z2 / (rho ** 2)) + t3) * rr[1] - t4 * vv[0] + acc[1]
    va[5] = (t1 + t2 * (3.0 - 5.0 * z2 / (rho ** 2))) * rr[2] + acc[2]
    return va

def glonassPosition(data, startTime, toc):
    nominalStep = 10.0
    dtPos = timeSub(startTime, toc)
    nSteps = int(fabs(dtPos) / nominalStep) + 1
    step = dtPos / nSteps
    tt = time2WeekSeconds(startTime)
    X = data["x"] * pow(10,3)
    Y = data["y"] * pow(10,3)
    Z = data["z"] * pow(10,3)
    vx = data["vx"] * pow(10,3)
    vy = data["vy"] * pow(10,3)
    vz = data["vz"] * pow(10,3)
    ax = data["ax"] * pow(10,3)
    ay = data["ay"] * pow(10, 3)
    az = data["az"] * pow(10, 3)
    xv = np.array([X, Y, Z, vx, vy, vz])
    acc = np.array([ax, ay, az])
    for _ in range(nSteps):
        xv = runge_kutta_4(tt, xv, step, acc, glo_deriv)
        tt += step
    tk = timeDiff(startTime, toc)
    for _ in range(2):
        tk = tk - (data["tau"] + data["gamma"] * tk)
    clk = data["tau"] + data["gamma"] * tk

    X = xv[0]
    Y = xv[1]
    Z = xv[2]
    xDot = xv[3]
    yDot = xv[4]
    zDot = xv[5]
    clk += 2.0 * (X * xDot + Y * yDot + Z * zDot) / c / c
    return X, Y, Z, clk, xDot, yDot, zDot