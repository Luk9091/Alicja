import socket
import threading

import time
from time import sleep

server_address = ("localhost", 50001)
client_address = ("localhost", 50000)
buffer_size = 368


UDP_serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_serverSocket.bind(server_address)
print("Server run")

current_time = -1
CONST_VALUE = 5

try:
    while True:
        local_time = time.localtime()
        # current_time: str = time.strftime("%H:%M:%S", local_time)
        current_time += 1
        print(current_time)
        data = bytearray(current_time.to_bytes(4, "little"))
        data = [*data, *CONST_VALUE.to_bytes(4, "little")]

        UDP_serverSocket.sendto(bytearray(data), client_address)
        sleep(1)
except (KeyboardInterrupt, EOFError):
    print("Good bye")

UDP_serverSocket.close()