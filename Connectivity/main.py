import pygame
import pygame.gfxdraw
import math
import ezdxf
import bezier
from sys import exit

class Point:
    
    def __init__(self, x, y, type):
        # coordinate origin is 46, 46

        # first: clamp x and y

        self.x = min(max(x, 46), 746)
        self.y = min(max(y, 46), 546)

        # next: round to nearest point
        
        self.x = round(self.x - ((self.x - 46) % 20))
        self.y = round(self.y - ((self.y - 46) % 20))

        # set real coords
        self.realx = ((self.x - 46) / 20) / 2
        self.realy = ((self.y - 46) / 20) / 2

        # set type
        self.type = type

    def transform(p, type):
        return Point(p.x, p.y, type)


class Curve:

    def __init__(self, type, controls):
        self.type = type
        self.controls = controls
        self.terminalSlope = (controls[-1].x - controls[-2].x, controls[-1].y - controls[-2].y)
        
        runningX = 0
        runningY = 0
        for p in controls:
            assert(isinstance(p, Point))
            runningX = runningX + (p.x / len(controls))
            runningY = runningY + (p.y / len(controls))
        self.avg = (runningX, runningY)
        
        # construct bezier object
        if self.type == "bez":
            nodes = [
                [controls[0].realx, controls[1].realx, controls[2].realx, controls[3].realx],
                [controls[0].realy, controls[1].realy, controls[2].realy, controls[3].realy]
            ]
            bez = bezier.curve.Curve(nodes, degree = 3)
            self.len = bez.length
        elif self.type == "line" or self.type == "conn":
            self.len = math.sqrt((controls[1].realx - controls[0].realx)**2 + (controls[1].realy - controls[0].realy)**2)
        elif self.type == "conn2":
            self.len = 0



    def draw(self):
        if self.type == "bez":
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[2].x, self.controls[2].y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[3].x, self.controls[3].y, 4, 4))
            pygame.gfxdraw.bezier(screen, [(self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y), (self.controls[2].x, self.controls[2].y), (self.controls[3].x, self.controls[3].y)], 50, (0, 0, 0))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[2].x, self.controls[2].y, 4, 4))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[3].x, self.controls[3].y, 4, 4))
            pygame.gfxdraw.bezier(cl.raster, [(self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y), (self.controls[2].x, self.controls[2].y), (self.controls[3].x, self.controls[3].y)], 50, (0, 0, 0))
        elif self.type == "line":
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.line(screen, (0, 0, 0), (self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.line(cl.raster, (0, 0, 0), (self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y))
        elif self.type == "conn":
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            #pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.line(screen, (255, 0, 0), (self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            #pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.line(cl.raster, (255, 0, 0), (self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y))
        elif self.type == "conn2":
            #pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.line(screen, (0, 255, 0), (self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y))
            #pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[0].x, self.controls[0].y, 4, 4))
            pygame.draw.rect(cl.raster, (0, 0, 0), pygame.Rect(self.controls[1].x, self.controls[1].y, 4, 4))
            pygame.draw.line(cl.raster, (0, 255, 0), (self.controls[0].x, self.controls[0].y), (self.controls[1].x, self.controls[1].y))


class Layer:
    def __init__(self, id, raster, curves, lineQueue, bezQueue):
        self.id = id
        self.raster = raster
        self.curves = curves
        self.lineQueue = lineQueue
        self.bezQueue = bezQueue
        self.length = 0
        self.locked = False

    def genRaster(self):
        self.raster = pygame.Surface((800,600))
        self.raster = self.raster.convert_alpha(self.raster)
        return self.raster


class Button:

    def __init__(self, id, graphic: pygame.Surface, coords):
        self.x = coords[0]
        self.y = coords[1]

        self.graphic = graphic

        self.width = graphic.get_width()
        self.height = graphic.get_height()

        self.id = id

    def checkClicked(self, mouseX, mouseY):
        xcond = self.x <= mouseX and mouseX <= self.x + self.width
        ycond = self.y <= mouseY and mouseY <= self.y + self.height
        return xcond and ycond


def updateQueues(newPoint, lineQueue, bezQueue, curves):

    if not isinstance(newPoint, Point):
        return (lineQueue, bezQueue, curves)
    else:
        
        if newPoint.type == "line":
            if len(lineQueue) == 1:
                # flush

                """
                for p in lineQueue:
                    if not (p in points):
                        points.append(p)
                points.append(newPoint)
                """

                if len(curves) > 0:
                    newX = lineQueue[0].x + curves[-1].terminalSlope[0]
                    newY = lineQueue[0].y + curves[-1].terminalSlope[1]
                    newPoint = Point(newX, newY, "line")

                curves.append(Curve("line", [lineQueue[0], newPoint]))

                # set up both queues
                lineQueue = [Point.transform(newPoint, "line")]
                bezQueue = [Point.transform(newPoint, "bez")]
            else:
                lineQueue.append(newPoint)


        elif newPoint.type == "bez":
            if len(bezQueue) == 3:
                # flush

                """
                for p in bezQueue:
                    if not (p in points):
                        points.append(p)
                points.append(newPoint)
                """

                curves.append(Curve("bez", [bezQueue[0], bezQueue[1], bezQueue[2], newPoint]))

                # set up both queues
                lineQueue = [Point.transform(newPoint, "line")]
                bezQueue = [Point.transform(newPoint, "bez")]
            elif len(bezQueue) == 1:
                if len(curves) > 0:
                    newX = bezQueue[0].x + curves[-1].terminalSlope[0]
                    newY = bezQueue[0].y + curves[-1].terminalSlope[1]
                    bezQueue.append(Point(newX, newY, "bez"))
                else:
                    bezQueue.append(newPoint)
            else:
                bezQueue.append(newPoint)
    return (lineQueue, bezQueue, curves)

def saveDXF(cl):
    bezCounter = 1
    for c in cl.curves:
        assert(isinstance(c, Curve))
        if c.type == "bez":
            splineControls = []
            for p in c.controls:
                splineControls.append((p.realx, p.realy, 0))

            # create DXF
            doc = ezdxf.new()
            modelSpace = doc.modelspace()
            modelSpace.add_spline(splineControls)

            doc.saveas("Layer" + str(cl.id) + "Part" + str(bezCounter) + ".dxf")
            bezCounter = bezCounter + 1
        if c.type == "conn":
            # special S-curve
            splineControls = []
            splineControls.append((0, 0))
            splineControls.append((c.len / 2, 0))
            splineControls.append((c.len / 2, 1.5))
            splineControls.append((c.len, 1.5))

            # create DXF
            doc = ezdxf.new()
            modelSpace = doc.modelspace()
            modelSpace.add_spline(splineControls)

            doc.saveas("Layer" + str(cl.id) + "Connect.dxf")

def saveRaster(cl):
    pygame.image.save(cl.raster, "Layer" + str(cl.id) + ".png")

def saveAll():
    for layer in layers:
        saveRaster(layer)
        saveDXF(layer)


def switchLayer(inc, currentLayer, layers):
    if inc == -1 or inc == 1:
        currentLayer = currentLayer + inc

        # never used
        if len(layers) < currentLayer:
            # create the new layer first
            newLayer = Layer(currentLayer, None, [], [], [])
            newLayer.genRaster()
            layers.append(newLayer)

        currentLayerObj = layers[currentLayer - 1]
        return (currentLayer, currentLayerObj)

def calcCurrentLayerLength(cl):
    sum = 0
    for c in cl.curves:
        assert(isinstance(c,Curve))
        sum = sum + c.len
    cl.length = sum


def layerAboveHasConnection(cl, layers):
    if cl.id == 3:
        return True
    else:
        return layers[cl.id].locked

def finalizeLayer(cl, layers):
    assert(isinstance(cl, Layer))
    if cl.curves == []:
        return False
    cl.curves.append(Curve("conn", [cl.lineQueue[0], Point(cl.lineQueue[0].x + cl.curves[-1].terminalSlope[0], cl.lineQueue[0].y + cl.curves[-1].terminalSlope[1], "conn")]))
    cl.locked = True

    # constrain the layer below
    layers[cl.id - 2].curves.append(Curve("conn2", [cl.lineQueue[0], Point(cl.lineQueue[0].x + cl.curves[-1].terminalSlope[0], cl.lineQueue[0].y + cl.curves[-1].terminalSlope[1], "conn")]))
    layers[cl.id - 2].lineQueue = [Point(cl.lineQueue[0].x + cl.curves[-1].terminalSlope[0], cl.lineQueue[0].y + cl.curves[-1].terminalSlope[1], "line")]
    layers[cl.id - 2].bezQueue = [Point(cl.lineQueue[0].x + cl.curves[-1].terminalSlope[0], cl.lineQueue[0].y + cl.curves[-1].terminalSlope[1], "bez")]

    return True

def estimateTime(layers):
    sumTime = 0
    runningEnergy = 0 # J
    dropHeight = 1.5 * 0.0254 # m above layer
    ballDensity = 7.85 # g / cm^3
    ballDiameter = 0.75 * 2.54 # cm
    gravity = 9.81 # m / s^2

    ballVol = (4/3) * math.pi * (1/ballDiameter)**3
    ballMass = ballVol * ballDensity

    
    for layer in layers:
        # calc initial velocity after ball is dropped
        energy = ballMass * gravity * dropHeight 
        runningEnergy = 0.25 * (runningEnergy + energy) # assume that the drop makes it lose 75% of its energy
        currentVelocity = math.sqrt((2*runningEnergy)/ballMass)
        # use current velocity to determine time to complete this layer
        time = (1/currentVelocity) * (layer.length * 0.0254)
        sumTime = sumTime + time
    
    return sumTime

if __name__ == '__main__':

    drawingMode = "bez"
    errText = "Ready!"

    layers = []

    buttons = []

    pygame.init()
    pygame.display.init()

    disp_size = (800, 600)

    screen = pygame.display.set_mode(disp_size)
    pygame.display.set_caption('Connectivity Test')

    # init layers
    cl = Layer(1, None, [], [], [])
    layers.append(cl)
    cl.genRaster()

    cl = Layer(2, None, [], [], [])
    layers.append(cl)
    cl.genRaster()

    cl = Layer(3, None, [], [], [])
    layers.append(cl)
    cl.genRaster()

    currentLayer = 3
    
    # load assets
    grid = pygame.image.load('protogrid.png')
    grid.set_alpha(25)
    line = pygame.image.load('line.png')
    curve = pygame.image.load('curve.png')
    arc = pygame.image.load('arc.png')
    img = pygame.image.load('img.png')
    dxf = pygame.image.load('dxf.png')
    sav = pygame.image.load('floppy.png')
    up = pygame.image.load('up.png')
    down = pygame.image.load('down.png')
    ruler = pygame.image.load('ruler.png')
    connect = pygame.image.load('connect.png')
    watch = pygame.image.load('watch.png')

    fontTiny = pygame.font.Font("roman.ttf", 20)

    # init. buttons
    buttons.append(Button(0, line, (0,0)))
    buttons.append(Button(1, curve, (40,0)))
    buttons.append(Button(2, dxf, (680,0)))
    buttons.append(Button(3, img, (720,0)))
    buttons.append(Button(4, sav, (760,0)))
    buttons.append(Button(5, up, (760,380)))
    buttons.append(Button(6, down, (760,420)))
    buttons.append(Button(7, ruler, (0,100)))
    buttons.append(Button(8, connect, (0,160)))
    buttons.append(Button(9, watch, (0,220)))

    # main loop
    running = True
    while running:
        # draw the current frame
        screen.fill((255, 255, 255))
        cl.raster.fill((255, 255, 255))
        screen.blit(grid, (46, 46))

        errorGraphic = fontTiny.render(errText, True, (0,0,0))
        screen.blit(errorGraphic, (25, 560))
        ltGraphic = fontTiny.render("Layer " + str(currentLayer), True, (0,0,0))
        screen.blit(ltGraphic, (350, 10))
        cl.raster.blit(ltGraphic, (350, 10))

        for b in buttons:
            screen.blit(b.graphic, (b.x, b.y))

        i = 0

        # draw curves and lines
        bezCounter = 1
        for c in cl.curves:
            if (isinstance(c, Curve)):
                c.draw()
                if c.type == "bez":
                    no = fontTiny.render(str(bezCounter), True, (0,0,0))
                    screen.blit(no, c.avg)
                    cl.raster.blit(no, c.avg)
                    bezCounter = bezCounter + 1

        # draw temporary points
        for p in cl.lineQueue:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(p.x, p.y, 4, 4))
        for p in cl.bezQueue:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(p.x, p.y, 4, 4))
            

        #screen.blit(raster, (0,0))

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit
                running = False
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                id = None
                for b in buttons:
                    if b.checkClicked(mouseX, mouseY):
                        id = b.id
                if id == None:
                    if (layerAboveHasConnection(cl, layers)):
                        if (not cl.locked):
                            cl.lineQueue, cl.bezQueue, cl.curves = updateQueues(Point(mouseX, mouseY, drawingMode), cl.lineQueue, cl.bezQueue, cl.curves)
                            errText = "Ready!"
                        else:
                            errText = "This layer has already been finalized!"
                    else:
                        errText = "You must finalize the layer above first!"
                elif id == 0:
                    drawingMode = "line"
                elif id == 1:
                    drawingMode = "bez"
                elif id == 2:
                    # save DXF
                    saveDXF(cl)
                    errText = "Successfully wrote curves on this layer to .DXF files"
                elif id == 3:
                    # save raster
                    saveRaster(cl)
                    errText = "Successfully wrote raster image of this layer to .PNG file"
                elif id == 4:
                    # save all
                    saveAll()
                    errText = "Successfully wrote .PNGs and .DXFs of all layers and their curves"
                elif id == 5:
                    # move up one layer
                    if currentLayer == 3:
                        errText = "You can't build any higher!"
                    else:
                        currentLayer, cl = switchLayer(1, currentLayer, layers)
                        errText = "Ready!"
                elif id == 6:
                    # move down one layer... never below 1
                    if currentLayer != 1:
                        if cl.locked:
                            currentLayer, cl = switchLayer(-1, currentLayer, layers)
                            errText = "Ready!"
                        else:
                            errText = "You need to finalize this layer first!"
                    else:
                        errText = "Can't move down: you are already on the lowest layer!"
                elif id == 7:
                    # calc layer length
                    calcCurrentLayerLength(cl)
                    errText = "The current layer length is " + str(round(cl.length,2)) + " inches."
                elif id == 8:
                    # connect down
                    if cl.id == 1:
                        errText = "Can't connect down: you are already on the lowest layer!"
                    elif cl.locked:
                        errText = "This layer has already been finalized!"
                    else:
                        if finalizeLayer(cl, layers):
                            errText = "Successfully finalized this layer"
                        else:
                            errText = "Can't finalize an empty layer!"
                elif id == 9:
                    # estimate time
                    complete = True
                    for layer in layers:
                        calcCurrentLayerLength(layer)
                        if not layer.locked and layer.id > 1:
                            complete = False
                    if complete:
                        errText = "The current marble race will take " + str(round(estimateTime(layers),2)) + " seconds to finish."
                    else:
                        errText = "Not all layers have been finalized yet!"

        pygame.display.update()

    pygame.quit()
    exit()

