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


from window.PlotThread import *


class PlotWindow(QWidget):

    printLogSignal = Signal(str)

    def __init__(self, settingWindow, parent=None):
        super().__init__(parent)
        self.settingWindow = settingWindow
        # sp3 input
        self.sp3InputPathText = QLabel(self)
        self.sp3InputPathText.setText("input sp3 path")
        self.sp3InputPathText.resize(120, 20)
        self.sp3InputPathText.move(20, 40)
        self.sp3InputPathEdit = QLineEdit(self)
        self.sp3InputPathEdit.resize(400, 20)
        self.sp3InputPathEdit.move(130, 40)
        self.sp3InputPathButton = QPushButton(self)
        self.sp3InputPathButton.setText("...")
        self.sp3InputPathButton.resize(50, 20)
        self.sp3InputPathButton.move(535, 40)
        self.sp3InputPathButton.clicked.connect(self.sp3InputButtonClick)
        # sp3 template
        self.sp3TemplatePathText = QLabel(self)
        self.sp3TemplatePathText.setText("template sp3 path")
        self.sp3TemplatePathText.resize(120, 20)
        self.sp3TemplatePathText.move(20, 80)
        self.sp3TemplatePathEdit = QLineEdit(self)
        self.sp3TemplatePathEdit.resize(400, 20)
        self.sp3TemplatePathEdit.move(130, 80)
        self.sp3TemplatePathButton = QPushButton(self)
        self.sp3TemplatePathButton.setText("...")
        self.sp3TemplatePathButton.resize(50, 20)
        self.sp3TemplatePathButton.move(535, 80)
        self.sp3TemplatePathButton.clicked.connect(self.sp3TemplateButtonClick)
        # nav Path
        self.navPathText = QLabel(self)
        self.navPathText.setText("nav path")
        self.navPathText.resize(120, 20)
        self.navPathText.move(20, 120)
        self.navPathEdit = QLineEdit(self)
        self.navPathEdit.resize(400, 20)
        self.navPathEdit.move(130, 120)
        self.navPathButton = QPushButton(self)
        self.navPathButton.setText("...")
        self.navPathButton.resize(50, 20)
        self.navPathButton.move(535, 120)
        self.navPathButton.clicked.connect(self.navPathButtonClick)
        # out img Dir
        self.imgPathText = QLabel(self)
        self.imgPathText.setText("img path")
        self.imgPathText.resize(120, 20)
        self.imgPathText.move(20, 160)
        self.imgPathEdit = QLineEdit(self)
        self.imgPathEdit.resize(400, 20)
        self.imgPathEdit.move(130, 160)
        self.imgPathButton = QPushButton(self)
        self.imgPathButton.setText("...")
        self.imgPathButton.resize(50, 20)
        self.imgPathButton.move(535, 160)
        self.imgPathButton.clicked.connect(self.imgPathButtonClick)
        # command line
        self.commandLine = QTextEdit(self)
        self.commandLine.resize(780, 380)
        self.commandLine.move(10, 200)
        self.commandLine.setReadOnly(True)
        # startButton
        self.startButton = QPushButton(self)
        self.startButton.resize(100, 30)
        self.startButton.move(600, 160)
        self.startButton.setText("start")
        self.startButton.clicked.connect(self.startButtonClik)
        # position check
        self.xCheck = QCheckBox(self)
        self.xCheck.setText("X")
        self.xCheck.move(600,40)
        self.yCheck = QCheckBox(self)
        self.yCheck.setText("Y")
        self.yCheck.move(650, 40)
        self.zCheck = QCheckBox(self)
        self.zCheck.setText("Y")
        self.zCheck.move(700, 40)
        self.pCheck = QCheckBox(self)
        self.pCheck.setText("3D")
        self.pCheck.move(750, 40)
        self.rCheck = QCheckBox(self)
        self.rCheck.setText("R")
        self.rCheck.move(600, 80)
        self.aCheck = QCheckBox(self)
        self.aCheck.setText("A")
        self.aCheck.move(650, 80)
        self.cCheck = QCheckBox(self)
        self.cCheck.setText("C")
        self.cCheck.move(700, 80)
        self.clkCheck = QCheckBox(self)
        self.clkCheck.setText("clk")
        self.clkCheck.move(750, 80)
        self.positionHash = {
            "X Position": self.xCheck,
            "Y Position": self.yCheck,
            "Z Position": self.zCheck,
            "3D Position": self.pCheck,
            "CLK": self.clkCheck,
            "R Position": self.rCheck,
            "A Position": self.aCheck,
            "C Position": self.cCheck,
        }
        # system check
        self.gpsCheck = QCheckBox(self)
        self.gpsCheck.setText("GPS")
        self.gpsCheck.move(600, 120)
        self.galCheck = QCheckBox(self)
        self.galCheck.setText("GAL")
        self.galCheck.move(650, 120)
        self.gloCheck = QCheckBox(self)
        self.gloCheck.setText("GLO")
        self.gloCheck.move(700, 120)
        self.bdsCheck = QCheckBox(self)
        self.bdsCheck.setText("BDS")
        self.bdsCheck.move(750, 120)
        self.systemHash = {
            "G": self.gpsCheck,
            "E": self.galCheck,
            "R": self.gloCheck,
            "C": self.bdsCheck,
        }
        # thread
        self.thread = PlotThread(self)
        self.threadRun = False
        # signal
        self.printLogSignal.connect(self.printLog)

    @Slot()
    def sp3InputButtonClick(self):
        self.printLog("open sp3")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileName(self, "Open Sp3 File", "", "RNX FILE(*.sp3)")[0]
        if filePath != "":
            self.sp3InputPathEdit.setText(filePath)
            self.printLogSignal.emit("successful open sp3 file {}".format(filePath))
        return

    @Slot()
    def sp3TemplateButtonClick(self):
        self.printLog("open sp3 template")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileName(self, "Open Sp3 File", "", "RNX FILE(*.sp3)")[0]
        if filePath != "":
            self.sp3TemplatePathEdit.setText(filePath)
            self.printLogSignal.emit("successful open sp3 file {}".format(filePath))
        return

    @Slot()
    def navPathButtonClick(self):
        self.printLog("open nav template")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileName(self, "Open nav File", "", "RNX FILE(*.*)")[0]
        if filePath != "":
            self.navPathEdit.setText(filePath)
            self.printLogSignal.emit("successful open sp3 file {}".format(filePath))
        return

    @Slot()
    def imgPathButtonClick(self):
        self.printLog("open img dir")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getExistingDirectory(self, "Open img dir", "")
        if filePath != "":
            self.imgPathEdit.setText(filePath)
            self.printLogSignal.emit("successful open dir {}".format(filePath))
        return

    @Slot()
    def startButtonClik(self):
        self.threadRun = True
        self.thread.start()
        self.startButton.setDisabled(True)
        return

    @Slot()
    def endThread(self):
        self.threadRun = False
        self.startButton.setDisabled(False)
        return

    @Slot(str)
    def printLog(self, text):
        lines = self.commandLine.toPlainText().split("\n")
        lines.append(text)
        while len(lines) > 10:
            lines.pop(0)
        self.commandLine.setText("\n".join(lines))