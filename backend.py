import config
from numba import njit
import numpy as np

def contur_ordering():
    X = config.curr_contur[0]
    Y = config.curr_contur[1]
    print("len X:",len(X))
    way = []
    ib = 0
    a = 0
    n = len(X)
    M = np.zeros([n, n])  # Шаблон матрицы относительных расстояний между пунктами
    for i in np.arange(0, n, 1):
        for j in np.arange(0, n, 1):
            if i != j:
                M[i, j] = np.sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)  # Заполнение матрицы
            else:
                M[i, j] = float('inf')  # Заполнение главной диагонали матрицы
    way.append(ib)
    for i in np.arange(1, n, 1):
        s = []
        for j in np.arange(0, n, 1):
            s.append(M[way[i - 1], j])
        way.append(s.index(min(s)))  # Индексы пунктов ближайших городов соседей
        for j in np.arange(0, i, 1):
            M[way[i], way[j]] = float('inf')
            M[way[i], way[j]] = float('inf')
    S = sum([np.sqrt((X[way[i]] - X[way[i + 1]]) ** 2 + (Y[way[i]] - Y[way[i + 1]]) ** 2) for i in
             np.arange(0, n - 1, 1)]) + np.sqrt((X[way[n - 1]] - X[way[0]]) ** 2 + (Y[way[n - 1]] - Y[way[0]]) ** 2)
    X1 = [X[way[i]] for i in np.arange(0, n, 1)]
    Y1 = [Y[way[i]] for i in np.arange(0, n, 1)]
    config.curr_contur = [X1, Y1]


