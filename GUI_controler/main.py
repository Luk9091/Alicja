import sys
from time import sleep
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from led import LedIndicator, LedColor

from GUI import ChannelStatus, BoardStatus


import serialDev
from AD import Analyzer


def removeChars(input_string: str, chars_to_remove: str) -> str:
    return ''.join(char for char in input_string if char not in chars_to_remove)

# def changeChar(input_string: str, toRemove: str, toReplace: str) -> str:



class MainApp(QtWidgets.QWidget):
    cmdList = {
        "RS": {"END LINE": "GBT"},
        "RF": {"END LINE": "CFD"},
        "RT": {"END LINE": "ok"},
        "RZ": {"END LINE": "OK"},
        "RC": {"END LINE": None},
        "RA": {"END LINE": "OK"},
    }


    def __init__(self):
        super().__init__()
        self.serial = serialDev.serialDevice()
        self.analyzer = Analyzer()


        self.serialDevComboBox = QtWidgets.QComboBox(self)
        self.serialDevComboBox.addItems(serialDev.getDevList())
        self.serialConnectButton = QtWidgets.QPushButton(parent=self, text="Connect")
        self.serialConnectButton.setCheckable(True)

        self.statusLabel = QtWidgets.QLabel("Status:")
        self.statusLed =  LedIndicator(self)

        self.channelComboBox = QtWidgets.QComboBox(self)
        self.channelComboBox.addItems([f"Channel {i+1}" for i in range(12)])


        self.grid = QtWidgets.QGridLayout(self)

        self.serialConnectLayout = QtWidgets.QVBoxLayout()
        self.serialConnectLayout.addWidget(self.serialDevComboBox)
        self.serialConnectLayout.addWidget(self.serialConnectButton)
        self.serialConnectLayout.addStretch()

        self.statusLayout = QtWidgets.QVBoxLayout()
        self.statusLayout.addWidget(self.channelComboBox)
        self.statusLayout.addWidget(self.statusLabel)


        self.ledsLayout = QtWidgets.QHBoxLayout()
        self.ledsLayout.addWidget(self.statusLed)

        self.statusLayout.addLayout(self.ledsLayout)
        self.statusLayout.addStretch()

        self.channelStatus = ChannelStatus()
        self.boardStatus = BoardStatus()



        self.grid.addLayout(self.statusLayout,          0, 0)
        self.grid.addWidget(self.channelStatus,         0, 1, 2, 1)
        self.grid.addLayout(self.serialConnectLayout,   0, 2)
        self.grid.addWidget(self.boardStatus,           1, 2)


        self.serialConnectButton.clicked.connect(self.connectionToCom)
        self.serialDevComboBox.currentIndexChanged.connect(self.changeSerialDev)


    @QtCore.Slot()
    def connectionToCom(self):
        if self.serialConnectButton.isChecked():
            if (not self.serial.isOpen()) and self.serial.connect(self.serialDevComboBox.currentText()):
                self.serialConnectButton.setText("Disconnect")
                self.serial.startReadRoutine()

                self.RS_read()
                self.RF_read()
                self.RT_read()
                self.RC_read()
                self.RZ_read()
                self.RA_read()
            else:
                self.serialConnectButton.setChecked(False)
        else:
            if self.serial.isOpen():
                self.serial.disconnect()

            self.serialConnectButton.setText("Connect")


    @QtCore.Slot()
    def changeSerialDev(self):
        if self.serialConnectButton.isChecked():
            if self.serial.isOpen():
                self.serial.disconnect()

            self.serialConnectButton.setChecked(False)
            self.serialConnectButton.setText("Connect")

    def setChannel(self, serialPort: str):
        if serialPort not in serialDev.getDevList():
            return

        if self.serialConnectButton.isChecked():
            if self.serial.isOpen():
                self.serial.disconnect()

            self.serialConnectButton.setChecked(False)
            self.serialConnectButton.setText("Connect")

        self.serialDevComboBox.setCurrentText(serialPort)




    @QtCore.Slot()
    def RS_read(self):
        self.serial.write("RS")

        while True:
            line = self.serial.read()
            if line is not None:
                worlds = line.split()

                if line.startswith("Board S/N"):
                    self.boardStatus.SN_value.setText(f"0x{worlds[2]}")

                if line.startswith("Temperature"):
                    self.boardStatus.temperature_value.setText(f"{worlds[-2]}°C")
                    self.boardStatus.temperature_status.setText(worlds[-1])
                    # if worlds[-1].upper() == "NORMAL":
                    #     self.boardStatus.temperature_status.setStyleSheet("font-weight: bold; background: green")
                    # else:
                    #     self.boardStatus.temperature_status.setStyleSheet("font-weight: bold; background: red")
                    #     self.boardStatus.temperature_value.setStyleSheet("color: red")

                if line.startswith("External power"):
                    self.boardStatus.extPowSrc_led.setStatus("ok" == worlds[-1].lower())

                if line.startswith("Board power"):
                    self.boardStatus.boardPower_led.setStatus(True)
                    if worlds[-1].lower() != "ok":
                        self.boardStatus.boardPower_led.setColor(LedColor.RED)
                        continue

                    self.boardStatus.boardPower_led.setColor(LedColor.GREEN)

                if line.startswith("Clock system"):
                    if worlds[-1].lower() == "ok":
                        self.boardStatus.clock_led.setStatus(True)
                if line.startswith("Clock source"):
                    msg = line.strip("Clock source ")
                    self.boardStatus.clock_source.setText(msg)

                if line.startswith("FPGA"):
                    self.boardStatus.FPGA_led.setStatus(True)
                    if worlds[-1] != "ready":
                        self.boardStatus.FPGA_led.setColor(LedColor.RED)

                if line.startswith("GBT"):
                    if worlds[2].lower() == "on,":
                        self.boardStatus.GBT_led.setStatus(True)
                    if not line.endswith("no errors"):
                        self.boardStatus.GBT_led.setColor(LedColor.RED)

                if line.startswith(self.cmdList["RS"]["END LINE"]):
                    break


    @QtCore.Slot()
    def RF_read(self):
        self.serial.write("RF")
        lineNumber = 0

        while True:
            line = self.serial.read()
            if line is not None:
                line = removeChars(line, ":")
                # line = line.replace("\t", " ")
                # words = removeEmptyStr(line.split())
                words = line.split()

                if lineNumber == self.channelComboBox.currentIndex():
                    self.channelStatus.RF_threshold_getValue.setText(words[words.index("Treshold") + 1])
                    self.channelStatus.RF_delay_getValue.setText(words[words.index("Delay") + 1])
                    self.channelStatus.RF_shift_getValue.setText(words[words.index("Shift") + 1])
                    self.channelStatus.RF_zeroOffset_getValue.setText(words[words.index("offs") + 1])
                lineNumber = lineNumber + 1


                if line.startswith(self.cmdList["RF"]["END LINE"]):
                    break

    @QtCore.Slot()
    def RC_read(self):
        self.serial.write("RC")
        channel = 0

        while True:
            line = self.serial.read()

            if line is not None:
                if channel == self.channelComboBox.currentIndex():
                    words = line.split()
                    self.channelStatus.RC_lCal_getValue.setText(words[3])
                    self.channelStatus.RC_TDC_getValue.setText(words[5])
                    self.channelStatus.RC_timeShift_value.setText(words[8])
                    self.channelStatus.RC_ADC0_rangeCorr_getValue.setText(words[11])
                    self.channelStatus.RC_ADC1_rangeCorr_getValue.setText(words[12])

                if channel == 11:
                    break
                channel = channel + 1



    @QtCore.Slot()
    def RT_read(self):
        self.serial.write("RT")
        lineNumber = -1

        while True:
            line = self.serial.read()
            if line is not None:
                if line.startswith(self.cmdList["RT"]["END LINE"]):
                    break

                if lineNumber == -1:
                    lineNumber = lineNumber + 1
                    continue

                words = line.split()
                if lineNumber == self.channelComboBox.currentIndex():
                    self.channelStatus.RT_TDC_FPGA_value.setText(f"0x{words[0][0:2]}")
                    self.channelStatus.RT_TDC_ASIC_value.setText(f"0x{words[0][2:4]}")


                lineNumber = lineNumber + 1



    @QtCore.Slot()
    def RZ_read(self):
        self.serial.write("RZ")
        channel = 0

        while True:
            line = self.serial.read()
            if line is not None:
                if line.startswith(self.cmdList["RZ"]["END LINE"]):
                    break

                if channel == self.channelComboBox.currentIndex():
                    words = line.split()
                    self.channelStatus.RZ_ADC0_baseLine_value.setText(words[0])
                    self.channelStatus.RZ_ADC1_baseLine_value.setText(words[1])
                    self.channelStatus.RZ_ADC0_RMS_value.setText(f"{np.sqrt(float(words[2])):.2f}")
                    self.channelStatus.RZ_ADC1_RMS_value.setText(f"{np.sqrt(float(words[3])):.2f}")


                channel = channel + 1

    @QtCore.Slot()
    def RA_read(self):
        self.serial.write("RA")
        channel = 0

        while True:
            line = self.serial.read()
            if line is not None:
                if line.startswith(self.cmdList["RA"]["END LINE"]):
                    break

                if channel == self.channelComboBox.currentIndex():
                    words = line.split()
                    for i, value in enumerate(words):
                        words[i] = float(value)
                    self.channelStatus.RA_ADC0_meanAmp_value.setText(str(words[0]) if words[0] < 65536/2 else str(words[0] - 65536))
                    self.channelStatus.RA_ADC1_meanAmp_value.setText(str(words[1]) if words[1] < 65536/2 else str(words[1] - 65536))

                channel = channel + 1



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainApp()
    args = sys.argv[1:]
    widget.setChannel(args[0])
    widget.resize(1200, 300)
    widget.show()

    status = app.exec()
    widget.serial.disconnect()
    sys.exit(status)