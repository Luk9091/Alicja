from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

from SerialPort import SerialDevice, getSerialDevices

class SerialDev_UI(QtWidgets.QWidget):
    def __init__(self, serial: SerialDevice, serialDevLabel: str, parent = None, serialDevLabel_aliment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft):
        super().__init__(parent)
        self.serial = serial


        self.serialDev_label    = QtWidgets.QLabel(serialDevLabel, alignment=serialDevLabel_aliment)
        self.serialDevComboBox  = QtWidgets.QComboBox(self)
        self.serialDevComboBox.addItems(getSerialDevices())

        self.serialConnectButton = QtWidgets.QPushButton(parent=self, text="Connect")
        self.serialConnectButton.setCheckable(True)




        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.serialDev_label,      1, 1, 1, 1)
        layout.addWidget(self.serialDevComboBox,    1, 2, 1, 1)
        layout.addWidget(self.serialConnectButton,  2, 1, 1, 2)


        self.serialDevShowPopup = self.serialDevComboBox.showPopup
        self.serialDevComboBox.showPopup = self.updateSerialDevice

        self.serialConnectButton.clicked.connect(self.connectionToCom)
        self.serialDevComboBox.currentIndexChanged.connect(self.changeSerialDev)


    @QtCore.Slot()
    def updateSerialDevice(self):
        self.serialDevComboBox.currentIndexChanged.disconnect(self.changeSerialDev)
        current = self.serialDevComboBox.currentText()
        self.serialDevComboBox.clear()
        devList = getSerialDevices()
        self.serialDevComboBox.addItems(devList)
        self.serialDevShowPopup()
        if current not in devList:
            self.changeSerialDev()
        else:
            self.serialDevComboBox.setCurrentText(current)
        self.serialDevComboBox.currentIndexChanged.connect(self.changeSerialDev)


    @QtCore.Slot()
    def changeSerialDev(self):
        if self.serialConnectButton.isChecked():
            if self.serial.isOpen:
                self.serial.close()

            self.serialConnectButton.setChecked(False)
            self.serialConnectButton.setText("Connect")


    @QtCore.Slot()
    def connectionToCom(self):
        if self.serialConnectButton.isChecked():
            if self.serial.open(self.serialDevComboBox.currentText()):
                self.serialConnectButton.setText("Disconnect")
                self.serial.readQueue.clear()

            else:
                self.serialConnectButton.setChecked(False)
        else:
            if self.serial.isOpen:
                self.serial.close()

            self.serialConnectButton.setText("Connect")

    def setPort(self, serialPort: str):
        if serialPort not in getSerialDevices():
            return

        if self.serialConnectButton.isChecked():
            if self.serial.isOpen:
                self.serial.close()

            self.serialConnectButton.setChecked(False)
            self.serialConnectButton.setText("Connect")

        self.serialDevComboBox.setCurrentText(serialPort)