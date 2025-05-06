from Node import Node
import Tools

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Board:
    def __init__(self, m_dim, n_dim, boardSize) -> None:
        self.m = m_dim
        self.n = n_dim
        self.boardSize = boardSize
        self.nodes = []
        self.nodesVertex = []
        
    def GenerarNodos(self) -> None:
        count=0
        NodesRow = []
        for i in range(self.m):
            for j in range(self.n):
                newNode = Node(id=count)
                NodesRow.append(newNode)
                count+=1
            self.nodes.append(NodesRow)
            NodesRow= []
        self.SetNodesCoords()
        self.SetNodesNeighs()
        
    def SetNodesCoords(self) -> None:
        ancho = self.boardSize//self.n
        largo = self.boardSize//self.m
        y = 0 # Y arbitraria (nivel de piso)
        i=0
        for x in range(-(self.boardSize//2), (self.boardSize//2), largo):
            j=0
            auxVertex = []
            for z in range(-(self.boardSize//2), (self.boardSize//2), ancho):
                V1= [x, y, z]
                V2= [x, y, z+ancho]
                V3= [x+largo,y,z]
                V4= [x+largo, y, z+ancho]
                
                vertex = [V1, V2, V3, V4]
                auxVertex.append(vertex) # save nodes vertex
                
                x_node, z_node = Tools.CalcCenter(V1,V2,V3)
                self.nodes[i][j].position = [x_node, y, z_node]
                j+=1
            self.nodesVertex.append(auxVertex)
            auxVertex = []
            i+=1
            
    def SetNodesNeighs(self) -> None:
        for i in range(self.m):
            for j in range(self.n):
                if (j+1<self.n): #Dentro de limites right
                    self.nodes[i][j].addNeigh(self.nodes[i][j+1])
                if (j-1>0): #Dentro de limites left
                    self.nodes[i][j].addNeigh(self.nodes[i][j-1])
                if (i+1<self.m): #Dentro de limites down
                    self.nodes[i][j].addNeigh(self.nodes[i+1][j])
                if (i-1>0): #Dentro de limites up
                    self.nodes[i][j].addNeigh(self.nodes[i-1][j])
                if (i-1>0) and (j+1<self.n): #Dentro de limites up-right
                    self.nodes[i][j].addNeigh(self.nodes[i-1][j+1])
                if (i-1>0) and (j-1>0): #Dentro de limites up-left
                    self.nodes[i][j].addNeigh(self.nodes[i-1][j-1])
                if (i+1<self.m) and (j+1<self.n): #Dentro de limites down-right
                    self.nodes[i][j].addNeigh(self.nodes[i+1][j+1])
                if (i+1<self.m) and (j-1>0): #Dentro de limites down-left
                    self.nodes[i][j].addNeigh(self.nodes[i+1][j-1])
    
    def drawBoardStreets(self):
        #y = 0.5 # Y arbitraria (encima de nivel de piso)
        for x in range(0, len(self.nodesVertex)):
            for z in range(0, len(self.nodesVertex[0])):
                V1= self.nodesVertex[x][z][0]
                V2= self.nodesVertex[x][z][1]
                V3= self.nodesVertex[x][z][2]
                V4= self.nodesVertex[x][z][3]
                
                if(len(self.nodes[x][z].carretera) != 0):
                    color= "negro"
                else:
                    color = "verde"
                
                if(self.nodes[x][z].isSemaforo):
                    color = "verde-claro"
                
                Tools.drawCube(V1,V2,V3,V4, color)
                
        Tools.drawAmbientWalls(self.boardSize)
                
    def drawBoardasChess(self):
        dimboard = self.boardSize
        ancho = dimboard//self.n
        largo = dimboard//self.m
        y = 0.5
        flag=False
        i=0
        for x in range(-(dimboard//2), (dimboard//2), largo):
            j=0
            for z in range(-(dimboard//2), (dimboard//2), ancho):
                V1= (x, y, z)
                V2= (x, y, z+ancho)
                V3= (x+largo,y,z)
                V4= (x+largo, y, z+ancho)
                
                color= ""
                if(j%2 == 0) and (flag==False):
                    color="negro"
                elif(flag==False):
                    color="blanco"
                
                if(j%2 == 0) and (flag==True):
                    color="blanco"
                elif(flag==True):
                    color="negro"
                    
                Tools.drawCube(V1,V2,V3,V4, color)
                j+=1
            if(flag): 
                flag=False
            else:
                flag=True
            i+=1
            
    def showNodesInfo(self):
        container+="\n\nNodos  ============\n"
        for i in range(self.m):
            for j in range(self.n):
                print("Nodo: ", self.nodes[i][j].id, "  pos: ", self.nodes[i][j].position)