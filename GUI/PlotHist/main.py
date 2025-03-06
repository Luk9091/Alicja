import sys
import random
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

from collections import deque

if __package__ == "PlotHist":
    from .GUI import SerialDev_UI, PlotControl_UI, Canvas_UI
else:
    from GUI import SerialDev_UI, PlotControl_UI, Canvas_UI
from SerialPort import SerialDevice


def bytes_to_custom_int(byte_data):
    return int(''.join(str(byte) for byte in byte_data))





class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.index = 0
        self.last = -1
        self.data = deque()
        self.run = False
        self.toClear = False
        self.time = {}
        self.charge = [{}, {}]
        self.acquisitionSample = 0
        self.acquisitionLimit = 6554 * 3

        self.serial = SerialDevice(readType= "numOfBytes", timeout= 0.2)

        self.setWindowTitle("Histogram draw")

        self.canvas_UI = Canvas_UI(450, 300)
        self.serial_UI = SerialDev_UI(self.serial, "Histogram\npico:", serialDevLabel_aliment=Qt.AlignmentFlag.AlignCenter)
        self.plot_UI = PlotControl_UI()



        self.grid = QtWidgets.QGridLayout(self)

        self.grid.addWidget(self.canvas_UI,        1, 2, 5, 1)
        self.grid.addWidget(self.serial_UI,        1, 3, 1, 1)
        self.grid.addWidget(self.plot_UI,          5, 3, 1, 1)


        self.serial_UI.serialConnectButton.clicked.connect(self.sendRunCmd)
        self.plot_UI.runButton.clicked.connect(self.sendRunCmd)
        self.plot_UI.clearButton.clicked.connect(self.clearHistogram)


        self.dataTimer = QtCore.QTimer()
        self.dataTimer.setInterval(1)
        self.dataTimer.timeout.connect(self.updateData)

        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.setInterval(100)
        self.plotUpdateTimer.timeout.connect(self.updatePlots)


        self.dataTimer.start()
        self.plotUpdateTimer.start()

    def close(self):
        if self.serial.isOpen:
            self.serial.write("DONE")
            self.serial.close()
            self.canvas_UI.clearError()



    @QtCore.Slot()
    def sendRunCmd(self):
        if self.serial.isOpen:
            self.runCmd(not self.run and self.plot_UI.runButton.isChecked())
        else:
            self.plot_UI.runButton.setChecked(False)
            self.plot_UI.runButton.setText("Run")

    def runCmd(self, run: bool = True):
        if run:
            self.serial.clear()
            self.serial.write("OK")
            self.run = True
            self.plot_UI.runButton.setText("Stop")
        else:
            self.serial.write("DONE")
            self.run = False
            self.plot_UI.runButton.setText("Run")
            self.plot_UI.runButton.setChecked(False)


    @QtCore.Slot()
    def clearHistogram(self):
        self.index = 0
        self.acquisitionSample = 0
        self.data.clear()
        self.time.clear()
        self.charge[0].clear()
        self.charge[1].clear()
        self.canvas_UI.clear()
        self.last = -1



    @QtCore.Slot()
    def updateData(self):
        if not self.serial.toRead or not self.run:
            return
        data = self.serial.readListOfValue()
        self.data.append(data)

        self.acquisitionSample = self.acquisitionSample + len(data)
        if (self.acquisitionSample > self.acquisitionLimit):
            self.acquisitionSample = 0
            self.runCmd(False)

        # print(f"{self.index: 3}\tTo read: {self.serial.toRead}, samples: {len(data)*2}")
        self.index = self.index + 1



    @QtCore.Slot()
    def updatePlots(self):
        try:
            data = self.data.popleft()
        except IndexError:
            return

        for i, value in enumerate(data):
            index = (value >> 14) - 1
            if index == 0:
                diff = value - self.last
                if diff != 1 and self.last != -1:
                    self.canvas_UI.addError()
                if value == 16383:
                    self.last = -1
                else:
                    self.last = value
                self.canvas_UI.addTransmission()
                self.canvas_UI.updateError()
            elif index == 1:
                zipValue = ((value & 0x3F00) >> 1) | value & 0x7F
                try:
                    self.time[zipValue] = self.time[zipValue] + 1
                except KeyError:
                    self.time[zipValue] = 0
            elif index == 2:
                chargeIndex = (value >> 12) & 1
                data = value & 0xFFF
                try:
                    self.charge[chargeIndex][data] = self.charge[chargeIndex][data] + 1
                except KeyError:
                    self.charge[chargeIndex][data] = 0

        self.canvas_UI.canvas.updatePlot(self.time, self.charge[0], self.charge[1], self.plot_UI.getTimeLimes(), self.plot_UI.getChargeLimes())




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainApp()

    args = sys.argv[1:]
    if len(args) > 0:
        window.serial_UI.setPort(args[0])

    window.resize(600, 300)
    window.show()


    status = app.exec()
    window.close()
    sys.exit(status)