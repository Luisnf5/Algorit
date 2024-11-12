from typing import Set, List, Generator, Tuple, KeysView, Iterable
import os

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
        ''' 
        Depth find search driver
    
            nodes_sorted: Si se le pasa un iterable el bucle principal de DFS
            se iterará según el orden del iterable (eg en Tarjan)
        
            Devuelve un bosque dfs en la que cada una de las sublistas es un
            árbol dfs. Cada elemnto del arbol es una tupla (vertex, parent)
        '''
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


    
### Driver code

if __name__ == '__main__':
    G = read_adjlist('./graph.txt')
    print(G)

