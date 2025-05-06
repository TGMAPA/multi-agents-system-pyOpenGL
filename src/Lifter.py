# Importación de librerías requeridas
import pygame, random, math, numpy
import datetime
from pygame.locals import *
from Cubo import Cubo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Lifter:
	def __init__(self, dim, vel, textures, idx, position, origen, csv_file_path = "", n_exec = 0, alive = False, distMin = 5):
		self.dim = dim

		# Atributo que indica el identificador del agente
		self.idx = idx

		# Atributo que indica el número de ejecución
		self.nExec = n_exec

		self.csv_file_path = csv_file_path

		self.ZonaDescarga = origen

		# Inicializar las coordenadas (x,y,z) del cubo en el tablero
		# almacenandolas en el vector Position
		self.Position = position #pos 
		
		# Se inicializa un vector de direccion aleatorio
		self.Direction = numpy.zeros(3)
		self.angle = 0

		# Velocidad constante para el agente
		self.vel = vel

		self.currentNode = origen
		self.nextNode = origen
		self.indxCurrent = 0

		# Arreglo de texturas
		self.textures = textures

		# Control variables for platform movement
		self.platformHeight = -1.5
		self.platformUp = False
		self.platformDown = False

		# Variable de control para colisiones con basura
		self.radiusCol = 5

		# Variable de control para colisiones con otros agentes activos
		self.radius2lifter = distMin

		#Control variables for animations
		self.status = "searching"
		self.trashID = -1

		# Atributo para indicar que el agente ha terminado su trabajo
		self.finished = False

		# Atributo para indicar si el agente esta en movimiento o no
		self.alive = alive
		self.collisionwith = []
		self.collisionwith_iswaiting = []

		# Atributo que indica si el agente ha sido inicializado
		self.started = False

		# Atributo para indicar que el agente ha realizado el último trabajo
		self.finisher = False

	# Método para obtener la dirección y la distancia hacía un Nodo determinado desde la posición actual del agente
	def ComputeDirection(self, Posicion, NodoSiguiente):
		Direccion = NodoSiguiente.position - Posicion
		Direccion = numpy.asarray( Direccion)
		Distancia = numpy.linalg.norm( Direccion )
		Direccion /= Distancia
		return Direccion, Distancia		

	# Método que devuelve el nodo por el que el agente ha de continuar su trayectoría
	def getNextNodeSeq(self):
		return self.currentNode.neighs[0]

	# Método para realizar el movimiento del agente dada una dirección
	def move(self, direccion):
		# Actualización de la posición
		self.Position += direccion * self.vel
		self.Direction = direccion
		
		self.angle = math.acos(self.Direction[0]) * 180 / math.pi
		if self.Direction[2] > 0:
			self.angle = 360 - self.angle

	# Método para frenar el movimiento del agente
	def stop(self, agent):
		self.alive = False
		if(agent not in self.collisionwith):
			self.collisionwith.append(agent)

	# Método para continuar con el movimeinto del agente después de una pausa
	def resume(self):
		self.alive = True
		#self.collisionwith = []

	def waiting(self):
		self.alive = False

	# Método para actualizar el estado y posición del agente
	def update(self, delta):
		# Validar que el agente ha sido inicializado
		if( self.started ):
			# Validar que el agente no esta en pausa
			if( self.alive ):
				# Encontrar un nuevo nodo para continuar con el recorrido hasta haber llegado al nododestino actual
				if( (self.alive) and (self.nextNode != None) and (numpy.allclose(numpy.asarray(self.Position, dtype=numpy.int64), numpy.asarray(self.nextNode.position, dtype=numpy.int64),  rtol=0.015))): #0.015
					self.nextNode = self.getNextNodeSeq()

				if( self.nextNode != None):
					# Calculo de dirección y distancia entre el agente y el nodo destino
					Direccion, Distancia =  self.ComputeDirection(self.Position, self.nextNode)
					
					# Transición de nodos
					if Distancia < 0.5:
						self.currentNode = self.nextNode
					
					# Actualizar el estado del agente
					match self.status:
						case "searching":
							self.move(Direccion) # Actualizar posición			
							# Mover plataforma
							if self.platformUp:
								if self.platformHeight >= 0:
									self.platformUp = False
								else:
									self.platformHeight += delta
							elif self.platformDown:
								if self.platformHeight <= -1.5:
									self.platformUp = True
								else:
									self.platformHeight -= delta		
						case "lifting":
							if self.platformHeight >= 0:
								self.status = "delivering"
							else:
								self.platformHeight += delta
						case "delivering":
							if(self.finisher and numpy.allclose(numpy.asarray(self.Position, dtype=numpy.int64), numpy.asarray(self.ZonaDescarga.position, dtype=numpy.int64),  rtol=0.015)):
								# Validar que el agente finsher ha descargado la última carga del trailer
								self.status = "finish"
							elif( numpy.allclose(numpy.asarray(self.Position, dtype=numpy.int64), numpy.asarray(self.ZonaDescarga.position, dtype=numpy.int64),  rtol=0.015) ):
								# Validar que el agente realiza la descarga de una carga en la Zona de Origen/Descarga
								self.status = "dropping"
							else:
								self.move(Direccion) # Actualizar posición
						case "dropping":
							if self.platformHeight <= -1.5:
								self.status = "searching"
							else:
								self.platformHeight -= delta
				else:
					self.finished = True	
			else:
				#print("agente inactivo :",self.idx)
				pass
    			# Agente Inactivo
		else:
			# Agente no iniciado
			pass

	# Método para dibujar al agente en la posición actual
	def draw(self):
		glPushMatrix()
		glTranslatef(self.Position[0], self.Position[1], self.Position[2])
		glRotatef(self.angle, 0, 1, 0)
		glScaled(5, 5, 5)
		glColor3f(1.0, 1.0, 1.0)
		# front face
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textures[2])
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, -1, 1)

		# 2nd face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-2, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(-2, -1, 1)

		# 3rd face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-2, 1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-2, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-2, -1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(-2, -1, -1)

		# 4th face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-2, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-2, -1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, -1, -1)

		# top
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-2, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-2, 1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, 1, -1)
		glEnd()

		# Head

		glPushMatrix()
		glTranslatef(0, 1.5, 0)
		glScaled(0.8, 0.8, 0.8)
		glColor3f(1.0, 1.0, 1.0)
		head = Cubo(self.textures, 0)
		head.draw()
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)

		# Wheels
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textures[1])
		glPushMatrix()
		glTranslatef(-1.2, -1, 1)
		glScaled(0.3, 0.3, 0.3)
		glColor3f(1.0, 1.0, 1.0)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(0.5, -1, 1)
		glScaled(0.3, 0.3, 0.3)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(0.5, -1, -1)
		glScaled(0.3, 0.3, 0.3)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(-1.2, -1, -1)
		glScaled(0.3, 0.3, 0.3)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)

		# Lifter
		glPushMatrix()
		if self.status in ["lifting","delivering","dropping"]:
			self.drawTrash()
		glColor3f(0.0, 0.0, 0.0)
		glTranslatef(0, self.platformHeight, 0)  # Up and down
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(3, 1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(3, 1, 1)
		glEnd()
		glPopMatrix()
		glPopMatrix()

	# Método para dibujar la basura que carga el agente 
	def drawTrash(self):
		glPushMatrix()
		glTranslatef(2, (self.platformHeight + 1.5), 0)
		glScaled(0.5, 0.5, 0.5)
		glColor3f(1.0, 1.0, 1.0)

		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textures[3])

		glBegin(GL_QUADS)

		# Front face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(-1, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-1, -1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, -1, 1)

		# Back face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-1, 1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-1, -1, -1)

		# Left face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-1, 1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(-1, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-1, -1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-1, -1, 1)

		# Right face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, -1, -1)

		# Top face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-1, 1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-1, 1, -1)

		# Bottom face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-1, -1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, -1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-1, -1, -1)

		glEnd()
		glDisable(GL_TEXTURE_2D)

		glPopMatrix()
