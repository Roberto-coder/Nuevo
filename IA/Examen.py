import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Inicializar de punto inicial y final 
punto_inicial = (0, 0)
meta = (7, 14)

# Laberinto de ejemplo sin obstáculos
laberinto = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Función para mover el agente
def mover_agente(laberinto, punto_inicial, meta):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    camino = [punto_inicial]
    x, y = punto_inicial

    while (x, y) != meta:
        # Elegir una dirección aleatoria para moverse en diagonal
        direccion = random.choice(['arriba-derecha', 'abajo-derecha', 'arriba-izquierda', 'abajo-izquierda'])
        if direccion == 'arriba-derecha':
            x = max(0, x - 1)  # Moverse una casilla hacia arriba y a la derecha
            y = min(columnas - 1, y + 1)
        elif direccion == 'abajo-derecha':
            x = min(filas - 1, x + 1)  # Moverse una casilla hacia abajo y a la derecha
            y = min(columnas - 1, y + 1)
        elif direccion == 'arriba-izquierda':
            x = max(0, x - 1)  # Moverse una casilla hacia arriba y a la izquierda
            y = max(0, y - 1)
        elif direccion == 'abajo-izquierda':
            x = min(filas - 1, x + 1)  # Moverse una casilla hacia abajo y a la izquierda
            y = max(0, y - 1)
        camino.append((x, y))  # Añadir la nueva posición al camino
        time.sleep(0.1)  # Pausar para simular el movimiento
        graficar_laberinto(laberinto, camino, punto_inicial, meta)  # Graficar el laberinto y el camino
        plt.pause(0.1)  # Pausar para actualizar la gráfica

    return camino  # Devolver el camino recorrido

# Función para graficar el laberinto y el camino del agente
def graficar_laberinto(laberinto, camino, punto_inicial, meta):
    plt.clf()
    plt.imshow(laberinto, cmap='binary')
    for (x, y) in camino:
        plt.plot(y, x, 'bo')
    plt.plot(punto_inicial[1], punto_inicial[0], 'go')  # Punto inicial en verde
    plt.plot(meta[1], meta[0], 'ro')  # Meta en rojo
    plt.draw()

# Configuración de la gráfica
plt.ion()
fig = plt.figure()

# Ejecutar el agente
camino = mover_agente(laberinto, punto_inicial, meta)

# Mostrar el resultado final
plt.ioff()
graficar_laberinto(laberinto, camino, punto_inicial, meta)
plt.show()