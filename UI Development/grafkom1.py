import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import grafkom1Framework as graphics

class objItem(object):

    def __init__(self):
        self.angle = 0
        self.vertices = []
        self.faces = []
        self.coordinates = [0, 0, -65]  # [x,y,z]
        self.teddy = graphics.ObjLoader("teddy.obj")
        self.position = [0, 0, -50]
        
    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.902, 0.902, 1, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 0, math.sin(math.radians(self.angle)), 0, math.cos(math.radians(self.angle)) * -1, 0, 1, 0)
        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])
        
    def move_forward(self):
        self.coordinates[2] += 10 * math.cos(math.radians(self.angle))
        self.coordinates[0] -= 10 * math.sin(math.radians(self.angle))

    def move_back(self):
        self.coordinates[2] -= 10 * math.cos(math.radians(self.angle))
        self.coordinates[0] += 10 * math.sin(math.radians(self.angle))

    def move_left(self, n):
        self.coordinates[0] += n * math.cos(math.radians(self.angle))
        self.coordinates[2] += n * math.sin(math.radians(self.angle))

    def move_right(self, n):
        self.coordinates[0] -= n * math.cos(math.radians(self.angle))
        self.coordinates[2] -= n * math.sin(math.radians(self.angle))

    def rotate(self, n):
        self.angle += n

    def fullRotate(self):
        for i in range(0, 72):
            self.angle += 5
            self.move_left(5)
            self.render_scene()
            self.teddy.render_scene()
            pygame.display.flip()
            

def main():
    """This initiate pygame windows"""
    pygame.init()
    pygame.display.set_mode((750, 600), pygame.DOUBLEBUF | pygame.OPENGL)#window size
    pygame.display.set_caption("3D visualization")#Title
    clock = pygame.time.Clock()
    # Feature checker
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    #
    glMatrixMode(GL_PROJECTION)
    #first number is the distance between camera and object
    #second number is for the image ratio, for example, <1 will be flatten and >1 stretch the image
    #third and fourth, i am not sure
    gluPerspective(100, float(800) / 600, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    objectTeddy = objItem()
    done = False
    
    #below are the keys for controlling the object view
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    objectTeddy.move_left(10)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    objectTeddy.move_right(10)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    objectTeddy.move_forward()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    objectTeddy.move_back()
                elif event.key == pygame.K_1:
                    objectTeddy.rotate(10)
                    objectTeddy.move_left(10)
                elif event.key == pygame.K_2:
                    objectTeddy.rotate(-10)
                    objectTeddy.move_right(10)
                elif event.key == pygame.K_3:
                    objectTeddy.fullRotate()
                elif event.key == pygame.K_r:
                    objectTeddy.rotate(0)

        objectTeddy.render_scene()
        objectTeddy.teddy.render_scene()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
if __name__ == '__main__':
    main()

