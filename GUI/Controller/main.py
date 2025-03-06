import sys, os
import numpy as np
from collections import deque
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer

if __package__ == "Controller":
    from .led import LedColor
    from .GUI import ChannelStatus, BoardStatus, SerialDev_UI
else:
    from led import LedColor
    from GUI import ChannelStatus, BoardStatus, SerialDev_UI

from SerialPort import SerialDevice, getSerialDevices


def fromComplex1toInt(data: int, bitSize: int = 8) -> int:
    sign = 1
    if data & (1 << (bitSize - 1)):
        sign = -1
        data = ~data
    return sign * (data & ((1 << bitSize) -1))

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
    def __init__(self):
        super().__init__()
        self.onRead = False
        self.waitOnWrite = False
        self.setWindowTitle("Serial PM controller")

        self.serial = SerialDevice()
        self.sendDataQueue = deque()
        self.isDataToSend = False
        self.readCmd = {
            "RS":  {"END LINE": "GBT",  "handler": self.RS_read},
            "RF":  {"END LINE": "CFD",  "handler": self.RF_read},
            "RT":  {"END LINE": "OK",   "handler": self.RT_read},
            "RZ":  {"END LINE": "OK",   "handler": self.RZ_read},
            "RC":  {"END LINE": None,   "handler": self.RC_read},
            "RA":  {"END LINE": "OK",   "handler": self.RA_read},
            "SEND":{"END LINE": None,   "handler": self._serialSend}
        }



        self.channelComboBox = QtWidgets.QComboBox(self)
        self.channelComboBox.addItems([f"Channel {i+1}" for i in range(12)])


        self.grid = QtWidgets.QGridLayout(self)



        self.serial_UI      = SerialDev_UI(self.serial, "FIT PM\nUART:")
        self.channelStatus  = ChannelStatus()
        self.boardStatus    = BoardStatus()

        self.serialConnectLayout = QtWidgets.QVBoxLayout()
        self.serialConnectLayout.addWidget(self.channelComboBox)
        self.serialConnectLayout.addWidget(self.serial_UI)
        self.serialConnectLayout.addStretch()


        self.grid.addWidget(self.channelStatus,         0, 0, 2, 1)
        self.grid.addLayout(self.serialConnectLayout,   0, 1)
        self.grid.addWidget(self.boardStatus,           1, 1)

        self.serial_UI.serialConnectButton.clicked.connect(self.connectionToCom)



        self.buttonEnter_connect()
        self.serialTimer = QTimer(self)
        self.serialTimer.setInterval(100)
        self.serialTimer.timeout.connect(self.serialUpdateData)







    def dataEnter_connect(self):
        self.channelStatus.RC_lCal_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SCL", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RC_lCal_setValue))
        self.channelStatus.RC_TimeShift_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SCT", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RC_TimeShift_setValue))

        self.channelStatus.RF_threshold_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SL", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_threshold_setValue))
        self.channelStatus.RF_shift_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SZ", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_shift_setValue))
        self.channelStatus.RF_zeroOffset_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SO", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_zeroOffset_setValue))
        self.channelStatus.RF_delay_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SD", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_delay_setValue))

        self.channelStatus.TRG_orGate_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "ST", sender= self.channelStatus.TRG_orGate_setValue))
        self.channelStatus.TRG_chargeHigh_setValue.returnPressed.connect(lambda: self.serial_send(cmd= "SS", sender= self.channelStatus.TRG_chargeHigh_setValue))

    def buttonEnter_connect(self):
        self.channelStatus.RC_lCal_setButton.clicked.connect(lambda: self.serial_send(cmd= "SCL", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RC_lCal_setValue))
        self.channelStatus.RC_TimeShift_setButton.clicked.connect(lambda: self.serial_send(cmd= "SCT", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RC_TimeShift_setValue))

        self.channelStatus.RF_threshold_setButton.clicked.connect(lambda: self.serial_send(cmd= "SL", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_threshold_setValue))
        self.channelStatus.RF_shift_setButton.clicked.connect(lambda: self.serial_send(cmd= "SZ", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_shift_setValue))
        self.channelStatus.RF_zeroOffset_setButton.clicked.connect(lambda: self.serial_send(cmd= "SO", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_zeroOffset_setValue))
        self.channelStatus.RF_delay_setButton.clicked.connect(lambda: self.serial_send(cmd= "SD", channel= self.channelComboBox.currentIndex(), sender= self.channelStatus.RF_delay_setValue))

        self.channelStatus.TRG_orGate_setButton.clicked.connect(lambda: self.serial_send(cmd= "ST", sender= self.channelStatus.TRG_orGate_setValue))
        self.channelStatus.TRG_chargeHigh_setButton.clicked.connect(lambda: self.serial_send(cmd= "SS", sender= self.channelStatus.TRG_chargeHigh_setValue))


    def io_timerStart(self):
        self.currentSerialInstruction = "RS"
        self.serialTimer.start()

    def io_timerStop(self):
        self.serialTimer.stop()

    def serialUpdateData(self):
        if self.isDataToSend and not self.onRead:
            self._serialSend()
        elif self.readCmd[self.currentSerialInstruction]["handler"]():
            self.onRead = False
            instructions = list(self.readCmd.keys())
            try:
                nextInstruction = instructions[instructions.index(self.currentSerialInstruction) + 1]
            except IndexError:
                nextInstruction = instructions[0]
            self.currentSerialInstruction = nextInstruction



    @QtCore.Slot()
    def connectionToCom(self):
        if self.serial_UI.serialConnectButton.isChecked():
            if self.serial.isOpen:
                self.io_timerStart()
        else:
            self.io_timerStop()


    @QtCore.Slot()
    def RS_read(self):
        if  not self.onRead:
            self.serial.write("RS")
            self.onRead = True

        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:
                if line.startswith("Syntax error"):
                    self.onRead = False
                    return False


                worlds = line.split()

                if line.startswith("Board S/N"):
                    self.boardStatus.SN_value.setText(f"0x{worlds[2]}")

                if line.startswith("Temperature"):
                    self.boardStatus.temperature_value.setText(f"{worlds[-2]}°C")
                    self.boardStatus.temperature_status.setText(worlds[-1])

                if line.startswith("External power"):
                    self.boardStatus.extPowSrc_led.setStatus("ok" == worlds[-1].lower())

                if line.startswith("Board power"):
                    self.boardStatus.boardPower_led.setStatus(True)
                    if worlds[-1].lower() != "ok":
                        self.boardStatus.boardPower_led.setColor(LedColor.RED)
                    else:
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

                if line.startswith(self.readCmd["RS"]["END LINE"]):
                    self.onRead = False
                    return True

        return False


    @QtCore.Slot()
    def RF_read(self):
        if not self.onRead:
            self.serial.write("RF")
            self.lineNumber = 0
            self.onRead = True

        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:
                if line.startswith("Syntax error"):
                    self.onRead = False
                    return False



                line = removeChars(line, ":")
                # line = line.replace("\t", " ")
                # words = removeEmptyStr(line.split())
                words = line.split()

                if self.lineNumber == self.channelComboBox.currentIndex():
                    self.channelStatus.RF_threshold_getValue.setText(str(int(float(words[words.index("Treshold") + 1]) * 100)))
                    self.channelStatus.RF_delay_getValue.setText(str(int(float(words[words.index("Delay") + 1])*1000)))
                    self.channelStatus.RF_shift_getValue.setText(str(int(float(words[words.index("Shift") + 1])*100)))
                    self.channelStatus.RF_zeroOffset_getValue.setText(str(int(float(words[words.index("offs") + 1]) * 100)))

                elif self.lineNumber == 12:
                    self.channelStatus.TRG_orGate_getValue.setText(words[-1])
                elif self.lineNumber == 13:
                    self.channelStatus.TRG_chargeHigh_getValue.setText(words[-1])
                self.lineNumber = self.lineNumber + 1


                if line.startswith(self.readCmd["RF"]["END LINE"]):
                    self.onRead = False
                    return True
        return False

    @QtCore.Slot()
    def RC_read(self):
        if not self.onRead:
            self.serial.write("RC")
            self.lineNumber = 0
            self.onRead = True


        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:
                if line.startswith("Syntax error"):
                    self.onRead = False
                    return False



                if self.lineNumber == self.channelComboBox.currentIndex():
                    words = line.split()
                    self.channelStatus.RC_lCal_getValue.setText(words[3])
                    self.channelStatus.RC_TimeShift_getValue.setText(words[8])
                    self.channelStatus.RC_ADC0_rangeCorr_getValue.setText(words[11])
                    self.channelStatus.RC_ADC1_rangeCorr_getValue.setText(words[12])

                if self.lineNumber >= 11:
                    self.onRead = False
                    return True
                self.lineNumber = self.lineNumber + 1
        return False



    @QtCore.Slot()
    def RT_read(self):
        if not self.onRead:
            self.serial.write("RT")
            print("Send RT")
            self.lineNumber = -1
            self.onRead = True

        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:
                print(line)
                if line.startswith("Syntax error"):
                    self.onRead = False
                    return False

                if line.startswith(self.readCmd["RT"]["END LINE"]):
                    self.onRead = False
                    return True

                if self.lineNumber == -1:
                    self.lineNumber = self.lineNumber + 1
                    return False

                words = line.split()
                if self.lineNumber == self.channelComboBox.currentIndex():
                    self.channelStatus.RT_TDC_FPGA_value.setText(f"0x{words[0][0:2]}")
                    self.channelStatus.RT_TDC_ASIC_value.setText(f"0x{words[0][2:4]}")
                    tdc = (int(words[1][0:2], base= 16)*64) + fromComplex1toInt(int(words[0][2:4], base= 16), 7)
                    self.channelStatus.TDC_raw_value.setText(f"{tdc}")
                    self.lineNumber = self.lineNumber + 1


        return False


    @QtCore.Slot()
    def RZ_read(self):
        if not self.onRead:
            self.serial.write("RZ")
            self.lineNumber = 0
            self.onRead = True


        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:

                if line.startswith("Syntax error"):
                    self.onRead = False
                    return False

                if line.startswith(self.readCmd["RZ"]["END LINE"]):
                    self.onRead = False
                    return True


                if self.lineNumber == self.channelComboBox.currentIndex():
                    words = line.split()
                    self.channelStatus.RZ_ADC0_baseLine_value.setText(words[0])
                    self.channelStatus.RZ_ADC1_baseLine_value.setText(words[1])
                    self.channelStatus.RZ_ADC0_RMS_value.setText(f"{np.sqrt(float(words[2])):.2f}")
                    self.channelStatus.RZ_ADC1_RMS_value.setText(f"{np.sqrt(float(words[3])):.2f}")

                self.lineNumber = self.lineNumber + 1
        return False

    @QtCore.Slot()
    def RA_read(self):
        if not self.onRead:
            self.serial.write("RA")
            self.lineNumber = 0
            self.onRead = True

        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:
                if line.startswith(self.readCmd["RA"]["END LINE"]):
                    self.onRead = False
                    return True

                if self.lineNumber == self.channelComboBox.currentIndex():
                    words = line.split()
                    for i, value in enumerate(words):
                        words[i] = float(value)
                    self.channelStatus.RA_ADC0_meanAmp_value.setText(str(words[0]) if words[0] < 65536/2 else str(words[0] - 65536))
                    self.channelStatus.RA_ADC1_meanAmp_value.setText(str(words[1]) if words[1] < 65536/2 else str(words[1] - 65536))

                self.lineNumber = self.lineNumber + 1
        return False

    @QtCore.Slot()
    def serial_send(self, cmd: str, sender: QtWidgets.QLineEdit, channel: int | None = None):
        try:
            value = str2int(sender.text())
        except ValueError:
            sender.clearFocus()
            return

        data = f"{cmd}{channel if channel is not None else ''} {value}"
        self.sendDataQueue.append(data)
        self.isDataToSend = True
        # self.serial.write(f"{cmd}{channel if channel is not None else ""} {value}")
        sender.clearFocus()

    def _serialSend(self):
        if not self.waitOnWrite:
            try:
                self.serial.write(self.sendDataQueue.popleft())
            except IndexError:
                return True
            self.waitOnWrite = True

        while self.serial.toRead:
            line = self.serial.readLine()
            if line is not None:
                self.waitOnWrite = False
                self.isDataToSend = False
                # print(f"Read line: {line}")
                # if not line.startswith("OK"):
                    # print("Invalid syntax")
                return True
        return False





if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainApp()
    args = sys.argv[1:]
    if len(args) > 0:
        window.serial_UI.setPort(args[0])
    window.resize(800, 400)
    window.show()

    status = app.exec()
    window.serial.close()
    sys.exit(status)