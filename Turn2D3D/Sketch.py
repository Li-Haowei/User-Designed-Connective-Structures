
"""

The code in the file can draw lines  by left click twice, 
and can draw triangles by right click three times. The code also includes 
color interpolation.py

"""


import os

import wx
import math
import random
import numpy as np
import BezierCurve as bezier
from Buff import Buff
from Point import Point
from ColorType import ColorType
from CanvasBase import CanvasBase
from writeDFX import writeDFX
try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    
    curveCoordinates = ""
    coordinates = []
    debug = 0
    texture = None
    # control flags
    randomColor = False
    doTexture = False
    doSmooth = False
    doAA = False
    doAAlevel = 4
    consecutive = False
    # test case status
    MIN_N_STEPS = 6
    MAX_N_STEPS = 192
    n_steps = 12  # For test case only
    test_case_index = 0
    test_case_list = []  # If you need more test case, write them as a method and add it to list

    def __init__(self, parent):
        """
        Initialize the instance, load texture file to Buff, and load test cases.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        
            
        """clean the curveCoords textfile"""
        file  = open("curveCoordinates.txt","w")
        file.close()
        

    def __addPoint2Pointlist(self, pointlist, x, y):
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)
        #print("this is the points list: ", pointlist)
    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x, y):
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point provided or a line when two ends provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.drawPoint(self.buff, self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-1], " -> ", self.points_l[-2])
            #self.drawPoint(self.buff, self.points_l[-1])
            self.drawLine(self.buff,self.points_l[-1],self.points_l[-2])
            self.points_l.clear()

    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x, y):
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 4 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 4 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            self.drawLine(self.buff,self.points_r[-1],self.points_r[-2])
        elif len(self.points_r) % 4 == 3 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            self.drawLine(self.buff,self.points_r[-1],self.points_r[-2])
        elif len(self.points_r) % 4 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            self.drawLine(self.buff,self.points_r[-1],self.points_r[-2])
            self.drawBezierCurve(self.buff,self.points_r[-4],self.points_r[-3],self.points_r[-2],self.points_r[-1])
            if self.consecutive:
                temp = self.points_r[-1]
            self.points_r.clear()
            if self.consecutive:
                self.points_r.append(temp)
            
    def drawBezierCurve(self, buff, p1,p2,p3,p4):
        ts = [t/100.0 for t in range(101)]
        x1,y1 = p1.coords
        x2,y2 = p2.coords
        x3,y3 = p3.coords
        x4,y4 = p4.coords
        ptlist = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        curve = bezier.make_bezier(ptlist)(ts)
        for i in range(len(curve)-1):
            x1,y1=curve[i]
            x2,y2=curve[i+1]
            pt1 = Point((int(x1), int(y1)), ColorType(0, 1, 0))
            pt2 = Point((int(x2), int(y2)), ColorType(0, 1, 0))
            newPtList = self.bresenham(pt1,pt2)
            for pt in newPtList:
                x,y=pt.coords
                self.curveCoordinates += "V " + str(x) + " " + str(y) + "\n"
                self.coordinates.append("V " + str(x) + " " + str(y) + "\n")
                self.drawPoint(buff, pt)
        return
    def Interrupt_Keyboard(self, keycode):
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screenW
        """
        if chr(keycode) in "lL":
            self.consecutive = not self.consecutive
            print("Consecutive mode: ", self.consecutive)
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.curveCoordinates = ""
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if self.debug > 1:
            if x != min(max(0, int(x)), texture.width - 1):
                print("Warning: Texture Query x coordinate outbound")
            if y != min(max(0, int(y)), texture.height - 1):
                print("Warning: Texture Query y coordinate outbound")
        return texture.getPointFromPointArray(x, y)

    @staticmethod
    def drawPoint(buff, point):
        """
        Draw a point on buff

        :param buff: The buff to draw point on
        :type buff: Buff
        :param point: A point to draw on buff
        :type point: Point
        :rtype: None
        """
        
        x, y = point.coords
        
        c = point.color
        
        # because we have already specified buff.buff has data type uint8, type conversion will be done in numpy
        buff.buff[x, y, 0] = c.r * 255
        buff.buff[x, y, 1] = c.g * 255
        buff.buff[x, y, 2] = c.b * 255
        
    def draw_horizontal_line(self,p1,p2):
        """this method dealing with when x1=x2 which leads to bresenham slope calculation error"""
        x1,y1 = p1.coords
        x2,y2 = p2.coords
        point_list  = [] #point_list will hold the points that form a lone
        #Get colors
        r1,g1,b1 = p1.color.getRGB()
        r2,g2,b2 = p2.color.getRGB()
        #Calculates the difference
        red_difference = r2 - r1
        green_difference = g2 - g1
        blue_difference = b2 - b1
        if(y1>y2):
            a = y2
            y2 = y1
            y1 = a
        if((y2-y1)!=0):
             number_of_rows = y2-y1
             #Calculates the index to get color transformation
             red_delta = red_difference/number_of_rows
             green_delta = green_difference/number_of_rows
             blue_delta = blue_difference/number_of_rows
             for y in range(y1,y2+1):
                 p = Point((x1, y), 
                             ColorType(r1+red_delta*(y-y2+number_of_rows), g1+green_delta*(y-y2+number_of_rows), b1+blue_delta*(y-y2+number_of_rows)))
                 point_list.append(p)
             return point_list
        else:
             for y in range(y1,y2+1):
                 p = Point((x1, y), p1.color)
                 point_list.append(p)
             return point_list
   
    def bresenham(self, p1,p2): 
         """this is Bresenham's line Algorithm: takes in 2 point object and based on
         their coordinates to calculate for the line coordinates"""
         x1,y1 = p1.coords
         x2,y2 = p2.coords
         
         point_list = [] #point_list will hold the points that form a lone
         
         if x2-x1 == 0: 
             return self.draw_horizontal_line(p1,p2)
         m = (y2-y1)/(x2-x1) #this m will be used to determined if it's in [-1,1] range
         if(m>=-1 and m<=1): #when the line is in the range of [-1,1], Bresenham's algorithm can calculate
             if (x1>x2): #swap points to make sure it's going left to right
                 a1 = x1
                 x1 = x2
                 x2 = a1
                 a1 = y1
                 y1 = y2
                 y2 = a1
                 c = p1.color
                 p1.color = p2.color
                 p2.color = c
             e=0
             y=y1 
             number_of_rows = x2-x1
             
             #Get colors
             r1,g1,b1 = p1.color.getRGB()
             r2,g2,b2 = p2.color.getRGB()
             #Calculates the difference
             red_difference = r2 - r1
             green_difference = g2 - g1
             blue_difference = b2 - b1
             #Calculates the index to get color transformation
             red_delta = red_difference/number_of_rows
             green_delta = green_difference/number_of_rows
             blue_delta = blue_difference/number_of_rows
             
             if(m<0): #if the slope is negative
                   for x in range(x1,x2+1):
                        p = Point((x, y), 
                        ColorType(r1+red_delta*(x-x2+number_of_rows), g1+green_delta*(x-x2+number_of_rows), b1+blue_delta*(x-x2+number_of_rows)))
                        point_list.append(p)
                        #determine which level the current point is close to
                        if(e+m>-0.5):
                             e=e+m
                        else:
                             y=y-1
                             e = e+m+1        
             else: #if the slope is positive
                   for x in range(x1,x2+1):
                       p = Point((x, y), 
                       ColorType(r1+red_delta*(x-x2+number_of_rows), g1+green_delta*(x-x2+number_of_rows), b1+blue_delta*(x-x2+number_of_rows)))
                       point_list.append(p)
                       #determine which level the current point is close to
                       if (e+m <0.5):
                           e=e+m
                       else:
                           y=y+1
                           e=e+m-1
         else: #if the slope is out of [-1,1] range, swapping the x-axis and the y-axis
              p1 = Point((y1, x1), p1.color)
              p2 = Point((y2, x2), p2.color)
              temp_point_list = self.bresenham(p1,p2)
              for point in temp_point_list:
                   x,y = point.coords
                   point_list.append(Point((y, x), point.color)) #reverse the x,y before adding into point_list
         return point_list
    def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Draw a line between p1 and p2 on buff
        """
        if(self.doSmooth==False):
             p2.color = p1.color
        x1,y1 = p1.coords
        x2,y2 = p2.coords
        if(self.doAA==False):
             point_list = self.bresenham(p1,p2)
        else:
             point_list = self.bresenham_antiAliasing(p1,p2)
        for point in point_list:
             self.drawPoint(self.buff, point)
        return
   
    def bresenham_antiAliasing(self, p1,p2): 
         """this is Bresenham's line Algorithm antialiasing version: takes in 2 point object and based on
         their coordinates to calculate for the line coordinates by floating point number"""
         x1,y1 = p1.coords
         x2,y2 = p2.coords
         
         point_list = [] #point_list will hold the points that form a lone
         
         if x2-x1 == 0: 
             return self.draw_horizontal_line(p1,p2)
         m = (y2-y1)/(x2-x1) #this m will be used to determined if it's in [-1,1] range
         if(m>=-1 and m<=1): #when the line is in the range of [-1,1], Bresenham's algorithm can calculate
             if (x1>x2): #swap points to make sure it's going left to right
                 a1 = x1
                 x1 = x2
                 x2 = a1
                 a1 = y1
                 y1 = y2
                 y2 = a1
                 c = p1.color
                 p1.color = p2.color
                 p2.color = c
             y=y1 
             number_of_rows = x2-x1
             b = y1-m*x1
             #Get colors
             r1,g1,b1 = p1.color.getRGB()
             r2,g2,b2 = p2.color.getRGB()
             #Calculates the difference
             red_difference = r2 - r1
             green_difference = g2 - g1
             blue_difference = b2 - b1
             #Calculates the index to get color transformation
             red_delta = red_difference/number_of_rows
             green_delta = green_difference/number_of_rows
             blue_delta = blue_difference/number_of_rows
             
             
             if(m<0): #if the slope is negative
                   #m = m/(x2-x1+1)
                   for x in range(x1,x2+1):
                        p = Sketch.plot_antialiased_point(x, y, 
                        ColorType(r1+red_delta*(x-x2+number_of_rows), g1+green_delta*(x-x2+number_of_rows), b1+blue_delta*(x-x2+number_of_rows)))
                        point_list += p 
                        #determine which level the current point is close to
                        y = x*m + b
             else: #if the slope is positive
                   #m = m/(x2-x1)
                   for x in range(x1,x2+1):
                       p = Sketch.plot_antialiased_point(x, y, 
                       ColorType(r1+red_delta*(x-x2+number_of_rows), g1+green_delta*(x-x2+number_of_rows), b1+blue_delta*(x-x2+number_of_rows)))
                       point_list += p
                       #determine which level the current point is close to
                       y = x*m + b
         else: #if the slope is out of [-1,1] range, swapping the x-axis and the y-axis
              p1 = Point((y1, x1), p1.color)
              p2 = Point((y2, x2), p2.color)
              temp_point_list = self.bresenham(p1,p2)
              for point in temp_point_list:
                   x,y = point.coords
                   point_list.append(Point((y, x), point.color)) #reverse the x,y before adding into point_list
         return point_list
     
    def plot_antialiased_point(x: float, y: float, color):
         """Plot of a single, white-on-black anti-aliased point."""
         r,g,b = color.getRGB()
         result = []
         for rounded_x in (math.floor(x),math.ceil(x)):
             for rounded_y in (math.floor(y),math.ceil(y)):
                 percent_x = 1 - abs(x - rounded_x)
                 percent_y = 1 - abs(y - rounded_y)
                 percent = percent_x * percent_y
                 newcolor = ColorType(r*percent,g*percent,b*percent)
                 result.append( Point((rounded_x, rounded_y), newcolor) )
         #print(result)
         return result
    
     
    def sortColorByY(self,plist):
         result = {}
         for point in plist:
              x,y = point.coords
              result[y] = point.color
         return result
    def colorAlgorithmAdv(xc,yc,p1,p2,p3):
         x1,y1 = p1.coords
         x2,y2 = p2.coords
         x3,y3 = p3.coords
         
         r1,g1,b1 = p1.color.getRGB()
         r2,g2,b2 = p2.color.getRGB()
         r3,g3,b3 = p3.color.getRGB()
         
         if(((y2-y3)*(x1-x3)+(x3-x2)*(y1-y3))!=0):
             w1 = ((y2-y3)*(xc-x3)+(x3-x2)*(yc-y3))/((y2-y3)*(x1-x3)+(x3-x2)*(y1-y3))
             w2 = ((y3-y1)*(xc-x3)+(x1-x3)*(yc-y3))/((y2-y3)*(x1-x3)+(x3-x2)*(y1-y3))
             w3 = 1-w1-w2
             cp = ColorType((w1*r1+w2*r2+w3*r3)/(w1+w2+w3),(w1*g1+w2*g2+w3*g3)/(w1+w2+w3),(w1*b1+w2*b2+w3*b3)/(w1+w2+w3))
         else:
             dp1 = math.sqrt( (x1-xc)**2 + (y1-yc)**2 )
             dp2 = math.sqrt( (x2-xc)**2 + (y2-yc)**2 )
             dp3 = math.sqrt( (x3-xc)**2 + (y3-yc)**2 )
             if(dp1==0):
                  w1 = 0
             else:
                  w1 = 1/dp1 
             if(dp2==0):
                  w2 = 0
             else:
                  w2 = 1/dp2 
             if(dp3==0):
                  w3 = 0
             else:
                  w3 = 1/dp3 
             
             cp = ColorType((w1*r1+w2*r2+w3*r3)/(w1+w2+w3),(w1*g1+w2*g2+w3*g3)/(w1+w2+w3),(w1*b1+w2*b2+w3*b3)/(w1+w2+w3))
             
             return cp
         return cp
    
    
        
    
        


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(1000, 1000), title="Application", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        canvas = Sketch(frame)
        canvas.debug = 0
        frame.Show()
        app.MainLoop()
        canvas.points_r.clear() #Since Bezier curve keeps the one of the previous coordinate
        with open("curveCoordinates.txt","w") as f:
            f.write(canvas.curveCoordinates)
        DFXwriter = writeDFX(canvas.coordinates)
        DFXwriter.draw()

    def codingDebug():
        """
        If you are still working on the assignment, we suggest to use this as the main call.
        There will be more strict type checking in this version, which might help in locating your bugs.
        """
        print("This is the debug entry! ")
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

        app = wx.App(False)
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        canvas = Sketch(frame)
        canvas.debug = 2
        frame.Show()
        app.MainLoop()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
        stats.print_stats()


    main()
    # codingDebug()
