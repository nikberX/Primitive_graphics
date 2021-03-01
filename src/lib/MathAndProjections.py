import numpy as np

def CKM_to_CKH(vertex, origin):
    rows, cols = vertex.shape

    #adds col of ones to right side of matrix
    vertex_ex = np.c_[vertex, np.ones(rows)]

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

    s = np.sqrt(d**2 + origin[2] ** 2)

    if s != 0:
        R_wx = np.array([[1, 0, 0, 0],
                         [0, d / s, -origin[2] / s, 0],
                         [0, origin[2] / s, d / s, 0],
                         [0, 0, 0, 1]])
    else:
        R_wx = np.eye(4)

    V = T @ S @ R_90x @ R_uy @ R_wx

    return (vertex_ex @ V)[:, :cols], s


def CKH_to_CKK_perspective(vertex, s):
    vertexCKK = vertex

    for point in vertexCKK:
        if point[2] != 0:
            point[0] *= s / point[2]
            point[1] *= s / point[2]

    return vertexCKK[:, 0:2]

def CKH_to_CKK_parallel(vertex, s):
    return vertex[:, 0:2]


def CKK_to_CKEi(vertex, pk, xc, yc, xe, ye):
    for point in vertex:
        point[0] *= xe / pk
        point[1] *= -ye / pk
        point[0] += xc
        point[1] += yc

    return vertex