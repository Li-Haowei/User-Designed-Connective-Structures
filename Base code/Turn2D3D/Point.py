"""
A Point class is defined here, which might store point coordinates, color and corresponding texture position.
"""

import copy
import time
from ColorType import ColorType

import typing


class Point:
    """
    Properties:
        coords: List<Integer>
        color: ColorType
        texture: List<Float>
    Desciption:
        Invisible Variables: 
        coords is used to describe coordinates of a point, only integers allowed
        color is used to describe color of a point, must be ColorType Object
        texture is used to describe corresponding coordinates in texture, can be float or double
        """

    # Enforce type checking for all variables, set them invisible 
    __slots__ = ["coords", "color", "texture"]

    def __init__(self, coords: typing.Optional[typing.Sequence[int]] = None,
                 color: typing.Optional[ColorType] = None,
                 textureCoords: typing.Optional[typing.Sequence[float]] = None) -> None:
        """
        init Point by using coords, color, textureCoords or an existing point
        if point given, ignore other input arguments
        if point not given, any missing argument will be set to all zero
        
        :param coords: The coordinates of current Point. Only integer coordinates are allowed here.
        :type coords: list[int] or tuple[int]
        :param color: Point color defined in ColorType.
        :type color: ColorType
        :param textureCoords: Corresponding position in texture
        :type textureCoords: list[float] or tuple[float]
        :rtype: None
        """
        # Set point coords
        self.coords = coords
        # Set color
        self.color = color
        # Set texture coords
        self.texture = textureCoords

    def __repr__(self):
        print(self.coords, self.color)
        return "p:" + str(self.coords) + \
               " c:" + str(self.color) + \
               " t:" + str(self.texture)

    def __hash__(self):
        if self.texture is not None:
            tuple_texture = tuple(self.texture)
        else:
            tuple_texture = self.texture
        if self.coords is not None:
            tuple_coords = tuple(self.coords)
        else:
            tuple_coords = self.coords
        return hash((tuple_coords, self.color, tuple_texture))

    def __eq__(self, other):
        try:
            result = self.coords == other.coords and \
                     self.texture == other.texture and \
                     self.color == other.color
        except AttributeError:
            return False
        return result

    def setColor(self, c):
        """
        c should be ColorType, use c to set up color of this point
        This method will deep copy the input argument.
        If you only want to shallow copy the input argument to point color, access that variable directly.

        :param c: the color which you want to set this point to
        :type c: ColorType
        :rtype: None
        """
        self.color = c.copy()

    def setColor_r(self, r):
        self.color.r = r

    def setColor_g(self, g):
        self.color.g = g

    def setColor_b(self, b):
        self.color.b = b

    def getCoords(self):
        """
        Get point coordinates

        :rtype: tuple[int]
        """
        return self.coords

    def getTextureCoords(self):
        """
        Get corresponding texture coordinates

        :rtype: tuple[float]
        """
        return self.texture

    def getColor(self):
        return self.color

    def setCoords(self, coords):
        """
        Use a tuple/list to set point coords

        :param coords: the point coordinates you want to set to
        :type coords: tuple[int] or list[int]
        """
        self.coords = tuple(int(i) for i in coords)

    def setTextureCoords(self, textureCoords):
        """
        Use a tuple/list of coords to set point textureCoords

        :param textureCoords: the texture coordinates you want to set to
        :type textureCoords: tuple[float] or list[float]
        """
        self.texture = tuple(i for i in textureCoords)

    def copy(self):
        """
        A deep copy of current point

        :rtype: Point
        """
        return Point(copy.deepcopy(self.coords), self.color.copy(), copy.deepcopy(self.texture))


if __name__ == "__main__":
    a = Point((1, 2))
    print(a)
    a.setColor(ColorType(0.5*255, 0.2*255, 0.3*255))
    print(a)
    a.setCoords([3, 4])
    print(a)
    a.setTextureCoords((2.22, 3.33))
    print("Point a: ", a)
    b = a.copy()
    print("Point copied from point a: ", b)

    print("Test for illegal input")
    c = Point((1.5, 4))
    print(c)

    # Test for list<Point>
    pl = [Point((1, 3)), Point((2, 3)), Point((3, 5))]
    print(pl)

    # Test for set<Point>
    ps = set(pl)
    print(ps)
    ps.add(Point((1, 3), ColorType(1, 0, 1)))
    print(ps)
    ps.add(Point((1, 3), ColorType(0, 0, 0)))
    print(ps)

    cds = (1, 2, 3)
    clr = ColorType(0.2, 0.3, 0.4)
    t1 = time.time()
    [Point() for _ in range(500 * 500)]
    print(time.time() - t1)
    t1 = time.time()
    for _ in range(500 * 500):
        a = Point(cds, clr)
    print(time.time() - t1)
    t1 = time.time()
    for _ in range(500 * 500):
        a = ColorType()
    print(time.time() - t1)
