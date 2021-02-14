import socket
from tkinter import *
import tkinter
from tkinter.filedialog import *
import threading
import time
import random
import datetime
from time import strftime
import os

UDP_IP = "127.0.0.2"
UDP_PORT = 5015
TCP_IP = "127.0.0.2"
TCP_PORT = 6015

class relojHilo(threading.Thread):
    hora = datetime.datetime.now()
    tiempo = 1000
    uno = 1

    def run(self):
        root = tkinter.Tk()
        root.title("Jugador 2")
        myClock1 = tkinter.Label(root)
        today = datetime.datetime.now()
        hora = today
        myClock1['text'] = today
        myClock1['font'] = 'Tahoma 50 bold'
        myClock1.grid(row=0, column=0, columnspan=3)
        # myClock1.pack()
        suma = tkinter.Label(root)
        suma['font'] = 'Tahoma 20 bold'
#        suma['text'] = '500'
        suma.grid(row=4, column=1)
        def archivo():# we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
            s = socket.socket(socket.AF_INET,   socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            print("Connected with Server")
            s.send(filename[0].encode())
            print(os.stat(filename[0]).st_size)
            s.send(str(os.stat(filename[0]).st_size).encode())
            f = open(filename[0],'rb')
            l = f.read(1024)
            while (l):
                s.send(l)
                l = f.read(1024)
            f.close()
            print('Done sending')
            sum = s.recv(1024).decode()
            print(sum)
            suma['text'] = sum
            s.close()


        bMin = tkinter.Button(root, text='enviar archivo', command=archivo)

        bMin.grid(row=1, column=1)

        def tic():
            self.hora = self.hora+datetime.timedelta(seconds=self.uno)
            myClock1['text'] = self.hora.strftime('%H:%M:%S')

        def tac():
            tic()
            myClock1.after(int(self.tiempo), tac)
        tac()
        root.mainloop()

class Comunicador(threading.Thread):
    def run(self):
        r1 = relojHilo(name="principal")
        r1.start()
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind((UDP_IP, UDP_PORT))
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode()
            print ("received message:", message)
            if message == 'pausa':
                if r1.uno == 1:
                    r1.uno = 0
                else:
                    r1.uno = 1
            elif message == "acelera":
                r1.tiempo = r1.tiempo/2
            elif message == "realentiza":
                r1.tiempo = r1.tiempo*2
            else:
                r1.hora = datetime.datetime.strptime(data.decode(), '%H:%M:%S')


encoding = 'utf-8'
c1=Comunicador(name="hilo1")
c1.start()