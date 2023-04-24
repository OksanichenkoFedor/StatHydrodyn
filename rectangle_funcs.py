import config
from numba import njit


@njit()
def is_point_in_rectangle(x, y, R, m, n):
    if (abs(x) < m*R) and (abs(y) < n*R):
        return 1
    elif (abs(x) > m*R) or (abs(y) > n*R):
        return -1
    else:
        return 0


@njit()
def is_cell_on_border_rectangle(i, j, dx, dy, R, a, b):
    a00 = is_point_in_rectangle((i + 0.0) * dx, (j + 0.0) * dy, R, a, b)
    a10 = is_point_in_rectangle((i + 0.0) * dx, (j + 1.0) * dy, R, a, b)
    a01 = is_point_in_rectangle((i + 1.0) * dx, (j + 0.0) * dy, R, a, b)
    a11 = is_point_in_rectangle((i + 1.0) * dx, (j + 1.0) * dy, R, a, b)
    if ((a00 + a10 + a01 + a11) + 4) % 8 != 0:
        return True
    return False



def generate_rectangle():
    X = []
    Y = []
    R = (1.0 * config.N * config.dx) / (2.2)
    m = config.m
    n = config.n
    config.R = R
    for i in range(config.N):
        for j in range(config.N):
            if is_cell_on_border_rectangle(i - config.N / 2, j - config.N / 2, config.dx, config.dx, R, m, n):
                X.append(i)
                Y.append(j)
    config.curr_contur = [X, Y]