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
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QTableWidgetItem

from window.IntegrityThread import *
from SSR.ssrDefine import *

class IntegrityWindow(QWidget):

    printLogSignal = Signal(str)

    def __init__(self, settingWindow, parent=None):
        super().__init__(parent)
        self.settingWindow = settingWindow
        # sp3 input
        self.inputPathText = QLabel(self)
        self.inputPathText.setText("input sp3/ssr")
        self.inputPathText.resize(120, 20)
        self.inputPathText.move(20, 40)
        self.inputPathEdit = QLineEdit(self)
        self.inputPathEdit.resize(400, 20)
        self.inputPathEdit.move(130, 40)
        self.inputPathButton = QPushButton(self)
        self.inputPathButton.setText("...")
        self.inputPathButton.resize(50, 20)
        self.inputPathButton.move(535, 40)
        self.inputPathButton.clicked.connect(self.inputButtonClick)
        self.commandLine = QTextEdit(self)
        self.commandLine.resize(780, 380)
        self.commandLine.move(10, 200)
        self.commandLine.setReadOnly(True)
        self.startButton = QPushButton(self)
        self.startButton.resize(100, 30)
        self.startButton.move(600, 160)
        self.startButton.setText("start")
        self.startButton.clicked.connect(self.startButtonClik)
        self.imgPathText = QLabel(self)
        self.imgPathText.setText("img path")
        self.imgPathText.resize(120, 20)
        self.imgPathText.move(20, 80)
        self.imgPathEdit = QLineEdit(self)
        self.imgPathEdit.resize(400, 20)
        self.imgPathEdit.move(130, 80)
        self.imgPathButton = QPushButton(self)
        self.imgPathButton.setText("...")
        self.imgPathButton.resize(50, 20)
        self.imgPathButton.move(535, 80)
        self.imgPathButton.clicked.connect(self.imgPathButtonClick)
        self.timeStepText = QLabel(self)
        self.timeStepText.setText("step:")
        self.timeStepText.move(600, 40)
        self.timeStepEdit = QLineEdit(self)
        self.timeStepEdit.resize(40, 20)
        self.timeStepEdit.move(640, 40)
        self.printLogSignal.connect(self.printLog)

    @Slot(str)
    def printLog(self, text):
        lines = self.commandLine.toPlainText().split("\n")
        lines.append(text)
        while len(lines) > 10:
            lines.pop(0)
        self.commandLine.setText("\n".join(lines))

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
    def inputButtonClick(self):
        self.printLogSignal.emit("open sp3/ssr")
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getOpenFileName(self, "Open Sp3/SSR File", "", "ssrFile (*.ssr);;sp3File (*.sp3)")[0]
        if filePath != "":
            self.inputPathEdit.setText(filePath)
            self.printLogSignal.emit("successful open sp3/ssr file {}".format(filePath))
        return

    @Slot()
    def startButtonClik(self):
        inputPath = self.inputPathEdit.text()
        outPath = self.imgPathEdit.text()
        thread = IntegrityThread(inputPath, outPath, mod=PLOT_SSR_S_INTEGRITY|PLOT_SSR_C_INTEGRITY, parent=self)
        thread.start()
        return