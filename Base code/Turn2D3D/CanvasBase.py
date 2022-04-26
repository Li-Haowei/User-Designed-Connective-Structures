"""
Set up our display pipeline. WxPython is used to solve system compatibility problem. It is mainly focusing on creating a
display window with a canvas. We will let the OpenGL to draw on it. OpenGL will orthogonal project a 2D plane which has
the exact size as the window on canvas. A texture will be applied to this plane later. Our program will update this
texture with a assigned buff object. This is the main pipeline we draw on a display window. Window resize and mouse
clicking have been implemented. All these things have been wrapped up, and the main class should inherit this class.
First version Created on 09/27/2018
"""

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut  # this fails on OS X 11.x
    except ImportError:
        print('Patching for Big Sur')
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

from Buff import Buff
from ColorType import ColorType

# -------------------------- System Checking --------------------------
WX_MINIMUM_REQUIRED = "3.0.0"
OPENGL_MINIMUM_REQUIRED = "3.1.0"

# Package version checking
if wx.__version__ < WX_MINIMUM_REQUIRED:
    # Not fully tested on older version.
    raise ImportError("wxPython minimum requirement " + WX_MINIMUM_REQUIRED)
if OpenGL.__version__ < OPENGL_MINIMUM_REQUIRED:
    # Not fully tested on older version.
    raise ImportError("PyOpenGL minimum requirement " + OPENGL_MINIMUM_REQUIRED)


# -------------------------- End of System Checking --------------------------

class CanvasBase(glcanvas.GLCanvas):
    """
    All methods are based on interruptions and events which start with capital letter
    methods for public use start with lower case letter
    methods which have protected access (but still accessible from outside) start with _(single underscore)
    methods for private use (not accessible outside) start with __ (double underscore)
    """
    # Some invisible variables can only be changed by using provided methods
    __pixelScale = 1
    __quadric = glu.gluNewQuadric()
    __background = ColorType(0, 0, 0)

    points_r = []
    points_l = []

    buff = Buff()
    buff_last = Buff()

    def __init__(self, parent):
        """
        Inherit from WxPython GLCanvas class. Bind implemented methods to window events.

        :param parent: The WxPython frame you want to inherit from
        :type parent: wx.Frame
        """
        super(CanvasBase, self).__init__(parent)
        self.init = False
        self.context = glcanvas.GLContext(self)
        self.size = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeft)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRight)
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def setPixelScale(self, size):
        if (not isinstance(size, int)) or size < 1:
            raise TypeError("PixelScale can only accept integer >= 1")
        self.__pixelScale = size

    def getPixelScale(self):
        return self.__pixelScale

    def clear(self):
        """
        clear display buff, but save last frame to buff_last
        """
        self.buff_last = self.buff.copy()
        self.buff.clear()
        self.points_l.clear()
        self.points_r.clear()

    def OnResize(self, event):
        """
        This method handles onresize event.
        """

        self.context = glcanvas.GLContext(self)
        self.size = self.GetClientSize()
        self.SetCurrent(self.context)

        gl.glViewport(0, 0, self.size.width, self.size.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(0, self.size.width, 0, self.size.height)

        # Create new buffer for display and store last frame buffer to buff_last
        self.buff_last = self.buff.copy()
        self.buff.resize(self.size.width, self.size.height)

        # Update screen and display
        self.Refresh(eraseBackground=True)
        self.Update()

    def OnPaint(self, event=None):
        """
        A simple wrap around OnDraw, added OpenGL init checking
        """
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):
        """
        This method is needed at the very beginning to initialize the opengl environment
        """

        # gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        # Set subsequent matrix operations to the projection matrix stack
        gl.glMatrixMode(gl.GL_PROJECTION)
        self.size = self.GetClientSize()
        # clear background on canvas. Texture background is determined by buff
        gl.glClearColor(0, 0, 0, 0)
        glu.gluOrtho2D(0, self.size.width, 0, self.size.height)

        # load buff as Texture
        # Create new buffer for display and store last frame buffer to buff_last
        self.buff_last = self.buff.copy()
        self.buff = Buff(self.size.width, self.size.height, ColorType(0, 0, 0))

        gl.glClearColor(0., 0., 0., 0.)
        gl.glClearDepth(1.0)
        gl.glDepthFunc(gl.GL_LEQUAL)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_COLOR_MATERIAL)

        glu.gluQuadricNormals(self.__quadric, glu.GLU_SMOOTH)
        glu.gluQuadricTexture(self.__quadric, gl.GL_TRUE)
        gl.glEnable(gl.GL_LIGHT0)

    def OnDraw(self):
        """
        The main method to draw our buff in the window. Don't forget to init GL first.
        """
        # clear color buffer and depth buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Replace current matrix with identity matrix
        gl.glLoadIdentity()
        # Set coordinate system, origin at left-bottom
        glu.gluOrtho2D(0, self.size.width, 0, self.size.height)
        # Save current frame to last frame in case you need it
        self.buff_last = self.buff.copy()

        # The core part for display: generate a rectangle which covers the whole canvas and map texture to it. \
        # Texture is the content we want to display on canvas
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.size.width, self.size.height, 0, gl.GL_RGB,
                        gl.GL_UNSIGNED_BYTE, self.buff.getBytes())
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex2i(self.buff.width, 0)
        gl.glTexCoord2f(0.0, 0.0)
        gl.glVertex2i(0, 0)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex2i(0, self.buff.height)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex2i(self.buff.width, self.buff.height)
        gl.glEnd()

        # Swap Buffer to display canvas
        self.SwapBuffers()

    def OnMouseLeft(self, event):
        """
        Record left mouse click event and feed coordinates to Interrupt_MouseL
        """
        x = event.GetX()
        y = event.GetY()
        self.Interrupt_MouseL(x, self.size.height - y)
        self.Refresh(True)

    def OnMouseRight(self, event):
        """
        Record right mouse click event and feed coordinates to Interrupt_MouseL
        """
        x = event.GetX()
        y = event.GetY()
        self.Interrupt_MouseR(x, self.size.height - y)
        self.Refresh(True)

    def OnKeyDown(self, event):
        """
        Record the key down event and feed the key to Interrupt_MouseL
        """
        keycode = event.GetKeyCode()
        self.Interrupt_Keyboard(keycode)
        self.Refresh(True)

    def Interrupt_MouseL(self, x, y):
        raise NotImplementedError("Mouse Left interrupt not implemented yet")

    def Interrupt_MouseR(self, x, y):
        raise NotImplementedError("Mouse Right interrupt not implemented yet")

    def Interrupt_Keyboard(self, keycode):
        raise NotImplementedError("keyboard interrupt not implemented yet")

    @staticmethod
    def OnDestroy(event):
        print("Destroy Window")


if __name__ == "__main__":
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame,
    # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
    canvas = CanvasBase(frame)

    frame.Show()
    app.MainLoop()
