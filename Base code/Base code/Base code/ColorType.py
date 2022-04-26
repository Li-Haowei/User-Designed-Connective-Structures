"""
This file contains a basic ColorType class, which is used to store RGB color in float.
For performance reason, instances of this class will only have three variable slots: r, g and b.
r, g and b will be stored as floats in range [0, 1].
Performance Suggestions:

* If you need to access the r, g and b values, direct RGB access is faster than calling methods.

"""


class ColorType:
    """
    A class to manage RGB color
    """
    __slots__ = ["r", "g", "b"]

    # r, g, b are floats in [0, 1]

    def __init__(self, r: float = 0, g: float = 0, b: float = 0) -> None:
        """
        can use r,g,b to create a ColorType
        recommend to pass through arguments using specific keys and values
        
        :param r: Red color value, should be in range [0, 1]
        :param g: Green color value, should be in range [0, 1]
        :param b: Blue color value, should be in range [0, 1]
        :type r: float
        :type g: float
        :type b: float
        :rtype: None
        """
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        """
        Defines ColorType print string
        """
        return str(self.getRGB())

    def __hash__(self):
        """
        Defines ColorType hashing. This will be needed in Set and Dict.
        """
        return hash((self.r, self.g, self.b))

    def __eq__(self, other):
        """
        For ColorType comparison
        """
        try:
            result = self.r == other.r and \
                     self.g == other.g and \
                     self.b == other.b
        except AttributeError:
            return False
        return result

    def setRGB(self, r=0, g=0, b=0):
        """
        This method will check input value to make sure they are in range.
        This is safe for input value, but might affect the ColorType performance.

        :param r: Red color value, should be in range [0, 1]
        :param g: Green color value, should be in range [0, 1]
        :param b: Blue color value, should be in range [0, 1]
        :type r: float
        :type g: float
        :type b: float
        :rtype: None
        """
        self.r = min(1.0, max(0.0, r))
        self.g = min(1.0, max(0.0, g))
        self.b = min(1.0, max(0.0, b))

    def setRGB_8bit(self, r=0, g=0, b=0):
        """
        :param r: Red color value, should be in range [0, 255]
        :param g: Green color value, should be in range [0, 255]
        :param b: Blue color value, should be in range [0, 255]
        :type r: int
        :type g: int
        :type b: int
        :rtype: None
        """
        self.r = r/255
        self.g = g/255
        self.b = b/255

    def setRGB_ARGB(self, argb):
        """
        set RGB by using only one integer, which is in ARGB format

        :param argb: ARGB color in int. Int length is 32 bits, the highest 8 bits are transparent value (\
        discarded), and it followed by 8 bits red color, 8 bits green color and 8 bits blue color.
        :type argb: int
        :rtype: None
        """
        self.r = ((argb & 0x00ff0000) >> 16) / 255
        self.g = ((argb & 0x0000ff00) >> 8) / 255
        self.b = (argb & 0x000000ff) / 255

    def setRGB_RGBA(self, rgba):
        """
        set RGB by using only one integer, which is in RGBA format

        :param rgba: ARGB color in int. Int length is 32 bits, the highest 8 bits are red value,\
        and 8 bits green color and 8 bits blue color.
        :type rgba: int
        :rtype: None
        """
        self.r = ((rgba >> 24) & 0xff) / 255.0
        self.g = ((rgba >> 16) & 0xff) / 255.0
        self.b = ((rgba >> 8) & 0xff) / 255.0

    def getRGB(self):
        """
        Get current RGB values as a tuple.

        :rtype: tuple[float]
        """
        return self.r, self.g, self.b

    def getRGB_8bit(self):
        """
        Get a tuple which contains current RGB 8 bits values.
        Each color is represented in char format (8 bits integer, value in range [0, 255])

        :rtype: tuple[int]
        """
        return int(self.r*255), int(self.g*255), int(self.b*255)

    def getRGB_RGBA(self):
        """
        Get color in RGBA format

        :rtype: int
        """
        RGB_tuple = self.getRGB_8bit()
        return (RGB_tuple[0] << 24) | (RGB_tuple[1] << 16) | (RGB_tuple[2] << 8) | 0xff

    def getRGB_BGR(self):
        """
        Get color in BGR format. This format is popular used in OpenCV library.

        :type: int
        """
        RGB_tuple = self.getRGB_8bit()
        return (RGB_tuple[2] << 16) | RGB_tuple[1] << 8 | RGB_tuple[0]

    def copy(self):
        """
        A deep copy of current ColorType instance.

        :rtype: ColorType
        """
        return ColorType(self.r, self.g, self.b)


if __name__ == "__main__":
    c = ColorType(0.5, 0.2, 0.1)
    print(c.getRGB_8bit())
    print(c.getRGB_RGBA())
    print(c)
    print()
    c = ColorType()
    c.setRGB_ARGB(8401690)
    print(c.getRGB_8bit())
    print(c.getRGB_RGBA())
    print(c)
    print()
    b = ColorType(*c.getRGB())
    print(b)

    # Test for set
    cs = set()
    cs.add(ColorType(1, 0, 1))
    cs.add(ColorType(1, 0, -1))
    cs.add(ColorType(0.5, 1, 1))
    cs.add(ColorType(1, 0, 1))
    print(cs)
