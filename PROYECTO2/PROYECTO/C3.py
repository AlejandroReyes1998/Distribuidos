import socket
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

Ips = IP('C3')

class Comunicador1(Thread):
	def __init__(self,r1):
		Thread.__init__(self)
		self.r1=r1

	def run(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
		sock.bind(Ips.respaldo)
		print(Ips.respaldo)
		print('siendo reloj respaldo...')
		while True:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			message = data.decode()
			if(message.startswith('RELOJ')):
				print('desperto!')
				rel = Reloj(r1)
				rel.start()
				break
			elif(message.startswith('C2')):
				data, addr = sock.recvfrom(1024)
				message = data.decode()
				hora = self.r1.hora.strftime('%H:%M:%S')
				print('llego de C2: ',message,'  es: ',hora)
				sock.sendto(hora.encode(),addr)
				ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
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
			elif(message.startswith('C1')):
				data, addr = sock.recvfrom(1024)
				message = data.decode()
				hora = self.r1.hora.strftime('%H:%M:%S')
				print('llego de C1: ',message,'  es: ',hora)
				sock.sendto(hora.encode(),addr)
				ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
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

class relojHilo(Thread):
	hora = datetime.datetime.now()
	tiempo = 1000
	uno = 1
	def __init__(self, root):
		self.root=root
		Thread.__init__(self)

	def run(self):

		myClock1 = tkinter.Label(self.root)

		today = datetime.datetime.now()
		hora = today
		myClock1['text'] = today

		myClock1['font'] = 'Tahoma 50 bold'
		myClock1.grid(row=0, column=0, columnspan=3)

		def anaSeg():
			self.hora = self.hora+datetime.timedelta(seconds=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('añadi segundos al hilo: ')

		bSeg = tkinter.Button(self.root, text='añade segundo', command=anaSeg)
		bSeg.grid(row=1, column=2)


		def anaMin():
			self.hora = self.hora+datetime.timedelta(minutes=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('añadi minutos al hilo: ')

		bMin = tkinter.Button(self.root, text='añade minuto', command=anaMin)

		bMin.grid(row=1, column=1)

		def anaHor():
			self.hora = self.hora+datetime.timedelta(hours=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('añadi horas al hilo: ')

		bHor = tkinter.Button(self.root, text='añade hora', command=anaHor)

		bHor.grid(row=1, column=0)

		def redSeg():
			self.hora = self.hora-datetime.timedelta(seconds=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('reduje segundos al hilo: ')

		brSeg = tkinter.Button(self.root, text='reduce segundo', command=redSeg)
		brSeg.grid(row=2, column=2)


		def redMin():
			self.hora = self.hora-datetime.timedelta(minutes=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('reduje un minuto al hilo: ')

		brMin = tkinter.Button(self.root, text='reduce minuto', command=redMin)

		brMin.grid(row=2, column=1)

		def redHor():
			self.hora = self.hora-datetime.timedelta(hours=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('reduje una hora al hilo: ')

		brHor = tkinter.Button(self.root, text='reduce hora', command=redHor)

		brHor.grid(row=2, column=0)

		def randDate():
			self.hora = self.hora + \
				datetime.timedelta(seconds=random.randint(1, 1000000))
			myClock1['text'] = self.hora

		def tic():
			self.hora = self.hora+datetime.timedelta(seconds=self.uno)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')

		def tac():
			tic()
			myClock1.after(int(self.tiempo), tac)

	   
		randDate()
		
		tac()

class ReadTCP(Thread):
	def __init__(self,r1):
		Thread.__init__(self)
		self.r1=r1
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(Ips.recibir)
	
	def run(self):
		print("Listening ...")

		while True:
			data, addr = self.s.recvfrom(1024)
			print("[+] Client connected: ", addr)
			if (data.decode().startswith('respaldo')):
				data, addr = self.s.recvfrom(1024)
				mess = data.decode()
				data = json.loads(mess)
				theip= data.get("ip")
				theport = data.get("puerto")
				thefront = data.get("front")
				thehour = self.r1.hora.strftime('%H:%M:%S')# data.get("hora")
				frecuencias = data.get("frecuencias")

				try:
					connection = mysql.connector.connect(host='localhost',
														database='base1',
														user='root',
														password='')
					cursor = connection.cursor()
					for x in range (1,31):
						mySql_insert_query = "insert into frecuencias(front_end,numero,frecuencia,ip,puerto,hora) values ({},{},{},'{}','{}','{}');".format(thefront,x,frecuencias[str(x)],theip,theport,thehour)
						result = cursor.execute(mySql_insert_query)
					
					connection.commit()
					print("Record inserted successfully into Laptop table")
					cursor.close()

				except Error as error:
					print("Failed to insert record into Laptop table {}".format(error))

				finally:
					if (connection.is_connected()):
						connection.close()
						print("MySQL connection is closed")
			elif (data.decode().startswith('desperte-1')):
				prioridades = Ips.prioridades
				if(prioridades['Coor3'] > prioridades['Coor2']):
					try:
						connection = mysql.connector.connect(host='localhost',
														database='base1',
														user='root',
														password='')
						mySql_select = "Select front_end,numero,frecuencia,ip,puerto,hora from frecuencias"
						cursor = connection.cursor(buffered=True)
						cursor.execute(mySql_select)
						res = cursor.fetchall()    
						connection.commit()
						cursor.close()

					except Error as error:
						print("Failed to insert record into Laptop table {}".format(error))

					finally:
						if (connection.is_connected()):
							connection.close()
							print("MySQL connection is closed")
					if len(res) > 0:
						s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
						tabla = {}
						i = 0
						for tup in res:
							tup2 ={}
							for x in range(6):
								tup2[str(x)] = tup[x]
							tabla[str(i)] = tup2
							i = i+1
						data = json.dumps(tabla)	
						print(data)
						s.sendto("refresh".encode(),Ips.c1)
						tam = len(data.encode())
						print(tam)
						s.sendto(str(tam).encode(),Ips.c1)
						while tam>0:
							if tam > 1024:
								cadena = data[0:1023]
								data = data[1023:]
								tam = tam-1024
								s.sendto(cadena.encode(),Ips.c1)
							else:
								s.sendto(data.encode(),Ips.c1)
								tam = 0
			elif (data.decode().startswith('desperte-2')):
				if(prioridades['Coor3'] > prioridades['Coor1']):
					try:
						connection = mysql.connector.connect(host='localhost',
														database='base1',
														user='root',
														password='')
						mySql_select = "Select front_end,numero,frecuencia,ip,puerto,hora from frecuencias"
						cursor = connection.cursor(buffered=True)
						cursor.execute(mySql_select)
						res = cursor.fetchall()    
						connection.commit()
						cursor.close()

					except Error as error:
						print("Failed to insert record into Laptop table {}".format(error))

					finally:
						if (connection.is_connected()):
							connection.close()
							print("MySQL connection is closed")
					if len(res) > 0:
						s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
						tabla = {}
						i = 0
						for tup in res:
							tup2 ={}
							for x in range(6):
								tup2[str(x)] = tup[x]
							tabla[str(i)] = tup2
							i = i+1
						data = json.dumps(tabla)	
						print(data)
						s.sendto("refresh".encode(),Ips.c2)
						tam = len(data.encode())
						print(tam)
						s.sendto(str(tam).encode(),Ips.c2)
						while tam>0:
							if tam > 1024:
								cadena = data[0:1023]
								data = data[1023:]
								tam = tam-1024
								s.sendto(cadena.encode(),Ips.c2)
							else:
								s.sendto(data.encode(),Ips.c2)
								tam = 0
			elif (data.decode().startswith('refresh')):
				data, addr = self.s.recvfrom(1024)
				tam = int(data.decode())
				print(tam)
				cadena = ""
				while tam > 0:
					if tam > 1024:
						data, addr = self.s.recvfrom(1024)
						cadena = cadena + data.decode()
						tam = tam-1023
					else:
						data, addr = self.s.recvfrom(tam)
						cadena = cadena + data.decode()
						tam = 0
				
				print(len(cadena.encode()))
				data = json.loads(cadena)
				thehour = self.r1.hora.strftime('%H:%M:%S')
				try:
					connection = mysql.connector.connect(host='localhost',
														database='base1',
														user='root',
														password='')
					cursor = connection.cursor(buffered=True)
					mySql_delete = "delete from frecuencias"
					result2 = cursor.execute(mySql_delete)
					for x in range(len(data)):
						row = data[str(x)]
						mySql_insert_query = "insert into frecuencias(front_end,numero,frecuencia,ip,puerto,hora) values ({},{},{},'{}','{}','{}');".format(row['0'],row['1'],row['2'],row['3'],row['4'],thehour)
						result = cursor.execute(mySql_insert_query)
					
					connection.commit()
					print("Record inserted successfully into Laptop table")
					cursor.close()

				except Error as error:
					print("Failed to insert record into Laptop table {}".format(error))

				finally:
					if (connection.is_connected()):
						connection.close()
						print("MySQL connection is closed")
			else :
				front = int(data.decode())
				data, addr = self.s.recvfrom(1024)	
				nombre = data.decode()
				print(nombre.split("/")[-1])
				data, addr = self.s.recvfrom(1024)
				tama = int(data.decode())
				# get file name to download
				with open(nombre.split("/")[-1], 'wb') as f:
					while tama>0:
						print('receiving data...')
						data, addr = self.s.recvfrom(1024 if tama>1024 else tama)
						# write data to a file
						f.write(data)
						tama = tama-1024
				f.close()
				f1 = open(nombre.split("/")[-1], "r")
				string = f1.read().split()
				f1.close() 

				frecuencias = {}
				for x in range (1,31):
					frecuencias[str(x)]=0

				for i in string:
					frecuencias[i]=frecuencias[i]+1

				data = json.dumps(frecuencias)
				print('Successfully get the file')
				self.s.sendto(data.encode(),addr)
				print(addr[0],' ',addr[1])
				try:
					connection = mysql.connector.connect(host='localhost',
														database='base1',
														user='root',
														password='')
					xd=self.r1.hora.strftime('%H:%M:%S')
					cursor = connection.cursor()
					for x in range (1,31):
						mySql_insert_query = "insert into frecuencias(front_end,numero,frecuencia,ip,puerto,hora) values ({},{},{},'{}','{}','{}');".format(front,x,frecuencias[str(x)],addr[0],addr[1],xd)
						result = cursor.execute(mySql_insert_query)
					
					connection.commit()
					print("Record inserted successfully into Laptop table")
					cursor.close()

				except Error as error:
					print("Failed to insert record into Laptop table {}".format(error))

				finally:
					if (connection.is_connected()):
						connection.close()
						print("MySQL connection is closed")

				s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
				data = json.dumps({"front": front, "frecuencias": frecuencias, "ip": addr[0],"puerto":addr[1],"hora":xd})
				s.sendto("respaldo".encode(),Ips.enviar1)
				s.sendto(data.encode(),Ips.enviar1)
				s.sendto("respaldo".encode(),Ips.enviar2)
				s.sendto(data.encode(),Ips.enviar2)
				s.close()

def enviar(r1):
	MESSAGE1 = r1.hora.strftime('%H:%M:%S')
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE1.encode(),Ips.cliente)

def pauseReanude(r1):
	if (r1.uno == 0):
		r1.uno = 1
	else:
		r1.uno = 0

	print('pause/reanude el reloj : ')
	MESSAGE = 'pausa'
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE.encode(), Ips.cliente)

def acelerar(r1):
	r1.tiempo = r1.tiempo/2
	print('acelere el reloj : ')
	MESSAGE = 'acelera'
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE.encode(), Ips.cliente)

def realentiza(r1):
	r1.tiempo = r1.tiempo*2
	print('realentize el reloj : ')
	MESSAGE = 'realentiza'
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE.encode(), Ips.cliente)

class Reloj(Thread):
	def __init__(self, root):
		self.root=root
		Thread.__init__(self)

	def run(self):
		while True:
			try:
				time.sleep(5)
				print('Que hora es?')
				sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
				sock.settimeout(1)
				message = self.root.hora.strftime('%H:%M:%S')
				starting_point = time.time()
				sock.sendto(message.encode(), Ips.reloj)
				data, addr = sock.recvfrom(1024)
				elapsed_time = time.time () - starting_point
				print(elapsed_time)
				print(data.decode())
				horaReal = datetime.datetime.strptime(data.decode(), '%H:%M:%S')
				if horaReal.time() >  self.root.hora.replace(microsecond=0).time():
					self.root.hora = horaReal+datetime.timedelta(seconds=elapsed_time)
					self.root.tiempo = 1000
				else:
					if( self.root.tiempo < 8000):
						self.root.tiempo = self.root.tiempo*2
			except:
				prioridades = Ips.prioridades
				if(prioridades['Coor3'] > prioridades['Coor2'] > prioridades['Coor1']):
					c1 = Comunicador1(r1)
					c1.start()
				else:
					while True:
						try:
							time.sleep(5)
							print('Que hora es?')
							sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
							sock2.settimeout(1)
							message = self.root.hora.strftime('%H:%M:%S')
							starting_point = time.time()
							sock2.sendto("C3".encode(),Ips.respaldo)
							sock2.sendto(message.encode(),Ips.respaldo)
							data, addr = sock2.recvfrom(1024)
							elapsed_time = time.time () - starting_point
							print(data.decode())
							horaReal = datetime.datetime.strptime(data.decode(), '%H:%M:%S')
							if horaReal.time() > self.root.hora.replace(microsecond=0).time():
								self.root.hora = horaReal+datetime.timedelta(seconds=round(elapsed_time))
								self.root.tiempo = 1000
							else:
								if(self.root.tiempo < 8000):
										self.root.tiempo = self.root.tiempo*2
						except:
							print('desperto!')
							rel = Reloj(r1)
							rel.start()
							break
				break
			


root = tkinter.Tk()
root.title("Coordinador 3")
r1 = relojHilo(root)

bEnviar = tkinter.Button(
			root, text='enviar', command=lambda : enviar(r1))
		# bMin.pack()
bEnviar.grid(row=6, column=1)
		

bPause = tkinter.Button(
	root, text='pause/reanude reloj', command=lambda:pauseReanude(r1))
bPause.grid(row=5, column=1)


bAce = tkinter.Button(root, text='acelera reloj', command=lambda:acelerar(r1))
bAce.grid(row=3, column=1)

bDece = tkinter.Button(
	root, text='realentiza reloj', command=lambda:realentiza(r1))
bDece.grid(row=4, column=1)

r1.start()
readTCP = ReadTCP(r1)
readTCP.start()
rel = Reloj(r1)
rel.start()
try:
	s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
	s.sendto("desperte-3".encode(),Ips.c1)
	s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
	s.sendto("desperte-3".encode(),Ips.c2)
	s.close()
except:
	pass
root.mainloop()

