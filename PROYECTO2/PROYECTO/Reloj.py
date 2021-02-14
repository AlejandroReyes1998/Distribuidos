import socket
import threading
from tkinter import *
import tkinter
from threading import Thread
import time
import random
import datetime
from datetime import datetime as ajit
from time import strftime
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from IPS import *
import json

Ips = IP('R')

class Comunicador1(threading.Thread):
    def run(self):
        print("Waiting....")
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind(Ips.C1)
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode()
            ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
            hora = ajit.now().strftime('%H:%M:%S')
            print('llego de C1: ',message,'  es: ',hora)
            sock.sendto(hora.encode(),addr)
            flag = 0
            if datetime.datetime.strptime(hora, '%H:%M:%S') > ajitzi:
                flag = 1
            try:
                connection = mysql.connector.connect(host='localhost',database='reloj',user='root',password='')
                mySql_select = "Select IFNULL(max(id),-1) from hora_central"
                cursor = connection.cursor(buffered=True)
                cursor.execute(mySql_select)
                res = cursor.fetchone()    
                id = int(res[0])+1
                mySql_insert_query = "INSERT INTO hora_central (id,h_prev,h_ref) VALUES ({},'{}','{}'); ".format(id,message,hora)
                if flag == 1:
                    mySql_insert_query2 = "insert into hora_equipos (id_h_sinc,id_equipo,h_equipo,acelerar,realentizar) values ({},1,'{}','{}','{}'); ".format(id,message,'SI','NO') 
                else :
                    mySql_insert_query2 = "insert into hora_equipos (id_h_sinc,id_equipo,h_equipo,acelerar,realentizar) values ({},1,'{}','{}','{}'); ".format(id,message,'NO','SI') 
                result = cursor.execute(mySql_insert_query)
                result2 = cursor.execute(mySql_insert_query2)
                connection.commit()
                print("Record inserted successfully into Laptop table")
                cursor.close()

            except Error as error:
                print("Failed to insert record into Laptop table {}".format(error))

            finally:
                if (connection.is_connected()):
                    connection.close()
                    print("MySQL connection is closed")

class Comunicador2(threading.Thread):
    def run(self):
        print("Waiting....")
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind(Ips.C2)
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode()
            ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
            hora = ajit.now().strftime('%H:%M:%S')
            print('llego de C2: ',message,'  es: ',hora)
            sock.sendto(hora.encode(),addr)
            flag = 0
            if datetime.datetime.strptime(hora, '%H:%M:%S') > ajitzi:
                flag = 1
            try:
                connection = mysql.connector.connect(host='localhost',database='reloj',user='root',password='')
                mySql_select = "Select IFNULL(max(id),-1) from hora_central"
                cursor = connection.cursor(buffered=True)
                cursor.execute(mySql_select)
                res = cursor.fetchone()    
                id = int(res[0])+1
                mySql_insert_query = "INSERT INTO hora_central (id,h_prev,h_ref) VALUES ({},'{}','{}'); ".format(id,message,hora)
                if flag == 1:
                    mySql_insert_query2 = "insert into hora_equipos (id_h_sinc,id_equipo,h_equipo,acelerar,realentizar) values ({},2,'{}','{}','{}'); ".format(id,message,'SI','NO') 
                else :
                    mySql_insert_query2 = "insert into hora_equipos (id_h_sinc,id_equipo,h_equipo,acelerar,realentizar) values ({},2,'{}','{}','{}'); ".format(id,message,'NO','SI') 
                result = cursor.execute(mySql_insert_query)
                result2 = cursor.execute(mySql_insert_query2)
                connection.commit()
                print("Record inserted successfully into Laptop table")
                cursor.close()

            except Error as error:
                print("Failed to insert record into Laptop table {}".format(error))

            finally:
                if (connection.is_connected()):
                    connection.close()
                    print("MySQL connection is closed")

class Comunicador3(threading.Thread):
    def run(self):
        print("Waiting....")
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
        sock.bind(Ips.C3)
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode()
            ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
            hora = ajit.now().strftime('%H:%M:%S')
            print('llego de C3: ',message,'  es: ',hora)
            sock.sendto(hora.encode(),addr)
            flag = 0
            if datetime.datetime.strptime(hora, '%H:%M:%S') > ajitzi:
                flag = 1
            try:
                connection = mysql.connector.connect(host='localhost',database='reloj',user='root',password='')
                mySql_select = "Select IFNULL(max(id),-1) from hora_central"
                cursor = connection.cursor(buffered=True)
                cursor.execute(mySql_select)
                res = cursor.fetchone()    
                id = int(res[0])+1
                mySql_insert_query = "INSERT INTO hora_central (id,h_prev,h_ref) VALUES ({},'{}','{}'); ".format(id,message,hora)
                if flag == 1:
                    mySql_insert_query2 = "insert into hora_equipos (id_h_sinc,id_equipo,h_equipo,acelerar,realentizar) values ({},3,'{}','{}','{}'); ".format(id,message,'SI','NO') 
                else :
                    mySql_insert_query2 = "insert into hora_equipos (id_h_sinc,id_equipo,h_equipo,acelerar,realentizar) values ({},3,'{}','{}','{}'); ".format(id,message,'NO','SI') 
                result = cursor.execute(mySql_insert_query)
                result2 = cursor.execute(mySql_insert_query2)
                connection.commit()
                print("Record inserted successfully into Laptop table")
                cursor.close()

            except Error as error:
                print("Failed to insert record into Laptop table {}".format(error))

            finally:
                if (connection.is_connected()):
                    connection.close()
                    print("MySQL connection is closed")

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
message = 'RELOJ'
sock.sendto(message.encode(), Ips.respaldo)

c1 = Comunicador1()
c1.start()
c2 = Comunicador2()
c2.start()
c3 = Comunicador3()
c3.start()
