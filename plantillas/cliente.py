import socket
import struct
from tkinter import *
import tkinter
import threading
import time
import random
import datetime
from threading import Thread
from time import strftime

root = Tk()  # Se crea raiz para ventana principal
multicastGroup = ('224.1.1.1', 5007)

hora = datetime.datetime.now()
tiempo = 1000
uno = 1
myClock1 = tkinter.Label(root)

def createSocket(timeOut):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(timeOut)
	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	return sock

def tic():
    global hora
    hora = hora+datetime.timedelta(seconds=uno)
    myClock1['text'] = hora.strftime('%H:%M:%S')


def tac():
    tic()
    myClock1.after(int(tiempo), tac)


def listeningSocket():
    global hora
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if True:
        sock.bind(('', multicastGroup[1]))
    else:
        sock.bind(multicastGroup)
    mreq = struct.pack("4sl", socket.inet_aton(
        multicastGroup[0]), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, address = sock.recvfrom(5007)
        if data in b'Hello UDP Server':
            pass
        else:
            commandMessage = data.decode()
            print(commandMessage)
            hora = datetime.datetime.strptime(commandMessage, '%H:%M:%S')
            hora = hora+datetime.timedelta(hours=1.5)
        


if __name__ == "__main__":
    Thread(target=listeningSocket).start()
    root.title("principal")
    today = hora + datetime.timedelta(seconds=random.randint(1, 1000000))
    hora = today
    myClock1['text'] = today

    myClock1['font'] = 'Tahoma 50 bold'
    myClock1.grid(row=0, column=0, columnspan=3)

    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    sock = createSocket(4)
    sent = sock.sendto(bytesToSend, multicastGroup)
    tac()
    root.mainloop()
