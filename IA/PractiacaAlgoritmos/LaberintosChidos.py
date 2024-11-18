import pygame
import time
from algorithms import a_star, dijkstra, bfs, dfs
from utils import draw_grid, create_grid

# Constantes de la ventana
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
BLOCK_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Inicialización de Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Algoritmos")

def select_algorithm():
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
    grid = create_grid(COLS, ROWS)
    start = None
    end = None
    running = True

    while running:
        draw_grid(WIN, grid, ROWS, COLS, BLOCK_SIZE)
        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            # Seleccionar punto inicial y final
            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                x, y = pygame.mouse.get_pos()
                row, col = y // BLOCK_SIZE, x // BLOCK_SIZE
                if not start:
                    start = (row, col)
                    grid[row][col] = 2  # Nodo inicial
                elif not end:
                    end = (row, col)
                    grid[row][col] = 3  # Nodo final

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Seleccionar algoritmo
                    algorithm = select_algorithm()
                    print(f"Ejecutando {algorithm.__name__}...")

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

                # Reiniciar la cuadrícula
                if event.key == pygame.K_r:
                    start, end = None, None
                    grid = create_grid(COLS, ROWS)
                    print("Reiniciando cuadrícula...")

    pygame.quit()

if __name__ == "__main__":
    main()
