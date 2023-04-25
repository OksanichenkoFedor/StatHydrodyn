import numpy as np
import time
import config
from custom_contur_funcs import step_custom

from numba import njit


@njit()
def boundary(grid):
    x = np.linspace(0, 1, len(grid))

    grid[0, :] = 0
    grid[:, -1] = 0
    grid[-1, :] = 0
    grid[:, 0] = 0


@njit()  # Начальная случайная сетка
def initgrid(gridsize):
    x = np.random.randn(gridsize, gridsize)
    boundary(x)

    return x


def count(progress_bar, progress_txt, progress_var, num_iters=10):
    config.iter_time = []
    x = initgrid(config.N)
    config.curr_x = x
    curr_flow = count_flow()
    num = 0
    is_in_custom = config.curr_custom_is_in
    for i in range(num_iters):

        curr_flow = config.curr_flow
        num += 1
        start = time.time()
        # x = step_circle(x, config.N, config.R, config.C)
        x = step_custom(x, config.C, is_in_custom)
        end = time.time()
        config.iter_time.append(end - start)
        config.curr_x = x
        count_flow()

        delta = np.abs(curr_flow - count_flow())
        if i == 0:
            initial_delta = int(1000.0 * np.log(delta) / np.log(10.0))
            #print(initial_delta)
            maximum = max(0, initial_delta - int(1000 * config.poss_err))
            progress_bar["maximum"] = maximum

        num_points = 0
        if int(np.log(delta) / np.log(10.0)) < 0:
            num_points = -int(np.log(delta) / np.log(10.0))+2
        progress_txt.set("Delta: " + str(round(delta, num_points)))
        progress_var.set(min(maximum, initial_delta - int(1000 * np.log(delta) / np.log(10.0))))
        #print(min(maximum, initial_delta - int(1000 * np.log(delta) / np.log(10.0))))
        #print("---")
        #print(maximum)
        progress_bar.update()

        # print(delta)

    while np.abs(curr_flow - count_flow()) > 10.0 ** config.poss_err:
        curr_flow = config.curr_flow
        num += 1
        start = time.time()
        # x = step_circle(x, config.N, config.R, config.C)
        x = step_custom(x, config.C, is_in_custom)
        end = time.time()
        config.iter_time.append(end - start)
        config.curr_x = x
        count_flow()

        delta = np.abs(curr_flow - count_flow())
        num_points = 0
        if int(np.log(delta) / np.log(10.0)) < 0:
            num_points = -int(np.log(delta) / np.log(10.0))+2
        progress_txt.set("Delta: " + str(round(delta, num_points)))
        progress_var.set(min(maximum, initial_delta - int(1000 * np.log(delta) / np.log(10.0))))
        #print(min(maximum, initial_delta - int(1000 * np.log(delta) / np.log(10.0))))
        #print("---")
        #print(maximum)
        progress_bar.update()

    #print(num)
    #print(np.array(config.iter_time).mean())
    config.num_iter = num


def count_flow():
    config.curr_flow = config.curr_x.sum()
    return config.curr_flow
