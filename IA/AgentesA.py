import matplotlib.pyplot as plt
import random
import multiprocessing
import time

# Función para generar una posición aleatoria válida
def generar_posicion_aleatoria(laberinto):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    while True:
        x = random.randint(0, filas - 1)
        y = random.randint(0, columnas - 1)
        if laberinto[x][y] == 0:
            return (x, y)

# Laberintos de ejemplo sin obstáculos
laberinto1 = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

laberinto2 = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Generar posiciones aleatorias válidas para el inicio y la meta
punto_inicial = generar_posicion_aleatoria(laberinto1)
meta = generar_posicion_aleatoria(laberinto1)

# Función para mover el agente 1
def mover_agente1(laberinto, punto_inicial, meta, cola):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    camino = [punto_inicial]
    x, y = punto_inicial
    start_time = time.time()

    while (x, y) != meta:
        direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if direccion == 'arriba' and x > 0 and laberinto[x-1][y] == 0:
            x -= 1
        elif direccion == 'abajo' and x < filas - 1 and laberinto[x+1][y] == 0:
            x += 1
        elif direccion == 'izquierda' and y > 0 and laberinto[x][y-1] == 0:
            y -= 1
        elif direccion == 'derecha' and y < columnas - 1 and laberinto[x][y+1] == 0:
            y += 1
        camino.append((x, y))
        cola.put((camino, time.time() - start_time))
        time.sleep(0.1)

    cola.put((camino, time.time() - start_time))

# Función para mover el agente 2
def mover_agente2(laberinto, punto_inicial, meta, cola):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    camino = [punto_inicial]
    x, y = punto_inicial
    start_time = time.time()
    direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])

    while (x, y) != meta:
        if direccion == 'arriba' and x > 0 and laberinto[x-1][y] == 0:
            x -= 1
        elif direccion == 'abajo' and x < filas - 1 and laberinto[x+1][y] == 0:
            x += 1
        elif direccion == 'izquierda' and y > 0 and laberinto[x][y-1] == 0:
            y -= 1
        elif direccion == 'derecha' and y < columnas - 1 and laberinto[x][y+1] == 0:
            y += 1
        else:
            direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
            continue
        camino.append((x, y))
        cola.put((camino, time.time() - start_time))
        time.sleep(0.1)

    cola.put((camino, time.time() - start_time))

# Función para graficar el laberinto y el camino del agente
def graficar_laberinto(laberinto, camino, punto_inicial, meta, color, ax):
    ax.clear()
    ax.imshow(laberinto, cmap='binary')
    for (x, y) in camino:
        ax.plot(y, x, color + 'o')
    ax.plot(punto_inicial[1], punto_inicial[0], 'go')
    ax.plot(meta[1], meta[0], 'ro')
    plt.draw()

if __name__ == '__main__':
    # Crear colas para recibir los caminos de los agentes
    cola1 = multiprocessing.Queue()
    cola2 = multiprocessing.Queue()

    # Crear procesos para los dos agentes
    agente1 = multiprocessing.Process(target=mover_agente1, args=(laberinto1, punto_inicial, meta, cola1))
    agente2 = multiprocessing.Process(target=mover_agente2, args=(laberinto2, punto_inicial, meta, cola2))

    # Configuración de la gráfica
    fig, (ax1, ax2) = plt.subplots(1, 2)
    plt.ion()

    # Iniciar los procesos
    agente1.start()
    agente2.start()

    tiempo1 = tiempo2 = None

    # Graficar en tiempo real
    while agente1.is_alive() or agente2.is_alive():
        if not cola1.empty():
            camino1, tiempo1 = cola1.get()
            graficar_laberinto(laberinto1, camino1, punto_inicial, meta, 'b', ax1)
            if (camino1[-1] == meta):
                agente1.terminate()
        if not cola2.empty():
            camino2, tiempo2 = cola2.get()
            graficar_laberinto(laberinto2, camino2, punto_inicial, meta, 'r', ax2)
            if (camino2[-1] == meta):
                agente2.terminate()
        plt.pause(0.1)

    # Esperar a que los procesos terminen
    agente1.join()
    agente2.join()

    # Mostrar el resultado final
    plt.ioff()
    plt.show()

    # Imprimir los tiempos y definir el ganador
    print(f"Tiempo del agente 1: {tiempo1:.2f} segundos")
    print(f"Tiempo del agente 2: {tiempo2:.2f} segundos")
    if tiempo1 < tiempo2:
        print("El ganador es el agente 1")
    elif tiempo2 < tiempo1:
        print("El ganador es el agente 2")
    else:
        print("Es un empate")