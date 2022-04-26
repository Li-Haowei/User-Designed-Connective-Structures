from enum import Enum
from Point import Point
from ColorType import ColorType
from Buff import Buff

class LayerObject():

    POINT = 1
    LINE = 2
    CURVE = 3

    type = None
    data = None

    def __init__(self, type, data):
        if type == self.POINT:
            assert(len(data) == 1)
        elif type == self.LINE:
            assert(len(data) == 2)
        elif type == self.CURVE:
            assert(len(data) == 4)
        else:
            raise ValueError()
        
        self.type = type
        self.data = data
            

class Layer():

    index = None
    data = None

    def __init__(self, index):
        self.index = index
        self.data = []

    def addPoint(self, p):
        assert(isinstance(p, Point))
        point = LayerObject(LayerObject.POINT, [p])
        self.data.append(point)

    def addLine(self, p1, p2):

        assert(isinstance(p1, Point))
        assert(isinstance(p2, Point))

        line = LayerObject(LayerObject.LINE, [p1, p2])

        self.data.append(line)

    def addCurve(self, p1, p2, p3, p4):

        assert(isinstance(p1, Point))
        assert(isinstance(p2, Point))
        assert(isinstance(p3, Point))
        assert(isinstance(p4, Point))

        curve = LayerObject(LayerObject.CURVE, [p1, p2, p3, p4])

        self.data.append(curve)

    def clearLayer(self):
        self.data = []

