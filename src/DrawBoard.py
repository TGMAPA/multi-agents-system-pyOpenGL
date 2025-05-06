# Importación de librerías requeridas
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Tools

# Método para dibujar un tablero tamaño MxN
def drawBoard(m,n, dimboard):
    ancho = dimboard//n
    largo = dimboard//m
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

def planoText(dimboard):
    # activate textures
    glColor(1.0, 1.0, 1.0)
    
    # front face
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-dimboard, 0, -dimboard)
    
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-dimboard, 0, dimboard)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3d(dimboard, 0, dimboard)
    
    glTexCoord2f(1.0, 0.0)
    glVertex3d(dimboard, 0, -dimboard)
    
    glEnd()

# Método para dibujar un circulo en la posición de un nodo    
def drawCircle(node, color):
    glPushMatrix()
    glTranslatef(node.position[0], node.position[1]+0.9, node.position[2])  # Posición del círculo
    glRotatef(90, 1, 0, 0)  # Rotar 90 grados alrededor del eje X para alinear con el plano XZ
    R,G,B = 0,0,0
    if(color== "cafe"): 
        R,G,B =  139/255, 69/255, 19/255
    if(color== "negro"): 
        R,G,B =  14/255, 17/255, 28/255
    if(color== "blanco"):
        R,G,B = 255/255, 248/255, 220/255
    if(color== "verde"):
        R,G,B = 35/255, 172/255, 29/255
    if(color== "verde-claro"):
        R,G,B = 163/255, 249/255, 14/255
    if(color== "rojo"): 
        R,G,B =  255/255, 0/255, 0/255
    
    glColor3f(R, G, B)
    quadric = gluNewQuadric()
    #gluDisk(quadric, 0, int(nodes.distanciaMinima*0.3 / 2), int(nodes.distanciaMinima*0.4 / 2), 1)  # gluDisk(objeto, radio_interno, radio_externo, segmentos, anillos)
    gluDisk(quadric, 0, 15, 15, 1)  # gluDisk(objeto, radio_interno, radio_externo, segmentos, anillos)
    gluDeleteQuadric(quadric)
    glPopMatrix()

# Método para dibujar el plano y las paredes junto con los nodos inidicados
def drawPlane(dimboard, nodes):
    for node in nodes:
        color = ""
        if(node.isZonaDescarga):
            color = "verde"
        elif(node.isZonaTrailer):
            color = "rojo"   
        else:
            color = "negro" 
        
        drawCircle(node, color)
    
    # Board dimensions 
    haldBoardSize = (dimboard/2)+(dimboard*0.2)
    
    #Se dibuja el plano gris
    #planoText(dimboard)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-haldBoardSize, 0, -haldBoardSize)
    glVertex3d(-haldBoardSize, 0, haldBoardSize)
    glVertex3d(haldBoardSize, 0, haldBoardSize)
    glVertex3d(haldBoardSize, 0, -haldBoardSize)
    glEnd()
    
    # Draw the walls bounding the plane
    wall_height = 20.0  # Adjust the wall height as needed
    
    glColor3f(188/255, 143/255, 143/255)  # Light gray color for walls
    
    # Draw the left wall
    glBegin(GL_QUADS)
    glVertex3d(-haldBoardSize, 0, -haldBoardSize)
    glVertex3d(-haldBoardSize, 0, haldBoardSize)
    glVertex3d(-haldBoardSize, wall_height, haldBoardSize)
    glVertex3d(-haldBoardSize, wall_height, -haldBoardSize)
    glEnd()
    
    # Draw the right wall
    glBegin(GL_QUADS)
    glVertex3d(haldBoardSize, 0, -haldBoardSize)
    glVertex3d(haldBoardSize, 0, haldBoardSize)
    glVertex3d(haldBoardSize, wall_height, haldBoardSize)
    glVertex3d(haldBoardSize, wall_height, -haldBoardSize)
    glEnd()
    
    # Draw the front wall
    glBegin(GL_QUADS)
    glVertex3d(-haldBoardSize, 0, haldBoardSize)
    glVertex3d(haldBoardSize, 0, haldBoardSize)
    glVertex3d(haldBoardSize, wall_height, haldBoardSize)
    glVertex3d(-haldBoardSize, wall_height, haldBoardSize)
    glEnd()
    
    # Draw the back wall
    glBegin(GL_QUADS)
    glVertex3d(-haldBoardSize, 0, -haldBoardSize)
    glVertex3d(haldBoardSize, 0, -haldBoardSize)
    glVertex3d(haldBoardSize, wall_height, -haldBoardSize)
    glVertex3d(-haldBoardSize, wall_height, -haldBoardSize)
    glEnd()