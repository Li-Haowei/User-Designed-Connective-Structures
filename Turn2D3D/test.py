# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:05:24 2022

@author: Haowei Li
"""

from dxfwrite import DXFEngine as dxf



drawing = dxf.drawing('drawing.dxf')
polyline= dxf.polyline(linetype='DOT')
polyline.add_vertices( [(0,20), (3,20), (6,23), (9,23)] )
drawing.add(polyline)
drawing.save()