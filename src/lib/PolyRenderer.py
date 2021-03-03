from Camera import Camera
from GraphicsObject import GraphicsObject
from MathAndProjections import *

class PolyRenderer:
    def __init__(self,camera,canvas,width,height):
        if (isinstance(camera,Camera)):
            self.camera = camera
        else:
            raise TypeError

        self.canvas = canvas
        self.canvas.pack()


        self.width  =  width
        self.height =  height


        self.objectList = []
        self.objectPolyList = []
        self.objectsPlanesCoefs = []
        self.objectsWeightCenters = []

        self.f_proj = perspective_proj



    def registerObject(self,graphicsObj):
        plane_coeffs = []
        camPos = self.camera.getPos()
        if (isinstance(graphicsObj,GraphicsObject)):
            self.objectList.append(graphicsObj)

            for face in graphicsObj.faces:
                plane_coeffs.append(plane_coef(face, graphicsObj.verticies))

            w_center = plane_w_center(graphicsObj.verticies)

            plane_coeffs = np.array(plane_coeffs)

            for i in range(plane_coeffs.shape[0]):
                plane_coeffs[i] = matrix_to_w_center(plane_coeffs[i], w_center)

            Model = graphicsObj.verticies
            Model, s = CKM_to_CKH(Model, camPos)
            Model = self.f_proj(Model, s)
            Model = CKK_to_CKEi(Model, 10, self.width / 2, self.height / 2, 200, 200)

            polys = []

            index_count = 0
            for face in graphicsObj.faces:
                points = []
                for index in face:
                    points.append(Model[index][0])
                    points.append(Model[index][1])

                polys.append(self.canvas.create_polygon(points, fill=graphicsObj.colors[index_count]))
                index_count += 1

                last = len(polys) - 1

                if (plane_coeffs[last][0] * camPos[0] + plane_coeffs[last][1] * camPos[1] + plane_coeffs[last][2] * camPos[2] + plane_coeffs[last][3] <= 0):
                    self.canvas.itemconfigure(polys[last], state="hidden")

            self.objectPolyList.append(np.array(polys))
            self.objectsPlanesCoefs.append(plane_coeffs)
            self.objectsWeightCenters.append(w_center)

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
        cPos = self.camera.getPos()
        for obj in self.objectList:
            Model = obj.verticies
            Model, s = CKM_to_CKH(Model, self.camera.getPos())
            s*=2
            Model = self.f_proj(Model, s)
            Model = CKK_to_CKEi(Model, 10, self.width / 2, self.height / 2, 200, 200)

            for i in range(self.objectPolyList[index_count].size):
                if (self.objectsPlanesCoefs[index_count][i][0] * cPos[0] + self.objectsPlanesCoefs[index_count][i][1] * cPos[1] +self.objectsPlanesCoefs[index_count][i][2] * cPos[2] + self.objectsPlanesCoefs[index_count][i][3] > 0):
                    points = []
                    for index in obj.faces[i]:
                        points.append(Model[index][0])
                        points.append(Model[index][1])

                    self.canvas.itemconfigure(self.objectPolyList[index_count][i], state="normal")
                    self.canvas.coords(self.objectPolyList[index_count][i], points)
                else:
                    self.canvas.itemconfigure(self.objectPolyList[index_count][i], state="hidden")