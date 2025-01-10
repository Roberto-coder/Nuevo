import matplotlib.pyplot as plt
import random
import multiprocessing
import time

#Un agente debe localizar y "capturar" un objetivo que también 
# se mueve dentro de un espacio definido.
# Un agente comienza en una posición aleatoria en un plano cartesiano 
# y debe encontrar un objetivo en coordenadas conocidas.

# Función para generar una posición aleatoria válida
def generar_posicion_aleatoria(laberinto):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    while True:
        x = random.randint(0, filas - 1)
        y = random.randint(0, columnas - 1)
        if laberinto[x][y] == 0:
            return (x, y)

# Laberinto de ejemplo sin obstáculos
laberinto = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Generar posiciones aleatorias válidas para el agente y el objetivo
punto_inicial = generar_posicion_aleatoria(laberinto)
objetivo = generar_posicion_aleatoria(laberinto)

# Función para mover el objetivo
def mover_objetivo(laberinto, punto_inicial, cola):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    x, y = punto_inicial

    while True:
        direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if direccion == 'arriba' and x > 0 and laberinto[x-1][y] == 0:
            x -= 1
        elif direccion == 'abajo' and x < filas - 1 and laberinto[x+1][y] == 0:
            x += 1
        elif direccion == 'izquierda' and y > 0 and laberinto[x][y-1] == 0:
            y -= 1
        elif direccion == 'derecha' and y < columnas - 1 and laberinto[x][y+1] == 0:
            y += 1
        cola.put((x, y))
        time.sleep(0.5)

# Función para mover el agente
def mover_agente(laberinto, punto_inicial, cola_objetivo, cola_agente):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    x, y = punto_inicial

    while True:
        if not cola_objetivo.empty():
            objetivo_x, objetivo_y = cola_objetivo.get()
            if x < objetivo_x and laberinto[x+1][y] == 0:
                x += 1
            elif x > objetivo_x and laberinto[x-1][y] == 0:
                x -= 1
            elif y < objetivo_y and laberinto[x][y+1] == 0:
                y += 1
            elif y > objetivo_y and laberinto[x][y-1] == 0:
                y -= 1
            cola_agente.put((x, y))
            if (x, y) == (objetivo_x, objetivo_y):
                break
        time.sleep(0.1)

# Función para graficar el laberinto y las posiciones del agente y el objetivo
def graficar_laberinto(laberinto, posicion_agente, posicion_objetivo, ax):
    ax.clear()
    ax.imshow(laberinto, cmap='binary')
    ax.plot(posicion_agente[1], posicion_agente[0], 'bo')
    ax.plot(posicion_objetivo[1], posicion_objetivo[0], 'ro')
    plt.draw()

if __name__ == '__main__':
    # Crear colas para recibir las posiciones del objetivo y del agente
    cola_objetivo = multiprocessing.Queue()
    cola_agente = multiprocessing.Queue()

    # Crear procesos para el objetivo y el agente
    proceso_objetivo = multiprocessing.Process(target=mover_objetivo, args=(laberinto, objetivo, cola_objetivo))
    proceso_agente = multiprocessing.Process(target=mover_agente, args=(laberinto, punto_inicial, cola_objetivo, cola_agente))

    # Configuración de la gráfica
    fig, ax = plt.subplots()
    plt.ion()

    # Iniciar los procesos
    proceso_objetivo.start()
    proceso_agente.start()

    # Graficar en tiempo real
    posicion_agente = punto_inicial
    posicion_objetivo = objetivo
    while proceso_agente.is_alive():
        if not cola_agente.empty():
            posicion_agente = cola_agente.get()
        if not cola_objetivo.empty():
            posicion_objetivo = cola_objetivo.get()
        graficar_laberinto(laberinto, posicion_agente, posicion_objetivo, ax)
        plt.pause(0.1)

    # Esperar a que los procesos terminen
    proceso_objetivo.terminate()
    proceso_agente.join()

    # Mostrar el resultado final
    plt.ioff()
    plt.show()

    print("El agente ha capturado el objetivo.")