import config
from numba import njit
import numpy as np


@njit()
def is_point_in_circle(x, y, R):
    if x ** 2 + y ** 2 > R ** 2:
        return 1
    elif x ** 2 + y ** 2 < R ** 2:
        return -1
    else:
        return 0


@njit()
def is_cell_on_border_circle(i, j, dx, dy, R):
    a00 = is_point_in_circle((i + 0.0) * dx, (j + 0.0) * dy, R)
    a10 = is_point_in_circle((i + 0.0) * dx, (j + 1.0) * dy, R)
    a01 = is_point_in_circle((i + 1.0) * dx, (j + 0.0) * dy, R)
    a11 = is_point_in_circle((i + 1.0) * dx, (j + 1.0) * dy, R)
    if ((a00 + a10 + a01 + a11) + 4) % 8 != 0:
        return True
    return False


def generate_circle():
    X = []
    Y = []
    R = (1.0 * config.N * config.dx) / (2.2)
    config.R = R
    for i in range(config.N):
        for j in range(config.N):
            if is_cell_on_border_circle(i - config.N / 2, j - config.N / 2, config.dx, config.dx, R):
                X.append(i)
                Y.append(j)
    config.curr_contur = [X, Y]


@njit()
def is_cell_on_border_circle(i, j, dx, dy, R):
    a00 = is_point_in_circle((i + 0.0) * dx, (j + 0.0) * dy, R)
    a10 = is_point_in_circle((i + 0.0) * dx, (j + 1.0) * dy, R)
    a01 = is_point_in_circle((i + 1.0) * dx, (j + 0.0) * dy, R)
    a11 = is_point_in_circle((i + 1.0) * dx, (j + 1.0) * dy, R)
    if ((a00 + a10 + a01 + a11) + 4) % 8 != 0:
        return True
    return False


@njit()
def is_cell_in_circle(i, j, dx, dy, R):
    a00 = is_point_in_circle((i + 0.0) * dx, (j + 0.0) * dy, R)
    a10 = is_point_in_circle((i + 0.0) * dx, (j + 1.0) * dy, R)
    a01 = is_point_in_circle((i + 1.0) * dx, (j + 0.0) * dy, R)
    a11 = is_point_in_circle((i + 1.0) * dx, (j + 1.0) * dy, R)
    if a00 + a10 + a01 + a11 == -4:
        return True
    else:
        return False


@njit()
def is_on_circle(i, j, N, R):
    return is_cell_on_border_circle(i - N / 2, j - N / 2, 1, 1, R=R)


@njit()
def is_in_circle(i, j, N, R):
    return is_cell_in_circle(i - N / 2, j - N / 2, 1, 1, R=R)





@njit()
def step_circle(grid, N, R, C):
    newgrid = grid.copy()

    for i in range(1, newgrid.shape[0] - 1):
        for j in range(1, newgrid.shape[1] - 1):
            ans = 0.25 * (newgrid[i, j + 1] + newgrid[i, j - 1] +
                          newgrid[i + 1, j] + newgrid[i - 1, j]) - 0.25 * C
            if is_in_circle(i, j, N, R):
                newgrid[i, j] = ans
            else:
                newgrid[i, j] = 0

    return newgrid
