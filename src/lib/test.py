import tkinter as tk
import numpy as np

h = 600
w = 1200
root = tk.Tk()
cv = tk.Canvas(root, width=1200, height=600, bg='white')



cv.pack()

cv.create_polygon(10,10,100,100,20,30,fill = 'black')


root.mainloop()
