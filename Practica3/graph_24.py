import random
from typing import Set, List, Generator, Tuple, KeysView, Iterable
import os
from scipy.stats import binom
import sys

sys.setrecursionlimit(2000)

class Graph:
    
    def __init__(self):
        self._V = dict()             # Dictionary with G nodes: Dict[str, Dict[str]] 
        self._E = dict()             # Dictionary with G edges: Dict[str, Set]

    def add_node(self, vertex) -> None:
        if str(vertex) not in self._V:
            self._V[str(vertex)] = dict()
            self._E[str(vertex)] = set()
            self._init_node(vertex)
    
    def add_edge(self, vertex_from, vertex_to) -> None:
        if str(vertex_from) in self._V and str(vertex_to) in self._V:
            self._E[str(vertex_from)].add(str(vertex_to))
   
    def nodes(self) -> KeysView[str]:
        return sorted(self._V.keys())
    
    def nodesint(self) -> KeysView[str]:
        return sorted(self._V.keys(), key=lambda x: int(x))

                      
    def adj(self, vertex) -> Set[str]:
        if str(vertex) not in self._E:
            raise KeyError('Vertex ' + str(vertex) + ' not in graph')
        return sorted(self._E[vertex])

    def exists_edge(self, vertex_from, vertex_to)-> bool:
        if vertex_to in self._E[vertex_from]:
            return True
        else:
            return False
        
    def _init_node(self, vertex) -> None:
        self._V[str(vertex)] = {'color': 'WHITE', 'parent': None, 'd_time': None, 'f_time': None}

    def restart(self) -> None:
        for v in self.nodes():
            self._V[v]['color'] = 'WHITE'
            self._V[v]['parent'] = None
            self._V[v]['d_time'] = None
            self._V[v]['f_time'] = None

    def dfs(self, nodes_sorted: Iterable[str] = None) -> List[List[Tuple]]:
        forest_forest= []
        cont = 0
        if nodes_sorted is None:
            nodes_sorted = self.nodes()
        for node in nodes_sorted:
            if (self._V[node]['color'] == 'WHITE'):
                forest = []
                cont = self.dfs_rec(node, forest, cont)
                forest_forest.append(forest)
            
        return forest_forest
    
    def dfs_rec(self, vertex, path: List[str], cont: int) -> List[Tuple]:
        self._V[vertex]['color'] = 'BLACK'
        cont += 1
        self._V[vertex]['d_time'] = cont
        path.append((vertex, self._V[vertex]['parent']))
        for a in self.adj(vertex):
            if self._V[a]['color'] == 'WHITE':
                self._V[a]['parent'] = vertex
                cont = self.dfs_rec(a, path, cont)
        cont += 1
        self._V[vertex]['f_time'] = cont
        return cont
    
    def tarjan(self) -> List[List[str]]:
        self.restart()
        self.dfs()

        graph_conj = graph_conjugate(self)

        nodes = self.nodes()

        # Ordenar los nodos por tiempo de finalización
        nodes = sorted(nodes, key = lambda x: self._V[x]['f_time'], reverse = True)

        dfs_forest_conj = graph_conj.dfs(nodes)
        scc = []
        for tree in dfs_forest_conj:
            scc.append([])
            for e in tree:
                scc[len(scc)-1].append(e[0])

        return scc


    def __str__(self) -> str:
        ret = ''

        ret += 'Vertices:\n'
        for v in self.nodes():
            ret += str(v) + ': ' + str(self._V[v]) + '\n'

        ret += '\n Aristas:\n'
        for u in self.nodes():
            ret += str(u) + ': ' + str(self._E[u]) + '\n'
        return ret

            
### Auxiliary functions to manage graphs ########
                
def read_adjlist(file: str) -> Graph:
    ''' Read graph in adjacency list format from file.
    '''

    print(f"Files in {os.getcwd()}:")
    print(os.listdir(os.getcwd()))

    G = Graph()
    with open(file,'r') as f:
        for line in f:
            l = line.split()
            if l:           
                u = l[0]
                G.add_node(u)
                for v in l[1:]:
                    G.add_edge(u, v)
    return G
        

def write_adjlist(G: Graph, file: str) -> None:
    '''Write graph G in single-line adjacency-list format to file.
    '''

    file_path = os.path.join(os.path.dirname(__file__), file) 
    with open(file_path,'r') as f:
        for u in G.nodes():
            f.write(f'{u}')
            f.writelines([f' {v}' for v in G.adj(u)])
            f.write('\n')

def graph_conjugate(G: Graph) -> Graph:
    conjGraph = Graph()

    for u in G.nodes():
        conjGraph.add_node(u)

    for u in G.nodes():
        for v in G.adj(u):
            conjGraph.add_edge(v, u)
    
    return conjGraph

def erdos_renyi(n: int, m: float = 1.) -> Graph:

    G = Graph()
    for i in range(n):
        G.add_node(i)

    numVecinos = binom.rvs(n, m/n, size=n)

    for u in G.nodesint():
        choices = list(G.nodesint())
        while numVecinos[int(u)] > 0 and choices:
            v = random.choice(choices)
            choices.remove(v)
            if not G.exists_edge(u, v):
                G.add_edge(u, v)
                numVecinos[int(u)] -= 1

    return G

def size_max_scc(n: int, m: int) -> Tuple[float, float]:

    g = erdos_renyi(n, m)

    componentes_conexas = g.tarjan()
    maximo = max(len(componente) for componente in componentes_conexas)

    return maximo/n, m

def edit_distance(str_1: str, str_2: str) -> int:
    '''
        Calcula la distancia de edición entre dos cadenas
    '''

    m = len(str_1)
    n = len(str_2)

    dp = [[0 for x in range(n+1)] for x in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str_1[i-1] == str_2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

    return dp[m][n]

def max_subsequence_length(str_1: str, str_2: str) -> int:
    '''
        Calcula la longitud de la subsecuencia común más larga
    '''

    m = len(str_1)
    n = len(str_2)

    dp = [[0 for x in range(n+1)] for x in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif str_1[i-1] == str_2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

def max_common_subsequence(str_1: str, str_2: str) -> str:
    '''
        Calcula la subsecuencia común más larga
    '''

    m = len(str_1)
    n = len(str_2)

    dp = [[0 for x in range(n+1)] for x in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif str_1[i-1] == str_2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    index = dp[m][n]

    lcs = [''] * (index+1)
    lcs[index] = ''

    i = m
    j = n
    while i > 0 and j > 0:

        if str_1[i-1] == str_2[j-1]:
            lcs[index-1] = str_1[i-1]
            i -= 1
            j -= 1
            index -= 1

        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    return ''.join(lcs)


def min_mult_matrix(l_dims: List[int]) -> int:
    n = len(l_dims) - 1  # Número de matrices a multiplicar

    if n <= 0:
        return 0
    
    dp = [[0] * n for _ in range(n)]

    # Calcular dp[i][j], que representa el costo mínimo de multiplicar matrices Ai...Aj
    for chain_length in range(2, n + 1):  
        for i in range(n - chain_length + 1):
            j = i + chain_length - 1
            dp[i][j] = float('inf')  
            
            for k in range(i, j):
                # Calcular el costo para dividir en (Ai...Ak) x (Ak+1...Aj)
                cost = dp[i][k] + dp[k + 1][j] + l_dims[i] * l_dims[k + 1] * l_dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)

    # El costo mínimo para multiplicar A1...An está en dp[0][n-1]
    return dp[0][n - 1]

    
### Driver code

if __name__ == '__main__':

    # Pruebas para edit_distance 
    print("Edit Distance:") 
    print(edit_distance("kitten", "sitting"))  
    print(edit_distance("same", "same"))  
    print(edit_distance("", "hello"))  
    print(edit_distance("world", ""))   
    print(edit_distance("", ""))  

    # Pruebas para max_subsequence_length 
    print("\nMax Subsequence Length:") 
    print(max_subsequence_length("ABCD", "ACDF"))  
    print(max_subsequence_length("common", "common"))  
    print(max_subsequence_length("abcd", "efgh"))  
    print(max_subsequence_length("abcd", ""))  
    print(max_subsequence_length("", "efgh"))   

    # Pruebas para max_common_subsequence 
    print("\nMax Common Subsequence:") 
    print(max_common_subsequence("ABCD", "ACDF"))  
    print(max_common_subsequence("common", "common"))
    print(f"Resultado 1: '{max_common_subsequence("abcd", "efgh")}'")  
    print(f"Resultado 2: '{max_common_subsequence("abcd", "")}'") 
    print(f"Resultado 3: '{max_common_subsequence("", "efgh")}'")  
    print()

    # Pruebas básicas con matrices de diferentes tamaños 
    test_cases = [ 
        [10, 20],  # Solo una matriz (no requiere multiplicación) 
        [10, 20, 30],  # Dos matrices (10x20 y 20x30) 
        [10, 20, 30, 40],  # Tres matrices 
        [5, 10, 3, 12, 5, 50],  # Varias matrices 
        [30, 35, 15, 5, 10, 20], # Más complejas 
    ]

    print("Pruebas de min_mult_matrix:") 
    for i, dims in enumerate(test_cases, start=1):
        print(f"Test case {i}: dimensiones {dims}") 
        print(f" Mínimo número de productos: {min_mult_matrix(dims)}") 
        print() 
    
    # Caso límite: ninguna matriz 
    empty_case = [] 
    print("Caso límite (sin matrices):", min_mult_matrix(empty_case)) 
    print()
    
    # Caso límite: una sola matriz 
    single_case = [10] 
    print("Caso límite (una sola matriz):", min_mult_matrix(single_case)) 
    print()
    
    # Caso grande 
    large_case = [10] + [20] * 10 + [30] 
    print("Caso grande:", min_mult_matrix(large_case))
