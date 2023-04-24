import config
from numba import njit


@njit()
def is_point_in_eclipse(x, y, R, a, b):
    if (a*x) ** 2 + (b*y) ** 2 > R ** 2:
        return 1
    elif (a*x) ** 2 + (b*y) ** 2 < R ** 2:
        return -1
    else:
        return 0


@njit()
def is_cell_on_border_eclipse(i, j, dx, dy, R, a, b):
    a00 = is_point_in_eclipse((i + 0.0) * dx, (j + 0.0) * dy, R, a, b)
    a10 = is_point_in_eclipse((i + 0.0) * dx, (j + 1.0) * dy, R, a, b)
    a01 = is_point_in_eclipse((i + 1.0) * dx, (j + 0.0) * dy, R, a, b)
    a11 = is_point_in_eclipse((i + 1.0) * dx, (j + 1.0) * dy, R, a, b)
    if ((a00 + a10 + a01 + a11) + 4) % 8 != 0:
        return True
    return False



def generate_eclipse():
    X = []
    Y = []
    R = (1.0 * config.N * config.dx) / (2.2)
    a = config.a
    b = config.b
    config.R = R
    for i in range(config.N):
        for j in range(config.N):
            if is_cell_on_border_eclipse(i - config.N / 2, j - config.N / 2, config.dx, config.dx, R, a, b):
                X.append(i)
                Y.append(j)
    config.curr_contur = [X, Y]
