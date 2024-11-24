import pygame
import random

# Constantes de colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Función para inicializar la cuadrícula
def create_grid(rows, cols):
    """
    Crea una cuadrícula inicial vacía con los valores iniciales.
    - 0: Espacio libre.
    - 1: Obstáculo.
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]

# Función para generar obstáculos aleatorios
def generate_obstacles(grid, occupancy=0.3):
    """
    Genera obstáculos aleatorios en la cuadrícula.
    - grid: La cuadrícula 2D.
    - occupancy: Porcentaje de celdas ocupadas por obstáculos.
    """
    rows = len(grid)
    cols = len(grid[0])
    num_obstacles = int(rows * cols * occupancy)
    for _ in range(num_obstacles):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if grid[row][col] == 0:  # Solo colocar en espacios libres
            grid[row][col] = 1

# Función para dibujar la cuadrícula en pantalla
def draw_grid(screen, grid, rows, cols, cell_size):
    """
    Dibuja la cuadrícula en la pantalla de `pygame`.
    - screen: Superficie donde se dibuja.
    - grid: La cuadrícula 2D.
    - rows, cols: Dimensiones de la cuadrícula.
    - cell_size: Tamaño de cada celda en píxeles.
    """
    for row in range(rows):
        for col in range(cols):
            color = WHITE  # Por defecto, espacio libre
            if grid[row][col] == 1:
                color = BLACK  # Obstáculo
            elif grid[row][col] == 2:
                color = GREEN  # Inicio
            elif grid[row][col] == 3:
                color = RED  # Final
            elif grid[row][col] == 4:
                color = YELLOW  # Nodo abierto
            elif grid[row][col] == 5:
                color = BLUE  # Nodo cerrado
            elif grid[row][col] == 6:
                color = ORANGE  # Camino encontrado
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Dibujar las líneas de la cuadrícula
    for row in range(rows):
        pygame.draw.line(screen, GREY, (0, row * cell_size), (cols * cell_size, row * cell_size))
    for col in range(cols):
        pygame.draw.line(screen, GREY, (col * cell_size, 0), (col * cell_size, rows * cell_size))

# Función para convertir coordenadas de clic a una celda de la cuadrícula
def get_clicked_pos(pos, cell_size):
    """
    Convierte una posición de clic en pantalla a una celda de la cuadrícula.
    - pos: (x, y) posición del clic en píxeles.
    - cell_size: Tamaño de cada celda.
    """
    x, y = pos
    return y // cell_size, x // cell_size

# Función para resetear la cuadrícula (opcional)
def reset_grid(grid):
    """
    Resetea todas las celdas de la cuadrícula excepto los obstáculos.
    """
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 1:  # Mantener los obstáculos
                grid[row][col] = 0
