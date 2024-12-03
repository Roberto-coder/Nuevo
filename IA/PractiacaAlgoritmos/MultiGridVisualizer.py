import pygame  # Importa la librería pygame para crear la interfaz gráfica
import threading  # Importa threading para ejecutar algoritmos en paralelo
import time  # Importa time para medir el tiempo de ejecución
from utils import create_grid, generate_obstacles, draw_grid, get_clicked_pos, draw_path  # Importa funciones de utilidades
from algorithms import a_star, dijkstra, bfs, dfs  # Importa los algoritmos de búsqueda

# Configuración de la ventana
SCREEN_WIDTH = 800  # Ancho de la ventana
SCREEN_HEIGHT = 600  # Alto de la ventana
ROWS = 20  # Número de filas en la cuadrícula
COLS = 20  # Número de columnas en la cuadrícula
CELL_SIZE = SCREEN_WIDTH // (2 * COLS)  # Tamaño de cada celda

# Función para configurar y ejecutar un algoritmo
def run_algorithm(algorithm, grid, start, end, screen, offset, label, speed=0.1):
    def draw():
        draw_grid(screen, grid, ROWS, COLS, CELL_SIZE)  # Dibuja la cuadrícula
        # Dibujar etiquetas
        font = pygame.font.SysFont("Arial", 20)  # Fuente para el texto
        text = font.render(label, True, (255, 255, 255))  # Renderiza el texto
        screen.blit(text, (offset[0], offset[1] - 30))  # Muestra el texto en la pantalla
        pygame.display.flip()  # Actualiza la pantalla

    start_time = time.time()  # Tiempo de inicio
    path = algorithm(start, end, grid, COLS, ROWS, draw, speed)  # Ejecuta el algoritmo
    end_time = time.time()  # Tiempo de finalización
    print(f"algorithm: {label} tomo {end_time - start_time:.2f} segundos")  # Muestra el tiempo de ejecución

    # Dibujar el camino encontrado
    draw_path(screen, path, CELL_SIZE)

def main():
    pygame.init()  # Inicializa pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crea la ventana
    pygame.display.set_caption("Comparación de Algoritmos de Búsqueda")  # Título de la ventana

    # Crear cuadrículas iniciales y obstáculos
    base_grid = create_grid(ROWS, COLS)  # Crea una cuadrícula vacía
    generate_obstacles(base_grid, occupancy=0.3)  # Genera obstáculos en la cuadrícula

    # Copiar cuadrículas para cada algoritmo
    grids = [list(map(list, base_grid)) for _ in range(4)]  # Copia la cuadrícula para cada algoritmo

    # Coordenadas de inicio y final
    start = None  # Posición de inicio
    end = None  # Posición final

    # Dividir la pantalla en 4 secciones
    offsets = [
        (0, 0),  # A*
        (SCREEN_WIDTH // 2, 0),  # Dijkstra
        (0, SCREEN_HEIGHT // 2),  # BFS
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # DFS
    ]
    labels = ["A*", "Dijkstra", "BFS", "DFS"]  # Etiquetas para los algoritmos

    # Variables para seleccionar inicio y final
    selecting_start = True  # Indica si se está seleccionando la posición de inicio
    algorithms_started = False  # Indica si los algoritmos han comenzado

    # Bucle principal para manejar eventos y mantener la ventana abierta
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not algorithms_started:  # Si se hace clic y los algoritmos no han comenzado
                pos = pygame.mouse.get_pos()  # Obtiene la posición del clic
                row, col = get_clicked_pos(pos, CELL_SIZE)  # Convierte la posición del clic a una celda de la cuadrícula
                if selecting_start:
                    start = (row, col)  # Establece la posición de inicio
                    for grid in grids:
                        grid[start[0]][start[1]] = 2  # Marca la posición de inicio en la cuadrícula
                    selecting_start = False
                else:
                    end = (row, col)  # Establece la posición final
                    for grid in grids:
                        grid[end[0]][end[1]] = 3  # Marca la posición final en la cuadrícula
                    selecting_start = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and start and end:  # Si se presiona la tecla espacio y se han seleccionado las posiciones de inicio y final
                algorithms_started = True
                # Crear hilos para cada algoritmo
                algorithms = [a_star, dijkstra, bfs, dfs]
                threads = []

                for i in range(4):
                    sub_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Crea una subpantalla
                    sub_screen.blit(screen, offsets[i])  # Dibuja la subpantalla en la pantalla principal
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
            sub_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Crea una subpantalla
            draw_grid(sub_screen, grids[i], ROWS, COLS, CELL_SIZE)  # Dibuja la cuadrícula en la subpantalla
            screen.blit(sub_screen, offset)  # Dibuja la subpantalla en la pantalla principal

        pygame.display.flip()  # Actualiza la pantalla

    pygame.quit()  # Cierra pygame

if __name__ == "__main__":
    main()  # Ejecuta la función principal
