from GraphicsObject import GraphicsObject
import time
class Animator:
    def __init__(self):
        self.objects =  []
        self.behavior = []
        self.time = time
    def registerObject(self,graphicsObj,behavior):
        if (isinstance(graphicsObj,GraphicsObject)):
            self.objects.append(graphicsObj)
            self.behavior.append(behavior)
        else:
            print("Failed to register graphicsObj")
    def update(self):
        deltatime = self.time.time()
        index = 0
        for obj in self.objects:
            self.behavior[index](obj,deltatime)
            index+=1
