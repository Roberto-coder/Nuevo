import pygame  # Importa la librería pygame para crear la interfaz gráfica
import time  # Importa time para controlar la velocidad de la animación
from algorithms import a_star, dijkstra, bfs, dfs  # Importa los algoritmos de búsqueda
from utils import draw_grid, create_grid, generate_obstacles  # Importa funciones de utilidades

# Constantes de la ventana
WIDTH, HEIGHT = 600, 600  # Ancho y alto de la ventana
ROWS, COLS = 20, 20  # Número de filas y columnas en la cuadrícula
BLOCK_SIZE = WIDTH // COLS  # Tamaño de cada celda

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Inicialización de Pygame
pygame.init()  # Inicializa pygame
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana
pygame.display.set_caption("Visualizador de Algoritmos")  # Título de la ventana

def select_algorithm():
    """
    Función para seleccionar el algoritmo de búsqueda.
    """
    print("\nSelecciona un algoritmo:")
    print("1. A*")
    print("2. Dijkstra")
    print("3. BFS")
    print("4. DFS")
    choice = input("Ingresa el número del algoritmo: ").strip()
    if choice == "1":
        return a_star
    elif choice == "2":
        return dijkstra
    elif choice == "3":
        return bfs
    elif choice == "4":
        return dfs
    else:
        print("Selección inválida. Intentando con A* por defecto.")
        return a_star

def main():
    grid = create_grid(COLS, ROWS)  # Crea una cuadrícula vacía
    start = None  # Posición de inicio
    end = None  # Posición final
    algorithm = None  # Algoritmo seleccionado
    running = True  # Variable para mantener el bucle principal

    while running:
        draw_grid(WIN, grid, ROWS, COLS, BLOCK_SIZE)  # Dibuja la cuadrícula
        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                running = False
                pygame.quit()

            # Seleccionar punto inicial, final y obstáculos
            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                x, y = pygame.mouse.get_pos()  # Obtiene la posición del clic
                row, col = y // BLOCK_SIZE, x // BLOCK_SIZE  # Convierte la posición del clic a una celda de la cuadrícula
                if not start:
                    start = (row, col)  # Establece la posición de inicio
                    grid[row][col] = 2  # Nodo inicial
                elif not end:
                    end = (row, col)  # Establece la posición final
                    grid[row][col] = 3  # Nodo final
                    # Seleccionar algoritmo después de colocar el nodo final
                    algorithm = select_algorithm()
                    print(f"Ejecutando {algorithm.__name__}...")
                else:
                    if grid[row][col] == 1:
                        grid[row][col] = 0  # Convertir obstáculo en espacio libre
                    else:
                        grid[row][col] = 1  # Convertir espacio libre en obstáculo

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # Si se presiona la tecla espacio y se han seleccionado las posiciones de inicio y final
                    # Ejecutar el algoritmo
                    path = algorithm(
                        start, end, grid, COLS, ROWS,
                        lambda: draw_grid(WIN, grid, ROWS, COLS, BLOCK_SIZE), speed=0.2
                    )

                    # Dibujar el camino encontrado
                    for pos in path:
                        if pos != start and pos != end:
                            grid[pos[0]][pos[1]] = 6  # Color del camino
                            draw_grid(WIN, grid, ROWS, COLS, BLOCK_SIZE)
                            pygame.display.flip()  # Actualiza la pantalla

                    print("Algoritmo completado.")

                # Generar obstáculos aleatorios
                if event.key == pygame.K_g:
                    generate_obstacles(grid)
                    print("Generando obstáculos aleatorios...")

                # Reiniciar la cuadrícula
                if event.key == pygame.K_r:
                    start, end = None, None
                    grid = create_grid(COLS, ROWS)
                    print("Reiniciando cuadrícula...")

        pygame.time.delay(50)  # Añade un pequeño retraso para permitir la actualización de la pantalla

    pygame.quit()  # Cierra pygame

if __name__ == "__main__":
    main()  # Ejecuta la función principal
