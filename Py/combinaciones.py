from itertools import permutations

# Definir los nodos del grafo
nodos = ['A', 'B', 'C', 'D', 'E']

# Definir los pesos de las aristas en un diccionario
pesos = {
    ('A', 'B'): 14, ('A', 'C'): 21, ('A', 'D'): 17, ('A', 'E'): 34,
    ('B', 'C'): 10, ('B', 'D'): 14, ('B', 'E'): 23,
    ('C', 'D'): 21, ('C', 'E'): 22,
    ('D', 'E'): 31
}

# Añadir las aristas en ambos sentidos (porque es un grafo no dirigido)
pesos.update({(v, u): w for (u, v), w in pesos.items()})

# Obtener todas las permutaciones de los nodos restantes (sin incluir 'A')
permutaciones_nodos = permutations(nodos[1:])

# Generar todas las rutas que comiencen y terminen en 'A'
rutas = []
for perm in permutaciones_nodos:
    ruta = ['A'] + list(perm) + ['A']
    rutas.append(ruta)

# Calcular la suma de los pesos para cada ruta
rutas_con_sumas = []
for ruta in rutas:
    suma_pesos = sum(pesos[(ruta[i], ruta[i+1])] for i in range(len(ruta) - 1))
    rutas_con_sumas.append((ruta, suma_pesos))

# Mostrar todas las rutas posibles y sus sumas de pesos
for ruta, suma in rutas_con_sumas:
    print(f"Ruta: {' -> '.join(ruta)}, Suma de pesos: {suma}")

