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
import json

#MANDAR HORAS A CLIENTES
#clientePrincipal = ("10.100.68.209",5015)
clientePrincipal = ("127.0.0.1",5015)
#clienteSecundario1 = ("127.0.0.1",5006)
#clienteSecundario2 = ("127.0.0.1",5007)

#RECIBIR ARCHIVOS TCP
#HOST = "10.100.70.121"
HOST = "127.0.0.1"
PORT = 6015

#Para recibir del servidor 1
#HOSTx = "10.100.70.121"
HOSTx = "127.0.0.1"
PORTx = 7005

#Para mandar al servidor 1
#IpS1 = "10.100.67.60"
IpS1 = "127.0.0.1"
PortS1 = 8005

#Pedir la hora
#ServerHora = ("10.100.76.144",9015)
ServerHora = ("127.0.0.1",9015)
#Coordinacion
miPrioridad = 0
#recibir cuando soy reloj
#IpR = "10.100.70.121"
IpR = "127.0.0.1"
PortR = 2005
#enviar al respaldo
#IpE = "10.100.67.60"
IpE = "127.0.0.1"
PortE = 2005

class Comunicador1(Thread):
	def __init__(self,r1):
		Thread.__init__(self)
		self.r1=r1

	def run(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UD
		sock.bind((IpR, PortR))
		print('siendo reloj respaldo...')
		while True:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			message = data.decode()
			if(message.startswith('RELOJ')):
				print('desperto!')
				rel = Reloj(r1)
				rel.start()
				break
			else:
				hora = self.r1.hora.strftime('%H:%M:%S')
				print('llego de S1: ',message,'  es: ',hora)
				sock.sendto(hora.encode(),addr)
				ajitzi = datetime.datetime.strptime(message, '%H:%M:%S')
				hora = ajit.now().strftime('%H:%M:%S')
				print('llego de S1: ',message,'  es: ',hora)
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
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((HOST, PORT))
		self.s.listen(5)
	
	def run(self):
		print("Listening ...")

		while True:
			conn, addr = self.s.accept()
			print("[+] Client connected: ", addr)
			nombre = conn.recv(1024).decode()
			print(nombre.split("/")[-1])
			tama = int(conn.recv(3).decode())
			# get file name to download
			with open(nombre.split("/")[-1], 'wb') as f:
				while tama>0:
					print('receiving data...')
					data = conn.recv(1024 if tama>1024 else tama)
					# write data to a file
					f.write(data)
					tama = tama-1024
			f.close()
			f1 = open(nombre.split("/")[-1], "r")
			archivo = f1.read()
			f1.close
			numeros = archivo.split()
			suma = 0
			for n in numeros:
				suma = suma + int(n)
			print(suma)
			print(addr[0],addr[1],self.r1.hora.strftime('%H:%M:%S'),suma)
			print('Successfully get the file')
			conn.sendall(str(suma).encode())
			conn.close()

			try:
				connection = mysql.connector.connect(host='localhost',
													database='base2',
													user='root',
													password='')
				xd=self.r1.hora.strftime('%H:%M:%S')
				mySql_insert_query = "INSERT INTO info (ip, puerto, jugador, hora, resultado) VALUES ('{}','{}','{}','{}',{}) ".format(addr[0],addr[1],1,xd,suma)

				cursor = connection.cursor()
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
			data = json.dumps({"ip": addr[0], "puerto": addr[1], "jugador": 1,"hora":xd,"resultado":suma})
			s.sendto(data.encode(),((IpS1,PortS1)))
			s.close()

class reciveServer(Thread):
	def __init__(self,r1):
		Thread.__init__(self)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind((HOSTx, PORTx))
		self.r1 = r1
	
	def run(self):
		print("Listening Server...")
		while True:
			data, addr = self.s.recvfrom(1024)
			mess = data.decode()
			print(mess)
			if (mess.startswith('PRIORIDAD')):
				suPrioridad = int(mess.split('-')[1])
				if(suPrioridad > miPrioridad):
					while True:
						try:
							time.sleep(5)
							print('Que hora es?')
							sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
							sock.settimeout(1)
							message = self.r1.hora.strftime('%H:%M:%S')
							starting_point = time.time()
							sock.sendto(message.encode(), (IpE, PortE))
							data, addr = sock.recvfrom(1024)
							elapsed_time = time.time () - starting_point
							print(data.decode())
							horaReal = datetime.datetime.strptime(data.decode(), '%H:%M:%S')
							if horaReal.time() > r1.hora.replace(microsecond=0).time():
								r1.hora = horaReal+datetime.timedelta(seconds=round(elapsed_time))
								r1.tiempo = 1000
							else:
								if(r1.tiempo < 8000):
										r1.tiempo = r1.tiempo*2
						except Exception as e:
							print(e)
							print('desperto')
							rel = Reloj(r1)
							rel.start()
							break
				else:
					c1 = Comunicador1(r1)
					c1.start()
			else:
				print("[+] Communicating with backup server: ", addr)
				data = json.loads(data.decode())
				theip= data.get("ip")
				theport = data.get("puerto")
				theplayer = data.get("jugador")
				thehour = data.get("hora")
				theresult = data.get("resultado")

				try:
					connection = mysql.connector.connect(host='localhost',
														database='base2',
														user='root',
														password='')
					xd=self.r1.hora.strftime('%H:%M:%S')
					mySql_insert_query = "INSERT INTO info (ip, puerto, jugador, hora, resultado) VALUES ('{}','{}','{}','{}',{}) ".format(theip,theport,theplayer,xd,theresult)

					cursor = connection.cursor()
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
				print("Information stored in backup server")

def enviar(r1):
	MESSAGE1 = r1.hora.strftime('%H:%M:%S')
	hora2 = r1.hora+datetime.timedelta(hours=1.5)
	hora3 = r1.hora-datetime.timedelta(hours=1.5)
	MESSAGE2 = hora2.strftime('%H:%M:%S')
	MESSAGE3 = hora3.strftime('%H:%M:%S')
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE1.encode(), (clientePrincipal))
	# sock.sendto(MESSAGE2.encode(), (clienteSecundario1))
	# sock.sendto(MESSAGE3.encode(), (clienteSecundario2))

def pauseReanude(r1):
	if (r1.uno == 0):
		r1.uno = 1
	else:
		r1.uno = 0

	print('pause/reanude el reloj : ')
	MESSAGE = 'pausa'
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE.encode(), (clientePrincipal))
	# sock.sendto(MESSAGE.encode(), (clienteSecundario1))
	# sock.sendto(MESSAGE.encode(), (clienteSecundario2))

def acelerar(r1):
	r1.tiempo = r1.tiempo/2
	print('acelere el reloj : ')
	MESSAGE = 'acelera'
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE.encode(), (clientePrincipal))
	# sock.sendto(MESSAGE.encode(), (clienteSecundario1))
	# sock.sendto(MESSAGE.encode(), (clienteSecundario2))

def realentiza(r1):
	r1.tiempo = r1.tiempo*2
	print('realentize el reloj : ')
	MESSAGE = 'realentiza'
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE.encode(), (clientePrincipal))
	# sock.sendto(MESSAGE.encode(), (clienteSecundario1))
	# sock.sendto(MESSAGE.encode(), (clienteSecundario2))

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
				sock.sendto(message.encode(), (ServerHora))
				data, addr = sock.recvfrom(1024)
				elapsed_time = time.time () - starting_point
				print(elapsed_time)
				print(data.decode())
				horaReal = datetime.datetime.strptime(data.decode(), '%H:%M:%S')
				if horaReal.time() > r1.hora.replace(microsecond=0).time():
					r1.hora = horaReal+datetime.timedelta(seconds=elapsed_time)
					r1.tiempo = 1000
				else:
					if(r1.tiempo < 8000):
						r1.tiempo = r1.tiempo*2
			except:
				s = socket.socket(socket.AF_INET,   socket.SOCK_DGRAM)
				data = 'PRIORIDAD-'+str(miPrioridad)
				print(data)
				s.sendto(data.encode(),(IpS1, PortS1))
				break

root = tkinter.Tk()
root.title("Servidor 2")
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
servc = reciveServer(r1)
servc.start()
rel = Reloj(r1)
rel.start()
root.mainloop()