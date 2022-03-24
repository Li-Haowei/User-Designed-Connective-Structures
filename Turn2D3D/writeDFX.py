# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:34:20 2022

@author: Haowei Li
"""

from dxfwrite import DXFEngine as dxf

#v3

class writeDFX():
    def __init__(self, vertices):
        self.vertices = self.parseVerticesFromStringToInt(vertices)
        
    def parseVerticesFromStringToInt(self, vertices):
        arr = []
        for i in range(len(vertices)):
            string = vertices[i].split('V ')
            string = string[1].split('\n')
            string = string[0].split(' ')
            arr.append((float(string[0])/50,float(string[1])/50))
        return arr
    def draw(self):
        drawing = dxf.drawing('test.dxf')
        polyline= dxf.polyline(linetype='DOT')
        polyline.add_vertices(self.vertices)
        drawing.add(polyline)
        drawing.save()


