import os

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QDialog, QPushButton
from PySide6 import QtCore
from PySide6 import QtGui

from window import RepairWindow, PlotWindow
from window import RtWindow
from window import IntegrityWindow
from window import SettingWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySSR")
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.resize(800, 600)
        self.settingWindow = SettingWindow.SeetingWindow(self)
        self.repairWindow = RepairWindow.RepairWindow(self.settingWindow, self)
        self.plotWindow = PlotWindow.PlotWindow(self.settingWindow, self)
        self.rtWindow = RtWindow.RtWindow(self)
        self.integrityWindow = IntegrityWindow.IntegrityWindow(self)
        self.tabWidget.addTab(self.repairWindow, "ssr repair")
        self.tabWidget.addTab(self.plotWindow, "diff plot")
        self.tabWidget.addTab(self.rtWindow, "rt data")
        self.tabWidget.addTab(self.integrityWindow, "integrity")
        self.tabWidget.addTab(self.settingWindow, "setting")
        return

    def getSettingData(self):
        return self.settingWindow.getSettingData()