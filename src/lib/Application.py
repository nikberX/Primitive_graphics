import tkinter as tk
from EventHandler import EventHandler

class Application:
    def __init__(self,height,width,name = 'App',bg_color = 'white'):
        self._height = height
        self._width = width
        self._appName = name
        self._bg_color = bg_color

        self._root = tk.Tk()
        self._window = tk.Canvas(self._root, width=self._width, height=self._height, bg=self._bg_color)
        self._root.title(self._appName)
        self.eventHandler = None


    def getRoot(self):
        return self._root

    def getCanvas(self):
        return self._window

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def setEventHandler(self,handler):
        if (isinstance(handler,EventHandler)):
            self.eventHandler = handler
        else:
            raise TypeError

    def mainloop(self):
        if (isinstance(self.eventHandler,EventHandler)):
            while True:
                self.eventHandler.update()
                self._root.update_idletasks()
                self._root.update()

        else:
            print("Error: No event handler set")

    def bindEvent(self,eventName,eventFunction):
        self._root.bind(eventName, eventFunction)
