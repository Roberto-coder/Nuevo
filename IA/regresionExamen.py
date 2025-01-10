import numpy as np
import matplotlib.pyplot as plt

# Datos
anios = np.array([2017, 2018, 2019, 2020, 2021])
puertas = np.array([4, 2, 4, 2, 4])
litros = np.array([350, 359, 420, 450, 500])
ventas = np.array([2, 2.9, 3.5, 4.2, 5])

# Nueva normalización: Min-Max
def normalizacion_minmax(X, X_min=None, X_max=None):
    if X_min is None:
        X_min = np.min(X)
    if X_max is None:
        X_max = np.max(X)
    if X_max == X_min:
        return np.zeros_like(X)
    return (X - X_min) / (X_max - X_min), X_min, X_max

# Normalizamos los datos
anios_norm, anios_min, anios_max = normalizacion_minmax(anios)
puertas_norm, puertas_min, puertas_max = normalizacion_minmax(puertas)
litros_norm, litros_min, litros_max = normalizacion_minmax(litros)

# Matriz de características
X = np.column_stack((anios_norm, puertas_norm, litros_norm))
y = ventas

# Depuración: Imprimir los valores normalizados
print("Años normalizados:", anios_norm)
print("Puertas normalizadas:", puertas_norm)
print("Litros normalizados:", litros_norm)

# Definición de hiperparámetros
lr = 0.01
epocas_max = 5000
b = np.random.rand(4)  # Inicialización aleatoria de los parámetros (incluye b0)
lamda = 0.001
epsilon = 1e-6  # Tolerancia para Early Stopping

m = len(y)
grafica = []

# Añadir una columna de unos a X para el término de sesgo (b0)
X = np.hstack((np.ones((m, 1)), X))

# Función para calcular Yobt sin usar @
def calcular_Yobt(X, b):
    Yobt = np.zeros(m)
    for i in range(m):
        Yobt[i] = b[0] + b[1] * X[i, 1] + b[2] * X[i, 2] + b[3] * X[i, 3]
    return Yobt

# Entrenamiento con Early Stopping
for epoch in range(epocas_max):
    Yobt = calcular_Yobt(X, b)

    # Cálculo de la función de costo ECM con regularización
    J = (1 / (2 * m)) * np.sum((Yobt - y) ** 2) + (lamda / 2) * np.sum(b[1:] ** 2)
    grafica.append(J)

    # Actualización de parámetros
    b0_new = b[0] - lr * (1 / m) * np.sum(Yobt - y)
    b1_new = b[1] - lr * (1 / m) * np.sum((Yobt - y) * X[:, 1]) + (lamda / m) * b[1]
    b2_new = b[2] - lr * (1 / m) * np.sum((Yobt - y) * X[:, 2]) + (lamda / m) * b[2]
    b3_new = b[3] - lr * (1 / m) * np.sum((Yobt - y) * X[:, 3]) + (lamda / m) * b[3]

    # Verificar Early Stopping
    if epoch > 0 and abs(grafica[-1] - grafica[-2]) < epsilon:
        print(f"Early Stopping activado en la época {epoch + 1}")
        break

    # Actualizar los parámetros
    b = np.array([b0_new, b1_new, b2_new, b3_new])

print("Parámetros:", b)

# Graficar J
plt.figure(figsize=(8, 6))
plt.plot(range(len(grafica)), grafica, label="Función de costo")
plt.xlabel("Épocas")
plt.ylabel("Función de costo")
plt.title("Función de costo vs Épocas")
plt.legend()
plt.show()

# Predicción para 2023, 4 puertas, 550 litros
anios_test_norm = (2023 - anios_min) / (anios_max - anios_min)
puertas_test_norm = (4 - puertas_min) / (puertas_max - puertas_min)
litros_test_norm = (550 - litros_min) / (litros_max - litros_min)

X_test = np.array([1, anios_test_norm, puertas_test_norm, litros_test_norm])
Y_test = np.dot(X_test, b)
print(f"Para el año 2023, con 4 puertas y 550 litros de combustible vendidos, se estiman {Y_test} millones de ventas")