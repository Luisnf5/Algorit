
def heap_heapify(h, i):
    l = 2 * i + 1
    r = 2 * i + 2
    min = i

    # Si hay hijos, obtener el mínimo basado en la prioridad
    if l < len(h) and h[l][1] < h[i][1]:
        min = l

    if r < len(h) and h[r][1] < h[min][1]:
        min = r

    # Si el nodo actual no es igual al nodo mínimo, intercambiamos e intentamos heapify
    if min != i:
        h[i], h[min] = h[min], h[i]
        heap_heapify(h, min)

    return h

def heap_insert(h, key):
    # Añadimos la key al final de la lista
    h.append(key)

    i = len(h) - 1  # Índice del último elemento

    # Procedimiento heapify-up
    while i > 0 and h[(i - 1) // 2][1] > h[i][1]:
        # Intercambiamos los valores
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]
        i = (i - 1) // 2

    return h

def heap_extract(h):
    # Si el heap está vacío no se extrae nada
    if not h:
        return h, None

    # En la raíz está el elemento con la menor prioridad
    e = h[0]

    # Movemos el último elemento a la raíz
    h[0] = h[-1]

    # Extraemos el último elemento
    h = h[:-1]

    # Hacemos heapify desde la raíz
    heap_heapify(h, 0)

    # Retornamos el heap modificado y el elemento con la menor prioridad
    return h, e

def heap_create(h):
    # Se empieza desde el nodo que tiene hijo, hasta el índice 0
    for i in range((len(h) // 2) - 1, -1, -1):
        heap_heapify(h, i)

    return h

def pq_ini():
    return []

def pq_insert(h, key):
    return heap_insert(h, key)

def pq_extract(h):
    return heap_extract(h)
