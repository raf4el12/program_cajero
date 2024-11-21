# utils/algoritmos.py

def quicksort_clientes(clientes, clave):
    """
    Ordena la lista de clientes usando QuickSort.
    :param clientes: Lista de objetos Cliente.
    :param clave: Clave de ordenamiento ('id_cliente' o 'nombre').
    :return: Lista ordenada de clientes.
    """
    if len(clientes) <= 1:
        return clientes

    pivote = clientes[len(clientes) // 2]
    izquierda = [cliente for cliente in clientes if getattr(cliente, clave) < getattr(pivote, clave)]
    igual = [cliente for cliente in clientes if getattr(cliente, clave) == getattr(pivote, clave)]
    derecha = [cliente for cliente in clientes if getattr(cliente, clave) > getattr(pivote, clave)]

    return quicksort_clientes(izquierda, clave) + igual + quicksort_clientes(derecha, clave)

def mergesort_cajeros(cajeros, clave):
    """
    Ordena la lista de cajeros usando MergeSort.
    :param cajeros: Lista de objetos Cajero.
    :param clave: Clave de ordenamiento ('id_cajero' o 'ubicacion').
    :return: Lista ordenada de cajeros.
    """
    if len(cajeros) <= 1:
        return cajeros

    medio = len(cajeros) // 2
    izquierda = mergesort_cajeros(cajeros[:medio], clave)
    derecha = mergesort_cajeros(cajeros[medio:], clave)

    return merge(izquierda, derecha, clave)

def merge(izquierda, derecha, clave):
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if getattr(izquierda[i], clave) <= getattr(derecha[j], clave):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

def busqueda_binaria(lista, clave, valor):
    """
    Realiza una búsqueda binaria en una lista ordenada.
    :param lista: Lista ordenada de objetos.
    :param clave: Clave de búsqueda ('id_cliente', 'id_cajero', etc.).
    :param valor: Valor a buscar.
    :return: Objeto encontrado o None.
    """
    izquierda, derecha = 0, len(lista) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if getattr(lista[medio], clave) == valor:
            return lista[medio]
        elif getattr(lista[medio], clave) < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None
