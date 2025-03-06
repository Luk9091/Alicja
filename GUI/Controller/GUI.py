from PySide6 import QtCore, QtWidgets, QtGui


if __package__ == "Controller":
    from .led import LedIndicator
    from .SerialDev_UI import SerialDev_UI
else:
    from led import LedIndicator
    from SerialDev_UI import SerialDev_UI


def str2int(value: str):
    value = value.replace(" ", "")
    if value.startswith("0x"):
        data = int(value[2:], 16)
        base = 16
    elif value.startswith("0b"):
        data = int(value[2:], 2)
        base = 2
    else:
        data = int(value)
        base = 10

    return data, base

def int2str(value: int, base: int= 10):
    if base == 16:
        out = hex(value)
        out = out[2:].upper()
        return f"0x{out}"
    elif base == 2:
        return bin(value)
    else:
        return f"{value}"

class ChannelStatus(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ChannelStatus, self).__init__(parent)

        channel0BoxGroup = QtWidgets.QGroupBox(self)
        channel1BoxGroup = QtWidgets.QGroupBox(self)
        channel0BoxLayout = QtWidgets.QGridLayout()
        channel1BoxLayout = QtWidgets.QGridLayout()
        channelSettingBoxGroup = QtWidgets.QGroupBox(self)
        channelSettingBoxLayout = QtWidgets.QGridLayout()


        ADCBoxGroup = QtWidgets.QGroupBox(self)
        ADCBoxLayout = QtWidgets.QGridLayout()

        TDCBoxGroupe = QtWidgets.QGroupBox(self)
        TDCBoxLayout = QtWidgets.QGridLayout()

        TRGBoxGroupe = QtWidgets.QGroupBox(self)
        TRGBoxLayout = QtWidgets.QGridLayout()




        self.RC_lCal_label = QtWidgets.QLabel("Threshold calibration", self)
        self.RC_lCal_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.RC_lCal_setValue = QtWidgets.QLineEdit(self)
        self.RC_lCal_setButton = QtWidgets.QPushButton("⎆")
        buttonSize = QtCore.QSize(self.RC_lCal_getValue.geometry().height(), self.RC_lCal_getValue.geometry().height())
        self.RC_lCal_setButton.setFixedSize(buttonSize)


        self.RC_TimeShift_label = QtWidgets.QLabel("Time alignment", self)
        self.RC_TimeShift_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.RC_TimeShift_setValue = QtWidgets.QLineEdit(self)
        self.RC_TimeShift_setButton = QtWidgets.QPushButton("⎆")
        self.RC_TimeShift_setButton.setFixedSize(buttonSize)

        self.RF_threshold_label = QtWidgets.QLabel("CFD Threshold")
        self.RF_threshold_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.RF_threshold_setValue = QtWidgets.QLineEdit(self)
        self.RF_threshold_setButton = QtWidgets.QPushButton("⎆")
        self.RF_threshold_setButton.setFixedSize(buttonSize)

        self.RF_shift_label = QtWidgets.QLabel("CFD zero")
        self.RF_shift_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.RF_shift_setValue = QtWidgets.QLineEdit(self)
        self.RF_shift_setButton = QtWidgets.QPushButton("⎆")
        self.RF_shift_setButton.setFixedSize(buttonSize)

        self.RF_zeroOffset_label = QtWidgets.QLabel("ADC zero")
        self.RF_zeroOffset_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.RF_zeroOffset_setValue = QtWidgets.QLineEdit(self)
        self.RF_zeroOffset_setButton = QtWidgets.QPushButton("⎆")
        self.RF_zeroOffset_setButton.setFixedSize(buttonSize)

        self.RF_delay_label = QtWidgets.QLabel("ADC Delay")
        self.RF_delay_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.RF_delay_setValue = QtWidgets.QLineEdit(self)
        self.RF_delay_setButton = QtWidgets.QPushButton("⎆")
        self.RF_delay_setButton.setFixedSize(buttonSize)


        self.RC_rangeCorr_label = QtWidgets.QLabel("Range correction", self)
        self.RC_ADC0_rangeCorr_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RC_ADC1_rangeCorr_getValue = QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.RZ_ADC_baseLine_label = QtWidgets.QLabel("Base\nline")
        self.RZ_ADC_baseLine_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RZ_ADC0_baseLine_value= QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RZ_ADC1_baseLine_value= QtWidgets.QLineEdit(self, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.RA_ADC_meanAmp_label = QtWidgets.QLabel("Mean\ncharge\\amplitude")
        self.RA_ADC_meanAmp_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RA_ADC0_meanAmp_value = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RA_ADC1_meanAmp_value = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.RZ_ADC_RMS_label = QtWidgets.QLabel("RMS")
        self.RZ_ADC0_RMS_value= QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RZ_ADC1_RMS_value= QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        ADC_label0 = QtWidgets.QLabel("ADC0", self)
        ADC_label1 = QtWidgets.QLabel("ADC1", self)


        self.RT_TDC_label       = QtWidgets.QLabel("TDC raw data")
        self.RT_TDC_FPGA_label  = QtWidgets.QLabel("FPGA")
        self.RT_TDC_ASIC_label  = QtWidgets.QLabel("ASIC")
        self.TDC_raw_label      = QtWidgets.QLabel("TDC value")
        self.RT_TDC_FPGA_value  = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RT_TDC_ASIC_value  = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TDC_raw_value      = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        TRG_label = QtWidgets.QLabel("PM TRG control")
        self.TRG_orGate_label = QtWidgets.QLabel("Or gate")
        self.TRG_chargeHigh_label = QtWidgets.QLabel("Charge\nhigh", alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.TRG_orGate_getValue = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.TRG_orGate_setValue = QtWidgets.QLineEdit()
        self.TRG_orGate_setButton = QtWidgets.QPushButton("⎆")
        self.TRG_orGate_setButton.setFixedSize(buttonSize)

        self.TRG_chargeHigh_getValue = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.TRG_chargeHigh_setValue = QtWidgets.QLineEdit()
        self.TRG_chargeHigh_setButton = QtWidgets.QPushButton("⎆")
        self.TRG_chargeHigh_setButton.setFixedSize(buttonSize)


        self.setReadOnly()
        self.setLimit()

############## Layout ###########
############## General settings #
        channel0BoxLayout.addWidget(self.RC_TimeShift_label,     0, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel0BoxLayout.addWidget(self.RC_TimeShift_getValue,  1, 0, 1, 1)
        channel0BoxLayout.addWidget(self.RC_TimeShift_setValue,  1, 1, 1, 1)
        channel0BoxLayout.addWidget(self.RC_TimeShift_setButton, 1, 2, 1, 1)

        channel0BoxLayout.addWidget(self.RF_delay_label,         0, 3, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel0BoxLayout.addWidget(self.RF_delay_getValue,      1, 3, 1, 1)
        channel0BoxLayout.addWidget(self.RF_delay_setValue,      1, 4, 1, 1)
        channel0BoxLayout.addWidget(self.RF_delay_setButton,     1, 5, 1, 1)

        channel0BoxLayout.addWidget(self.RF_zeroOffset_label,    0, 6, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel0BoxLayout.addWidget(self.RF_zeroOffset_getValue, 1, 6, 1, 1)
        channel0BoxLayout.addWidget(self.RF_zeroOffset_setValue, 1, 7, 1, 1)
        channel0BoxLayout.addWidget(self.RF_zeroOffset_setButton,1, 8, 1, 1)

        channel1BoxLayout.addWidget(self.RC_lCal_label,          0, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel1BoxLayout.addWidget(self.RC_lCal_getValue,       1, 0, 1, 1)
        channel1BoxLayout.addWidget(self.RC_lCal_setValue,       1, 1, 1, 1)
        channel1BoxLayout.addWidget(self.RC_lCal_setButton,      1, 2, 1, 1)

        channel1BoxLayout.addWidget(self.RF_threshold_label,     0, 3, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel1BoxLayout.addWidget(self.RF_threshold_getValue,  1, 3, 1, 1)
        channel1BoxLayout.addWidget(self.RF_threshold_setValue,  1, 4, 1, 1)
        channel1BoxLayout.addWidget(self.RF_threshold_setButton, 1, 5, 1, 1)

        channel1BoxLayout.addWidget(self.RF_shift_label,         0, 6, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel1BoxLayout.addWidget(self.RF_shift_getValue,      1, 6, 1, 1)
        channel1BoxLayout.addWidget(self.RF_shift_setValue,      1, 7, 1, 1)
        channel1BoxLayout.addWidget(self.RF_shift_setButton,     1, 8, 1, 1)
#################################

############## Layout ###########
############## ADC    ###########
        ADCBoxLayout.addWidget(self.RC_rangeCorr_label,         0, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        ADCBoxLayout.addWidget(self.RZ_ADC_baseLine_label,      0, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        ADCBoxLayout.addWidget(self.RA_ADC_meanAmp_label,       0, 4, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        ADCBoxLayout.addWidget(self.RZ_ADC_RMS_label,           0, 5, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        ADCBoxLayout.addWidget(ADC_label0,                      1, 0)
        ADCBoxLayout.addWidget(ADC_label1,                      2, 0)

        ADCBoxLayout.addWidget(self.RC_ADC0_rangeCorr_getValue, 1, 1)
        # ADCBoxLayout.addWidget(self.RC_ADC0_rangeCorr_setValue, 1, 2)
        ADCBoxLayout.addWidget(self.RC_ADC1_rangeCorr_getValue, 2, 1)
        # ADCBoxLayout.addWidget(self.RC_ADC1_rangeCorr_setValue, 2, 2)

        ADCBoxLayout.addWidget(self.RZ_ADC0_baseLine_value, 1, 3)
        ADCBoxLayout.addWidget(self.RZ_ADC1_baseLine_value, 2, 3)

        ADCBoxLayout.addWidget(self.RA_ADC0_meanAmp_value, 1, 4)
        ADCBoxLayout.addWidget(self.RA_ADC1_meanAmp_value, 2, 4)

        ADCBoxLayout.addWidget(self.RZ_ADC0_RMS_value, 1, 5)
        ADCBoxLayout.addWidget(self.RZ_ADC1_RMS_value, 2, 5)

        channel0BoxGroup.setLayout(channel0BoxLayout)
        channel1BoxGroup.setLayout(channel1BoxLayout)
        channelSettingBoxLayout.addWidget(channel0BoxGroup, 0, 0)
        channelSettingBoxLayout.addWidget(channel1BoxGroup, 1, 0)
        channelSettingBoxGroup.setLayout(channelSettingBoxLayout)


        ADCBoxGroup.setLayout(ADCBoxLayout)
#################################

############## Layout ###########
############## TDC raw###########
        TDCBoxLayout.addWidget(self.RT_TDC_label,       0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        TDCBoxLayout.addWidget(self.RT_TDC_FPGA_label,  1, 0)
        TDCBoxLayout.addWidget(self.RT_TDC_ASIC_label,  2, 0)
        TDCBoxLayout.addWidget(self.TDC_raw_label,      3, 0)
        TDCBoxLayout.addWidget(self.RT_TDC_FPGA_value,  1, 1)
        TDCBoxLayout.addWidget(self.RT_TDC_ASIC_value,  2, 1)
        TDCBoxLayout.addWidget(self.TDC_raw_value,      3, 1)


        TDCBoxGroupe.setLayout(TDCBoxLayout)
#################################

############## Layout ###########
############## TRG cnt###########


        TRGBoxLayout.addWidget(TRG_label, 0, 0, 1, 4, QtCore.Qt.AlignmentFlag.AlignCenter)
        TRGBoxLayout.addWidget(self.TRG_orGate_label,           1, 0)
        TRGBoxLayout.addWidget(self.TRG_chargeHigh_label,       2, 0)

        TRGBoxLayout.addWidget(self.TRG_orGate_getValue,        1, 1)
        TRGBoxLayout.addWidget(self.TRG_orGate_setValue,        1, 2)
        TRGBoxLayout.addWidget(self.TRG_orGate_setButton,       1, 3)

        TRGBoxLayout.addWidget(self.TRG_chargeHigh_getValue,    2, 1)
        TRGBoxLayout.addWidget(self.TRG_chargeHigh_setValue,    2, 2)
        TRGBoxLayout.addWidget(self.TRG_chargeHigh_setButton,   2, 3)


        TRGBoxGroupe.setLayout(TRGBoxLayout)




        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(channelSettingBoxGroup,   1, 0, 1, 2)
        lay.addWidget(ADCBoxGroup,              2, 0, 1, 2)
        lay.addWidget(TDCBoxGroupe,             3, 0, 1, 1)
        lay.addWidget(TRGBoxGroupe,             3, 1, 1, 1)






    def setReadOnly(self):
        self.RC_lCal_getValue.setReadOnly(True)
        self.RC_TimeShift_getValue.setReadOnly(True)
        self.RC_ADC0_rangeCorr_getValue.setReadOnly(True)
        self.RC_ADC1_rangeCorr_getValue.setReadOnly(True)

        self.RF_delay_getValue.setReadOnly(True)
        self.RF_shift_getValue.setReadOnly(True)
        self.RF_threshold_getValue.setReadOnly(True)
        self.RF_zeroOffset_getValue.setReadOnly(True)

        self.RA_ADC0_meanAmp_value.setReadOnly(True)
        self.RA_ADC1_meanAmp_value.setReadOnly(True)

        self.RZ_ADC0_baseLine_value.setReadOnly(True)
        self.RZ_ADC1_baseLine_value.setReadOnly(True)
        self.RZ_ADC0_RMS_value.setReadOnly(True)
        self.RZ_ADC1_RMS_value.setReadOnly(True)

        self.RT_TDC_FPGA_value.setReadOnly(True)
        self.RT_TDC_ASIC_value.setReadOnly(True)

        self.TRG_orGate_getValue.setReadOnly(True)
        self.TRG_chargeHigh_getValue.setReadOnly(True)

    def setLimit(self):
        self.TRG_orGate_setValue.editingFinished.connect(lambda: self.checkValue(self.TRG_orGate_setValue, 0, 255))
        self.TRG_chargeHigh_setValue.editingFinished.connect(lambda: self.checkValue(self.TRG_chargeHigh_setValue, 0, 4095))

        self.RC_lCal_setValue.editingFinished.connect(lambda: self.checkValue(self.RC_lCal_setValue, 0, 4000))
        self.RC_TimeShift_setValue.editingFinished.connect(lambda: self.checkValue(self.RC_TimeShift_setValue, -2048, 2047))

        self.RF_threshold_setValue.editingFinished.connect(lambda: self.checkValue(self.RF_threshold_setValue, 300, 30_000))
        self.RF_shift_setValue.editingFinished.connect(lambda: self.checkValue(self.RF_shift_setValue, -500, 500))
        self.RF_zeroOffset_setValue.editingFinished.connect(lambda: self.checkValue(self.RF_zeroOffset_setValue, -500, 500))
        self.RF_delay_setValue.editingFinished.connect(lambda: self.checkValue(self.RF_delay_setValue, 0, 20_000))


    @QtCore.Slot()
    def checkValue(self, sender: QtWidgets.QLineEdit, min: int, max: int):
        try:
            value, base = str2int(sender.text())
        except ValueError:
            sender.setText("NaN")
            return

        if value > max:
            sender.setText(int2str(max, base))
        elif value < min:
            sender.setText(int2str(min, base))




class BoardStatus(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(BoardStatus, self).__init__(parent)

        self.SN_label = QtWidgets.QLabel("Serial number")
        self.SN_value = QtWidgets.QLineEdit("Unknown")
        self.SN_value.setReadOnly(True)
        self.SN_value.setMinimumSize(80, 24)
        self.SN_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.extPowSrc_label = QtWidgets.QLabel("External power src")
        self.extPowSrc_led = LedIndicator(scale= 0.75)

        self.boardPower_label = QtWidgets.QLabel("Board power")
        self.boardPower_led = LedIndicator(scale=0.75)

        self.FPGA_label = QtWidgets.QLabel("FPGA")
        self.FPGA_led   = LedIndicator(scale=0.75)

        self.GBT_label  = QtWidgets.QLabel("GBT")
        self.GBT_led    = LedIndicator(scale=0.75)

        self.clock_label = QtWidgets.QLabel("Clock")
        self.clock_led = LedIndicator(scale=0.75)
        self.clock_source = QtWidgets.QLineEdit("Unknown")
        self.clock_source.setReadOnly(True)
        self.clock_source.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.temperature_label = QtWidgets.QLabel("Temperature")
        self.temperature_value = QtWidgets.QLineEdit("Unknown")
        self.temperature_status= QtWidgets.QLineEdit("Unknown")
        self.temperature_value.setReadOnly(True)
        self.temperature_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.temperature_status.setReadOnly(True)
        self.temperature_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)



        lay = QtWidgets.QGridLayout(self)

        lay.addWidget(self.SN_label, 0, 0)
        lay.addWidget(self.SN_value, 0, 1)

        lay.addWidget(self.extPowSrc_label, 2, 0)
        lay.addWidget(self.extPowSrc_led,   2, 1)

        lay.addWidget(self.boardPower_label, 3, 0)
        lay.addWidget(self.boardPower_led, 3, 1)

        lay.addWidget(self.FPGA_label, 4, 0)
        lay.addWidget(self.FPGA_led,   4, 1)

        lay.addWidget(self.GBT_label, 5, 0)
        lay.addWidget(self.GBT_led,   5, 1)

        lay.addWidget(self.clock_label,  6, 0)
        lay.addWidget(self.clock_led,    6, 1)
        lay.addWidget(self.clock_source, 7, 0, 1, 2)

        lay.addWidget(self.temperature_label,  8, 0)
        lay.addWidget(self.temperature_value,  8, 1)
        lay.addWidget(self.temperature_status, 9, 0, 1, 2)
