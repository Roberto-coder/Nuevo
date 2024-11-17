import matplotlib.pyplot as plt
import numpy as np
import time
import tracemalloc

# Inicializar de punto inicial y final 
punto_inicial = (0, 0)
meta = (0, 14)

# Tipos de movimiento
movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]

laberinto = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0]
]

def eliminar_de_lista(lista, indice):
    # Mover todos los elementos después del índice hacia la izquierda
    for i in range(indice, len(lista) - 1):
        lista[i] = lista[i + 1]
    # Reducir el tamaño de la lista
    lista[:] = lista[:-1]

# Función para agregar elementos usando índices
def agregar_a_lista(arr, valor):
    # Expandir la lista en 1 unidad
    arr.append(None)  # Añadir un espacio vacío
    # Asignar el nuevo valor en la siguiente posición
    arr[len(arr) - 1] = valor

def bfs(maze, punto_inicial, meta):
    # Lista para manejar los nodos por explorar (cola)
    cola = [(punto_inicial, [punto_inicial])]
    considerados = []
    # Matriz de visitados
    filas = np.shape(maze)[0]
    columnas = np.shape(maze)[1]
    visitados = np.zeros((filas, columnas))
    visitados[punto_inicial[0], punto_inicial[1]] = 1

    tracemalloc.start()
    start_time = time.perf_counter()

    while len(cola) > 0:
        nodo_actual, camino = cola[0]
        eliminar_de_lista(cola, 0)
        agregar_a_lista(considerados, nodo_actual)

        if nodo_actual == meta:
            # Tiempo y memoria al encontrar la solución
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print("Se encontró la solución en nivel:", len(camino))
            print("Solución:", nodo_actual)
            print("El tiempo de ejecución fue de:", end_time - start_time)
            print(f'La memoria consumida fue de: {current / 10**6} MB, Pico de uso: {peak / 10**6} MB.')
            return camino + [nodo_actual], considerados

        for direccion in movimientos:
            nueva_posicion = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])
            # Ver que el vecino (nueva posición) esté dentro del laberinto
            if (0 <= nueva_posicion[0] < filas) and (0 <= nueva_posicion[1] < columnas):
                ##Si no es un muro y no esta en la lista cerrada
                if maze[nueva_posicion[0]][nueva_posicion[1]] == 0 and visitados[nueva_posicion[0], nueva_posicion[1]] == 0:
                    visitados[nueva_posicion[0], nueva_posicion[1]] = 1
                    ##Poner el vecino en la lista abierta
                    agregar_a_lista(cola, (nueva_posicion, camino + [nueva_posicion]))

    print("No se encontró la solución.")
    return None, considerados

def desplegar_laberinto(maze, camino=None, considerados=None):
    plt.imshow(maze, cmap='binary')
    if considerados:
        for i in considerados:
            plt.plot(i[1], i[0], 'o', color='blue')

    if camino:
        for i in camino:
            plt.plot(i[1], i[0], 'o', color='red')

    plt.show()

# Ejemplo de uso
camino, considerados = bfs(laberinto, punto_inicial, meta)
desplegar_laberinto(laberinto, camino, considerados)