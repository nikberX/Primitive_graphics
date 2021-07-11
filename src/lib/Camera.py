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




