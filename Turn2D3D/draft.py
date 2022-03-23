"""code from:
    https://livebook.manning.com/book/math-for-programmers/a-loading-and-rendering-3d-models-with-opengl-and-pygame/v-8/35"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from vectors import *
from math import *

def normal(face):
     return(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))
  
# =============================================================================
# blues = matplotlib.cm.get_cmap('Blues')
#   
# def shade(face,color_map=blues,light=(1,2,3)):
#      return color_map(1 - dot(unit(normal(face)), unit(light)))
# =============================================================================
 
light = (1,2,3)

faces = [
     [(1,0,0), (0,1,0), (0,0,1)],
     [(1,0,0), (0,0,-1), (0,1,0)],
     [(1,0,0), (0,0,1), (0,-1,0)],
     [(1,0,0), (0,-1,0), (0,0,-1)],
     [(-1,0,0), (0,0,1), (0,1,0)],
     [(-1,0,0), (0,1,0), (0,0,-1)],
     [(-1,0,0), (0,-1,0), (0,0,1)],
     [(-1,0,0), (0,0,-1), (0,-1,0)],
]

pygame.init()
display = (400,400)
window = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, 1, 0.1, 50.0)
glTranslatef(0.0,0.0, -5)   
glEnable(GL_CULL_FACE)
glEnable(GL_DEPTH_TEST)
glCullFace(GL_BACK)
done = False
clock = pygame.time.Clock()


while not done:
    clock.tick()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    max_ = 1
    for face in faces:
        max_ -= 0.1
        for vertex in face:
            glColor3fv((max_, 0, 0))
            glVertex3fv(vertex)
    glEnd()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()










