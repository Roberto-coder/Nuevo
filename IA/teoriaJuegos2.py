import numpy as np
import matplotlib.pyplot as plt

##En este ejemplo se parte de la logica de tener un agente que en un plano cartesiano, donde este se puede mover en cualquier
##direccion, encuentra el punto de meta a travez de sumar su posicion en 1 en cada iteracion 

meta=[5,9]

def buscador(meta):
	pos_objeto = (np.random.randint(0,20), np.random.randint(0,20))

	##Definimos 2 variables para cada posicion
	posicion_objeto_x = pos_objeto[0]
	posicion_objeto_y = pos_objeto[1]

	##Listas para el guardado de las diferentes posiciones
	camino_x = [None]*400
	camino_y = [None]*400

	cantidad_movimientos = 0;

	while (pos_objeto != meta) :
		if posicion_objeto_x < meta[0] :
			posicion_objeto_x = posicion_objeto_x+1
		elif posicion_objeto_x < meta[0] :
			posicion_objeto_x = posicion_objeto_x-1
		camino_x[cantidad_movimientos] = posicion_objeto_x

		if posicion_objeto_y < meta[1] :
			posicion_objeto_y = posicion_objeto_y+1
		elif posicion_objeto_x < meta[1] :
			posicion_objeto_y = posicion_objeto_y-1
		camino_y[cantidad_movimientos] = posicion_objeto_y

		cantidad_movimientos=cantidad_movimientos+1

		pos_objeto[0] = posicion_objeto_x
		pos_objeto[1] = posicion_objeto_y

	return camino_x, camino_y


camino_x, camino_y = buscador(meta)

