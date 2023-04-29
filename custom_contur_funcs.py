import matplotlib.path as mplPath
import config
import numpy as np
from numba import njit
from tqdm.autonotebook import tqdm


def generate_is_in_array():
    curr_custom_is_in = np.zeros((config.N, config.N))
    points = []
    bbPaths = []
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

def custom_generate_is_in_array():
    curr_custom_is_in = np.zeros((config.N, config.N))
    bbPaths = []
    for ind in range(config.number_conturs):
        points = []
        curr_contur = config.curr_contur[ind]
        for i in range(len(curr_contur[0])):
            points.append([curr_contur[0][i], curr_contur[1][i]])

        bbPaths.append(mplPath.Path(points))
    for i in range(config.N):
        for j in range(config.N):
            curr_custom_is_in[i, j] = -1.0
            for ind in range(config.number_conturs):
                if bbPaths[ind].contains_point([i, j]):
                    curr_custom_is_in[i, j] = 1.0
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


def generate_unordered_contur_array():
    for ind in range(config.number_conturs):
        new_contur = [[], []]

        points = []
        for j in range(len(config.curr_contur[ind][0])):
            points.append([config.curr_contur[ind][0][j], config.curr_contur[ind][1][j]])
        for j in range(len(points) - 1):
            x1, y1 = points[j]
            x2, y2 = points[j + 1]
            newX, newY = make_segment(x1, y1, x2, y2)
            new_contur[0] = new_contur[0] + newX
            new_contur[1] = new_contur[1] + newY
        x1, y1 = points[-1]
        x2, y2 = points[0]
        newX, newY = make_segment(x1, y1, x2, y2)
        new_contur[0] = new_contur[0] + newX[:-1]
        new_contur[1] = new_contur[1] + newY[:-1]

        config.curr_contur[ind] = np.array(new_contur)


@njit()
def is_cell_in_line(x1, y1, x2, y2, x3, y3):
    a00 = is_point_in_line(x1, y1, x2, y2, x3 + 0, y3 + 0)
    a10 = is_point_in_line(x1, y1, x2, y2, x3 + 1, y3 + 0)
    a01 = is_point_in_line(x1, y1, x2, y2, x3 + 0, y3 + 1)
    a11 = is_point_in_line(x1, y1, x2, y2, x3 + 1, y3 + 1)
    if ((a00 + a10 + a01 + a11) + 4) % 8 != 0:
        return True
    return False


@njit()
def is_point_in_line(x1, y1, x2, y2, x3, y3):
    d = (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)
    if d > 0:
        return 1
    if d < 0:
        return -1
    return 0


def make_segment(x1, y1, x2, y2):
    curr_arr_x = [x1]
    curr_arr_y = [y1]
    curr_x = x1
    curr_y = y1
    x_vec = 1
    if x1 > x2:
        x_vec = -1
    y_vec = 1
    if y1 > y2:
        y_vec = -1
    reached_x = False
    if x1 == x2:
        reached_x = True
    reached_y = False
    if y1 == y2:
        reached_y = True
    while not (reached_x and reached_y):
        if not reached_x:
            if is_cell_in_line(x1, y1, x2, y2, curr_x + x_vec, curr_y):
                curr_arr_x.append(curr_x + x_vec)
                curr_arr_y.append(curr_y)
                if curr_x + x_vec == x2:
                    reached_x = True
                curr_x = curr_x + x_vec
            else:
                curr_arr_x.append(curr_x)
                curr_arr_y.append(curr_y + y_vec)
                if curr_y + y_vec == y2:
                    reached_y = True
                curr_y = curr_y + y_vec
        else:
            curr_arr_x.append(curr_x)
            curr_arr_y.append(curr_y + y_vec)
            if curr_y + y_vec == y2:
                reached_y = True
            curr_y = curr_y + y_vec
    return (curr_arr_x, curr_arr_y)


@njit()
def step_custom(grid, C, is_in_arr=np.array([[]])):
    newgrid = grid.copy()

    for i in range(1, newgrid.shape[0] - 1):
        for j in range(1, newgrid.shape[1] - 1):
            ans = 0.25 * (newgrid[i, j + 1] + newgrid[i, j - 1] +
                          newgrid[i + 1, j] + newgrid[i - 1, j]) - 0.25 * C
            newgrid[i, j] = is_in_arr[i, j] * ans

    return newgrid
