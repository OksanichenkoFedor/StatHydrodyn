import matplotlib.path as mplPath
import config
import numpy as np
from numba import njit


def generate_is_in_array():
    curr_custom_is_in = np.zeros((config.N, config.N))
    points = []
    curr_contur = config.curr_contur
    for i in range(len(curr_contur[0])):
        points.append([curr_contur[0][i], curr_contur[1][i]])
    bbPath = mplPath.Path(points)
    for i in range(config.N):
        for j in range(config.N):
            curr_custom_is_in[i, j] = 2.0 * float(bbPath.contains_point([i, j])) - 1
    curr_custom_is_in = curr_custom_is_in.astype(np.float64)
    arr = np.zeros((config.N, config.N))
    for i in range(config.N):
        for j in range(config.N):
            if (((i != 0) and (i != (config.N - 1))) and (j != 0 and j != (config.N - 1))):
                a00 = curr_custom_is_in[i + 0, j + 0]
                a10 = curr_custom_is_in[i + 0, j + 1]
                a01 = curr_custom_is_in[i + 1, j + 0]
                a11 = curr_custom_is_in[i + 1, j + 1]
                if a00 + a10 + a01 + a11 > -3.5:
                    arr[i, j] = 1
                else:
                    arr[i, j] = 0
    config.curr_custom_is_in = arr.astype(np.int64)


@njit()
def step_custom(grid, C, is_in_arr=np.array([[]])):
    newgrid = grid.copy()

    for i in range(1, newgrid.shape[0] - 1):
        for j in range(1, newgrid.shape[1] - 1):
            ans = 0.25 * (newgrid[i, j + 1] + newgrid[i, j - 1] +
                          newgrid[i + 1, j] + newgrid[i - 1, j]) - 0.25 * C
            newgrid[i, j] = is_in_arr[i, j] * ans

    return newgrid
