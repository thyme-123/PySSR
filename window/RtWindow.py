import os.path

from PySide6.QtCore import Slot
from PySide6.QtCore import QEvent
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QCheckBox

from window.RtThread import *
from window.mountWindow import *

from ntrip.ntrip import *
from gnssBase.gnssRT import *

class RtWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # BASE input
        # url text
        self.urlText = QLabel(self)
        self.urlText.setText("url")
        self.urlText.resize(30, 20)
        self.urlText.move(20, 20)
        # url input
        self.urlPath = QLineEdit(self)
        self.urlPath.resize(120, 20)
        self.urlPath.move(60, 20)
        # port text
        self.portText = QLabel(self)
        self.portText.setText("port")
        self.portText.resize(30, 20)
        self.portText.move(200, 20)
        # port input
        self.portPath = QLineEdit(self)
        self.portPath.resize(120, 20)
        self.portPath.move(240, 20)
        self.portPath.setText("2101")
        # username text
        self.userNameText = QLabel(self)
        self.userNameText.setText("userName")
        self.userNameText.resize(60, 20)
        self.userNameText.move(380, 20)
        # username input
        self.userName = QLineEdit(self)
        self.userName.resize(120, 20)
        self.userName.move(450, 20)
        # password text
        self.passWordText = QLabel(self)
        self.passWordText.resize(60, 20)
        self.passWordText.setText("password")
        self.passWordText.move(590, 20)
        # password input
        self.passWord = QLineEdit(self)
        self.passWord.resize(120, 20)
        self.passWord.move(660, 20)
        # eph mount text
        self.ephMountText = QLabel(self)
        self.ephMountText.resize(30, 20)
        self.ephMountText.move(20, 70)
        self.ephMountText.setText("eph")
        # ehp mount input
        self.ephMount = QLineEdit(self)
        self.ephMount.resize(400, 20)
        self.ephMount.move(60, 70)
        # eph mount get
        self.ephGetMountButton = QPushButton(self)
        self.ephGetMountButton.resize(50, 20)
        self.ephGetMountButton.move(480, 70)
        self.ephGetMountButton.setText("...")
        self.ephGetMountButton.clicked.connect(self.ephGetMountButtonClick)
        # ssr mount text
        self.ssrMountText = QLabel(self)
        self.ssrMountText.resize(30, 20)
        self.ssrMountText.move(20, 120)
        self.ssrMountText.setText("ssr")
        # ssr mount input
        self.ssrMount = QLineEdit(self)
        self.ssrMount.resize(400, 20)
        self.ssrMount.move(60, 120)
        # ssr mount get
        self.ssrGetMountButton = QPushButton(self)
        self.ssrGetMountButton.resize(50, 20)
        self.ssrGetMountButton.move(480, 120)
        self.ssrGetMountButton.setText("...")
        self.ssrGetMountButton.clicked.connect(self.ssrGetMountButtonClick)
        # out dir text
        self.outMountText = QLabel(self)
        self.outMountText.resize(30, 20)
        self.outMountText.move(20, 170)
        self.outMountText.setText("out")
        # out dir input
        self.outMount = QLineEdit(self)
        self.outMount.resize(400, 20)
        self.outMount.move(60, 170)
        # out dir get
        self.outGetMountButton = QPushButton(self)
        self.outGetMountButton.resize(50, 20)
        self.outGetMountButton.move(480, 170)
        self.outGetMountButton.setText("...")
        self.outGetMountButton.clicked.connect(self.outGetMountButtonClick)
        # thread
        self.isRun = False
        # start button
        self.startButton = QPushButton(self)
        self.startButton.resize(90, 30)
        self.startButton.move(550, 160)
        self.startButton.setText("start")
        self.startButton.clicked.connect(self.startButtonClick)
        # end button
        self.endButton = QPushButton(self)
        self.endButton.resize(90, 30)
        self.endButton.move(650, 160)
        self.endButton.setText("end")
        self.endButton.clicked.connect(self.endButtonClick)

    @Slot()
    def ephGetMountButtonClick(self):
        if not self.urlPath.text():
            return
        url = self.urlPath.text()
        if not self.portPath.text():
            return
        port = self.portPath.text()
        if not port.isdigit():
            return
        mountData = getMount(url, int(port))
        self.mountWindow = MountWindow(mountData, self.ephMount, "eph")
        self.mountWindow.show()
        # self.ssrMount = QLineEdit(self)
        # self.outPath = QLineEdit(self)

    @Slot()
    def ssrGetMountButtonClick(self):
        if not self.urlPath.text():
            return
        url = self.urlPath.text()
        if not self.portPath.text():
            return
        port = self.portPath.text()
        if not port.isdigit():
            return
        mountData = getMount(url, int(port))
        self.mountWindow = MountWindow(mountData, self.ssrMount, "ssr")
        self.mountWindow.show()

    @Slot()
    def outGetMountButtonClick(self):
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getExistingDirectory(self, "Open out dir", "")
        if filePath != "":
            self.outMount.setText(filePath)
        return

    @Slot()
    def startButtonClick(self):
        ephMount = self.ephMount.text()
        ssrMount = self.ssrMount.text()
        outPath = self.outMount.text()
        if not self.urlPath.text():
            return
        url = self.urlPath.text()
        if not self.portPath.text():
            return
        port = self.portPath.text()
        if not port.isdigit():
            return
        if outPath == "":
            return
        if ephMount == "":
            return
        if ssrMount == "":
            return
        if not os.path.isabs(outPath):
            os.mkdir(outPath)
        username = self.userName.text()
        password = self.passWord.text()
        self.runThread = RTThread(ephMount, ssrMount, url, int(port), username, password, outPath, self)
        self.runThread.start()
        return

    @Slot()
    def endButtonClick(self):
        return
