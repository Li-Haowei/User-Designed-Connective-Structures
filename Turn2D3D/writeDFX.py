# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:34:20 2022

@author: Haowei Li
"""

from dxfwrite import DXFEngine as dxf



class writeDFX():
    def __init__(self, vertices):
        print(vertices)
        self.vertices = self.parseVerticesFromStringToInt(vertices)
        
    def parseVerticesFromStringToInt(self, vertices):
        arr = []
        for i in range(len(vertices)):
            string = vertices[i].split('V ')
            string = string[1].split('\n')
            string = string[0].split(' ')
            arr.append((int(string[0])/100,int(string[0])/100))
        return arr
    def draw(self):
        drawing = dxf.drawing('test.dxf')
        drawing.add_layer('LINES')
        for i in range(0,len(self.vertices),2):
            drawing.add(dxf.line(self.vertices[i], self.vertices[i+1], color=7, layer='LINES'))
        drawing.save()
            