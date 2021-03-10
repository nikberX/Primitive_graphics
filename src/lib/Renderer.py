from Camera import Camera
from GraphicsObject import GraphicsObject
from MathAndProjections import *

class Renderer:
    def __init__(self,camera,canvas,width,height):
        if (isinstance(camera,Camera)):
            self.camera = camera
        else:
            raise TypeError

        self.canvas = canvas
        self.canvas.pack()


        self.width  =  width
        self.height =  height

        #objectMap[0] - GraphicsObject, objectMap[1] - lines of GraphicsObject
        self.objectList = []
        self.objectLinesList = []

        self.f_proj = parallel_proj



    def registerObject(self,graphicsObj):
        if (isinstance(graphicsObj,GraphicsObject)):
            self.objectList.append(graphicsObj)
            Model = graphicsObj.verticies
            Model, s = worldToCamera(Model, self.camera.getPos())
            s *= 2
            Model = self.f_proj(Model, s)
            Model = CKK_to_CKEi(Model, 10, self.width / 2, self.height / 2, 200, 200)

            lines = []
            # все остальные линии
            for edge in graphicsObj.edges:
                lines.append(
                    self.canvas.create_line(Model[edge[0], 0], Model[edge[0], 1], Model[edge[1], 0], Model[edge[1], 1]))
            self.objectLinesList.append(lines)
        else:
            print("Failed to register graphicsObj")

    def changeProjection(self):
        if (self.f_proj == parallel_proj):
            self.f_proj = perspective_proj
            self.update()
        else:
            self.f_proj = parallel_proj
            self.update()

    def update(self):
        index_count = 0
        for obj in self.objectList:
            Model = obj.verticies
            Model, s = worldToCamera(Model, self.camera.getPos())
            s*=2
            Model = self.f_proj(Model, s)
            Model = CKK_to_CKEi(Model, 10, self.width / 2, self.height / 2, 200, 200)

            for i in range(0, obj.edges.shape[0]):
                self.canvas.coords( self.objectLinesList[index_count][i], Model[obj.edges[i][0], 0],
                                    Model[obj.edges[i][0], 1], Model[obj.edges[i][1], 0],
                                    Model[obj.edges[i][1], 1])
            index_count+=1