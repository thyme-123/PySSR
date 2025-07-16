import time
import datetime

leaps = [
    [2017, 1, 1, 0, 0, 0, -18],
    [2015, 7, 1, 0, 0, 0, -17],
    [2012, 7, 1, 0, 0, 0, -16],
    [2009, 1, 1, 0, 0, 0, -15],
    [2006, 1, 1, 0, 0, 0, -14],
    [1999, 1, 1, 0, 0, 0, -13],
    [1997, 7, 1, 0, 0, 0, -12],
    [1996, 1, 1, 0, 0, 0, -11],
    [1994, 7, 1, 0, 0, 0, -10],
    [1993, 7, 1, 0, 0, 0,  -9],
    [1992, 7, 1, 0, 0, 0,  -8],
    [1991, 1, 1, 0, 0, 0,  -7],
    [1990, 1, 1, 0, 0, 0,  -6],
    [1988, 1, 1, 0, 0, 0,  -5],
    [1985, 7, 1, 0, 0, 0,  -4],
    [1983, 7, 1, 0, 0, 0,  -3],
    [1982, 7, 1, 0, 0, 0,  -2],
    [1981, 7, 1, 0, 0, 0,  -1],
    [   0, 0, 0, 0, 0, 0,   0],
]

def date2doy(dTime):
    year, doy = time2YearDoy(dTime)
    doy += (dTime.hour/24 + dTime.minute/(24*60) + dTime.second/(24*60*60))
    return doy

def dateList2doy(dTimeList):
    ans_List = []
    for dTime in dTimeList:
        ans_List.append(date2doy(dTime))
    return ans_List


def day2JD(gtime):
    Y = gtime.year
    M = gtime.month
    d = gtime.day
    h = gtime.hour
    JD = 1721013.5 + 367 * Y - int(7 / 4 * (Y + int((M + 9)/12))) + d + h / 24 + int(275 * M / 9) - 2400000.5
    return JD

def gnssTime(year, month, day, hour, minute, second):
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=int(second))

def getDaySec(t):
    return t.hour * 3600 + t.minute * 60 + t.second

def time2WeekSeconds(rtTime):
    gps_start = datetime.datetime(1980, 1, 6)
    day = (rtTime - gps_start).days
    second = (rtTime - gps_start).seconds
    return second + (day % 7) * 24 * 3600

def rtTime_gps2gpsTime(rtTime):
    gps_start = datetime.datetime(1980, 1, 6)
    gps_end = datetime.datetime.now()
    gps_start += datetime.timedelta(seconds=rtTime)
    while gps_start < gps_end:
        gps_start += datetime.timedelta(seconds=604800)
    return gps_start - datetime.timedelta(seconds=604800)

def rtTime_dbs2gpsTime(rtTime):
    gps_start = datetime.datetime(1980, 1, 6)
    gps_end = datetime.datetime.now()
    gps_start += datetime.timedelta(seconds=rtTime)
    while gps_start < gps_end:
        gps_start += datetime.timedelta(seconds=604800)
    return gps_start - datetime.timedelta(seconds=604800) + datetime.timedelta(seconds=14)

def rtTime_glo2gpsTime(rtTime):
    glo_start = datetime.datetime(1980, 1, 6)
    gps_end = datetime.datetime.now()
    glo_start += datetime.timedelta(minutes=rtTime) - datetime.timedelta(hours=3)
    while glo_start < gps_end:
        glo_start += datetime.timedelta(seconds=86400)
    return glo_start - datetime.timedelta(seconds=86400)

def rtTime_ssrglo2gpsTime(rtTime):
    glo_start = datetime.datetime(1980, 1, 6)
    gps_end = datetime.datetime.now()
    glo_start += datetime.timedelta(seconds=rtTime)
    while glo_start < gps_end:
        glo_start += datetime.timedelta(seconds=86400)
    return glo_start - datetime.timedelta(seconds=86400) - datetime.timedelta(hours=3) + datetime.timedelta(seconds=18)

def timeSub(time1, time2):
    ans = time2WeekSeconds(time1) - time2WeekSeconds(time2)
    if ans < -302400:
        ans += 604800
    if ans > 302400:
        ans -= 604800
    return ans

def timeDiff(time1,time2):
    # print(time1)
    # print(time2)
    ans = time1 - time2
    return ans.total_seconds()


def doy_to_date(year, doy):
    base = datetime.date(year, 1, 1)
    t = base + datetime.timedelta(doy - 1)
    return t.year, t.month, t.day


def time2WeekDay(rtTime):
    gps_start = datetime.datetime(1980, 1, 6)
    day = (rtTime - gps_start).days
    second = (rtTime - gps_start).seconds
    return day // 7, day % 7

def gpst2utc(gpst):
    for leap in leaps:
        tu = gpst + datetime.timedelta(seconds=leap[6])
        dt = datetime.datetime(year=leap[0], month=leap[1], day=leap[2], hour=leap[3], minute=leap[4], second=leap[5])
        if tu > dt:
            return tu
    return None

def utc2gpst(utc):
    for leap in leaps:
        tg = utc - datetime.timedelta(seconds=leap[6])
        dt = datetime.datetime(year=leap[0], month=leap[1], day=leap[2], hour=leap[3], minute=leap[4], second=leap[5])
        if tg > dt:
            return tg
    return None

def getUTDay():
    timestamp = int(time.time())
    utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    return utc_time

def getDay(gtime):
    return gtime - datetime.timedelta(seconds=gtime.second) - datetime.timedelta(minutes=gtime.minute) - datetime.timedelta(hours=gtime.hour)

def getTimetamp(gtime):
    return datetime.datetime.timestamp(gtime)

def weekDay2Time(week, day):
    gTime = datetime.datetime(1980, 1, 6)
    print(week,day)
    gTime += datetime.timedelta(days=week * 7) + datetime.timedelta(days=day)
    return gTime

def time2YearDoy(gtime):
    return gtime.year, gtime.timetuple().tm_yday
