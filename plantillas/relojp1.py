#import essential modules
from tkinter import *
import tkinter
import threading
import time
import random
import datetime
from time import strftime

class relojHilo(threading.Thread):
	hora= datetime.datetime.now()
	tiempo= 1000
	uno=1
	def run(self):
		
		
		root = tkinter.Tk()
		root.title(threading.currentThread().getName())
		myClock1 = tkinter.Label(root)
		
		today = datetime.datetime.now()
		hora=today
		myClock1['text'] = today

		myClock1['font'] = 'Tahoma 50 bold'
		myClock1.grid(row=0,column=0,columnspan=3)
		#myClock1.pack()
		

		def anaSeg():
			self.hora=self.hora+datetime.timedelta(seconds=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('añadi segundos al hilo: ',threading.currentThread().getName())
		
		bSeg=tkinter.Button(root,text='añade segundo',command=anaSeg)
		bSeg.grid(row=1,column=2)
		#bSeg.pack()


		def anaMin():
			self.hora=self.hora+datetime.timedelta(minutes=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('añadi minutos al hilo: ',threading.currentThread().getName())
		
		bMin=tkinter.Button(root,text='añade minuto',command=anaMin)
		#bMin.pack()
		bMin.grid(row=1,column=1)
		print(today)


		def anaHor():
			self.hora=self.hora+datetime.timedelta(hours=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('añadi horas al hilo: ',threading.currentThread().getName())
		
		bHor=tkinter.Button(root,text='añade hora',command=anaHor)
		#bMin.pack()
		bHor.grid(row=1,column=0)
		print(today)



		def redSeg():
			self.hora=self.hora-datetime.timedelta(seconds=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('reduje segundos al hilo: ',threading.currentThread().getName())
		
		brSeg=tkinter.Button(root,text='reduce segundo',command=redSeg)
		brSeg.grid(row=2,column=2)
		#bSeg.pack()


		def redMin():
			self.hora=self.hora-datetime.timedelta(minutes=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('reduje un minuto al hilo: ',threading.currentThread().getName())
		
		brMin=tkinter.Button(root,text='reduce minuto',command=redMin)
		#bMin.pack()
		brMin.grid(row=2,column=1)
		print(today)


		def redHor():
			self.hora=self.hora-datetime.timedelta(hours=1)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('reduje una hora al hilo: ',threading.currentThread().getName())
		
		brHor=tkinter.Button(root,text='reduce hora',command=redHor)
		#bMin.pack()
		brHor.grid(row=2,column=0)
		print(today)


		def acelerar():
			self.tiempo=self.tiempo/2

			#myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('acelere el reloj : ',threading.currentThread().getName())
		
		bAce=tkinter.Button(root,text='acelera reloj',command=acelerar)
		#bMin.pack()
		bAce.grid(row=3,column=1)
		print(today)

		def realentiza():
			
			self.tiempo=self.tiempo*2

			#myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('realentize el reloj : ',threading.currentThread().getName())
		
		bDece=tkinter.Button(root,text='realentiza reloj',command=realentiza)
		#bMin.pack()
		bDece.grid(row=4,column=1)
		print(today)

		def pauseReanude():
			if (self.uno==0):
				self.uno=1
			else:
				self.uno=0
			
			#myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print('pause/reanude el reloj : ',threading.currentThread().getName())
		
		bPause=tkinter.Button(root,text='pause/reanude reloj',command=pauseReanude)
		#bMin.pack()
		bPause.grid(row=5,column=1)
		print(today)

						

		def randDate():
			self.hora = self.hora+datetime.timedelta(seconds=random.randint(1,1000000))
			myClock1['text']=self.hora
		
		def tic() :
			self.hora=self.hora+datetime.timedelta(seconds=self.uno)
			myClock1['text'] = self.hora.strftime('%H:%M:%S')
			print(self.hora)

		def tac() :
			tic()
			myClock1.after(int(self.tiempo),tac)


		
		if (threading.currentThread().getName()!='reloj 1'):
			randDate();
			pass
		tac()

		root.mainloop()


r1 = relojHilo(name='reloj 1')
r2 = relojHilo(name='reloj 2')
r3 = relojHilo(name='reloj 3')
r4 = relojHilo(name='reloj 4')

r1.start()
r2.start()
r3.start()
r4.start()