#PT_BR bibliotecas para processamento de imagem
#US_EN libraries for image processing

import cv2
import matplotlib.pyplot as plt
import numpy as np
from pykuwahara import kuwahara
from math import *

#PT_BR arquivo criado pelos desenvolvedores para armazenar as funções e deixar o código mais limpo
#US_EN developer created file in order to store the functions and make a cleaner code here
import FunctionsV2

#PT_BR bibliotecas para comunicação com o UR5
#US_EN libraries for UR5 communication
import socket
import time
import threading

# Constants
HOST = '10.103.16.140'  # Replace with the actual IP address of your UR5 robot
PORT_SEND = 12345    # Replace with the desired port for sending data to the robot
PORT_RECEIVE = 12346 # Replace with the desired port for receiving data from the robot

### Code

# Function to handle receiving data from UR5
def receive_data_from_ur5():
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receive_socket.bind((HOST, PORT_RECEIVE))
    receive_socket.listen(5)
    c, addr = s.accept()
    if (addr[0] != ''):
        reciever_connected = True
        print(f"Listening for UR5 data on {HOST}:{PORT_RECEIVE}")
    return reciever_connected


# Function to handle sending instructions to UR5
def send_instructions_to_ur5():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    send_socket.bind((HOST, PORT_RECEIVE))
    send_socket.listen(5)
    c, addr = s.accept()
    if (addr[0] != ''):
        sender_connected = True
        print(f"Connected to UR5 for sending instructions on {HOST}:{PORT_SEND}")
    return sender_connected

img_in = cv2.imread("imgs_avancadas/birb.jpeg", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)
    


print ('Program Started')
print('Trying Connection')
count = 0