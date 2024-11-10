import time
import tracemalloc
import random


def Bfs(grafo, nodo_raiz, solucion):
	##Medicion de tiempo
	tracemalloc.start()
	start_time = time.perf_counter()
    ##Definir una lista/arreglo que vaya guardando los nodos
	previos = [nodo_raiz]
    ##Definir una lista o arreglo para guardar los nodos visitados
	visitados = [False]*(len(grafo)+1)
	##Cambiar a true o a 1 el nodo raiz en visitados
	visitados[nodo_raiz] = True

	i = 0
	while i < len(previos) :
		##Llegamos a un nivel i
		nodo_actual = previos[i]
		##Condicion que corrobere si aun no se encuentra la solucion
		print(nodo_actual)
		if solucion == nodo_actual :
			print("Se encontró la solución en el nivel " + str(i-1))
			print("Solucion " + str(nodo_actual))
			end_time =time.perf_counter()
			current, peak = tracemalloc.get_traced_memory()
			tracemalloc.stop()

			print("El tiempo de ejecucion fue de: ", end_time-start_time)
			print(f'La memoria consumida fue de:  {current/10**6} MB, Pico de uso: {peak/10**6}MB.')
			break

		
		#Recorremos los nodos de ese nivel
		for vecino in grafo[nodo_actual] :
			if not visitados[vecino] :##Si falso 0, SI no han sido visitados

				##Cambiamos el nodo que ya visite a True siempre que
				##este no haya sido visitado
				visitados[vecino] = True
				##Se agrega al nodo previo el nodo vecino
				#QUITAR EL APPEND previos.append(vecino)
				previos += [vecino]

		i= i + 1


def Dfs(grafo, nodo_raiz, solucion):

	pila = [nodo_raiz]

	##Medicion de tiempo
	tracemalloc.start()
	start_time = time.perf_counter()
    ##Definir una lista/arreglo que vaya guardando los nodos
	previos = [nodo_raiz]
    ##Definir una lista o arreglo para guardar los nodos visitados
	visitados = [False]*(len(grafo)+1)
	##Cambiar a true o a 1 el nodo raiz en visitados
	visitados[nodo_raiz] = True

	i = 0

	if solucion == nodo_raiz:
		print("Se encontró la solución en el nodo raiz " + str(nodo_raiz))
		end_time =time.perf_counter()
		current, peak = tracemalloc.get_traced_memory()
		tracemalloc.stop()
		print("El tiempo de ejecucion fue de: ", end_time-start_time)
		print(f'La memoria consumida fue de:  {current/10**6} MB, Pico de uso: {peak/10**6}MB.')
		exit();
	while len(pila)>0 :

		nodo_actual = pila[-1]
		print("El nodo actual es:", nodo_actual)
		pila=pila[:-1]
		#Recorremos los nodos de ese nivel
		for vecino in grafo[nodo_actual] :
			if solucion == nodo_actual :
				print("Se encontró la solución " + str(nodo_actual))
				end_time =time.perf_counter()
				current, peak = tracemalloc.get_traced_memory()
				tracemalloc.stop()
				print("El tiempo de ejecucion fue de: ", end_time-start_time)
				print(f'La memoria consumida fue de:  {current/10**6} MB, Pico de uso: {peak/10**6}MB.')
				exit();
			if not visitados[vecino] :##Si falso 0

				##Cambiamos el nodo que ya visite a True siempre que
				##este no haya sido visitado
				visitados[vecino] = True
				##Se agrega al nodo previo el nodo vecino
				#QUITAR EL APPEND previos.append(vecino)
				#pila.append(vecino)
				pila+= [vecino]

	end_time =time.perf_counter()
	current, peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()

	print("El tiempo de ejecucion fue de: ", end_time-start_time)
	print(f'La memoria consumida fue de:  {current/10**6} MB, Pico de uso: {peak/10**6}MB.')

grafo = {
	1: [2,3],
	2: [1,4,5],
	3: [1,6],
	4: [2],
	5: [2],
	6: [3]
}

solucion=random.randint(0,len(grafo))
print("La solucion a encontrar es: "+ str(solucion))
print("-----------BFS---------")
Bfs(grafo, 1, solucion)
print("-----------DFS---------")
Dfs(grafo, 1, solucion)