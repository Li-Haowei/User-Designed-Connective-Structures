#!/usr/bin/env python
#coding:utf-8
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import sys
import os

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

# Dimlines are separated from the core library.
# Dimension lines will not generated by the DXFEngine.
from dxfwrite.dimlines import dimstyles, LinearDimension, AngularDimension
from dxfwrite.dimlines import ArcDimension, RadialDimension

# create a new drawing: dxfwrite.DXFEngine.drawing(filename)
name = 'dimlines.dxf'
dwg = dxf.drawing(name)

# add block and layer definition to drawing
dimstyles.setup(dwg)

# create a dimension line for following points
points = [ (1.7,2.5), (0,0), (3.3,6.9), (8,12)]

# define new dimstyles, for predefined ticks see dimlines.py
dimstyles.new("dots", tick="DIMTICK_DOT", scale=1., roundval=2, textabove=.5)
dimstyles.new("arrow", tick="DIMTICK_ARROW", tick2x=True, dimlineext=0.)
dimstyles.new('dots2', tick="DIMTICK_DOT", tickfactor=.5)

#add linear dimension lines
dwg.add(LinearDimension((3,3), points, dimstyle='dots', angle=15.))
dwg.add(LinearDimension((0,3), points, angle=90.))
dwg.add(LinearDimension((-2,14), points, dimstyle='arrow', angle=-10))

# next dimline is added as anonymous block
dimline = LinearDimension((-2,3), points, dimstyle='dots2', angle=90.)
dimline.set_text(1, 'CATCH')

# add dimline as anonymous block
dwg.add_anonymous_block(dimline, layer='DIMENSIONS')

# add polyline to drawing
dwg.add(dxf.polyline(points, color=5))

# There are three dimstyle presets for angular dimension
# 'angle.deg' (default), 'angle.rad', 'angle.grad' (gon)
# for deg and grad default roundval = 0
# for rad default roundval = 3

# angular dimension in grad (gon)
dwg.add(AngularDimension(pos=(18, 5), center=(15, 0), start=(20, 0),
                         end=(20, 5), dimstyle='angle.grad'))

# angular dimension in degree (default dimstyle), with one fractional digit
dwg.add(AngularDimension(pos=(18, 10), center=(15, 5), start=(20, 5),
                         end=(20, 10), roundval=1))

dwg.add(ArcDimension(pos=(23, 5), center=(20, 0), start=(25, 0),
                     end=(25, 5), dimstyle='dots2'))

# RadialDimension has a special tick
dimstyles.new("radius", height=0.25, prefix='R=')
dwg.add(RadialDimension((20, 0), (24, 1.5), dimstyle='radius'))
dwg.save()
print("drawing '%s' created.\n" % name)
