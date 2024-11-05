import time

'''
Para crear todas las permutaciones de una lista podemos coger cada elemento de la lista mas todas las permutaciones de la lista restante.

Al hacer esto con todos los elementos tenemos todas las permutaciones posibles.

Ejemplo: Para la lista [1, 2, 3] podemos hacer (1 + permutaciones([2, 3]) +  (2 + permutaciones([1, 3])) + (3 + permutaciones([1, 2])).
'''

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


    


