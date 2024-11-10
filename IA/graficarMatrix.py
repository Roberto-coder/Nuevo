import matplotlib.pyplot as plt
import numpy as np

# Definir la matriz con 1 y 0 (1: cuadros negros, 0: cuadros blancos)
grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
])

# Función para manejar los clics
def on_click(event):
    # Obtener las coordenadas del clic
    x = event.xdata
    y = event.ydata

    # Verificar si el clic está dentro del rango de la matriz
    if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
        # Determinar la celda correspondiente
        grid_x = int(x)
        grid_y = int(y)
        
        # Verificar si el clic está dentro de la celda (considerando el tamaño del cuadrado)
        if grid[grid_y, grid_x] == 0:  # Si es 0 (cuadro blanco)
            grid[grid_y, grid_x] = 2  # Marcar la celda como pulsada
            ax.add_patch(plt.Rectangle((grid_x, grid_y), 1, 1, color='blue', alpha=0.5))  # Color azul semitransparente
            plt.draw()  # Actualizar la gráfica
        else:  # Si es 1 o 2, mostrar mensaje
            print("Ingrese una posición válida o ya pulsada")

# Dibujar la matriz usando plt.plot()
fig, ax = plt.subplots()

# Crear el grid de 1 y 0
for i in range(grid.shape[0]):  # Filas
    for j in range(grid.shape[1]):  # Columnas
        color = 'black' if grid[i, j] == 1 else 'white'
        ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))  # Dibujar cada celda como un rectángulo

# Ajustes de la gráfica
ax.set_aspect('equal')  # Asegurarse de que los cuadros sean cuadrados
ax.set_xticks([])  # Sin etiquetas en los ejes x
ax.set_yticks([])  # Sin etiquetas en los ejes y

# Conectar el evento de clic con la función on_click
cid = fig.canvas.mpl_connect('button_press_event', on_click)

plt.xlim(-0.5, grid.shape[1] - 0.5)  # Ajustar límites x
plt.ylim(-0.5, grid.shape[0] - 0.5)  # Ajustar límites y
plt.grid(False)  # Sin cuadrícula

plt.show()
