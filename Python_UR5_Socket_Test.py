import socket
import time

print ('Program Started')

HOST = '192.168.56.1'
PORT = 2000

print('Trying Connection')
count = 0

while (count < 1000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    c, addr = s.accept()

    print('Connected')

    try:
        msg = c.recv(1024)
        print (msg)
        time.sleep(1)
        if (msg == b'asking_for_data'):
            count = count + 1
            print ('The count is:', count)
            time.sleep(0.5)
            print ('')
            time.sleep(0.5)
            c.send(b'(200,50,45)')
            print ('Send 200, 50, 45')
    
    except socket.error as socketerror:
        print (count)

c.close()
s.close()

print('Disconnected')
print('Program Finished')