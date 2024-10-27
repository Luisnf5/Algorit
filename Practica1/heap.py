def heap_heapify(h, i):
    l = 2*i+1
    r = 2*i+2
    min = i

    #Si hay hijos, obtener el minimo
    if l < len(h) and h[l] < h[i]:
        min = l
    
    if r < len(h) and h[r] < h[min]:
        min = r
    
    #Si el nodo actual no es igual al nodo minimo, intercambiamos e intentamos heapify
    if min != i:
        h[i], h[min] = h[min], h[i]
        
        heap_heapify(h, min)
    
    return h

def heap_insert(h, key):
    #Añadimos la key al final de la lista
    h.append(key)

    i = len(h) -1 #Indice del ultimo elemento

    #Procedimiento heapify-up 
    while i > 0 and h[(i - 1) // 2] > h[i]:

        #Intercambiamos los valores
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]
        i = (i - 1) // 2
        
    return h

def heap_extract(h):
    #Si el heap esta vacío no se extrae nada
    if not h:
        return h, None
    
    #en la raíz está el elemento más pequeño
    e = h[0]

    #Movemos el ultimo elemento a la raiz
    h[0] = h[-1]

    #Extraemos el ultimo elemento
    h = h[:-1]     

    #Hacemos heapify desde la raiz
    heap_heapify(h, 0)

    #Retornamos el heap modificado y el elemneto más pequeño
    return h, e

def heap_create(h):

    #Se empieza desde el nodo que tiene hijo, hasta el indice 0
    for i in range((len(h) // 2) -1, -1, -1):  
        heap_heapify(h, i)

    return h

def pq_ini():
    return []

def pq_insert(h, key):
    return heap_insert(h, key)

def pq_extract(h):

    return heap_extract(h)