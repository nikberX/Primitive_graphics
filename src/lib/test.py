import tkinter as tk
import numpy as np

h = 400
w = 400
root = tk.Tk()
cv = tk.Canvas(root, width=400, height=400, bg='black')


def CKM_to_CKH(vertex, origin):
    n = vertex.shape[0]
    m = vertex.shape[1]

    vertex_ex = np.c_[vertex, np.ones(n)]

    T = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [-origin[0], -origin[1], -origin[2], 1]])

    S = np.array([[-1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

    R_90x = np.array([[1, 0, 0, 0],
                      [0, 0, -1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

    d = np.sqrt(origin[0] ** 2 + origin[1] ** 2)

    if d != 0:
        R_uy = np.array([[origin[1] / d, 0, origin[0] / d, 0],
                         [0, 1, 0, 0],
                         [-origin[0] / d, 0, origin[1] / d, 0],
                         [0, 0, 0, 1]])
    else:
        R_uy = np.eye(4)

    s = np.sqrt(origin[0] ** 2 + origin[1] ** 2 + origin[2] ** 2)

    if s != 0:
        R_wx = np.array([[1, 0, 0, 0],
                         [0, d / s, -origin[2] / s, 0],
                         [0, origin[2] / s, d / s, 0],
                         [0, 0, 0, 1]])
    else:
        R_wx = np.eye(4)

    V = T @ S @ R_90x @ R_uy @ R_wx

    return (vertex_ex @ V)[:, :3], s


def CKH_to_CKK(vertex, s):
    vertexCKK = vertex

    # for point in vertexCKK:
    #    if point[2] != 0:
    #        point[0] *= s / point[2]
    #        point[1] *= s / point[2]

    for point in vertexCKK:
        if point[2] != 0:
            point[0] *= 1.5
            point[1] *= 1.5

    return vertexCKK[:, 0:2]


def CKK_to_CKEi(vertex, pk, xc, yc, xe, ye):
    for point in vertex:
        point[0] *= xe / pk
        point[1] *= -ye / pk
        point[0] += xc
        point[1] += yc

    return vertex


class Watcher:
    def __init__(self, WatcherPoint):
        self.x = WatcherPoint[0]
        self.y = WatcherPoint[1]
        self.z = WatcherPoint[2]
        self.lines = []
        self.verticies = []

        cv.pack()

        def key(event):
            if event.char == 'w':
                y = self.y
                z = self.z
                cos = 0.99995
                sin = 0.00999983
                self.move(event, [0, (y * cos - z * sin) - self.y, (y * sin + z * cos) - self.z])
            elif event.char == 's':
                y = self.y
                z = self.z
                cos = 0.99995
                sin = -0.00999983
                self.move(event, [0, (y * cos - z * sin) - self.y, (y * sin + z * cos) - self.z])
            elif event.char == 'd':
                if self.m < self.n:
                    self.m += 1
                    self.update()
            elif event.char == 'a':
                if self.m > 0:
                    self.m -= 1
                    self.update()

        root.bind("<Key>", lambda event: key(event))

        self.s = None
        self.xmin = -2 * np.pi
        self.xmax = 2 * np.pi
        self.n = 40
        self.dx = (self.xmax - self.xmin) / self.n
        self.zmin = -2 * np.pi
        self.zmax = 2 * np.pi
        self.dz = (self.zmax - self.zmin) / self.n

        self.vids = np.zeros((self.n, self.n))

        self.up = np.zeros(w)
        self.down = np.repeat(h, w)

        self.m = self.n

        # функция от х и z
        def func(x, z):
            return 1.5 * np.cos((x ** 2 + z ** 2) ** 0.5)
            #return x*x+z*z
            #return abs(x)+abs(z)

        max_v = -1e6

        for z in np.arange(self.zmin, self.zmax, self.dz):
            for x in np.arange(self.xmin, self.xmax, self.dx):
                point = np.array([x, func(x, z), z])
                self.verticies.append(point)
                if (abs(point[1]) > max_v):
                    max_v = abs(point[1])

        points = np.reshape(self.verticies, (self.n, self.n, 3))

        dc = 255.0 / max_v

        self.verticies = np.array(self.verticies)

        self.M = self.verticies
        self.M, self.s = CKM_to_CKH(self.M, [self.x, self.y, self.z])
        self.M = CKH_to_CKK(self.M, self.s)
        self.M = CKK_to_CKEi(self.M, 10, w / 2, h / 2, 200, 200)
        self.M = np.reshape(self.M, (self.n, self.n, 2))

        self.update()

    def move(self, event, d):
        self.x += d[0]
        self.y += d[1]
        self.z += d[2]
        self.M = self.verticies
        self.M, self.s = CKM_to_CKH(self.M, [self.x, self.y, self.z])
        self.M = CKH_to_CKK(self.M, self.s)
        self.M = CKK_to_CKEi(self.M, 10, w / 2, h / 2, 200, 200)
        self.M = np.reshape(self.M, (self.n, self.n, 2))

        self.update()

    def update(self):

        cv.delete('all')

        self.up = np.zeros(w)
        self.down = np.repeat(h, w)
        # признак видимости точки
        def vis_state(point):
            ind = int(point[0])
            if point[1] < self.up[ind] and point[1] > self.down[ind]:
                return 0
            elif point[1] >= self.up[ind]:
                return 1
            elif point[1] <= self.down[ind]:
                return 2

        for i in range(self.m):

            self.vids[i][0] = vis_state(self.M[i][0])

            for j in range(1, self.n):

                self.vids[i][j] = vis_state(self.M[i][j])
                vid_t = self.vids[i][j - 1]
                vid_p = self.vids[i][j]

                fir_p = self.M[i][j - 1]
                sec_p = self.M[i][j]

                # случаи когда видна вся линия
                case_1 = vid_t == 1 and vid_p == 1
                case_2 = vid_t == 2 and vid_p == 2

                if case_1 or case_2:

                    dx = (fir_p[0] - sec_p[0])
                    dy = (sec_p[1] - fir_p[1])
                    # THIS.  IS.  m
                    step_y = dy / dx
                    sec_p = np.copy(fir_p)

                    if case_1:
                        for k in range(int(dx) + 1):
                            ind = int(sec_p[0])
                            self.up[ind] = sec_p[1]
                            if i == 0:
                                self.down[ind] = sec_p[1]
                            sec_p[0] -= 1
                            sec_p[1] += step_y
                    else:
                        for k in range(int(dx) + 1):
                            ind = int(sec_p[0])
                            self.down[ind] = sec_p[1]
                            if i == 0:
                                self.up[ind] = sec_p[1]
                            sec_p[0] -= 1
                            sec_p[1] += step_y

                    if case_1:
                        cv.create_line(fir_p[0], fir_p[1], sec_p[0], sec_p[1], fill='red')
                    else:
                        cv.create_line(fir_p[0], fir_p[1], sec_p[0], sec_p[1], fill='green')

                else:

                    # если видна вторая точка, а не первая, то достаточно их
                    # поменять местами
                    if vid_p > 0:
                        vid_t, vid_p = vid_p, vid_t
                        fir_p, sec_p = sec_p, fir_p

                    if vid_t > 0:
                        if fir_p[0] == sec_p[0]:
                            if vid_t == 1:
                                sec_p[1] = self.up[fir_p[0]]
                                self.up[fir_p[0]] = fir_p[1]
                            else:
                                sec_p[1] = self.down[fir_p[0]]
                                self.down[fir_p[0]] = fir_p[1]
                        else:
                            dx = (sec_p[0] - fir_p[0])
                            dy = (sec_p[1] - fir_p[1])
                            step_x = np.sign(dx)
                            # this is m
                            step_y = dy / abs(dx)
                            sec_p = np.copy(fir_p)

                            if vid_t == 1:
                                self.up[int(sec_p[0])] = sec_p[1]
                                sec_p[0] += step_x
                                sec_p[1] += step_y

                                ind = int(sec_p[0])
                                while sec_p[1] - 1.5 >= self.up[ind]:
                                    self.up[ind] = sec_p[1]
                                    sec_p[0] += step_x
                                    sec_p[1] += step_y
                                    ind = int(sec_p[0])
                            else:
                                self.down[int(sec_p[0])] = sec_p[1]
                                sec_p[0] += step_x
                                sec_p[1] += step_y

                                ind = int(sec_p[0])
                                while sec_p[1] + 1.5 <= self.down[ind]:
                                    self.down[ind] = sec_p[1]
                                    sec_p[0] += step_x
                                    sec_p[1] += step_y
                                    ind = int(sec_p[0])

                        cv.create_line(fir_p[0], fir_p[1], sec_p[0], sec_p[1], fill='yellow')




watcher = Watcher([0, 0, -5])
root.mainloop()