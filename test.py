import matplotlib.path as mplPath
import numpy as np
from numba import *
@njit()
def is_cell_in_custom(i=0, j=0, N=0, is_in_arr=np.array([[]])):
    a00 = is_in_arr[i + 0, j + 0]
    a10 = is_in_arr[i + 0, j + 1]
    a01 = is_in_arr[i + 1, j + 0]
    a11 = is_in_arr[i + 1, j + 1]
    #a00 = is_in_arr[i + 0 - N / 2, j + 0 - N / 2]
    #a10 = is_in_arr[i + 0 - N / 2, j + 1 - N / 2]
    #a01 = is_in_arr[i + 1 - N / 2, j + 0 - N / 2]
    #a11 = is_in_arr[i + 1 - N / 2, j + 1 - N / 2]
    if a00 + a10 + a01 + a11 == -4:
        return True
    else:
        return False

def is_in_custom(i, j, N, is_in_arr=np.array([[]])):
    return is_cell_in_custom(i - N / 2, j - N / 2, is_in_arr)

print(is_cell_in_custom(6-0,6-0,0,np.zeros((10,10))))


