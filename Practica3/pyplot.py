import matplotlib.pyplot as plt
from graph_24 import *
import numpy as np

points = []
n = 1000



def grafica(points, file='percolation.png') -> None:
    '''Genera una gráfica en el fichero file'''

    y, x = zip(*points)

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.scatter(x, y, alpha=0.6, s=3)
    ax.set_ylabel (f'Tamaño normalizado mayor scc')
    ax.set_xlabel (f'Valor esperado de vecinos por nodo')
    ax.grid()
    plt.savefig(file)
    #plt.show()

mmax = 6
incr = 0.01
for m in np.arange(0, mmax, incr):
    os.system('clear')
    print(f'Graficando... {((m/mmax)*100):.2f}%\n')
    points.append(size_max_scc(n, m))

grafica(points)