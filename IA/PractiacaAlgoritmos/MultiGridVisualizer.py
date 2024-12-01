import pygame
import threading
import time
from utils import create_grid, generate_obstacles, draw_grid, get_clicked_pos
from algorithms import a_star, dijkstra, bfs, dfs

# Configuración de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 20
COLS = 20
CELL_SIZE = SCREEN_WIDTH // (2 * COLS)  # Ajustar para mostrar 4 cuadrículas

# Función para configurar y ejecutar un algoritmo
def run_algorithm(algorithm, grid, start, end, screen, offset, label, speed=0.1):
    def draw():
        draw_grid(screen, grid, ROWS, COLS, CELL_SIZE)
        # Dibujar etiquetas
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(label, True, (255, 255, 255))
        screen.blit(text, (offset[0], offset[1] - 30))
        pygame.display.flip()

    start_time = time.time()
    algorithm(start, end, grid, COLS, ROWS, draw, speed)
    end_time = time.time()
    print(f"{label} algorithm took {end_time - start_time:.2f} seconds")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Comparación de Algoritmos de Búsqueda")

    # Crear cuadrículas iniciales y obstáculos
    base_grid = create_grid(ROWS, COLS)
    generate_obstacles(base_grid, occupancy=0.3)

    # Copiar cuadrículas para cada algoritmo
    grids = [list(map(list, base_grid)) for _ in range(4)]

    # Coordenadas de inicio y final
    start = None
    end = None

    # Dividir la pantalla en 4 secciones
    offsets = [
        (0, 0),                             # A*
        (SCREEN_WIDTH // 2, 0),             # Dijkstra
        (0, SCREEN_HEIGHT // 2),            # BFS
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # DFS
    ]
    labels = ["A*", "Dijkstra", "BFS", "DFS"]

    # Variables para seleccionar inicio y final
    selecting_start = True
    algorithms_started = False

    # Bucle principal para manejar eventos y mantener la ventana abierta
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not algorithms_started:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, CELL_SIZE)
                if selecting_start:
                    start = (row, col)
                    for grid in grids:
                        grid[start[0]][start[1]] = 2  # Inicio
                    selecting_start = False
                else:
                    end = (row, col)
                    for grid in grids:
                        grid[end[0]][end[1]] = 3  # Final
                    selecting_start = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and start and end:
                algorithms_started = True
                # Crear hilos para cada algoritmo
                algorithms = [a_star, dijkstra, bfs, dfs]
                threads = []

                for i in range(4):
                    sub_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    sub_screen.blit(screen, offsets[i])
                    thread = threading.Thread(
                        target=run_algorithm,
                        args=(algorithms[i], grids[i], start, end, sub_screen, offsets[i], labels[i])
                    )
                    threads.append(thread)

                # Iniciar hilos
                for thread in threads:
                    thread.start()

                # Esperar a que los hilos terminen
                for thread in threads:
                    thread.join()

        # Dibujar las cuadrículas en sus secciones
        for i, offset in enumerate(offsets):
            sub_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            draw_grid(sub_screen, grids[i], ROWS, COLS, CELL_SIZE)
            screen.blit(sub_screen, offset)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
