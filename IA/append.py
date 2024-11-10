# Inicialización de la lista con un valor inicial
arr = [5]

# Función para agregar elementos usando índices
def agregar_a_pila(valor):
    # Expandir la lista en 1 unidad
    arr.append(None)  # Añadir un espacio vacío
    # Asignar el nuevo valor en la siguiente posición
    arr[len(arr) - 1] = valor
    print(f'Pila actual: {arr}')

# Solicitar valores al usuario
while True:
    nuevo_valor = input("Ingrese un valor para agregar a la pila (o 'salir' para terminar): ")
    if nuevo_valor.lower() == 'salir':
        break
    agregar_a_pila(int(nuevo_valor))

print("Programa terminado. Estado final de la pila:", arr)
