import pygame
import random
import time

# Dimensiones del laberinto
FILAS = 20
COLUMNAS = 35
TAMANIO_CELDA = 20

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
GRIS = (200, 200, 200)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((COLUMNAS * TAMANIO_CELDA + 50, FILAS * TAMANIO_CELDA + 50))
pygame.display.set_caption("Laberinto - Resolución Paso a Paso")
fuente = pygame.font.SysFont("Arial", 16)


# Generar el laberinto aleatorio con un 30% de celdas ocupadas
def generar_laberinto():
    total_celdas = FILAS * COLUMNAS
    paredes = int(total_celdas * 0.3)  # 30% de celdas ocupadas
    laberinto = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

    # Añadir paredes aleatoriamente
    for _ in range(paredes):
        while True:
            fila = random.randint(0, FILAS - 1)
            columna = random.randint(0, COLUMNAS - 1)
            if laberinto[fila][columna] == 0:  # Asegurarse de no sobrescribir
                laberinto[fila][columna] = 1
                break

    return laberinto


# Dibujar el laberinto en pantalla con etiquetas de coordenadas
def dibujar_laberinto(laberinto, camino=None, explorados=None):
    pantalla.fill(NEGRO)
    
    # Dibujar etiquetas del eje X
    for columna in range(COLUMNAS):
        texto = fuente.render(str(columna), True, BLANCO)
        pantalla.blit(texto, (columna * TAMANIO_CELDA + 25, 5))

    # Dibujar etiquetas del eje Y
    for fila in range(FILAS):
        texto = fuente.render(str(fila), True, BLANCO)
        pantalla.blit(texto, (5, fila * TAMANIO_CELDA + 25))

    # Dibujar el laberinto
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = BLANCO if laberinto[fila][columna] == 0 else GRIS
            pygame.draw.rect(pantalla, color, (columna * TAMANIO_CELDA + 50, fila * TAMANIO_CELDA + 50, TAMANIO_CELDA, TAMANIO_CELDA))

    # Dibujar casillas exploradas
    if explorados:
        for x, y in explorados:
            pygame.draw.rect(pantalla, VERDE, (y * TAMANIO_CELDA + 50, x * TAMANIO_CELDA + 50, TAMANIO_CELDA, TAMANIO_CELDA))
            pygame.display.update()
            pygame.time.wait(50)

    # Dibujar el camino encontrado
    if camino:
        for x, y in camino:
            pygame.draw.rect(pantalla, AZUL, (y * TAMANIO_CELDA + 50, x * TAMANIO_CELDA + 50, TAMANIO_CELDA, TAMANIO_CELDA))
            pygame.display.update()
            pygame.time.wait(100)

    pygame.display.update()


# Validar si la posición es válida
def posicion_valida(laberinto, posicion):
    x, y = posicion
    return 0 <= x < FILAS and 0 <= y < COLUMNAS and laberinto[x][y] == 0


# Algoritmo BFS
def bfs(laberinto, inicio, fin):
    queue = [(inicio, [inicio])]
    visitados = set()
    explorados = []

    while queue:
        (nodo, camino) = queue.pop(0)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        explorados.append(nodo)

        # Si encontramos el fin, devolvemos el camino
        if nodo == fin:
            return camino, explorados

        # Generar vecinos
        x, y = nodo
        vecinos = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for vecino in vecinos:
            if posicion_valida(laberinto, vecino) and vecino not in visitados:
                queue.append((vecino, camino + [vecino]))

    return None, explorados


# Algoritmo A*
def a_estrella(laberinto, inicio, fin):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(0, inicio, [inicio])]
    visitados = set()
    explorados = []

    while open_set:
        open_set.sort(key=lambda x: x[0])  # Ordenar por costo f
        _, nodo, camino = open_set.pop(0)

        if nodo in visitados:
            continue
        visitados.add(nodo)
        explorados.append(nodo)

        if nodo == fin:
            return camino, explorados

        x, y = nodo
        vecinos = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for vecino in vecinos:
            if posicion_valida(laberinto, vecino) and vecino not in visitados:
                g = len(camino)
                h = heuristica(vecino, fin)
                f = g + h
                open_set.append((f, vecino, camino + [vecino]))

    return None, explorados


# Algoritmo Dijkstra
def dijkstra(laberinto, inicio, fin):
    open_set = [(0, inicio, [inicio])]
    visitados = set()
    explorados = []

    while open_set:
        open_set.sort(key=lambda x: x[0])  # Ordenar por costo acumulado
        costo, nodo, camino = open_set.pop(0)

        if nodo in visitados:
            continue
        visitados.add(nodo)
        explorados.append(nodo)

        if nodo == fin:
            return camino, explorados

        x, y = nodo
        vecinos = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for vecino in vecinos:
            if posicion_valida(laberinto, vecino) and vecino not in visitados:
                nuevo_costo = costo + 1
                open_set.append((nuevo_costo, vecino, camino + [vecino]))

    return None, explorados


# Función principal
def main():
    while True:
        laberinto = generar_laberinto()

        pantalla.fill(NEGRO)
        dibujar_laberinto(laberinto)

        # Pedir coordenadas de inicio y fin
        while True:
            try:
                inicio = tuple(map(int, input("Ingrese la coordenada de inicio (formato: fila,columna): ").split(",")))
                if not posicion_valida(laberinto, inicio):
                    print("La posición de inicio no es válida. Debe ser una casilla blanca.")
                    continue
                break
            except:
                print("Coordenadas inválidas. Intente de nuevo.")

        while True:
            try:
                fin = tuple(map(int, input("Ingrese la coordenada de fin (formato: fila,columna): ").split(",")))
                if not posicion_valida(laberinto, fin):
                    print("La posición de fin no es válida. Debe ser una casilla blanca.")
                    continue
                break
            except:
                print("Coordenadas inválidas. Intente de nuevo.")

        # Seleccionar algoritmo
        print("Seleccione el algoritmo:")
        print("1. BFS")
        print("2. A*")
        print("3. Dijkstra")
        opcion = int(input("Opción: "))

        if opcion == 1:
            camino, explorados = bfs(laberinto, inicio, fin)
        elif opcion == 2:
            camino, explorados = a_estrella(laberinto, inicio, fin)
        elif opcion == 3:
            camino, explorados = dijkstra(laberinto, inicio, fin)
        else:
            print("Opción no válida.")
            pygame.quit()
            return

        # Dibujar resultados
        dibujar_laberinto(laberinto, camino, explorados)

        # Preguntar si desea continuar
        continuar = input("¿Desea probar otro laberinto? (s/n): ").lower()
        if continuar != 's':
            print("Saliendo del programa.")
            pygame.quit()
            break


if __name__ == "__main__":
    main()
