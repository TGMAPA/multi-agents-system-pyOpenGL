import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from CCamera import *
from math import *

def camera_init(camera, screen):
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glTranslate(0, 0, -5)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update()
    
class Camera:
    def __init__(self, initialEye, initialMouse) -> None:
        self.eye = pygame.math.Vector3(initialEye[0], initialEye[1] ,initialEye[2])
        self.up = pygame.math.Vector3(0, 1 , 0)
        self.right = pygame.math.Vector3(1, 0 , 0)
        self.forward = pygame.math.Vector3(0, 0 , 1)
        self.look = self.eye + self.forward
        self.yaw = -90
        self.pitch = 0
        self.last_mouse = pygame.math.Vector2(initialMouse[0], initialMouse[1])
        #self.last_mouse = pygame.math.Vector2(0.0)
        self.mouse_sensitivityX = 0.25
        self.mouse_sensitivityY = 0.15
        self.key_sensitivity = 1
        
    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch += pitch
        
        if (self.pitch > 89.0):
            self.pitch = 89.9
        if (self.pitch < -89.0):
            self.pitch = 89.9
            
        self.forward.x = cos(radians(self.yaw) * cos(radians(self.pitch)))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw) * cos(radians(self.pitch)))
        self.forward = self.forward.normalize()
        self.right = self.forward.cross(pygame.math.Vector3(0,1,0)).normalize()
        self.up = self.right.cross(self.forward).normalize()
    
    def update(self):
        #print(f"eyePos: {self.eye}  Last Mouse: {self.last_mouse}")
        if(not pygame.mouse.get_visible()):
            return
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        
        self.last_mouse = mouse_pos
        
        self.rotate(-mouse_change.x * self.mouse_sensitivityX,
                    mouse_change.y * self.mouse_sensitivityY)
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN]):
            self.eye -= self.forward * self.key_sensitivity
        elif (keys[pygame.K_UP]):
            self.eye += self.forward * self.key_sensitivity
        elif (keys[pygame.K_RIGHT]):
            self.eye += self.right * self.key_sensitivity
        elif (keys[pygame.K_LEFT]):
            self.eye -= self.right * self.key_sensitivity
        
        self.look = self.eye + self.forward
        gluLookAt(self.eye.x, self.eye.y, self.eye.z, 
                  self.look.x, self.look.y, self.look.z,
                  self.up.x, self.up.y, self.up.z)