from serial import Serial, SerialException, SerialTimeoutException
from serial.tools import list_ports
from collections import deque
from time import sleep, perf_counter
import threading
import struct


def getDevList() -> list:
    info = []
    comList = list_ports.comports()
    for com in comList:
        info.append(com.device)
    return info

class Device():
    __BYTE_SIZE = 256


    def __init__(self, port = "/dev/ttyACM0", baudrate = 115200, timeout = 0.1):
        self.dev = Serial()
        self.dev.port = port
        self.dev.baudrate = baudrate
        self.dev.timeout = timeout
        self.dev.exclusive = True
        self.readQueue = deque()


    def __del__(self):
        self.close()


    def startReadRoutine(self):
        self.stopThread = threading.Event()
        self.readThread = threading.Thread(target = self.readThread_handler)
        self.readThread.start()


    def connect(self, portName: str | None = None) -> bool:
        if portName is not None:
            self.dev.port = portName
        try:
            self.dev.open()
        except SerialException:
            return False
        return self.dev.is_open


    def close(self):
        if self.dev.is_open:
            self.stopThread.set()
            self.dev.cancel_read()
            self.dev.cancel_write()
            self.readThread.join(0.1)
            self.dev.close()

            self.readQueue.clear()


    def read(self):
        return self.readQueue.popleft()

    def write(self, data: str):
        self.dev.write(data.encode("utf-8"))

    def toRead(self) -> int:
        return len(self.readQueue)


    def readThread_handler(self):
        while self.dev.is_open and not self.stopThread.is_set():
            try:
                data = self.dev.read(self.__BYTE_SIZE)
            except SerialTimeoutException:
                pass
            except SerialException:
                return

            if len(data) != 0:
                self.readQueue.append(data)


    @property
    def isOpen(self):
        return self.dev.is_open












if __name__ == "__main__":
    serialDevice = Device()
    serialDevice.connect()
    serialDevice.startReadRoutine()


    try:
        serialDevice.write("OK\n")
        while True:
            if serialDevice.toRead():
                data = serialDevice.read()

                # print(data)

                value = struct.unpack("<" + "H"*(len(data)//2), data)
                print(value[0:10])

            sleep(0.1)
    except KeyboardInterrupt:
        print("Good bay")

    serialDevice.close()

