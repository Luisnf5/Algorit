import heap_mod as heap
import random
import time
import itertools

#=======================================CONJUNTOS DISJUNTOS=======================================

def ds_init(n):
    p = []
    for _ in range(n):
        p.append(-1)
    return p

#=======================================FUNCION UNION=======================================

#FUNCION UNION POR ALTURA
def ds_union(p_ds, rep_1, rep_2):

    x = rep_1
    y = rep_2

    if rep_1 > 0 or rep_2 > 0:
        return None

    if x == y:
        return None
    if p_ds[y] < p_ds[x]:            #El arbol y es más alto
        p_ds[x] = y
        return y
    elif p_ds[x] < p_ds[y]:          #El arbol x es más alto
        p_ds[y] = x
        return x
    else:                            #Los dos son de la misma altura
        p_ds[y] = x
        p_ds[x] -= 1                 #Se incrementa en uno la altura del arbol
        return x

#=======================================FUNCION FIND=======================================

#FUNCION FIND RECURSIVA
def ds_find(p_ds, m):
    z = m

    while p_ds[z] >= 0:
        z = p_ds[z]
    
    while p_ds[m] >= 0:
        y = p_ds[m]
        p_ds[m] = z
        m = y

    return z

#=======================================COMPONENTES CONEXAS=======================================
def connected(n, e):

    p = ds_init(n)              #Inicializamos los conjuntos disjuntos
    for (u, v) in e:            #Recorremos la lista de arcos
        ds_union(p, ds_find(p, u), ds_find(p, v))  #Unimos los conjuntos disjuntos
    return p

def connected_count(p):

    count = 0
    #Por cada elemento en p
    for i in p:
        if i < 0:                   #Si es menor que 0, significa que es raiz
            count +=1               #Se suma al contador
    return count

def connected_sets(p):

    componente = {}
    for u in range(len(p)):         #Recorremos todos los elementos de p
        v = ds_find(p, u)           #obtenemos la raiz
        if v not in componente:     #si la razi no esta en el diccionario se crea una lista
            componente[v] = []
        componente[v].append(u)     #Se añade el elemento a su raiz(componente) correspodiente
    #componente.values() devuelve todos los valores en el diccionario
    return list(componente.values())  

"""lst = [(1,4), (3,4), (2,5)]
s = connected(6, lst)
n = connected_count(s)
ccp = connected_sets(s)

print(n)
print(ccp)"""

#=======================================GRAFOS=======================================

def kruskal(n, E):
    mst = []  # Lista para el árbol de expansión mínima
    p_ds = ds_init(n)  # Inicializamos los conjuntos disjuntos
    arcos = heap.pq_ini()
    aux = ()

    for (u, v, w) in E:
        p = (w, u, v)  # La prioridad es el peso del arco y los nodos en orden lexicográfico
        heap.pq_insert(arcos, ((u, v, w), p))

    while len(mst) < n - 1 and len(arcos) > 0:
        arcos, aux = heap.pq_extract(arcos)  # Extraemos el arco con el menor peso
        u, v, w = aux[0]
        if ds_find(p_ds, u) != ds_find(p_ds, v):
            ds_union(p_ds, ds_find(p_ds, u), ds_find(p_ds, v))
            mst.append((u, v, w))

    if len(mst) != n - 1:
        return None  # Si no se han añadido n-1 arcos, el grafo no es conexo y no tiene árbol abarcador

    return n, mst
    

def k_weight(n, E):
    suma = 0

    for i in range(n-1):
        suma+=E[i][2]

    return suma

"""E = [(0, 1, 10), (0, 3, 3), (1, 2, 1), (2, 3, 1), (2, 5, 1), (3, 4, 10), (4, 5, 1)]
n = 6
n_k, E_k = kruskal(n, E)
print(E_k)
print(k_weight(n_k, E_k))"""


def erdos_conn(n, m):
    '''n grafo de Erd¨os-Renyi ponderados y modificado por conexion es un grafo aleatorio con n nodos en que cada
nodo tiene en media m vecinos (n y m son los parametros que definen el grafo). En nuestro grafo consideraremos
solo pesos contenidos en el intervalo [0, 1]. El grafo se genera con el metodo siguiente:
i) Se crea una lista de arcos vacia
ii) para i = 0, . . . , (n - 1), se elige un nodo aleatorio en el intervalo [0, i - 1] (sea m este nodo) , se genera un
peso aleatorio w y se crea un arco (i, m, w) (estos arcos garantizan que el grafo final es conexo)

ii) Para i = 0, . . . n x (m - 1) - 1 se eligen dos nodos aleatorios u, v que todavia no estan conectado, se genera
un peso aleatorio w, y se añade el arco (u, v, w) a la lista de arcos.
Se escriba una funcion
erdos conn(n, m)
que, dado los parametros n y m construya el grafo aleatorio y devuelva la lista de arcos'''

    p = ds_init(n)
    arcos = []
    for i in range(n):
        if i == 0:
            m = 0
        else:
            m = random.randint(0, i-1)
        w = random.randint(0, 1)
        arcos.append((i, m, w))
        ds_union(p, ds_find(p, i), ds_find(p, m))

      # Inicializamos los conjuntos disjuntos para comprobar conexiones

    for i in range(n*(m - 1)):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        
        # Si no estan conectados, seguir el bucle generando el peso y añadiendo la conexion
        if (ds_find(p, u) == ds_find(p, v)):
            continue
        
        w = random.randint(0, 1)

        if (u, v, w) in arcos or (v, u, w) in arcos:
            continue
        arcos.append((u, v, w))
        ds_union(p, ds_find(p, u), ds_find(p, v))  # Unimos los conjuntos disjuntos

    return arcos

#print(erdos_conn(10, 3))

def time_kruskal(n, m, n_graphs):
    
    times = []
    for _ in range(n_graphs):
        E = erdos_conn(n, m)
        start = time.perf_counter()
        kruskal(n, E)
        end = time.perf_counter()
        times.append(end-start)

    media = sum(times)/n_graphs
    varianza = sum((i-media)**2 for i in times) / n_graphs

    return media, varianza

#print(time_kruskal(12, 2, 1000))

def dist_matrix(n_cities, w_max = 10):
    M = [ [ random.uniform(0, w_max) for _ in range(n_cities)] for _ in range(n_cities) ]
    for k in range(n_cities):
        M[k][k] = 0
        for h in range(k):
            u = (M[k][h] + M[h][k])/2.0
            M[h][k] = M[k][h] = u
    return M

def greedy_tsp(dist_m, node_ini):

    visited = [node_ini]
    act_node = node_ini

    if (node_ini > len(dist_m)-1):
        return None

    while len(visited) < len(dist_m):
        min_dist = float('inf')
        for i in range(len(dist_m)):
            if dist_m[act_node][i] < min_dist and i not in visited:
                min_dist = dist_m[act_node][i]
                next_node = i
            else:
                continue
        visited.append(next_node)
        act_node = next_node

    visited.append(node_ini)

    return visited

#print(greedy_tsp(dist_matrix(5), 0))

def len_circuit(circuit, dist_m):
    suma = 0

    for i in range(len(circuit)-1):
        suma += dist_m[circuit[i]][circuit[i+1]]

    return suma

def repeated_greedy_tsp(dist_m):

    best_circuit = []
    act_circuit = []
    best_len = float('inf')
    act_len = float('inf')

    for i in range(len(dist_m)):
        act_circuit = greedy_tsp(dist_m, i)
        act_len = len_circuit(act_circuit, dist_m)

        if act_len < best_len:
            best_len = act_len
            best_circuit = act_circuit

    return best_circuit

def exhaustive_tsp(dist_m):

    best_circuit = []
    act_circuit = []
    best_len = float('inf')
    act_len = float('inf')

    for perm in itertools.permutations(range(len(dist_m))):
        act_circuit += perm
        act_circuit.append(perm[0])

        act_len = len_circuit(act_circuit, dist_m)

        if act_len < best_len:
            best_len = act_len
            best_circuit.clear()
            best_circuit.extend(act_circuit)
        
        act_circuit.clear()

    return best_circuit

#=======================================EXTRA=======================================

def permute(lst): 
    act_list = []

    if len(lst) == 1:
        return [lst]

    res = []

    for i in range(len(lst)):
        ele = lst[i]

        restante = lst[:i] + lst[i+1:]

        for p in permute(restante):
            act_list.append(ele)
            act_list.extend(p)
            res.append(act_list)
            act_list = []

    return res

'''
Para crear todas las permutaciones de una lista podemos coger cada elemento de la lista mas todas las permutaciones de la lista restante.

Al hacer esto con todos los elementos tenemos todas las permutaciones posibles.

Ejemplo: Para la lista [1, 2, 3] podemos hacer (1 + permutaciones([2, 3]) +  (2 + permutaciones([1, 3])) + (3 + permutaciones([1, 2])).
'''
    

