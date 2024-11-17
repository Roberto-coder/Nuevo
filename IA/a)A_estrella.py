import matplotlib.pyplot as plt
import numpy as np

# Inicializar de punto inicial y final 
punto_inicial = (0, 0)
meta = (7, 14)

# Tipos de movimiento
movimientos = [(-1, -1),(-1, 0), (-1, 1),(0, 1), (1, 1),(1, 0), (1, -1), (0, -1)]

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

def heuristica_diagonal(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    D1 = 10  # Costo de moverse horizontal o verticalmente
    D2 = 14  # Costo de moverse en diagonal
    return D1 * (dx + dy) + (D2 - 2 * D1) * min(dx, dy)

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

def A_estrella(maze, punto_inicial, meta):
    # Lista para manejar los nodos por explorar (pila)
    lista_abierta = [(punto_inicial, 0, heuristica_diagonal(punto_inicial, meta), [])]
    ##lista abierta = (nodo, g, h, camino)
    considerados = []
    # Matriz de visitados
    filas = np.shape(maze)[0]
    columnas = np.shape(maze)[1]
    lista_cerrada = np.zeros((filas, columnas))
    ##lista_cerrada = np.zeros_like(laberinto)
    while len(lista_abierta) > 0:
        menor_h = lista_abierta[0][2]
        nodo_actual, g_actual, h_actual, camino_actual = lista_abierta[0]
        indice_menor_h = 0

        ##Se recorre la posicion 2 de la fila i-esima(Distancia manhattan) de la lista abierta preguntando¿Cual es el de menor_valor?(Menor energia)
        ##Obtener el nodo actual a partir del menor f, (h la primera vez g=0)
        for i in range(1, len(lista_abierta)):
            if lista_abierta[i][2] < menor_h:
                menor_h = lista_abierta[i][2]
                nodo_actual, g_actual, h_actual, camino_actual = lista_abierta[i]
                indice_menor_h = i

        ##Eliminarlo de la lista abierta
        eliminar_de_lista(lista_abierta, indice_menor_h)
        
        ## Guardar todos los nodos que fueron evaluados aunque no formen parte del camino actual
        agregar_a_lista(considerados, nodo_actual)
        ##Evaluamos si el nodo actual es o no el nodo meta
        if nodo_actual == meta:
            return camino_actual + [nodo_actual], considerados
        
        ##añadir el nodo actual a la lista cerrada
        lista_cerrada[nodo_actual[0], nodo_actual[1]] = 1

        for direccion in movimientos:
            nueva_posicion = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])
            # Ver que el vecino (nueva posición) esté dentro del laberinto
            if (0 <= nueva_posicion[0] < filas) and (0 <= nueva_posicion[1] < columnas):
                ##Si no es un muro y no esta en la lista cerrada
                if maze[nueva_posicion[0]][nueva_posicion[1]] == 0 and lista_cerrada[nueva_posicion[0], nueva_posicion[1]] == 0:
                    ##Evaluamos si el movimiento o direccion es diagonal
                    if abs(direccion[0]) + abs(direccion[1]) == 2:
                        g_nuevo = g_actual + 14
                    else:
                        g_nuevo = g_actual + 10

                    f_nuevo = g_nuevo + heuristica_diagonal(nueva_posicion, meta)

                    bandera_lista = False
                    for nodo, g, f, camino in lista_abierta:
                        ##Si el vecino.posicion esta en alguna posicion de algin nodo de la lista abierta
                        ##Si el vecino.g es mayor que el costo g del que esta en la lista abierta
                        if nodo == nueva_posicion and g <= g_nuevo:
                            bandera_lista = True
                            break
                    if not bandera_lista:
                        ##Poner el vecino en la lista abierta
                        agregar_a_lista(lista_abierta, (nueva_posicion, g_nuevo, f_nuevo, camino_actual + [nueva_posicion]))

    print("No se encontró la solución.")
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

camino, considerados = A_estrella(laberinto, punto_inicial, meta)
desplegar_leberinto(laberinto, camino, considerados)