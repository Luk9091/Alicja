from PySide6 import QtCore, QtWidgets, QtGui

import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure



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
        self.grid()
        self.draw()

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