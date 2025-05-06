# Importación de librerías requeridas
import numpy

class Node:
    # Método Constructor de la clase Node
    def __init__(self,id: int=0 , position: list[float] = [0.0, 0.0, 0.0]) -> None:
        self.id = id  # Identificador del nodo
        self.position = numpy.array(position, dtype=numpy.float64) # Arreglo con posición (x, y, z) del nodo en el espacio
        self.neighs = [] # arreglo con conexiones a nodos vecinos de acuerdo con matriz de adyacencia
        self.isZonaDescarga = False # bandera para conocer si el nodo es la Zona de Descarga
        self.isZonaTrailer = False  # bandera para conocer si el nodo es la Zona de Trailer
        
    # Método para agregar conexiones a nodos vecinos
    def addNeigh(self, neigh):
        self.neighs.append(neigh)
    