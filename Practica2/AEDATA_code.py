import heap_mod as heap
import random
import time
import itertools

#=======================================CONJUNTOS DISJUNTOS=======================================

def ds_init(n):
    # Inicializa un conjunto disjunto con n elementos, cada uno representado por -1
    p = []
    for _ in range(n):
        p.append(-1)
    return p

#=======================================FUNCION UNION=======================================

#FUNCION UNION POR ALTURA
def ds_union(p_ds, rep_1, rep_2):
    # Une dos conjuntos disjuntos por altura
    x = rep_1
    y = rep_2

    if x == y:
        return None
    if p_ds[y] < p_ds[x]:            # El árbol y es más alto
        p_ds[x] = y
        return y
    elif p_ds[x] < p_ds[y]:          # El árbol x es más alto
        p_ds[y] = x
        return x
    else:                            # Los dos son de la misma altura
        p_ds[y] = x
        p_ds[x] -= 1                 # Se incrementa en uno la altura del árbol
        return x

#=======================================FUNCION FIND=======================================

#FUNCION FIND CON COMPRESIÓN
def ds_find(p_ds, m):
    # Encuentra el representante del conjunto al que pertenece el elemento m
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
    # Determina los conjuntos conexos en un grafo
    p = ds_init(n)              # Inicializamos los conjuntos disjuntos
    for (u, v) in e:            # Recorremos la lista de arcos
        if ds_union(p, ds_find(p, u), ds_find(p, v)) is None:
            continue  # Si la unión falla, continuar con el siguiente arco
    return p

def connected_count(p):
    # Cuenta el número de componentes conexas
    count = 0
    # Por cada elemento en p
    for i in p:
        if i < 0:                   # Si es menor que 0, significa que es raíz
            count +=1               # Se suma al contador
    return count

def connected_sets(p):
    # Devuelve una lista de conjuntos conexos
    componente = {}
    for u in range(len(p)):         # Recorremos todos los elementos de p
        v = ds_find(p, u)           # Obtenemos la raíz
        if v not in componente:     # Si la raíz no está en el diccionario se crea una lista
            componente[v] = []
        componente[v].append(u)     # Se añade el elemento a su raíz (componente) correspondiente
        
    return list(componente.values())  



#=======================================GRAFOS=======================================

def kruskal(n, E):
    # Algoritmo de Kruskal para encontrar el árbol de expansión mínima
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
    # Calcula el peso total del árbol de expansión mínima
    suma = 0

    for i in range(n-1):
        suma+=E[i][2]

    return suma

def erdos_conn(n, m):
    # Genera un grafo aleatorio utilizando el modelo de Erdős-Rényi
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
        
        # Si no están conectados, seguir el bucle generando el peso y añadiendo la conexión
        if (ds_find(p, u) == ds_find(p, v)):
            continue
        
        w = random.randint(0, 1)

        if (u, v, w) in arcos or (v, u, w) in arcos:
            continue
        arcos.append((u, v, w))
        ds_union(p, ds_find(p, u), ds_find(p, v))  # Unimos los conjuntos disjuntos

    return arcos

def time_kruskal(n, m, n_graphs):
    # Mide el tiempo de ejecución del algoritmo de Kruskal en varios grafos
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

def dist_matrix(n_cities, w_max = 10):
    # Genera una matriz de distancias aleatorias entre ciudades
    M = [ [ random.uniform(0, w_max) for _ in range(n_cities)] for _ in range(n_cities) ]
    for k in range(n_cities):
        M[k][k] = 0
        for h in range(k):
            u = (M[k][h] + M[h][k])/2.0
            M[h][k] = M[k][h] = u
    return M

def greedy_tsp(dist_m, node_ini):
    # Algoritmo voraz para resolver el problema del viajante
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

def len_circuit(circuit, dist_m):
    # Calcula la longitud total de un circuito dado
    suma = 0

    for i in range(len(circuit)-1):
        suma += dist_m[circuit[i]][circuit[i+1]]

    return suma

def repeated_greedy_tsp(dist_m):
    # Algoritmo codicioso repetido para resolver el problema del viajante
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
    # Algoritmo exhaustivo para resolver el problema del viajante
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

def times_kruskal_erdos(mp, me, mincr, n_graphs):
    # Mide los tiempos de ejecución del algoritmo de Kruskal en varios grafos
    times = []
    for m in range (mp, me, mincr):
        n = 2*m
        times.append((n, time_kruskal(n, m, n_graphs)[0]))
    return times


   






