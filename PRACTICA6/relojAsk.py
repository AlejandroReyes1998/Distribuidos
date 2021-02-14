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
import json

#S1Ad = ('10.100.67.60',9005)
S1Ad = ("127.0.0.1",9005)
prioridadS1=1
#S2Ad = ('10.100.76.144',9015)
S2Ad = ("127.0.0.1",9015)
prioridadS2=0
IpS = ("127.0.0.1",2005)
#IpS = ("127.0.0.1",2005)
#PortS = 2005

class Comunicador1(threading.Thread):
	def run(self):
		print("Waiting....")
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
		#sock.bind(('10.100.70.121',9005))
		sock.bind(('127.0.0.1',9005))
		while True:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			message = data.decode()
			ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
			hora = ajit.now().strftime('%H:%M:%S')
			print('llego de S1: ',message,'  es: ',hora)
			sock.sendto(hora.encode(),addr)
			flag = 0
			if datetime.datetime.strptime(hora, '%H:%M:%S') > ajitzi:
				flag = 1
			try:
				connection = mysql.connector.connect(host='localhost',
													database='Reloj',
													user='root',
													password='')
				mySql_insert_query = "INSERT INTO HoraCentral (hPrev,hRef) VALUES ('{}','{}') ".format(message,hora)

				mySql_insert_query2 = "INSERT INTO HoraEquipos (idhsincr,idequipo,hEquipo,aEquipo,ralentizar) VALUES ((select max(id) from HoraCentral),'{}','{}','{}','{}') ".format(1,hora,message,flag)
				cursor = connection.cursor()
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
		print("Waiting2....")
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
		#sock.bind(('10.100.70.121',9015))
		sock.bind(('127.0.0.1',9015))
		while True:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			message = data.decode()
			ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
			hora = ajit.now().strftime('%H:%M:%S')
			print('llego de S2: ',message,'  es: ',hora)
			sock.sendto(hora.encode(),addr)
			flag = 0
			if datetime.datetime.strptime(hora, '%H:%M:%S') > ajitzi:
				flag = 1
			try:
				connection = mysql.connector.connect(host='localhost',
													database='Reloj',
													user='root',
													password='')
				mySql_insert_query = "INSERT INTO HoraCentral (hPrev,hRef) VALUES ('{}','{}') ".format(message,hora)

				mySql_insert_query2 = "INSERT INTO HoraEquipos (idhsincr,idequipo,hEquipo,aEquipo,ralentizar) VALUES ((select max(id) from HoraCentral),'{}','{}','{}','{}') ".format(2,hora,message,flag)
				cursor = connection.cursor()
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

if(prioridadS1 > prioridadS2):
	IpS = S1Ad
else:
	IpS = S2Ad

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
message = 'RELOJ'
sock.sendto(message.encode(), (IpS))

c1 = Comunicador1()
c1.start()
c2 = Comunicador2()
c2.start()