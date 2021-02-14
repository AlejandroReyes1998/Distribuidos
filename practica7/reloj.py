from datetime import datetime
import socket
import threading

S1Ad = ('127.0.0.1',9005)
S2Ad = ('127.0.0.1',9015)
IpS = "127.0.0.1"
PortS = 2005

class Comunicador1(threading.Thread):
    def run(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind(S1Ad)
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode()
            hora = datetime.now().strftime('%H:%M:%S')
            print('llego de S1: ',message,'  es: ',hora)
            sock.sendto(hora.encode(),addr)

class Comunicador2(threading.Thread):
    def run(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind(S2Ad)
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode()
            hora = datetime.now().strftime('%H:%M:%S')
            print('llego de S2: ',message,'  es: ',hora)
            sock.sendto(hora.encode(),addr)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
message = 'RELOJ'
sock.sendto(message.encode(), (IpS, PortS))

c1 = Comunicador1()
c1.start()
c2 = Comunicador2()
c2.start()
print("Time server running---------")