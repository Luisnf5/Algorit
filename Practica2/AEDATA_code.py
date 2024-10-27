import heap_mod as heap

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



