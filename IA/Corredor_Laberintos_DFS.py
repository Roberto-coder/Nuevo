import matplotlib.pyplot as plt
import numpy as np

# Inicializar de punto inicial y final 
punto_inicial = (0, 0)
meta = (0, 3)

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

def dfs(laberinto, punto_inicial, meta):
    # Lista para manejar los nodos por explorar (pila)
    pila = [(punto_inicial, [])]
    # Matriz de visitados
    filas = np.shape(laberinto)[0]
    columnas = np.shape(laberinto)[1]
    visitados = np.zeros((filas, columnas))
    # Definir una lista que contenga a todos los nodos que he visitado
    considerados = []

    while len(pila) > 0:
        nodo_actual, camino = pila.pop()
        # Guardar los nodos que se han ido visitando
        considerados += [nodo_actual]

        if nodo_actual == meta:
            return camino + [nodo_actual], considerados

        #Marcar nodo actual como visitado
        visitados[nodo_actual[0], nodo_actual[1]] = 1

        for direccion in movimientos:
            nueva_posicion = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])
            # Ver que el vecino (nueva posición) esté dentro del laberinto
            if ((0 <= nueva_posicion[0] < filas) and (0 <= nueva_posicion[1] < columnas)):
                #Ver que sea casilla valida y que no haya sido visitado
                if (laberinto[nueva_posicion[0]][nueva_posicion[1]] == 0 and visitados[nueva_posicion[0], nueva_posicion[1]] == 0):
                    pila.append((nueva_posicion, camino + [nodo_actual]))

    return None, considerados

def desplegar_leberinto(maze, camino=None, considerados=None):
    plt.imshow(maze, cmap='binary')
    if considerados:
        for i in considerados:
            plt.plot(i[1], i[0], 'o', color='blue')

    if camino:
        for i in camino:
            plt.plot(i[1], i[0], 'o', color='red')

    plt.show()

camino, considerados = dfs(laberinto, punto_inicial, meta)
desplegar_leberinto(laberinto, camino, considerados)

##tarea: Implementar BFS





