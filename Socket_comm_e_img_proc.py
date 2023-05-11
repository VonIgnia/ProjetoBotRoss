import socket
import time

import numpy as np
from random import randint

print ('Program Started')

HOST = '10.103.16.140'
PORT = 20000

print('Trying Connection')
count = 0

point_positions = np.ones(30)


# Create a host socket


connected = False

while (connected == False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    c, addr = s.accept()
    if (addr[0] != ''):
        connected = True
        print("Connected")

print(addr)
while (count < 100):
    try:
        time.sleep(0.5)
        c.send(str(tuple(point_positions*count)).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
        print(tuple(point_positions*count))
        
    except socket.error as socketerror:
        print (count)
    count += 1

c.close()
s.close()
print('Disconnected')
print('Program Finished')
