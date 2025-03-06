from serial import Serial, SerialException, SerialTimeoutException
from serial.tools import list_ports
from collections import deque
import threading
from typing import Literal
import struct


def getSerialDevices_forLinux() -> list[str]:
    comList = list_ports.comports()
    nameList = []

    for com in comList:
        if com.device.startswith("/dev/ttyS"):
            continue
        nameList.append(com.device)
    return nameList

def getSerialDevices_forWindows() -> list[str]:
    comList = list_ports.comports()
    nameList = []

    for com in comList:
        nameList.append(com.device)
    return nameList



class SerialDevice():
    def __init__(
            self, portName: str | None = None, baudrate: int = 115200, timeout: float | None = None, open: bool = False,
            readType: Literal["newLine", "char", "numOfBytes"] = "newLine", readUntil: str | None = None
        ):
        self._device = Serial(baudrate= baudrate, timeout= timeout, exclusive= True)
        self._device.port = portName

        self.readQueue = deque()

        if readType == "newLine":
            self._thread_handler = self._readThread_newLine_handler
        elif readType == "char":
            print("Not implemented")
        #     self._readUntil = readUntil.encode("utf-8")
        #     self._readThread = threading.Thread(target= self._readThread_newLine_handler)
        elif readType == "numOfBytes":
            self._thread_handler = self._readThread_numOfByte_handler
            if readUntil is None:
                self._readUntil = 256
            else:
                self._readUntil = readUntil

        if open:
            self._device.open()

    def __del__(self):
        self.close()

    def open(self, port: str | None = None) -> bool:
        if port is not None:
            self.port = port

        if not self.isOpen:
            self.readQueue.clear()
            self._readThread_event = threading.Event()
            self._readThread = threading.Thread(target= self._thread_handler)
            self._device.open()

            self._readThread.start()

        return self.isOpen

    def close(self):
        if self.isOpen:
            self._readThread_event.set()
            self._device.cancel_read()
            self._readThread.join(0.2)

            self._device.close()

    def clear(self):
        self.readQueue.clear()

    def write(self, data: str, end: str = "\r") -> int | None:
        '''
            Sends a string over the serial port.

            - data (str): The string to send.
            - end (str, optional): The line termination character(s). Defaults to '\\r.

            Returns:
            - int | None: The number of bytes written, or None if the write operation fails.

            Note:
            When data is transmitted via tools like PuTTY, the end-of-line character is typically '\\n\\r'.
            But a lot of device ignore first '\\n'

        '''
        if data is None or not self.isOpen:
            return 0
        return self._device.write(f"{data}{end}".encode("utf-8"))


    @property
    def toRead(self):
        return len(self.readQueue)

    def readLine(self) -> str | None:
        try:
            rawData: bytes = self.readQueue.popleft()
        except IndexError:
            return None
        data = rawData.decode("utf-8")
        data = data.strip("\n")
        data = data.strip("\r")
        return data

    # def readListOfValue(self, byteOrder: Literal["little", "big"] = "little", charPerValue: int = 2) -> list[int] | None:
    def readListOfValue(self) -> list[int] | None:
        try:
            rawData: bytes = self.readQueue.popleft()
        except IndexError:
            return None

        data = struct.unpack("<"+ "H"*(len(rawData)//2), rawData)
        return data


    def _readThread_newLine_handler(self):
        while self.isOpen and not self._readThread_event.is_set():
            try:
                data = self._device.readline()
            except SerialTimeoutException:
                continue
            except SerialException:
                return

            if len(data) != 0:
                self.readQueue.append(data)

    def _readThread_numOfByte_handler(self):
        while self.isOpen and not self._readThread_event.is_set():
            try:
                data = self._device.read(self._readUntil)
            except SerialTimeoutException:
                continue
            except SerialException:
                return

            if len(data) != 0:
                self.readQueue.append(data)

    @property
    def isOpen(self) -> bool:
        return self._device.is_open

    @property
    def port(self):
        return self._device.name

    @port.setter
    def port(self, value: str | None):
        self._device.close()
        self._device.port = value




if __name__ == "__main__":
    from time import sleep
    # serialDevice = SerialDevice(portName= "/dev/ttyACM0", readType= "numOfBytes")
    # serialDevice.open()

    # try:
    #     serialDevice.write("OK\n")
    #     i = 0
    #     while (i < 100):
    #         if serialDevice.toRead:
    #             print(f"Iteration: {i: 3}")
    #             data = serialDevice.readListOfValue()
    #             with open("out.csv", "a") as file:
    #                 for value in data:
    #                     if value >> 14 == 1:
    #                         file.write(f"{value},")
    #                 file.write("\n")
    #             i = i + 1

    #         sleep(0.1)
    # except KeyboardInterrupt:
    #     print("Good bay")

    # serialDevice.close()

    dev = SerialDevice("/dev/ttyACM0")

    print(dev.readLine())

    dev.open()

    dev.write("RS")
    sleep(5)
    dev.close()

    while dev.toRead:
        print(dev.readLine())