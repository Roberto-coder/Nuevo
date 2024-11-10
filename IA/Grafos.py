##Representacion grafica de los nodos

import networks as nx
import matplotlib.pyplot as plt

def graficar_grafos(grafo, nodo_raiz):
	G=nx.Graph()

	for nodo,vecinos in grafo.items():
		for vecino in vecinos:
			G.add_edge(nodo, vecino)

	##Graficar el grafico anterior
	pos = nx.spring_layout(G)
	nx.draw(G,pos,with_labels=True,node_color="lightblue",node_size=500,font_size=11,font_weight=18)
	plt.show()

grafo = {
	1: [2,3],
	2: [1,4,5],
	3: [1,6],
	4: [2],
	5: [2],
	6: [3]
}

graficar_grafos(grafo, 1)