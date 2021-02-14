import socket
import struct
from tkinter import *
import tkinter
import threading
import time
import random
import datetime
from time import strftime

multicastGroup = ('225.1.1.1', 5007)
hora = datetime.datetime.now()
tiempo = 1000
uno = 1
root = tkinter.Tk()
myClock1 = tkinter.Label(root)


def createSocket(timeOut):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(timeOut)
	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	return sock


def send():
        sock = createSocket(0.5)
        print(hora.strftime('%H:%M:%S'))
        sock.sendto((hora.strftime('%H:%M:%S')).encode(), multicastGroup)
        sock.close()


def anaSeg():
    global hora
    hora = hora+datetime.timedelta(seconds=1)
    myClock1['text'] = hora.strftime('%H:%M:%S')


def anaMin():
    global hora
    hora = hora+datetime.timedelta(minutes=1)
    myClock1['text'] = hora.strftime('%H:%M:%S')
    print('añadi minutos al hilo: ',
            threading.currentThread().getName())


def anaHor():
    global hora
    hora = hora+datetime.timedelta(hours=1)
    myClock1['text'] = hora.strftime('%H:%M:%S')
    print('añadi horas al hilo: ', threading.currentThread().getName())


def redSeg():
    global hora
    hora = hora-datetime.timedelta(seconds=1)
    myClock1['text'] = hora.strftime('%H:%M:%S')
    print('reduje segundos al hilo: ',
            threading.currentThread().getName())


def redMin():
    global hora
    hora = hora-datetime.timedelta(minutes=1)
    myClock1['text'] = hora.strftime('%H:%M:%S')
    print('reduje un minuto al hilo: ',
            threading.currentThread().getName())


def redHor():
    global hora
    hora = hora-datetime.timedelta(hours=1)
    myClock1['text'] = hora.strftime('%H:%M:%S')
    print('reduje una hora al hilo: ',
            threading.currentThread().getName())


def acelerar():
    global tiempo
    tiempo = tiempo/2
    # myClock1['text'] = hora.strftime('%H:%M:%S')
    print('acelere el reloj : ', threading.currentThread().getName())

def realentiza():
    global tiempo
    tiempo = tiempo*2
    # myClock1['text'] = hora.strftime('%H:%M:%S')

def pauseReanude():
    global uno
    if (uno == 0):
        uno = 1
    else:
        uno = 0

def tic():
    global hora
    hora = hora+datetime.timedelta(seconds=uno)
    myClock1['text'] = hora.strftime('%H:%M:%S')

def tac():
    tic()
    myClock1.after(int(tiempo), tac)

if __name__ == "__main__":
	# Diseño de Login
    
    root.title("maestro")
    today = hora + datetime.timedelta(seconds=random.randint(1, 1000000))
    hora = today
    myClock1['text'] = today

    myClock1['font'] = 'Tahoma 50 bold'
    myClock1.grid(row=0, column=0, columnspan=3)
    
    bSeg = tkinter.Button(root, text='añade segundo', command=anaSeg)
    bSeg.grid(row=1, column=2)

    bMin = tkinter.Button(root, text='añade minuto', command=anaMin)
    # bMin.pack()
    bMin.grid(row=1, column=1)

    bHor = tkinter.Button(root, text='añade hora', command=anaHor)
    # bMin.pack()
    bHor.grid(row=1, column=0)

    brSeg = tkinter.Button(root, text='reduce segundo', command=redSeg)
    brSeg.grid(row=2, column=2)

    brMin = tkinter.Button(root, text='reduce minuto', command=redMin)
    # bMin.pack()
    brMin.grid(row=2, column=1)

    brHor = tkinter.Button(root, text='reduce hora', command=redHor)
    # bMin.pack()
    brHor.grid(row=2, column=0)

    bAce = tkinter.Button(root, text='acelera reloj', command=acelerar)
    # bMin.pack()
    bAce.grid(row=3, column=1)

    bDece = tkinter.Button(root, text='realentiza reloj', command=realentiza)
    # bMin.pack()
    bDece.grid(row=4, column=1)

    bPause = tkinter.Button(root, text='pause/reanude reloj', command=pauseReanude)
    # bMin.pack()
    bPause.grid(row=5, column=1)

    bSend = tkinter.Button(root, text='send', command=send)
    # bMin.pack()
    bSend.grid(row=6, column=1)

    tac()
    root.mainloop()
