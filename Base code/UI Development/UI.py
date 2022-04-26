# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:01:49 2022

@author: Haowei Li
"""
import os
import pygame
import tkinter as tk
from tkinter import *
import platform
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import grafkom1Framework as graphics


class objItem(object):
    """class that renders obj"""
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

#tkinter          
screenOn = True
root = tk.Tk()
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)



    
    
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500,500), pygame.DOUBLEBUF | pygame.OPENGL)
screen.fill(pygame.Color(255,255,255))
pygame.display.init()

# Feature checker 
clock = pygame.time.Clock()
glDisable(GL_TEXTURE_2D) 
glEnable(GL_DEPTH_TEST) 
glEnable(GL_BLEND) 
glEnable(GL_CULL_FACE) 
glMatrixMode(GL_PROJECTION)

#pygame.display.update()
gluPerspective(100, float(800) / 600, .1, 1000.)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
objectTeddy = objItem()


done = False
def quitUI():
    root.destroy()
    pygame.quit()
    done = True
Button(root, text="Quit", command=quitUI).pack()
root.update()

while not done:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                     done = True
        objectTeddy.render_scene()
        objectTeddy.teddy.render_scene()
        pygame.display.flip()
        clock.tick(30)
        #pygame.display.update()
        root.update()
        if done:
            pygame.quit()
            root.destroy()
    except:
        done = True
        print("game ends")
    