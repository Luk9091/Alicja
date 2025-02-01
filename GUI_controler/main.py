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

def str2int(value: str):
    if value.startswith("0x"):
        data = int(value[2:], 16)
    elif value.startswith("0b"):
        data = int(value[2:], 2)
    else:
        data = int(value)

    return data



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

        self.channelComboBox = QtWidgets.QComboBox(self)
        self.channelComboBox.addItems([f"Channel {i+1}" for i in range(12)])


        self.grid = QtWidgets.QGridLayout(self)

        self.serialConnectLayout = QtWidgets.QVBoxLayout()
        self.serialConnectLayout.addWidget(self.channelComboBox)
        self.serialConnectLayout.addWidget(self.serialDevComboBox)
        self.serialConnectLayout.addWidget(self.serialConnectButton)
        self.serialConnectLayout.addStretch()


        self.channelStatus = ChannelStatus()
        self.boardStatus = BoardStatus()



        self.grid.addWidget(self.channelStatus,         0, 1, 2, 1)
        self.grid.addLayout(self.serialConnectLayout,   0, 2)
        self.grid.addWidget(self.boardStatus,           1, 2)

        self.serialDevShowPopup = self.serialDevComboBox.showPopup
        self.serialDevComboBox.showPopup = self.updateSerialDevice

        self.serialConnectButton.clicked.connect(self.connectionToCom)
        # self.serialDevComboBox.currentIndexChanged.connect(self.changeSerialDev)

        self.channelStatus.RC_lCal_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SCL", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RC_lCal_setValue))
        self.channelStatus.RC_TDC_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SCT", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RC_TDC_setValue))

        self.channelStatus.RF_threshold_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SL", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_threshold_setValue))
        self.channelStatus.RF_shift_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SZ", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_shift_setValue))
        self.channelStatus.RF_zeroOffset_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SO", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_zeroOffset_setValue))
        self.channelStatus.RF_delay_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SD", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_delay_setValue))

        self.channelStatus.TRG_orGate_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SD", sender= self.channelStatus.TRG_orGate_setValue))
        self.channelStatus.TRG_chargeHigh_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SD", sender= self.channelStatus.TRG_chargeHigh_setValue))

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
    def updateSerialDevice(self):
        current = self.serialDevComboBox.currentText()
        self.serialDevComboBox.clear()
        devList = serialDev.getDevList()
        self.serialDevComboBox.addItems(devList)
        self.serialDevShowPopup()
        if current not in devList:
            self.changeSerialDev()
        else:
            self.serialDevComboBox.setCurrentText(current)


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
                    self.channelStatus.RF_threshold_getValue.setText(str(int(float(words[words.index("Treshold") + 1]) * 100)))
                    self.channelStatus.RF_delay_getValue.setText(str(int(float(words[words.index("Delay") + 1])*1000)))
                    self.channelStatus.RF_shift_getValue.setText(str(int(float(words[words.index("Shift") + 1])*100)))
                    self.channelStatus.RF_zeroOffset_getValue.setText(str(int(float(words[words.index("offs") + 1]) * 100)))

                elif lineNumber == 12:
                    self.channelStatus.TRG_orGate_getValue.setText(words[-1])
                elif lineNumber == 13:
                    self.channelStatus.TRG_chargeHigh_getValue.setText(words[-1])
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
                    # self.channelStatus.RC_timeShift_value.setText(words[8])
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

    @QtCore.Slot()
    def serial_send(self, cmd: str, sender: QtWidgets.QLineEdit, channel: int | None = None):
        try:
            value = str2int(sender.text())
        except ValueError:
            sender.clearFocus()
            return

        self.serial.write(f"{cmd}{channel if channel is not None else ""} {value}")
        sender.clearFocus()
        print(self.serial.read())






if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainApp()
    args = sys.argv[1:]
    if len(args) > 0:
        widget.setChannel(args[0])
    widget.resize(1200, 300)
    widget.show()

    status = app.exec()
    widget.serial.disconnect()
    sys.exit(status)