# Importación de librerías requeridas
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy

def get_descarga_trailer_positions(origenPos, trailerPos):
    return [float(origenPos[0]), 0.0, float(origenPos[1])], [float(trailerPos[0]), 0.0, float(trailerPos[1])]

def initializeCSVout(header, path):       
    # Verificación de archivo de salida
    csv_path = str(path)
    if(not os.path.exists(csv_path)):
        arch = open(csv_path, "w")
        arch.write(header)
        arch.close()

def verifyConfigArch(txt_path):
    # Verificación de archivo de salida
    txt_path = str(txt_path)
    if(not os.path.exists(txt_path) ):
        arch = open(txt_path, "w")
        arch.close()

def writeConfigArch(txt_path, printable):
    # Verificación de archivo de salida
    txt_path = str(txt_path)
    arch = open(txt_path, "a")
    arch.write(printable)
    arch.close()

def CalcCenter(V1,V2,V3):
    x=(V1[0]+V3[0])/2
    z=(V1[2]+V2[2])/2
    return x,z

def drawCube(V1, V2, V3, V4, color):
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
        
    glColor3f(R, G, B)
    glBegin(GL_QUADS)
    glVertex3d(V1[0], V1[1], V1[2])
    glVertex3d(V2[0], V2[1], V2[2])
    glVertex3d(V4[0], V4[1], V4[2])
    glVertex3d(V3[0], V3[1], V3[2])
    glEnd()

def ComputeDistance(a, b):
    Direccion =  numpy.asarray(b) -  numpy.asarray(a)
    Direccion = numpy.asarray( Direccion)
    Distancia = numpy.linalg.norm( Direccion )
    return Distancia	