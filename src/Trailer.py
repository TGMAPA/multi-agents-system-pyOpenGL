# Importación de librerías requeridas
from Basura import *
import datetime

class Trailer:
    Board_size = None
    trash_textures = None
    
    def __init__(self, node, n_basuras, dx) -> None:
        self.Node = node
        self.Node.isZonaTrailer= True
        self.nbasuras= n_basuras
        self.basuras= []
        
        self.t0 = None # Tiempo inicial
        self.tf = None #Tiempo final de descarga
        
        self.dx = dx + (dx*0.001)
        self.isOcupied = None
        self.ocupiedwith = None
        self.generarBasuras()
    
    def generarBasuras(self):
        for i in range(self.nbasuras):
            # i es el identificador de la carga: sirve para realizar el inventario
            self.basuras.append(Basura(Trailer.Board_Size,1,Trailer.trash_textures,3, i, [self.Node.position[0], self.Node.position[1], self.Node.position[2]]))

    def changeisOcupied(self, bool):
        self.isOcupied = bool
    
    def changeOcupiedBy(self, agent):
        self.ocupiedwith = agent

    def starttime(self):
        self.t0 = datetime.datetime.now()
    
    def update(self):
        if(self.nbasuras == 0):
            self.tf = self.t0 - datetime.datetime.now()
            return True
        else:
            return False