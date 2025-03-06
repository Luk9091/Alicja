
import sys
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui

import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from collections import deque
import struct

from serialDev import Device


def bytes_to_custom_int(byte_data):
    return int(''.join(str(byte) for byte in byte_data))


class MplCanvas(FigureCanvasQTAgg, QtWidgets.QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        numOfRow  = 1
        numOfCols = 1


        self.axes = fig.add_subplot(numOfRow, numOfCols, 1)
        super().__init__(fig)


    def clearPlot(self):
        self.axes.clear()

    def grid(self):
        self.axes.grid(True)

    def getDiff(self, data: list) -> list:
        diff = data[1:-1] - data[0:-2]
        return diff

    @QtCore.Slot()
    def updatePlot(self, dataRaw: list):
        data = []
        for i, value in enumerate(dataRaw):
            data.append(value & 0x3FFF)


        self.clearPlot()
        self.axes.plot(data)
        # self.axes.plot(self.getDiff(data))

        self.grid()

        self.draw()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial = Device()
        self.serial.connect()
        self.serial.startReadRoutine()
        self.serial.write("OK")


        self.sc = MplCanvas(self)
        toolbar = NavigationToolbar2QT(self.sc, self)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(toolbar, 1, 1)
        layout.addWidget(self.sc, 2, 1)


        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


        self.data = deque(maxlen=int(65536/4))

        self.dataTimer = QtCore.QTimer()
        self.dataTimer.setInterval(10)
        self.dataTimer.timeout.connect(self.updateData)
        self.index = 0
        self.dataTimer.start()


    def updateData(self):
        if not self.serial.toRead():
            return
        self.index = self.index + 1
        if self.index % 3 == 0:
            self.updatePlots()

        data = self.serial.read()

        values = struct.unpack("<" + "H"*(len(data)//2), data)
        self.data.extend(values)

        print(f"{self.index: 3}\tTo read: {self.serial.toRead()}, samples: {len(data)}")
        if (self.index >= 65536/4):
            self.dataTimer.stop()
            self.updatePlots()



    def updatePlots(self):
        self.sc.updatePlot(self.data)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainApp()



    status = app.exec()
    w.serial.close()
    sys.exit(status)