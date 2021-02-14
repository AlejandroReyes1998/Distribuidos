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
from IPS import *
import json

Ips = IP('U3')

class relojHilo(threading.Thread):
    hora = datetime.datetime.now()
    tiempo = 1000
    uno = 1

    def run(self):
        root = tkinter.Tk()
        root.title("Usuario 3")
        myClock1 = tkinter.Label(root)
        today = datetime.datetime.now()
        hora = today
        myClock1['text'] = today
        myClock1['font'] = 'Tahoma 50 bold'
        myClock1.grid(row=0, column=0, columnspan=3)
        # myClock1.pack()
        nums = []
        for x in range(15):
            nums.append(tkinter.Label(root))
            nums[x]['font'] = 'Tahoma 20'
            nums[x]['text'] = str(x+1)+" = "
            nums[x].grid(row=x+4, column=0)

        ind = 4
        for x in range(15,30):
            nums.append(tkinter.Label(root))
            nums[x]['font'] = 'Tahoma 20'
            nums[x]['text'] = str(x+1)+" = "
            nums[x].grid(row=ind, column=2)
            ind = ind + 1
        
        vals = []
        for x in range(15):
            vals.append(tkinter.Label(root))
            vals[x]['font'] = 'Tahoma 20 bold'
            vals[x].grid(row=x+4, column=1)

        ind = 4
        for x in range(15,30):
            vals.append(tkinter.Label(root))
            vals[x]['font'] = 'Tahoma 20 bold'
            vals[x].grid(row=ind, column=3)
            ind = ind + 1    
        
        def archivo():# we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
            s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
            s.sendto("3".encode(), Ips.enviar)
            s.sendto(filename[0].encode(), Ips.enviar)
            print("Connected with Server")
            print(os.stat(filename[0]).st_size)
            s.sendto(str(os.stat(filename[0]).st_size).encode(),Ips.enviar)
            f = open(filename[0],'rb')
            l = f.read(1024)
            while (l):
                s.sendto(l, Ips.enviar)
                l = f.read(1024)
            f.close()
            print('Done sending')
            sum = s.recv(1024).decode()
            valores = json.loads(sum)
            for x in range(30):
                vals[x]['text'] = valores.get(str(x+1))
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
        r1 = relojHilo(name="Usuario 1")
        r1.start()
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind(Ips.recibir)
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


c1=Comunicador(name="hilo1")
c1.start()