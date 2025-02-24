import serial
import serial.serialutil
import serial.tools.list_ports
import threading
from collections import deque
from time import sleep


# from debugData import debugData, debugAns





def getDevList() -> list:
    info = []
    comList = serial.tools.list_ports.comports()
    for com in comList:
        info.append(com.device)
    return info




class serialDevice():
    def __init__(self, portName: str | None = None, baudrate: int = 115200, timeout: float | None = None):
        self.dev = serial.Serial()
        self.dev.baudrate = baudrate
        self.dev.port = portName
        self.dev.xonxoff = True
        self.dev.parity = serial.PARITY_NONE
        self.dev.stopbits = serial.STOPBITS_ONE
        self.dev.bytesize = serial.EIGHTBITS
        self.dev.exclusive= True
        self.dev.timeout = timeout

        self.readQueue = deque()
        self.waitOnRead: bool = False

        self.handler = self._readLine

    def __del__(self):
        self.disconnect()


    @property
    def port(self) -> str | None:
        return self.dev.port




    def connect(self, portName: str | None = None) -> bool:
        if portName is not None:
            self.dev.port = portName
        try:
            self.dev.open()
        except serial.serialutil.SerialException:
            return False
        return self.dev.is_open


    def disconnect(self):
        if self.isOpen():
            self.stopThread.set()
            self.readThread.join(0.2)
            self.dev.cancel_read()
            self.dev.close()

            self.readQueue.clear()
            self.waitOnRead = False


    def isOpen(self) -> bool:
        return self.dev.is_open


    def write(self, data: str, end = "\r") -> int | None:
        if data == "":
            return 0
        self.waitOnRead = True
        # data = data.lower()
        # print(f"Send: {data}")
        data = data + end
        byteData = data.encode("utf-8")
        return self.dev.write(byteData)

    def read(self) -> str | None:
        try:
            return self.readQueue.popleft()
        except IndexError:
            return None

    def toRead(self) -> int:
        return len(self.readQueue)

    def _read(self) -> str:
        byteData = self.dev.readline()
        data = byteData.decode("utf-8")
        # print(f"Read: {data}")

        return data


    def startReadRoutine(self):
        self.stopThread = threading.Event()
        self.readThread = threading.Thread(target = self.handler)
        self.readThread.start()



    def _readNBytes(self):
        numOfByte = 256

        while not self.stopThread.is_set() and self.isOpen():
            try:
                data = self.dev.read(numOfByte)
            except serial.SerialTimeoutException:
                continue
            except serial.SerialException:
                return

            self.readQueue.append(data)


    def _readLine(self):
        while not self.stopThread.is_set() and self.isOpen():
            try:
                data = self._read()
            except:
                return

            data = data.strip("\n")
            data = data.strip("\r")
            self.readQueue.append(data)




if __name__ == "__main__":
    dev = serialDevice("/dev/ttyACM0")

    print(dev.read())

    dev.connect()
    dev.startReadRoutine()

    dev.write("RS")
    dev.disconnect()

    while dev.toRead():
        print(dev.read())

