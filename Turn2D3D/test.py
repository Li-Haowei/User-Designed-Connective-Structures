# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:05:24 2022

@author: Haowei Li
"""

from dxfwrite import DXFEngine as dxf


#Polyline
drawing = dxf.drawing('drawing.dxf')
point = dxf.point((1.0, 1.0))
point['layer'] = 'points'
point['color'] = 7
point['point'] = (2, 3) # int or float
drawing.add(point)
drawing.save()


