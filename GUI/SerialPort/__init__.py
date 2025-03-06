#
# This is a wrapper to serial communication lib
# This lib base on pySerial. https://github.com/pyserial/pyserial'
#
import sys


from SerialPort.main import SerialDevice


if sys.platform == "linux":
    from SerialPort.main import getSerialDevices_forLinux as getSerialDevices
else:
    from SerialPort.main import getSerialDevices_forWindows as getSerialDevices