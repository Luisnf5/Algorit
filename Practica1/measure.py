import time

def dataprep(n):
    lista = []
    for i in range(n):
        lista.append(i)
    return lista

#Medir tiempos de ejecucion

#Calcular la media
def calculate_average(ele):
   return sum(ele)/len(ele)  

#Calcular la varianza
def calculate_variance(ele, average):
   return sum((i-average)**2 for i in ele) / len(ele)

def time_measure(f, dataprep, Nlst, Nrep=1000, Nstat=100):
    time_k = []
    total_time = []

    for i in Nlst:
        for j in range(Nstat):
            ini = time.perf_counter()
            for k in range (Nrep):
                f(dataprep(i))
            final = time.perf_counter()
            time_k.append((final-ini)/Nrep)
        
        average = calculate_average(time_k)
        variance = calculate_variance(time_k, average)

        total_time.append((average, variance))
        time_k.clear()

    return total_time

def two_sum(lst, n):
    #Hacemos un diccionario para almacenar los numeros
    number_is = {}

    for element in lst:
        number = n - element

        #Si el numero ya esta en el diccionario, hemos encontrado el complemento
        if number in number_is:
            return True
        
        #Añadimos el numero al diccionario si no estaba antes
        number_is[element] = True
    
    return False



#Busqueda binaria en listas

def rec_bs(lst, lft, rgt, key):
    if rgt <= lft:
        return None
    
    #Encontramos el valor medio
    idx = (lft + rgt) // 2

    #Si el valor medio es igual al elemento buscado
    if lst[idx]==key:
        return idx
    #Si el valor medio es menor que el elemento buscado se busca en la mitad derecha
    elif lst[idx] < key:
        return rec_bs(lst, idx+1, rgt, key)
    #Si el valor medio es mayor que el elemento buscado se busca en la mitad izquierda
    elif lst[idx] > key:
        return rec_bs(lst, lft, idx, key)

def itr_bs(lst, lft, rgt, key):
    while rgt > lft:
        #Encontramos el valor medio
        idx = (lft + rgt) // 2
        #Si el valor medio es igual al elemento buscado
        if lst[idx]==key:
            return idx
        #Si el valor medio es menor que el elemento buscado se busca en la mitad derecha
        elif lst[idx] < key:
            lft = idx+1
        #Si el valor medio es mayor que el elemento buscado se busca en la mitad izquierda
        elif lst[idx] > key:
            rgt = idx
    
    #Si no se encuentra el elemento buscado
    return None

