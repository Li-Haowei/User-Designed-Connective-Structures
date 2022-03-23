# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:05:24 2022

@author: Haowei Li
"""

from dxfwrite import DXFEngine as dxf


#Polyline
drawing = dxf.drawing('drawing.dxf')
polyline= dxf.polyline(linetype='DOT')
polyline.add_vertices( [(0,20), (3,20), (6,23), (9,23), (15,23)] )
polyline.POLYMESH_BEZIER_SURFACE
drawing.add(polyline)
drawing.save()


