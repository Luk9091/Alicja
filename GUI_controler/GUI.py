from PySide6 import QtCore, QtWidgets
from led import LedIndicator



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




        self.RC_lCal_label = QtWidgets.QLabel("Threshold calibration", self)
        self.RC_lCal_setValue = QtWidgets.QLineEdit(self)
        self.RC_lCal_getValue = QtWidgets.QLineEdit(self)

        self.RC_TDC_label = QtWidgets.QLabel("Time alignment", self)
        self.RC_TDC_getValue = QtWidgets.QLineEdit(self)
        self.RC_TDC_setValue = QtWidgets.QLineEdit(self)

        self.RC_timeShift_label = QtWidgets.QLabel("Time shift", self)
        self.RC_timeShift_value = QtWidgets.QLineEdit(self)
        self.RC_timeShift_value.setReadOnly(True)

        self.RC_rangeCorr_label = QtWidgets.QLabel("Range correction", self)
        self.RC_ADC0_rangeCorr_getValue = QtWidgets.QLineEdit(self)
        self.RC_ADC0_rangeCorr_setValue = QtWidgets.QLineEdit(self)
        self.RC_ADC1_rangeCorr_getValue = QtWidgets.QLineEdit(self)
        self.RC_ADC1_rangeCorr_setValue = QtWidgets.QLineEdit(self)


        self.RF_threshold_label = QtWidgets.QLabel("CFD Threshold")
        self.RF_threshold_setValue = QtWidgets.QLineEdit(self)
        self.RF_threshold_getValue = QtWidgets.QLineEdit(self)

        self.RF_shift_label = QtWidgets.QLabel("CFD zero")
        self.RF_shift_setValue = QtWidgets.QLineEdit(self)
        self.RF_shift_getValue = QtWidgets.QLineEdit(self)

        self.RF_zeroOffset_label = QtWidgets.QLabel("ADC zero")
        self.RF_zeroOffset_setValue = QtWidgets.QLineEdit(self)
        self.RF_zeroOffset_getValue = QtWidgets.QLineEdit(self)

        self.RF_delay_label = QtWidgets.QLabel("ADC Delay")
        self.RF_delay_setValue = QtWidgets.QLineEdit(self)
        self.RF_delay_getValue = QtWidgets.QLineEdit(self)

        self.RF_TRG_label = QtWidgets.QLabel("Trigger window")
        self.RF_TRG_value = QtWidgets.QLineEdit(self)
        self.RF_TRG_value.setReadOnly(True)

        self.RF_CFD_label = QtWidgets.QLabel("CFD")
        self.RF_CFD_value = QtWidgets.QLineEdit(self)
        self.RF_CFD_value.setReadOnly(True)


        self.RZ_ADC_baseLine_label = QtWidgets.QLabel("Base\nline")
        self.RZ_ADC_baseLine_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RZ_ADC0_baseLine_value= QtWidgets.QLineEdit(self)
        self.RZ_ADC1_baseLine_value= QtWidgets.QLineEdit(self)

        self.RZ_ADC_RMS_label = QtWidgets.QLabel("RMS")
        self.RZ_ADC0_RMS_value= QtWidgets.QLineEdit()
        self.RZ_ADC1_RMS_value= QtWidgets.QLineEdit()


        ADC_label0 = QtWidgets.QLabel("ADC0:", self)
        ADC_label1 = QtWidgets.QLabel("ADC1:", self)

############## Layout ###########
############## General settings #
        channel0BoxLayout.addWidget(self.RC_TDC_label,           0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel0BoxLayout.addWidget(self.RC_TDC_getValue,        1, 0, 1, 1)
        channel0BoxLayout.addWidget(self.RC_TDC_setValue,        1, 1, 1, 1)

        channel0BoxLayout.addWidget(self.RF_delay_label,         0, 2, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel0BoxLayout.addWidget(self.RF_delay_getValue,      1, 2, 1, 1)
        channel0BoxLayout.addWidget(self.RF_delay_setValue,      1, 3, 1, 1)

        channel0BoxLayout.addWidget(self.RF_zeroOffset_label,    0, 4, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel0BoxLayout.addWidget(self.RF_zeroOffset_getValue, 1, 4, 1, 1)
        channel0BoxLayout.addWidget(self.RF_zeroOffset_setValue, 1, 5, 1, 1)

        channel1BoxLayout.addWidget(self.RC_lCal_label,          0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel1BoxLayout.addWidget(self.RC_lCal_getValue,       1, 0, 1, 1)
        channel1BoxLayout.addWidget(self.RC_lCal_setValue,       1, 1, 1, 1)

        channel1BoxLayout.addWidget(self.RF_threshold_label,     0, 2, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel1BoxLayout.addWidget(self.RF_threshold_getValue,  1, 2, 1, 1)
        channel1BoxLayout.addWidget(self.RF_threshold_setValue,  1, 3, 1, 1)

        channel1BoxLayout.addWidget(self.RF_shift_label,         0, 4, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        channel1BoxLayout.addWidget(self.RF_shift_getValue,      1, 4, 1, 1)
        channel1BoxLayout.addWidget(self.RF_shift_setValue,      1, 5, 1, 1)
#################################

############## Layout ###########
############## General settings #
        ADCBoxLayout.addWidget(self.RC_rangeCorr_label,         0, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        ADCBoxLayout.addWidget(self.RZ_ADC_baseLine_label,      0, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        ADCBoxLayout.addWidget(self.RZ_ADC_RMS_label,           0, 4, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        ADCBoxLayout.addWidget(ADC_label0,                      1, 0)
        ADCBoxLayout.addWidget(ADC_label1,                      2, 0)

        ADCBoxLayout.addWidget(self.RC_ADC0_rangeCorr_getValue, 1, 1)
        ADCBoxLayout.addWidget(self.RC_ADC0_rangeCorr_setValue, 1, 2)
        ADCBoxLayout.addWidget(self.RC_ADC1_rangeCorr_getValue, 2, 1)
        ADCBoxLayout.addWidget(self.RC_ADC1_rangeCorr_setValue, 2, 2)

        ADCBoxLayout.addWidget(self.RZ_ADC0_baseLine_value, 1, 3)
        ADCBoxLayout.addWidget(self.RZ_ADC1_baseLine_value, 2, 3)

        ADCBoxLayout.addWidget(self.RZ_ADC0_RMS_value, 1, 4)
        ADCBoxLayout.addWidget(self.RZ_ADC1_RMS_value, 2, 4)
#################################

############## Layout ###########
############## General settings #



        # labelLayout.addWidget(self.RC_timeShift_label,     0, 6, 1, 2)
        # labelLayout.addWidget(self.RF_TRG_label,           0, 8, 1, 2)
        # labelLayout.addWidget(self.RF_CFD_label,           1, 8, 1, 2)

        # valueLayout.addWidget(self.RC_timeShift_value,     2, 1, 1, 2)
        # valueLayout.addWidget(self.RC_rangeCorr_value,     3, 1, 1, 2)


        # valueLayout.addWidget(self.RF_TRG_value,           0, 9, 1, 2)
        # valueLayout.addWidget(self.RF_CFD_value,           1, 9, 1, 2)

        channel0BoxGroup.setLayout(channel0BoxLayout)
        channel1BoxGroup.setLayout(channel1BoxLayout)
        channelSettingBoxLayout.addWidget(channel0BoxGroup, 0, 0)
        channelSettingBoxLayout.addWidget(channel1BoxGroup, 1, 0)
        channelSettingBoxGroup.setLayout(channelSettingBoxLayout)


        ADCBoxGroup.setLayout(ADCBoxLayout)


        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(channelSettingBoxGroup, 0, 0)
        lay.addWidget(ADCBoxGroup, 1, 0)




class BoardStatus(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(BoardStatus, self).__init__(parent)

        self.SN_label = QtWidgets.QLabel("Serial number:")
        self.SN_value = QtWidgets.QLineEdit("Unknown")
        self.SN_value.setReadOnly(True)
        self.SN_value.setMinimumSize(80, 24)
        self.SN_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.extPowSrc_label = QtWidgets.QLabel("External power src:")
        self.extPowSrc_led = LedIndicator(scale= 0.75)

        self.boardPower_label = QtWidgets.QLabel("Board power:")
        self.boardPower_led = LedIndicator(scale=0.75)

        self.FPGA_label = QtWidgets.QLabel("FPGA:")
        self.FPGA_led   = LedIndicator(scale=0.75)

        self.GBT_label  = QtWidgets.QLabel("GBT:")
        self.GBT_led    = LedIndicator(scale=0.75)

        self.clock_label = QtWidgets.QLabel("Clock:")
        self.clock_led = LedIndicator(scale=0.75)
        self.clock_source = QtWidgets.QLineEdit("Unknown")
        self.clock_source.setReadOnly(True)
        self.clock_source.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.temperature_label = QtWidgets.QLabel("Temperature:")
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
