from Camera import Camera
from Application import Application
from EventHandler import *
from Renderer import *
from numpy import array
from math import sin,cos
from Animator import Animator
from PolyRenderer import *
SCR_HEIGHT = 600
SCR_WIDTH  = 1200
BG_COLOR   = 'white'

cubeVerticies = array([
                                   [ 1,  1, -1],
                                   [ 1, -1, -1],
                                   [-1, -1, -1],
                                   [-1,  1, -1],
                                   [ 1,  1,  1],
                                   [ 1, -1,  1],
                                   [-1, -1,  1],
                                   [-1,  1,  1]
])

cubeFaces = array([
    [1,5,4,0],
    [2,6,7,3],
    [0,4,7,3],
    [3,0,1,2],
    [4,5,6,7],
    [1,2,6,5],
])

cubeEdges = array([
                               [0, 1],
                               [1, 2],
                               [2, 3],
                               [3, 0],
                               [0, 4],
                               [1, 5],
                               [2, 6],
                               [3, 7],
                               [4, 5],
                               [5, 6],
                               [6, 7],
                               [7, 4]
])

colors = ["red", "green", "blue", "orange", "purple","black"]

CoordsVertices = array([           [0, 0, 0],
                                   [6, 0, 0],
                                   [0, 6, 0],
                                   [0, 0, 6],
])

CoordsEdges =  array([           [0, 1],
                                 [0, 2],
                                 [0, 3]
])

def cubeAmimation1(obj,ttime):
    time = ttime * 2
    x = 1*sin(time)
    y = 1*cos(time)
    obj.translate([x,y,0])

def cubeAmimation2(obj,ttime):
    time = ttime
    y = 2*sin(time)
    z = 2*cos(time)
    obj.translate([0,y,z])

def cubeAmimation3(obj,ttime):
    time = ttime / 2
    x = 3*sin(time)
    z = 3*cos(time)
    obj.translate([x,0,z])


def main():
    app = Application(SCR_HEIGHT,SCR_WIDTH)
    camera = Camera([6, 6, 5], app.getCanvas(), app.getRoot())
    renderer = PolyRenderer(camera,app.getCanvas(),app.getWidth(),app.getHeight())
    myobj = GraphicsObject(cubeVerticies,cubeFaces,[0,0,0],cubeFaces,colors)
    #myobj2 = GraphicsObject(cubeVerticies,cubeEdges,[0,0,0])

    myobj.translate([-1,-1,-1])
    animator = Animator()
    renderer.registerObject(myobj)
    #renderer.registerObject(myobj2)
    eventHandler = EventHandler(camera,renderer,animator)
    app.setEventHandler(eventHandler)
    app.bindEvent("<Key>",app.eventHandler.keyEvent)
    app.mainloop()

if __name__ == '__main__':
    main()

#old code with another math
"""
from graphics import *
from math import (pi,sin,cos,sqrt,trunc)
from numpy import matrix
import time
import keyboard
from GraphicsObject import GraphicsObject
from Camera import Camera
from Matrices import vec4
SCR_WIDTH  = 600
SCR_HEIGHT = 600

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return trunc(stepper * number) / stepper


boxEdges = (
    matrix([[-0.50], [-0.50], [-0.50], [1]]),
    matrix([[ 0.50], [-0.50], [-0.50], [1]]),
    matrix([[ 0.50], [ 0.50], [-0.50], [1]]),
    matrix([[-0.50], [ 0.50], [-0.50], [1]]),
    matrix([[-0.50], [-0.50], [ 0.50], [1]]),
    matrix([[ 0.50], [-0.50], [ 0.50], [1]]),
    matrix([[ 0.50], [ 0.50], [ 0.50], [1]]),
    matrix([[-0.50], [ 0.50], [ 0.50], [1]]),
)

arrowEdges = (
    matrix([[ 0.0], [0], [0], [1]]),
    matrix([[0.50], [-0.10], [0], [1]]),
    matrix([[ 0.50], [-0.20], [0], [1]]),
    matrix([[0.75], [0], [0], [1]]),
    matrix([[ 0.50], [ 0.20], [0], [1]]),
    matrix([[0.50], [ 0.10], [0], [1]]),
)

orts = (
    matrix([[1], [0], [0], [1]]),
    matrix([[0], [1], [0], [1]]),
    matrix([[0], [0], [1], [1]]),
    matrix([[0], [0], [0], [1]]),
)

def main():
    win = GraphWin('App',SCR_WIDTH,SCR_HEIGHT)
    win.setCoords(-SCR_HEIGHT/2,-SCR_WIDTH/2,SCR_HEIGHT/2,SCR_WIDTH/2)

    angle = 0


    pointList = []
    lineList = []
    ortlist = []
    pOrtlist=[]


    for i in range(12): lineList.append(Line(Point(0,0),Point(1,1)))
    camera = Camera(win,[1.0,1.0,1.0])
    box = GraphicsObject(boxEdges,[0,0,-2])
    ort = GraphicsObject(orts,[0,0,0])
    ort.scaling(5)
    box.scaling(2)
    while(True):
        angle = -time.time()
        #scale = 2+sin(angle)
        box.rotateXYZ(angle,angle,angle)
        box.translate([0, 2 * sin(angle / 2), 0])
        #print(0.5*sin(angle/64))

        #box.scaling(scale)
        pointList = box.draw(camera)


        for i in range(4):
            lineList.append(Line(pointList[i],pointList[(i+1)%4]))
            lineList.append(Line(pointList[i+4], pointList[((i + 1) % 4) + 4]))
            lineList.append(Line(pointList[i], pointList[i + 4]))
        #for i in range(5):
            #lineList.append(Line(pointList[i], pointList[i + 1]))
        #lineList.append(Line(pointList[5], pointList[0]))

        n = len(lineList)

        #for i in range(n//2):
            #lineList[i+6].setWidth(2)
            #lineList[i+6].draw(win)

        for i in range(n//2):
            lineList[i+12].setWidth(4)
            lineList[i+12].draw(win)

        for i in range(n//2):
            (lineList.pop(0)).undraw()

        pointList.clear()

        pOrtlist = ort.draw(camera)

        for item in ortlist:
            item.undraw()
        ortlist.clear()

        ortlist.append(Line(pOrtlist[0],pOrtlist[3]))
        ortlist.append(Line(pOrtlist[1], pOrtlist[3]))
        ortlist.append(Line(pOrtlist[2], pOrtlist[3]))

        

        ortlist[0].setFill('red')
        ortlist[0].setFill('blue')
        ortlist[0].setFill('green')

        for item in ortlist:
            item.draw(win)

        pOrtlist.clear()






if __name__ == '__main__':
    main()
"""
