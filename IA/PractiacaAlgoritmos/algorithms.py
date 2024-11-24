import heapq
import pygame
import time
from collections import deque

# Heurística de Manhattan (para A* y opcionalmente para Dijkstra)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Obtener vecinos válidos
def get_neighbors(node, grid, cols, rows):
    x, y = node
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows and grid[nx][ny] != 1:  # No obstáculos
            neighbors.append((nx, ny))
    return neighbors

# Algoritmo A*
def a_star(start, end, grid, cols, rows, draw_grid, speed=0.5):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid, cols, rows):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                if grid[neighbor[0]][neighbor[1]] != 3:  # No sobrescribir la meta
                    grid[neighbor[0]][neighbor[1]] = 4  # Nodo abierto

        if current != start:
            grid[current[0]][current[1]] = 5  # Nodo cerrado

        draw_grid()
        pygame.display.flip()  # Actualiza la pantalla
        time.sleep(speed)

    return []  # Retorna vacío si no hay solución

# Algoritmo Dijkstra
def dijkstra(start, end, grid, cols, rows, draw_grid, speed=0.5):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    distances = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid, cols, rows):
            tentative_distance = distances[current] + 1
            if neighbor not in distances or tentative_distance < distances[neighbor]:
                came_from[neighbor] = current
                distances[neighbor] = tentative_distance
                heapq.heappush(open_set, (distances[neighbor], neighbor))
                if grid[neighbor[0]][neighbor[1]] != 3:
                    grid[neighbor[0]][neighbor[1]] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw_grid()
        pygame.display.flip()  # Actualiza la pantalla
        time.sleep(speed)

    return []

# Algoritmo BFS
def bfs(start, end, grid, cols, rows, draw_grid, speed=0.5):
    queue = deque([start])
    came_from = {start: None}
    visited = set()
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid, cols, rows):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current
                if grid[neighbor[0]][neighbor[1]] != 3:
                    grid[neighbor[0]][neighbor[1]] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw_grid()
        pygame.display.flip()  # Actualiza la pantalla
        time.sleep(speed)

    return []

# Algoritmo DFS
def dfs(start, end, grid, cols, rows, draw_grid, speed=0.5):
    stack = [start]
    came_from = {start: None}
    visited = set()
    visited.add(start)

    while stack:
        current = stack.pop()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid, cols, rows):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                came_from[neighbor] = current
                if grid[neighbor[0]][neighbor[1]] != 3:
                    grid[neighbor[0]][neighbor[1]] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw_grid()
        pygame.display.flip()  # Actualiza la pantalla
        time.sleep(speed)

    return []
