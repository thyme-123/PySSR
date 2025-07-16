import os


from PySide6.QtCore import Slot
from PySide6.QtCore import QEvent
from PySide6.QtCore import Signal
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QCheckBox


from gnssBase.gnssIO import *
from gnssBase.gnssSSR import *
from window.RepairThread import *



class RepairWindow(QWidget):

    printLogSignal = Signal(str)

    def __init__(self, settingWindow, parent=None):
        super().__init__(parent)
        self.settingWindow = settingWindow
        #nav Dir
        self.navPathText = QLabel(self)
        self.navPathText.setText("nav path")
        self.navPathText.resize(120,20)
        self.navPathText.move(20,40)
        self.navPathEdit = QLineEdit(self)
        self.navPathEdit.resize(400,20)
        self.navPathEdit.move(130,40)
        self.navPathButton = QPushButton(self)
        self.navPathButton.setText("...")
        self.navPathButton.resize(50, 20)
        self.navPathButton.move(535, 40)
        self.navPathButton.clicked.connect(self.navPathButtonClick)
        #ssr Dir
        self.ssrPathText = QLabel(self)
        self.ssrPathText.setText("ssr path")
        self.ssrPathText.resize(120, 20)
        self.ssrPathText.move(20, 80)
        self.ssrPathEdit = QLineEdit(self)
        self.ssrPathEdit.resize(400, 20)
        self.ssrPathEdit.move(130, 80)
        self.ssrPathButton = QPushButton(self)
        self.ssrPathButton.setText("...")
        self.ssrPathButton.resize(50, 20)
        self.ssrPathButton.move(535, 80)
        self.ssrPathButton.clicked.connect(self.ssrPathButtonClick)
        # out sp3 Dir
        self.sp3PathText = QLabel(self)
        self.sp3PathText.setText("sp3 path")
        self.sp3PathText.resize(120, 20)
        self.sp3PathText.move(20, 120)
        self.sp3PathEdit = QLineEdit(self)
        self.sp3PathEdit.resize(400, 20)
        self.sp3PathEdit.move(130, 120)
        self.sp3PathButton = QPushButton(self)
        self.sp3PathButton.setText("...")
        self.sp3PathButton.resize(50, 20)
        self.sp3PathButton.move(535, 120)
        self.sp3PathButton.clicked.connect(self.sp3PathButtonClick)
        # out clk Dir
        self.clkPathText = QLabel(self)
        self.clkPathText.setText("clk path")
        self.clkPathText.resize(120, 20)
        self.clkPathText.move(20, 160)
        self.clkPathEdit = QLineEdit(self)
        self.clkPathEdit.resize(400, 20)
        self.clkPathEdit.move(130, 160)
        self.clkPathButton = QPushButton(self)
        self.clkPathButton.setText("...")
        self.clkPathButton.resize(50, 20)
        self.clkPathButton.move(535, 160)
        self.clkPathButton.clicked.connect(self.clkPathButtonClick)
        #atx Dir
        self.atxPathText = QLabel(self)
        self.atxPathText.setText("atx path")
        self.atxPathText.resize(120, 20)
        self.atxPathText.move(20, 200)
        self.atxPathEdit = QLineEdit(self)
        self.atxPathEdit.resize(400, 20)
        self.atxPathEdit.move(130, 200)
        self.atxPathButton = QPushButton(self)
        self.atxPathButton.setText("...")
        self.atxPathButton.resize(50,20)
        self.atxPathButton.move(535,200)
        self.atxPathButton.clicked.connect(self.atxPathButtonClick)
        # no ssr
        self.ssrCheck = QCheckBox(self)
        self.ssrCheck.setText("no ssr")
        self.ssrCheck.move(600, 40)
        # pco
        self.pcoCheck = QCheckBox(self)
        self.pcoCheck.setText("pco")
        self.pcoCheck.move(700, 40)
        # CNAV
        # self.cnavCheck = QCheckBox(self)
        # self.cnavCheck.setText("cnav")
        # self.cnavCheck.move(600, 80)
        # startButton
        self.startButton = QPushButton(self)
        self.startButton.resize(90, 30)
        self.startButton.move(600, 200)
        self.startButton.setText("start")
        self.startButton.clicked.connect(self.startButtonClik)
        # endButton
        self.endButton = QPushButton(self)
        self.endButton.resize(90, 30)
        self.endButton.move(700, 200)
        self.endButton.setText("end")
        self.endButton.clicked.connect(self.endButtonClick)
        self.endButton.setDisabled(True)
        # command line
        self.commandLine = QTextEdit(self)
        self.commandLine.resize(780, 350)
        self.commandLine.move(10, 230)
        self.commandLine.setReadOnly(True)
        # thread
        self.thread = RepairThread(self)
        self.threadRun = False
        # signal
        self.printLogSignal.connect(self.printLog)


    @Slot()
    def endButtonClick(self):
        self.thread.terminate()
        self.thread = RepairThread(self)
        self.endThread()
        return

    @Slot()
    def navPathButtonClick(self):
        self.printLogSignal.emit("open nav")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileNames(self,"Open Nav File","","RNX FILE(*.*)")[:-1][0]
        print(filePath)
        if filePath != []:
            self.navPathEdit.setText(";".join(filePath))
            for filepath in filePath:
                self.printLogSignal.emit("successful open ssr file {}".format(filepath))
        return

    @Slot()
    def ssrPathButtonClick(self):
        self.printLogSignal.emit("open ssr")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileName(self, "Open SSR File", "", "RNX FILE(*.ssr)")[0]
        if filePath != "":
            self.ssrPathEdit.setText(filePath)
            self.printLogSignal.emit("successful open ssr file {}".format(filePath))
        return

    @Slot()
    def sp3PathButtonClick(self):
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getSaveFileName(self, "Open Sp3 File", "", "RNX FILE(*.sp3)")[0]
        if filePath != "":
            self.sp3PathEdit.setText(filePath)
        return

    @Slot()
    def clkPathButtonClick(self):
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getSaveFileName(self, "Open clk File", "", "RNX FILE(*.clk)")[0]
        if filePath != "":
            self.clkPathEdit.setText(filePath)
        return

    @Slot()
    def atxPathButtonClick(self):
        self.printLogSignal.emit("open atx")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileName(self, "Open atx File", "", "RNX FILE(*.atx)")[0]
        if filePath != "":
            self.atxPathEdit.setText(filePath)
            self.printLogSignal.emit("successful open ssr file {}".format(filePath))
        return

    @Slot()
    def startButtonClik(self):
        self.threadRun = True
        self.thread.start()
        self.startButton.setDisabled(True)
        self.endButton.setDisabled(False)
        return

    @Slot()
    def endThread(self):
        self.threadRun = False
        self.endButton.setDisabled(True)
        self.startButton.setDisabled(False)

    @Slot()
    def repairRun(self):
        navPath = self.navPathEdit.text()
        ssrPath = self.ssrPathEdit.text()
        if not navPath:
            self.printLog("no nav file")
            return
        if not ssrPath:
            self.printLog("no ssr file")
        if not os.path.isfile(navPath):
            self.printLog("nav file is not exist")
            return
        if not os.path.isfile(ssrPath):
            self.printLog("ssr file is not exist")
            return
        sp3Path = self.sp3PathEdit.text()
        clkPath = self.clkPathEdit.text()
        rnxData, times = readNav(navPath)
        cData, sData = readSSR(ssrPath)
        while True:
            if not sp3Path:
                self.printLog("no out sp3 path,skip processing")
                break
            if os.path.isfile(sp3Path):
                self.printLog(
                    "sp3 file {} is not exist".format(sp3Path)
                )
                msg = QMessageBox()
                ret = msg.question(
                    self,
                    "Warring",
                    "sp3 file {} is not exist,whether to replace or not".format(sp3Path),
                )
                if ret == 1:
                    break
            lines = sp3Lines(rnxData, times, cData, sData)
            with open(sp3Path,"w") as f:
                for line in lines:
                    f.write(line)
            break
        return

    @Slot(str)
    def printLog(self, text):
        lines = self.commandLine.toPlainText().split("\n")
        lines.append(text)
        while len(lines) > 10:
            lines.pop(0)
        self.commandLine.setText("\n".join(lines))

