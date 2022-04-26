# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 02:15:33 2022
3D with matplotlib: https://likegeeks.com/3d-plotting-in-python/
conda install qdarkstyle=2.8.1
@author: Haowei Li

Bezier curve:
    https://www.youtube.com/watch?v=aVwxzDHniEw&t=382s

matplotlib 3d:
    https://www.geeksforgeeks.org/how-to-change-angle-of-3d-plot-in-python/

Create obj file with 3d array in python:
    https://inareous.github.io/posts/opening-obj-using-py
    https://vovaprivalov.medium.com/work-with-obj-meshes-using-openmesh-in-python-5871ac1237ae
    https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python

More tutorial on creating 3D object file with python:
    https://www.youtube.com/watch?v=gVUvnSJ-t3M
    https://www.youtube.com/watch?v=tsmkqU25_As

"""
from openmesh import *
from openmesh import TriMesh
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits import mplot3d
import pickle
from matplotlib.figure import Figure
import wx
# =============================================================================
# mesh = TriMesh()
# 
# 
# vh0 = mesh.add_vertex(TriMesh.Point(0, 1, 0))
# vh1 = mesh.add_vertex(TriMesh.Point(1, 0, 0))
# vh2 = mesh.add_vertex(TriMesh.Point(2, 1, 0))
# vh3 = mesh.add_vertex(TriMesh.Point(0,-1, 0))
# vh4 = mesh.add_vertex(TriMesh.Point(2,-1, 0))
# =============================================================================



#mesh = openmesh.read_trimesh('test.obj', vertex_tex_coord=True, face_color=True)
"""to plot a point"""
# =============================================================================
# ax = plt.axes(projection="3d")
# ax.scatter(3,5,7)
# plt.show()
# 
# =============================================================================

"""to plot a curve"""
x = np.linspace(0, 0)
y = np.linspace(-2*np.pi, 2*np.pi, 50)
z = x**2 + y**2
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x,y,z)
# =============================================================================
# for angle in range(0, 360):
#     ax.view_init(30, angle)
#     plt.draw()
#     plt.pause(.001)
# =============================================================================
plt.savefig("test.obj")
plt.show()

"""spiral"""
# =============================================================================
# fig = plt.figure(figsize = (8,8))
# ax = plt.axes(projection = '3d')
#   
# # Data for a three-dimensional line
# z = np.linspace(0, 15, 1000)
# x = np.sin(z)
# y = np.cos(z)
# ax.plot3D(x, y, z, 'green')
#   
# ax.view_init(-140, 60)
#   
# plt.show()
# =============================================================================
"""to plot random patterns"""
# =============================================================================
# np.random.seed(42)
# xs = np.random.random(100)*10+20
# ys = np.random.random(100)*5+7
# zs = np.random.random(100)*15+50
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(xs,ys,zs)
# plt.show()
# =============================================================================

"""to plot a map"""
# =============================================================================
# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True
# 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# X, Y, Z = axes3d.get_test_data(0.1)
# ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5)
# 
# for angle in range(0, 360):
#    ax.view_init(30, angle)
#    plt.draw()
#    plt.pause(.001)
# 
# plt.show()
# =============================================================================
