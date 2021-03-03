from numpy import array,c_,ones
class GraphicsObject:
    def __init__(self,vertices,edges,worldPos,polys = None,colors = None):
        self.localVerticies = vertices
        self.verticies = vertices
        self.edges = edges
        self.faces = edges
        self.polys = polys
        self.worldPos = worldPos
        self.scale = 1
        self.colors = colors
        self.update()

    def translate(self, pos):
        self.worldPos = pos
        self.update()

    def resize(self,scaleSize):
        self.scale = scaleSize
        self.update()

    def update(self):

        T = array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [-self.worldPos[0], -self.worldPos[1], -self.worldPos[2], 1]])
        vertex_ex = c_[self.localVerticies, ones(self.localVerticies.shape[0])]
        vertex_ex = (vertex_ex @ T)[:, :3]
        self.verticies = vertex_ex

"""
from numpy import matrix
from Matrices import *
class GraphicsObject:
    def __init__(self,edgesArr,worldPos):
        self.worldPos = vec4(worldPos)
        self.edgesArr = edgesArr
        self.scale = 1
        self.rotatedX=0
        self.rotatedY=0
        self.rotatedZ=0
        self.modelMatrix = matrix(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )

    def draw(self,cameraObj):
        list = cameraObj.draw(self)
        return list

    def scaling(self,scaleSize):
        self.scale = scaleSize
        self.update()

    def translate(self,pos):
        self.worldPos = vec4(pos)
        self.update()

    def rotateXYZ(self,X=0,Y=0,Z=0):
        self.rotatedX = X
        self.rotatedY = Y
        self.rotatedZ = Z
        self.update()

    def update(self):
        scaleMat = scale(self.scale)
        transMat = translate(self.worldPos)
        rXMatrix = rotationX(self.rotatedX)
        rYMatrix = rotationY(self.rotatedY)
        rZMatrix = rotationZ(self.rotatedZ)
        self.modelMatrix = transMat@rZMatrix@rYMatrix@rXMatrix@scaleMat
"""