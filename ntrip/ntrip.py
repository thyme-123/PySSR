import asyncio
import socket
import base64

import pyrtcm

from gnssBase.gnssRT import ssrDecode,ephDecode


headerMessage = """GET /{mount} HTTP/1.1
User-Agent:NTRIP 
Accept:*/*
host:{url}
Connection:close
{base}

"""



def str2Base64(userName,passWord):
    st = "{}:{}".format(userName, passWord)
    return base64.b64encode(st.encode("utf-8")).decode("utf-8")

def recvMess(st,length=2048):
    ret = b""
    while length != len(ret):
        #ret += asyncio.get_event_loop().sock_recv(st, length - len(ret))
        ret += st.recv(length - len(ret))
    return ret

def sendMess(st,data):
    # await asyncio.get_event_loop().sock_sendall(st,data.encode())
    st.send(data.encode())

def getMount(url,port=2101,version=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    mesage = ""
    mesage += "GET / HTTP/1.1\r\n"
    mesage += "User-Agent:NTRIP \r\n"
    mesage += "Accept:*/*\r\n"
    mesage += "host:{}\r\n".format(url)
    mesage += "Connection:close\r\n"
    mesage += "\r\n"
    s.send(mesage.encode("utf-8"))
    mountData = ""
    while mountRecv := s.recv(2048).decode():
        mountData += mountRecv
        if "ENDSOURCETABLE" in mountData:
            break
    casterStrList = mountData.split("\n")
    return casterStrList

class NtripStream:

    def __init__(self, parent, url, mount, port=2101, userName=None, passWord=None):
        self.parent = parent
        if userName != None and passWord != None:
            self.basePassWord = "Authorization:Basic {}".format(str2Base64(userName,passWord))
        else:
            self.basePassWord = ""
        self.url = url
        self.mount = mount
        self.port = port
        self.stream = None
        self.isRun = False

    def reStart(self):
        self.isRun = True
        self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream.settimeout(800)
        try:
            self.stream.connect((self.url, self.port))
            # message = ""
            # message += "GET /{mount} HTTP/1.1\r\n".format(mount = self.mount)
            # message += "User-Agent:NTRIP\r\n"
            # message += "Accept:*/*\r\n"
            # message += "host:{url}\r\n".format(url=self.url)
            # message += "Connection:close\r\n"
            # if self.basePassWord != "":
            #     message += "{base}\r\n".format(base=self.basePassWord)
            message = headerMessage.format(mount=self.mount, url=self.url, base=self.basePassWord)
            sendMess(self.stream, message)
        except TimeoutError:
            print("E")
            self.reStart()
        except:
            self.reStart()

    def run(self):
        self.reStart()
        while self.isRun:
            try:
                message = b""
                magic = recvMess(self.stream, 1)
                if magic != b"\xD3":
                    continue
                message += magic
                messageHeader = recvMess(self.stream, 2)
                message += messageHeader
                undefine = int.from_bytes(messageHeader, byteorder='big', signed=False) & 0b1111110000000000
                if undefine != 0:
                    continue
                messageLength = (int.from_bytes(messageHeader, byteorder='big', signed=False) & 0b0000001111111111) + 3
                messageData = recvMess(self.stream, messageLength)
                message += messageData
                data = pyrtcm.RTCMReader.parse(message)
                yield data, message
            except ConnectionResetError:
                print("CE")
                self.reStart()
            except pyrtcm.exceptions.RTCMParseError:
                print("CRC")
                self.reStart()
            except TimeoutError:
                self.reStart()
            except:
                self.reStart()
        self.stream.close()

    def stop(self):
        self.isRun = False


