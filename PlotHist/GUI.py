from PySide6 import QtCore, QtWidgets, QtGui

from serialDev import Device, getDevList as getSerialDevList



class SerialDev_UI(QtWidgets.QWidget):
    def __init__(self, serial: Device, parent = None):
        super().__init__(parent)
        self.serial = serial


        self.serialDevComboBox = QtWidgets.QComboBox(self)
        self.serialDevComboBox.addItems(getSerialDevList())

        self.serialConnectButton = QtWidgets.QPushButton(parent=self, text="Connect")
        self.serialConnectButton.setCheckable(True)




        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.serialDevComboBox, 1, 1, 1, 1)
        lay.addWidget(self.serialConnectButton, 2, 1, 1, 1)


        self.serialDevShowPopup = self.serialDevComboBox.showPopup
        self.serialDevComboBox.showPopup = self.updateSerialDevice

        self.serialConnectButton.clicked.connect(self.connectionToCom)
        self.serialDevComboBox.currentIndexChanged.connect(self.changeSerialDev)


    @QtCore.Slot()
    def updateSerialDevice(self):
        self.serialDevComboBox.currentIndexChanged.disconnect(self.changeSerialDev)
        current = self.serialDevComboBox.currentText()
        self.serialDevComboBox.clear()
        devList = getSerialDevList()
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
            if self.serial.connect(self.serialDevComboBox.currentText()):
                self.serialConnectButton.setText("Disconnect")
                self.serial.readQueue.clear()
                self.serial.startReadRoutine()

            else:
                self.serialConnectButton.setChecked(False)
        else:
            if self.serial.isOpen:
                self.serial.close()

            self.serialConnectButton.setText("Connect")

    def setChannel(self, serialPort: str):
        if serialPort not in getSerialDevList():
            return

        if self.serialConnectButton.isChecked():
            if self.serial.isOpen:
                self.serial.close()

            self.serialConnectButton.setChecked(False)
            self.serialConnectButton.setText("Connect")

        self.serialDevComboBox.setCurrentText(serialPort)



class PlotControl_UI(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.runButton           = QtWidgets.QPushButton("Run")
        self.runButton.setCheckable(True)

        self.clearButton         = QtWidgets.QPushButton("Clear")

        self.autoAlignLabel      = QtWidgets.QLabel("Auto align:")
        self.autoAlignCheckBox   = QtWidgets.QCheckBox()
        self.autoAlignCheckBox.setChecked(True)

        self.aliment_ADCLabel    = QtWidgets.QLabel("ADC:")
        self.aliment_ADCHighEdit = QtWidgets.QLineEdit("10")
        self.aliment_ADCLowEdit  = QtWidgets.QLineEdit("-10")

        self.aliment_TDCLabel    = QtWidgets.QLabel("TDC:")
        self.aliment_TDCHighEdit = QtWidgets.QLineEdit("10")
        self.aliment_TDCLowEdit  = QtWidgets.QLineEdit("-10")



        layout = QtWidgets.QGridLayout(self)

        layout.addWidget(self.autoAlignLabel,       1, 1, 1, 2)
        layout.addWidget(self.autoAlignCheckBox,    1, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.aliment_TDCLabel,     2, 1, 1, 1)
        layout.addWidget(self.aliment_TDCHighEdit,  2, 3, 1, 1)
        layout.addWidget(self.aliment_TDCLowEdit,   2, 2, 1, 1)

        layout.addWidget(self.aliment_ADCLabel,     3, 1, 1, 1)
        layout.addWidget(self.aliment_ADCHighEdit,  3, 3, 1, 1)
        layout.addWidget(self.aliment_ADCLowEdit,   3, 2, 1, 1)
        layout.addWidget(self.runButton,            4, 1, 1, 3)
        layout.addWidget(self.clearButton,          5, 1, 1, 3)



    def getTimeLimes(self) -> tuple[int, int] | None:
        if self.autoAlignCheckBox.isChecked():
            return None

        minValue = int(self.aliment_TDCLowEdit.text())
        maxValue = int(self.aliment_TDCHighEdit.text())

        return [minValue, maxValue]

    def getChargeLimes(self) -> tuple[int, int] | None:
        if self.autoAlignCheckBox.isChecked():
            return None

        minValue = int(self.aliment_ADCLowEdit.text())
        maxValue = int(self.aliment_ADCHighEdit.text())

        return [minValue, maxValue]
