import matplotlib.pyplot as plt
import numpy as np
import time
import tracemalloc

# Inicializar de punto inicial y final 
punto_inicial = (0, 0)
meta = (0, 14)

# Tipos de movimiento
movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Representación del laberinto (0 es transitable, 1 es obstáculo)
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

def bfs(laberinto, punto_inicial, meta):
    # Medición de tiempo y memoria
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Lista para manejar los nodos por explorar (cola para BFS)
    cola = [(punto_inicial, [])]
    # Matriz de visitados
    filas = np.shape(laberinto)[0]
    columnas = np.shape(laberinto)[1]
    visitados = np.zeros((filas, columnas))
    # Definir una lista para guardar todos los nodos considerados
    considerados = []

    # Marcar el nodo inicial como visitado
    visitados[punto_inicial[0], punto_inicial[1]] = 1
    
    while len(cola) > 0:
        nodo_actual, camino = cola.pop(0)
        considerados.append(nodo_actual)

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

        # Explorar los vecinos (movimientos)
        for direccion in movimientos:
            nueva_posicion = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])
            if (0 <= nueva_posicion[0] < filas) and (0 <= nueva_posicion[1] < columnas):
                if laberinto[nueva_posicion[0]][nueva_posicion[1]] == 0 and visitados[nueva_posicion[0], nueva_posicion[1]] == 0:
                    # Marcar como visitado y agregar a la cola
                    visitados[nueva_posicion[0], nueva_posicion[1]] = 1
                    cola.append((nueva_posicion, camino + [nodo_actual]))

    # Si no se encuentra solución
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("No se encontró la solución.")
    print("El tiempo de ejecución fue de:", end_time - start_time)
    print(f'La memoria consumida fue de: {current / 10**6} MB, Pico de uso: {peak / 10**6} MB.')
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

# Ejecutar BFS y mostrar el laberinto con el camino
camino, considerados = bfs(laberinto, punto_inicial, meta)
desplegar_laberinto(laberinto, camino, considerados)
