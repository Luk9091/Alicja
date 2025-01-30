import serial
import serial.serialutil
import serial.tools.list_ports
import threading
from collections import deque
from time import sleep


from debugData import debugData





def getDevList() -> list:
    info = []
    comList = serial.tools.list_ports.comports()
    for com in comList:
        info.append(com.device)
    return info




class serialDevice():
    def __init__(self, portName: str | None = None, baudrate: int = 115200):
        self.dev = serial.Serial()
        self.dev.baudrate = baudrate
        self.dev.port = portName

        self.readQueue = deque()

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
            self.readThread.join(0.1)
            self.dev.close()


    def isOpen(self) -> bool:
        return self.dev.is_open


    def write(self, data: str, end = "\n") -> int | None:
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

        return data


    def startReadRoutine(self):
        self.stopThread = threading.Event()
        self.readThread = threading.Thread(target = self._readData)
        self.readThread.start()


    def _readData(self):
        while not self.stopThread.is_set() and self.isOpen():
            try:
                data = self._read()
                data = data.strip("\n")

                ansLen, ans = debugData(data)
                for i in range(ansLen):
                    self.readQueue.append(ans[i])
                print(data)
            except:
                return




if __name__ == "__main__":
    dev = serialDevice("/dev/ttyUSB0")

    print(dev.read())

    dev.connect()
    dev.startReadRoutine()

    dev.write("RS")
    dev.disconnect()

    while dev.toRead():
        print(dev.read())

