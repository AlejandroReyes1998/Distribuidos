class IP:
    def __init__(self,tipo):
        direcciones = []

        f = open("ips.txt", "r")
        for x in f:
            direcciones.append(x.split()[1])
        f.close()
        self.prioridades = {'Coor1':3,'Coor2':2,'Coor3':1}
        ####################################### USUARIOS
        if tipo == 'U1':
            self.recibir = (direcciones[0],5005)
            if self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.enviar = (direcciones[3],6005)
                if self.prioridades['Coor2'] > self.prioridades['Coor3']:
                    self.enviar2 = (direcciones[4],6005)
                    self.enviar3 = (direcciones[5],6005)
                else:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[4],6005)
            elif self.prioridades['Coor2'] > self.prioridades['Coor1'] > self.prioridades['Coor3'] :
                self.enviar = (direcciones[4],6005)
                if self.prioridades['Coor1'] > self.prioridades['Coor3']:
                    self.enviar2 = (direcciones[3],6005)
                    self.enviar3 = (direcciones[5],6005)
                else:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[3],6005)
            else :
                self.enviar = (direcciones[5],6005)
                if self.prioridades['Coor2'] > self.prioridades['Coor1']:
                    self.enviar2 = (direcciones[4],6005)
                    self.enviar3 = (direcciones[3],6005)
                else:
                    self.enviar2 = (direcciones[3],6005)
                    self.enviar3 = (direcciones[4],6005)
        elif tipo == 'U2':
            self.recibir = (direcciones[1],5005)
            if self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.enviar = (direcciones[3],6005)
                if self.prioridades['Coor2'] > self.prioridades['Coor3']:
                    self.enviar2 = (direcciones[4],6005)
                    self.enviar3 = (direcciones[5],6005)
                else:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[4],6005)
            elif self.prioridades['Coor2'] > self.prioridades['Coor1'] > self.prioridades['Coor3'] :
                self.enviar = (direcciones[4],6005)
                if self.prioridades['Coor3'] > self.prioridades['Coor1']:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[3],6005)
                else:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[3],6005)
            else :
                self.enviar = (direcciones[5],6005)
                if self.prioridades['Coor2'] > self.prioridades['Coor1']:
                    self.enviar2 = (direcciones[4],6005)
                    self.enviar3 = (direcciones[3],6005)
                else:
                    self.enviar2 = (direcciones[3],6005)
                    self.enviar3 = (direcciones[4],6005)
        elif tipo == 'U3':
            self.recibir = (direcciones[2],5005)
            if self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.enviar = (direcciones[3],6005)
                if self.prioridades['Coor2'] > self.prioridades['Coor3']:
                    self.enviar2 = (direcciones[4],6005)
                    self.enviar3 = (direcciones[5],6005)
                else:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[4],6005)
            elif self.prioridades['Coor2'] > self.prioridades['Coor1'] > self.prioridades['Coor3'] :
                self.enviar = (direcciones[4],6005)
                if self.prioridades['Coor3'] > self.prioridades['Coor1']:
                    self.enviar2 = (direcciones[5],6005)
                    self.enviar3 = (direcciones[3],6005)
                else:
                    self.enviar2 = (direcciones[3],6005)
                    self.enviar3 = (direcciones[5],6005)
            else :
                self.enviar = (direcciones[5],6005)
                if self.prioridades['Coor2'] > self.prioridades['Coor1']:
                    self.enviar2 = (direcciones[4],6005)
                    self.enviar3 = (direcciones[3],6005)
                else:
                    self.enviar2 = (direcciones[3],6005)
                    self.enviar3 = (direcciones[4],6005)
        ########################################   FRONTS
        elif tipo == 'C1':
            self.cliente = (direcciones[0],5005)
            self.reloj = (direcciones[6],7005)
            self.recibir = (direcciones[3],6005)
            if self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.enviar1 = (direcciones[4],6005)
                self.enviar2 = (direcciones[5],6005)
                self.respaldo = (direcciones[3],2005)
            elif self.prioridades['Coor2'] > self.prioridades['Coor1'] > self.prioridades['Coor3'] :
                self.respaldo = (direcciones[4],2005)
                self.coor = (direcciones[4],6005)
            else :
                self.respaldo = (direcciones[5],2005)
                self.coor = (direcciones[5],6005)    
        elif tipo == 'C2':
            self.cliente = (direcciones[1],5005)
            self.reloj = (direcciones[6],7015)
            self.recibir = (direcciones[4],6005)
            if self.prioridades['Coor2'] > self.prioridades['Coor1'] > self.prioridades['Coor3'] :
                self.enviar1 = (direcciones[3],6005)
                self.enviar2 = (direcciones[5],6005)
                self.respaldo = (direcciones[4],2005)
            elif self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.respaldo = (direcciones[3],2005)
                self.coor = (direcciones[3],6005)
            else :
                self.respaldo = (direcciones[5],2005)
                self.coor = (direcciones[5],6005)

        elif tipo == 'C3':
            self.cliente = (direcciones[2],5005)
            self.reloj = (direcciones[6],7025)
            self.recibir = (direcciones[5],6005)
            if self.prioridades['Coor3'] > self.prioridades['Coor1'] > self.prioridades['Coor2'] :
                self.enviar1 = (direcciones[3],6005)
                self.enviar2 = (direcciones[4],6005)
                self.respaldo = (direcciones[5],2005)
            elif self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.respaldo = (direcciones[3],2005)
                self.coor = (direcciones[3],6005)
            else :
                self.respaldo = (direcciones[4],2005)
                self.coor = (direcciones[4],6005)
        else:
            self.C1 = (direcciones[6],7005)
            self.C2 = (direcciones[6],7015)
            self.C3 = (direcciones[6],7025)
            if self.prioridades['Coor1'] > self.prioridades['Coor2'] > self.prioridades['Coor3'] :
                self.respaldo = (direcciones[3],2005)
            elif self.prioridades['Coor2'] > self.prioridades['Coor1'] > self.prioridades['Coor3'] :
                self.respaldo = (direcciones[4],2005)
            else :
                self.respaldo = (direcciones[5],2005)
                              