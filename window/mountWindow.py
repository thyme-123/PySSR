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

class MountWindow(QWidget):

    def __init__(self, data, dirPath, type):
        super().__init__(None)
        if type == "eph":
            self.typeList = ["1019", "1020", "1042", "1045", "1046"]
        elif type == "ssr":
            self.typeList = ["1060", "1066"]
        self.dirPath = dirPath
        self.selectButton = QPushButton(self)
        self.selectButton.resize(120,50)
        self.selectButton.move(40, 350)
        self.selectButton.setText("select")
        self.selectButton.clicked.connect(self.selectButtonClick)
        self.closeButton = QPushButton(self)
        self.closeButton.resize(120, 50)
        self.closeButton.move(180, 350)
        self.closeButton.setText("close")
        self.closeButton.clicked.connect(self.closeButtonClick)
        self.casterTable = QTableWidget(self)
        self.casterTable.setColumnCount(1)
        self.casterTable.setHorizontalHeaderLabels(
            ["mount"])
        self.casterTable.resize(200, 200)
        self.casterTable.setColumnWidth(0, 190)
        self.casterTable.move(20, 20)
        # self.casterTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        for casterStr in data:
            casterData = casterStr.split(";")
            if not casterData:
                continue
            elif casterData[0] == "CAS":
                continue
            elif casterData[0] == "NET":
                continue
            elif casterData[0] == "STR":
                casterName = casterData[1]
                typeData = casterData[4]
                for t in self.typeList:
                    if t in typeData:
                        qItem = QTableWidgetItem()
                        qItem.setText(casterName)
                        self.casterTable.insertRow(self.casterTable.rowCount())
                        self.casterTable.setItem(self.casterTable.rowCount() - 1, 0, qItem)
                        break

    @Slot()
    def selectButtonClick(self):
        for index in range(self.casterTable.rowCount()):
            if self.casterTable.item(index, 0).isSelected():
                self.dirPath.setText(self.casterTable.item(index, 0).text())
                return self.close()

    @Slot()
    def closeButtonClick(self):
        return self.close()