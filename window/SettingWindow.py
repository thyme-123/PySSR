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
from PySide6.QtWidgets import QComboBox

class SeetingWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # out format in plotdiff
        # out format text
        self.formatText = QLabel(self)
        self.formatText.setText("foramt:")
        self.formatText.resize(40, 20)
        self.formatText.move(20, 20)
        # out format comboBox
        self.formatComboBox = QComboBox(self)
        self.formatComboBox.resize(70, 20)
        self.formatComboBox.move(65, 20)
        self.formatComboBox.addItem("png")
        self.formatComboBox.addItem("tiff")
        self.formatComboBox.addItem("jpg")
        # base satellite text
        self.baseSatelliteText = QLabel(self)
        self.baseSatelliteText.setText("base satellite")
        self.baseSatelliteText.resize(75, 20)
        self.baseSatelliteText.move(20, 50)
        # base satellite input
        self.baseSatellite = QLineEdit(self)
        self.baseSatellite.resize(120, 20)
        self.baseSatellite.move(105, 50)
        self.baseSatellite.setText("G02,E08,R02,C06")
        # base dpi text
        self.dpiText = QLabel(self)
        self.dpiText.setText("dpi")
        self.dpiText.resize(40, 20)
        self.dpiText.move(20, 80)
        # base dpi input
        self.dpi = QLineEdit(self)
        self.dpi.resize(80, 20)
        self.dpi.move(60, 80)
        self.dpi.setText("600")
        # title check
        self.titleCheck = QCheckBox(self)
        self.titleCheck.setText("title")
        self.titleCheck.move(20, 110)
        self.titleCheck.setChecked(True)
        # Lenged check
        self.pcoCheck = QCheckBox(self)
        self.pcoCheck.setText("Lenged")
        self.pcoCheck.move(80, 110)
        self.pcoCheck.setChecked(True)
        # log check
        self.logCheck = QCheckBox(self)
        self.logCheck.setText("log")
        self.logCheck.move(150, 110)
        self.logCheck.setChecked(False)
        # base log path
        self.logText = QLabel(self)
        self.logText.setText("log Path:")
        self.logText.resize(50, 20)
        self.logText.move(20, 140)
        # log input
        self.logEdit = QLineEdit(self)
        self.logEdit.resize(200, 20)
        self.logEdit.move(80, 140)
        # log button
        self.logButton = QPushButton(self)
        self.logButton.resize(50, 20)
        self.logButton.move(290, 140)
        self.logButton.setText("...")
        self.logButton.clicked.connect(self.logButtonClick)
        # ignore text
        self.ignoreText = QLabel(self)
        self.ignoreText.setText("ignore prn:")
        self.ignoreText.resize(70, 20)
        self.ignoreText.move(20, 170)
        # ignore input
        self.ignore = QLineEdit(self)
        self.ignore.resize(200, 20)
        self.ignore.move(100, 170)
        return

    def getSettingData(self, printLogSignal=None):
        data = {
            "baseSatellite": self.baseSatellite.text(),
            "dpi": self.dpi.text(),
            "imgFormat": self.formatComboBox.currentText(),
            "log": self.logCheck.isChecked(),
            "logPath": self.logEdit.text(),
            "noLenged": not self.pcoCheck.isChecked(),
            "noTitle": not self.pcoCheck.isChecked(),
            "ignore": self.ignore.text(),
        }
        return data

    @Slot()
    def logButtonClick(self):
        fileDilog = QFileDialog(self)
        filePath = fileDilog.getExistingDirectory(self, "Open log Path", "")
        self.logEdit.setText(filePath)
