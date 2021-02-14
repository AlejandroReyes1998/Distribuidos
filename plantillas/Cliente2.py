import socket
import threading
import sys
import pickle
import os
import math
import App
import subprocess
from struct import pack
from pathlib import Path

class Cliente():
    # go_flag can have like 4 states duuuuuuuudeeee so fucked up
    go_flag = 0
    resend_flag = 0
    split_extensions = ['a', 'b', 'c', 'd']
    mega_list = App.collectFiles()
    
    def __init__(self, host="localhost", port=4004):
        home_path=str(Path.home())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        msg_recv = threading.Thread(target=self.msg_recv)
        msg2 = []
        msg_recv.daemon = True
        msg_recv.start()

        while True:
            msg = input()
            if msg.lower() == "salir":
                self.sock.close()
                os._exit(0)
            elif msg.lower() == "create":
                print("Creando Backup...")
                print("Listo.")
            elif msg.lower() == "send":
                for path in self.mega_list:
                    file_name = path.split('/')[-1]
                    print('FILENAME',file_name)
                    # we gotta do the stuff here
                    if ' ' not in file_name:
                        # purge buffer file
                        command = 'rm ~/buffer_file/*'
                        subprocess.run(command, shell=True)
                        # retrieve dat file
                        # split the file in 4 parts. efficently. by usin split
                        command = 'split -n 4 '+ path +' '+home_path+'/buffer_file/'+file_name
                        print(command)
                        subprocess.run(command, shell=True)
                        # ya need a directory named ~/buffer_file for fucks sake
                        command = 'ls '+home_path+'/buffer_file/'
                        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
                        subfiles = result.split('\n')[:4]
                        
            
                        #print(file_name,size)
                        
                       
                        for subfile in subfiles:
                            while self.go_flag != 1:
                                pass
                            print(home_path+'/buffer_file/'+subfile)
                            size = os.path.getsize(home_path+'/buffer_file/'+subfile)
                            self.sock.send(pickle.dumps("send "+str(size)+" "+subfile))
                            while self.go_flag != 1:
                                pass                            
                            print('go!!!')
                            print('go_flagpre', self.go_flag)
                            with open(home_path+'/buffer_file/'+subfile, 'rb') as infile:
                                d = infile.read(64)
                                while d:
                                    self.sock.send(d)
                                    d = infile.read(64)
                            print('go_flagpost',self.go_flag)            
                            print('listo')
                                    
            elif msg.lower() == "recv":
                pass
            else:
                self.sock.sendall(pickle.dumps(msg))
                
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    print("Servidor cerrado")
                    self.sock.close()
                    os._exit(0)
                else:
                    if 'go_flag' in pickle.loads(data).lower():
                        self.go_flag = 1
                    if 'stop_flag' in pickle.loads(data).lower():
                        self.go_flag = 0
                    elif 'resend_flag' in pickle.loads(data).lower():
                        self.resend_flag= 1
                        #print('flags',self.go_flag,self.resend_flag)
            except:
                pass

c = Cliente(str(sys.argv[1]),int(sys.argv[2]))
