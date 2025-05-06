# Importación de librerías requeridas
from Node import *
import numpy 
import math

class NodeSet:
    # Método Constructor de la clase NodeSet
    def __init__(self, origenPos, finalPos, distMin, dx) -> None:
        
        self.matrixAdy=[[0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0]]
        
        self.nodes = [] # Arreglo contenedor de los nodos para la simulación
        self.distanciaMinima = distMin # Atributo que indica la distancia mínima a guardar entre los agentes de la simulación
        self.distancia_origen_trailer = dx # Atributo que indica la distancia entre el nodo origen y el trailer
        self.generarNodos(origenPos, finalPos) # Generación de los nodos de acuerdo con el nodo origen y el trailer
        #self.setAdjacency() 
        self.setAdyacencyWithMatrix() # Establecimiento de asyacencias para los nodos mediante matriz
    
    # Método para generar los Nodos de acuerdo con el nodo origen y el nodo de Trailer
    def generarNodos(self, origenPos, finalPos):
        nodoOrigen = Node(id=0, position=  numpy.asarray(origenPos)) #Nodo origen
        nodoOrigen.isZonaDescarga = True
        
        nodoTrailer = Node(id=3, position=  numpy.asarray(finalPos)) # nodo de trailer
        nodoOrigen.isZonaTrailer = True
        
        Direccion, Distancia = self.ComputeDirection(origenPos, finalPos) 
        angle = math.acos(Direccion[0]) * 180 / math.pi
        if Direccion[2] < 0:
            angle = 360 - angle
        node1Pos, node5Pos = self.getExternNodes2Origin( angle, origenPos) # nodos externos al nodo origen
        
        Direccion, Distancia = self.ComputeDirection(finalPos, origenPos)
        angle = math.acos(Direccion[0]) * 180 / math.pi
        if Direccion[2] < 0:
            angle = 360 - angle
        node4Pos, node2Pos = self.getExternNodes2Origin(angle, finalPos) # nodos externos al nodo trailer
        
        # Agregar los nodos con las posiciónes generadas al contenedor de Nodos
        self.nodes.append(nodoOrigen)
        self.nodes.append(Node(id=1, position=  numpy.asarray(node1Pos)))
        self.nodes.append(Node(id=2, position=  numpy.asarray(node2Pos)))
        self.nodes.append(nodoTrailer)
        self.nodes.append(Node(id=4, position=  numpy.asarray(node4Pos)))
        self.nodes.append(Node(id=5, position=  numpy.asarray(node5Pos)))
    
    # Método para establecer las adyacencias entre los nodos
    def setAdjacency(self):
        for i in range(len(self.nodes)):
            if( i < len(self.nodes)-1):
                self.nodes[i].addNeigh(self.nodes[i+1])
            else:
                self.nodes[i].addNeigh(self.nodes[0])
                
    def setAdyacencyWithMatrix(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if( self.matrixAdy[i][j] == 1 ):
                    self.nodes[i].addNeigh(self.nodes[j])
    
    # Método para generar las posiciónes para los nodos externos a las raices
    def getExternNodes2Origin(self, angulo, reference):
        xorigin = reference[0]
        zorigin = reference[2]
        
        # Angulo de apertura para los nodos externos a la referencia
        apertura = 45
        if(self.distanciaMinima>740):
            apertura= (self.distanciaMinima*45)/740
            
        offset = 10
        ditminAndOffset = self.distanciaMinima + offset
        
        # Ajustar distancia para nodos de acuerdo con el cercania entre los el trailer y el origen
        if( self.distancia_origen_trailer <=  ditminAndOffset):
            ditminAndOffset = ditminAndOffset - (ditminAndOffset - self.distancia_origen_trailer)
        
        alpha = (ditminAndOffset)/2
        magnitud2extern = math.sqrt((alpha**2) + (alpha**2))
        
        angle2extern1 = angulo - apertura
        Xexextern1 = magnitud2extern * math.cos(math.radians(angle2extern1)) # Calculo de x para el primer nodo externo a la referencia
        Zexextern1 = magnitud2extern * math.sin(math.radians(angle2extern1)) # Calculo de z para el primer nodo externo a la referencia
        
        angle2extern2 = angulo + apertura
        Xexextern2 = magnitud2extern * math.cos(math.radians(angle2extern2)) # Calculo de x para el segundos nodo externo a la referencia
        Zexextern2 = magnitud2extern * math.sin(math.radians(angle2extern2)) # Calculo de z para el segundos nodo externo a la referencia
        
        return [xorigin + Xexextern1, 0.0, zorigin + Zexextern1],[xorigin + Xexextern2, 0.0, zorigin + Zexextern2]
    
    # Método para calcular la distancia entre dos puntos
    def ComputeDirection(self, Posicion, next):
        Direccion =  numpy.asarray(next) -  numpy.asarray(Posicion)
        Direccion = numpy.asarray( Direccion)
        Distancia = numpy.linalg.norm( Direccion )
        Direccion /= Distancia
        return Direccion, Distancia	