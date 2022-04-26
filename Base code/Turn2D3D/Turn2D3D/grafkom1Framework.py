# grafkom1Framework.py
from OpenGL.GL import * #move this to line 1
class ObjLoader(object):
    """This is the class for loading the 3d object in which it load the vertex and append it into a
    vertices list for displaying in python"""
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        ##
        try:
            f = open(fileName)
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                    self.vertices.append(vertex)

                elif line[0] == "f":
                    string = line.replace("//", "/")
                    ##
                    i = string.find(" ") + 1
                    face = []
                    for item in range(string.count(" ")):
                        if string.find(" ", i) == -1:
                            face.append(string[i:-1])
                            break
                        face.append(string[i:string.find(" ", i)])
                        i = string.find(" ", i) + 1
                    ##
                    self.faces.append(tuple(face))

            f.close()
        except IOError:
            print(".obj file not found.")
    
    def render_scene(self):
        if len(self.faces) > 0:
            ##
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for f in face:
                    vertexDraw = self.vertices[int(f) - 1]
                    if int(f) % 3 == 1:
                        glColor4f(0.282, 0.239, 0.545, 0.35)
                    elif int(f) % 3 == 2:
                        glColor4f(0.729, 0.333, 0.827, 0.35)
                    else:
                        glColor4f(0.545, 0.000, 0.545, 0.35)
                    glVertex3fv(vertexDraw)
            glEnd()