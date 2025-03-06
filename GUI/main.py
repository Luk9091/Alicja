import sys
from PySide6 import QtCore, QtWidgets

from Controller import Controller_UI
from PlotHist import PlotHist_UI


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial controller and histogram")

        self.controller_ui = Controller_UI()
        self.histogram_ui = PlotHist_UI()
        controller_box = QtWidgets.QGroupBox("Controller")
        histogram_box = QtWidgets.QGroupBox("Histogram")

        controller_box.setLayout(self.controller_ui.grid)
        histogram_box.setLayout(self.histogram_ui.grid)



        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(controller_box)
        layout.addWidget(histogram_box)

    def serialClose(self):
        self.controller_ui.serial.close()
        self.histogram_ui.serial.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainApp()
    window.resize(400, 800)
    window.show()

    status = app.exec()
    window.serialClose()
    sys.exit(status)

