from PySide6 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

if __package__ == "PlotHist":
    from .plot import MplCanvas
    from .SerialDev_UI import SerialDev_UI
else:
    from plot import MplCanvas
    from SerialDev_UI import SerialDev_UI



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



class Canvas_UI(QtWidgets.QWidget):
    def __init__(self, minWith = 300, minHeight = 200, parent = None):
        super().__init__(parent= parent)
        self.ok_transmission = 0
        self.er_transmission = 0
        self.canvas = MplCanvas(self)
        self.canvas.setMinimumWidth(minWith)
        self.canvas.setMinimumHeight(minHeight)
        toolbar = NavigationToolbar2QT(self.canvas)


        error_label     = QtWidgets.QLabel("Error")
        self.errorValue = QtWidgets.QLabel("0/\n0")
        self.errorBar   = QtWidgets.QProgressBar()
        self.errorBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.errorBar.setTextVisible(False)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(error_label,       1, 1, 1, 1)
        layout.addWidget(self.errorValue,   2, 1, 1, 1)
        layout.addWidget(self.errorBar,     3, 1, 3, 1)
        layout.addWidget(self.canvas,       1, 2, 5, 1)
        layout.addWidget(toolbar,           6, 2, 1, 1)


    def clearError(self):
        self.ok_transmission = 0
        self.er_transmission = 0
        self.updateError()

    def addTransmission(self, value: int = 1):
        self.ok_transmission = self.ok_transmission + value
    def addError(self, value: int = 1):
        self.er_transmission = self.er_transmission + value

    def updateError(self):
        self.errorValue.setText(f"{self.er_transmission}/\n{self.ok_transmission}")
        self.errorBar.setValue(self.er_transmission)

    def clear(self):
        self.canvas.clearPlot()
        self.clearError()