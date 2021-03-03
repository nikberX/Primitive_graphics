import GraphicsObject
from numpy import array


h = 600
w = 1200

class Camera:
    def __init__(self, cameraPos, cv,root):
        self.x = cameraPos[0]
        self.y = cameraPos[1]
        self.z = cameraPos[2]
        self.lines = []

        self.s = None


    def getPos(self):
        return [self.x,self.y,self.z]

    def move(self, d):
        self.x += d[0]
        self.y += d[1]
        self.z += d[2]



    def update(self, Model):
        return 0


"""

from graphics import GraphWin,Point
from math import sqrt
from numpy import matrix
from Matrices import orthoMatrix,vec4,rotationX,rotationZ,rotationY,translate
from GraphicsObject import GraphicsObject
class Camera:
    def __init__(self,graphWin,pos = [0,0,1] ,target = [0,0,0],up = [0,1,0]):
        if (isinstance(graphWin,GraphWin)):
            self.win = graphWin
            self.pos = vec4(pos)
            self.target = vec4(target)
            self.up = vec4(up)
            direction = [0, 0, 0, 1]
            direction[0] = self.pos[0][0] - self.target[0][0]
            direction[1] = self.pos[1][0] - self.target[1][0]
            direction[2] = self.pos[2][0] - self.target[2][0]
            norm = sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
            direction[0] /= norm
            direction[1] /= norm
            direction[2] /= norm

            right = [0, 0, 0, 1]
            right[0] = self.up[1][0] * direction[2] - self.up[2][0] * direction[1]
            right[1] = self.up[2][0] * direction[0] - self.up[0][0] * direction[2]
            right[2] = self.up[0][0] * direction[1] - self.up[1][0] * direction[0]

            norm = sqrt(right[0] ** 2 + right[1] ** 2 + right[2] ** 2)
            right[0] /= norm
            right[1] /= norm
            right[2] /= norm

            cameraup = [0, 0, 0, 1]
            cameraup[0] = direction[1] * right[2] - direction[2] * right[1]
            cameraup[1] = direction[2] * right[0] - direction[0] * right[2]
            cameraup[2] = direction[0] * right[1] - direction[1] * right[0]

            lookAt = matrix(
                [
                    [right[0], right[1], right[2], 0],
                    [cameraup[0], cameraup[1], cameraup[2], 0],
                    [direction[0], direction[1], direction[2], 0],
                    [0, 0, 0, 1]
                ]
            )
            self.lookAt = lookAt @ matrix(
                [
                    [1, 0, 0, -self.pos[0][0]],
                    [0, 1, 0, -self.pos[1][0]],
                    [0, 0, 1, -self.pos[2][0]],
                    [0, 0, 0, 1]
                ]
            )
            self.lookAt = orthoMatrix(50) @ lookAt
        else:
            raise TypeError

    def draw(self,obj):
        if (isinstance(obj,GraphicsObject)):
            pointList = []
            for item in obj.edgesArr:
                vec = self.lookAt@obj.modelMatrix@item
                pointList.append(Point(vec[0][0],vec[1][0]))

            return pointList
        else:
            return None

    def rotateXYZ(self,X,Y,Z):
        rotX = rotationX(X)
        rotY = rotationY(Y)
        rotZ = rotationZ(Z)
        rotate = rotZ @ rotY @ rotX

        movedPl = translate([self.pos[0][0],self.pos[1][0],self.pos[2][0]])
        movedMi = translate([-self.pos[0][0], -self.pos[1][0], -self.pos[2][0]])

        self.pos = movedMi@self.pos
        self.target = movedMi@self.pos
        self.up = movedMi@self.pos
        self.pos = rotate@self.pos
        self.target = rotate@ self.target
        self.up = rotate @self.up
        self.pos = movedPl @ self.pos
        self.target = movedPl @ self.pos
        self.up = movedPl @ self.pos
        self.update()

    def translate(self,vec):
        self.pos[0][0] =vec[0] + self.pos[0][0]
        self.pos[1][0] = vec[1] + self.pos[1][0]
        self.pos[2][0] = vec[2] + self.pos[2][0]

        self.target[0][0]=vec[0] + self.target[0][0]
        self.target[1][0]= vec[1] + self.target[1][0]
        self.target[2][0]= vec[2]+ self.target[2][0]

        self.up[0][0]= vec[0] + self.up[0][0]
        self.up[1][0]= vec[1]+ self.up[1][0]
        self.up[2][0]= vec[2]+ self.up[2][0]
        print("up:",self.up)
        print("targ:", self.target)
        print("pos:", self.pos)
        self.update()

    def update(self, ):
        direction = [0, 0, 0, 1]
        direction[0] = self.pos[0][0] - self.target[0][0]
        direction[1] = self.pos[1][0] - self.target[1][0]
        direction[2] = self.pos[2][0] - self.target[2][0]
        norm = sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
        direction[0] /= norm
        direction[1] /= norm
        direction[2] /= norm

        right = [0, 0, 0, 1]
        right[0] = self.up[1][0] * direction[2] - self.up[2][0] * direction[1]
        right[1] = self.up[2][0] * direction[0] - self.up[0][0] * direction[2]
        right[2] = self.up[0][0] * direction[1] - self.up[1][0] * direction[0]

        norm = sqrt(right[0] ** 2 + right[1] ** 2 + right[2] ** 2)
        right[0] /= norm
        right[1] /= norm
        right[2] /= norm

        cameraup = [0, 0, 0, 1]
        cameraup[0] = direction[1] * right[2] - direction[2] * right[1]
        cameraup[1] = direction[2] * right[0] - direction[0] * right[2]
        cameraup[2] = direction[0] * right[1] - direction[1] * right[0]

        lookAt = matrix(
            [
                [right[0], right[1], right[2], 0],
                [cameraup[0], cameraup[1], cameraup[2], 0],
                [direction[0], direction[1], direction[2], 0],
                [0, 0, 0, 1]
            ]
        )
        self.lookAt = lookAt @ matrix(
            [
                [1, 0, 0, -self.pos[0][0]],
                [0, 1, 0, -self.pos[1][0]],
                [0, 0, 1, -self.pos[2][0]],
                [0, 0, 0, 1]
            ]
        )
        self.lookAt = orthoMatrix(50) @ lookAt

"""

