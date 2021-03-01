from numpy import matrix
from math import (sin,cos)
rotationZ = lambda angle: matrix(
        [
            [cos(angle),-sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [         0,          0, 1, 0],
            [         0,          0, 0, 1]
        ]
    )

rotationX = lambda angle: matrix(
        [
            [1,          0,          0, 0],
            [0, cos(angle),-sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0,          0,          0, 1]
        ]
    )

rotationY = lambda angle: matrix(
        [
            [cos(angle),  0,-sin(angle), 0],
            [         0,  1,          0, 0],
            [sin(angle),  0, cos(angle), 0],
            [         0,  0,          0, 1]
        ]
    )

translate = lambda pos: matrix(
        [
            [1, 0, 0, pos[0]],
            [0, 1, 0, pos[1]],
            [0, 0, 1, pos[2]],
            [0, 0, 0,      1]
        ]
)

scale = lambda size: matrix(
    [
            [size,    0,    0, 0],
            [   0, size,    0, 0],
            [   0,    0, size, 0],
            [   0,    0,    0, 1]
    ]
)

orthoMatrix = lambda scale: matrix(
    [
    [scale,    0.0,  0.0,  0.0],
    [  0.0,  scale,  0.0,  0.0],
    [  0.0,    0.0,  0.0,    1]
    ]
)

vec4 = lambda pos: matrix(
            [
                [pos[0]],
                [pos[1]],
                [pos[2]],
                [1]
            ]
)