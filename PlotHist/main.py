import sys
import random
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui, QtGraphs

import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from collections import deque
import struct

from GUI import SerialDev_UI, PlotControl_UI
from serialDev import Device


def bytes_to_custom_int(byte_data):
    return int(''.join(str(byte) for byte in byte_data))


class MplCanvas(FigureCanvasQTAgg, QtWidgets.QWidget):
    def __init__(self, parent=None, width=200, height=200, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        numOfRow  = 1
        numOfCols = 2


        self.axes_Time = fig.add_subplot(numOfRow, numOfCols, 1)
        self.axes_Charge = fig.add_subplot(numOfRow, numOfCols, 2)
        super().__init__(fig)


    def clearPlot(self):
        self.axes_Time.clear()
        self.axes_Charge.clear()

    def grid(self):
        self.axes_Time.grid(True)
        self.axes_Charge.grid(True)

    @QtCore.Slot()
    def updatePlot(self, time: dict, charge_1: dict, charge_2: dict, timeLimes: tuple[int, int] | None = None, chargeLimes: tuple[int, int] | None = None):
        self.clearPlot()
        self.axes_Time.bar(time.keys(), time.values())
        self.axes_Charge.bar(charge_1.keys(), charge_1.values())
        self.axes_Charge.bar(charge_2.keys(), charge_2.values(), alpha=0.5, color="green")

        if timeLimes is not None:
            self.axes_Time.set_xlim(timeLimes)
        if chargeLimes is not None:
            self.axes_Charge.set_xlim(chargeLimes)

        self.grid()
        self.draw()

class Canvas_UI(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent= parent)
        self.canvas = MplCanvas(self)
        toolbar = NavigationToolbar2QT(self.canvas)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.canvas, 1, 1, 4, 1)
        layout.addWidget(toolbar, 5, 1, 1, 1)


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.last = 0
        self.data = deque(maxlen=int(65536/4))
        self.run = False
        self.dataChange = False
        self.toClear = False
        self.time = {}
        self.charge = [{}, {}]

        self.serial = Device()

        self.canvas_UI = Canvas_UI()
        self.serial_UI = SerialDev_UI(self.serial)
        self.plot_UI = PlotControl_UI()


        self.errorBar = QtWidgets.QProgressBar()
        self.errorBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.errorBar.setTextVisible(False)
        self.errorBar.setValue(-1)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.canvas_UI,        1, 2, 5, 1)
        layout.addWidget(self.errorBar,         2, 1, 3, 1)
        layout.addWidget(self.serial_UI,        1, 3, 1, 1)
        layout.addWidget(self.plot_UI,          5, 3, 1, 1)


        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.serial_UI.serialConnectButton.clicked.connect(self.sendRunCmd)
        self.plot_UI.runButton.clicked.connect(self.sendRunCmd)
        self.plot_UI.clearButton.clicked.connect(self.clearHistogram)


        self.dataTimer = QtCore.QTimer()
        self.dataTimer.setInterval(10)
        self.dataTimer.timeout.connect(self.updateData)

        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.setInterval(500)
        self.plotUpdateTimer.timeout.connect(self.updatePlots)


        self.show()
        self.dataTimer.start()
        self.plotUpdateTimer.start()

    def close(self):
        if self.serial.isOpen:
            self.serial.write("DONE")
            self.serial.close()
            self.errorBar.setValue(0)



    @QtCore.Slot()
    def sendRunCmd(self, run: bool = True):
        if self.serial.isOpen:
            if not self.run and self.plot_UI.runButton.isChecked() and run:
                self.serial.write("OK")
                self.run = True
                self.plot_UI.runButton.setText("Stop")
            else:
                self.serial.write("DONE")
                self.run = False
                self.plot_UI.runButton.setText("Run")
                self.plot_UI.runButton.setChecked(False)
        else:
            self.plot_UI.runButton.setChecked(False)
            self.plot_UI.runButton.setText("Run")

    @QtCore.Slot()
    def clearHistogram(self):
        self.serial.readQueue.clear()
        self.index = 0
        self.canvas_UI.canvas.clearPlot()
        self.canvas_UI.canvas.draw()
        self.errorBar.setValue(0)

    @QtCore.Slot()
    def updateData(self):
        if not self.serial.toRead():
            return

        self.index = self.index + 1
        self.dataChange = True

        data = self.serial.read()

        values = struct.unpack("<" + "H"*(len(data)//2), data)
        self.data.extend(values)

        print(f"{self.index: 3}\tTo read: {self.serial.toRead()}, samples: {len(data)}")


    @QtCore.Slot()
    def updatePlots(self):
        if not self.dataChange:
            return

        self.dataChange = False


        for i, value in enumerate(self.data):
            index = (value >> 14) - 1
            if index == 0:
                diff = value - self.last
                if diff != 1:
                    self.errorBar.setValue(self.errorBar.value() + 1)
                self.last = value
            elif index == 1:
                zipValue = ((value & 0x3F00) >> 1) | value & 0x7F
                try:
                    self.time[zipValue] = self.time[zipValue] + 1
                except KeyError:
                    self.time[zipValue] = 0
                # time.append(zipValue)
            elif index == 2:
                chargeIndex = (value >> 12) & 1
                data = value & 0xFFF
                try:
                    self.charge[chargeIndex][data] = self.charge[chargeIndex][data] + 1
                except KeyError:
                    self.charge[chargeIndex][data] = 0
                # charge[chargeIndex].append(value & 0xFFF)

        if self.run:
            if self.toClear:
                self.toClear = False
                self.time.clear()
                self.charge[0].clear()
                self.charge[1].clear()
            else:
                if (max(self.time.values()) > 65536):
                    self.sendRunCmd(False)
                    self.toClear = True
                if (max(*self.charge[0].values(), *self.charge[1].values()) > 65536):
                    self.sendRunCmd(False)
                    self.toClear = True
            self.canvas_UI.canvas.updatePlot(self.time, self.charge[0], self.charge[1], self.plot_UI.getTimeLimes(), self.plot_UI.getChargeLimes())
        else:
            if self.plot_UI.getTimeLimes() is not None:
                self.canvas_UI.canvas.axes_Time.set_xlim(self.plot_UI.getTimeLimes())
            self.canvas_UI.canvas.draw()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainApp()

    args = sys.argv[1:]
    if len(args) > 0:
        widget.serial_UI.setChannel(args[0])



    status = app.exec()
    widget.close()
    sys.exit(status)