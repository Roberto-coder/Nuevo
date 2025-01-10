import numpy as np
import matplotlib.pyplot as plt

# Datos iniciales
X = np.array([2019, 2020, 2021, 2022, 2023, 2024])
yd = np.array([4.0, 5.0, 6.5, 7.0, 8.5, 12.0])

# Nueva normalización: Z-score
def normalizacion_zscore(X):
    X_mean = np.mean(X)
    X_std = np.std(X)
    return (X - X_mean) / X_std

# Normalizamos los datos
X_norm = normalizacion_zscore(X)

# Depuración: Imprimir los valores normalizados
print("Valores normalizados de X:", X_norm)

# Definición de hiperparámetros
lr = 0.01
epocas_max = 5000
b0 = 0.1  # Inicialización aleatoria
b1 = 0.2
lamda = 0.001
epsilon = 1e-6  # Tolerancia para Early Stopping

m = len(X_norm)
grafica = []

# Entrenamiento con Early Stopping
epoch_count = 0
for epoch in range(epocas_max):
    Yobt = b0 + b1 * X_norm

    # Cálculo de la función de costo ECM con regularización
    J = (1 / (2 * m)) * np.sum((Yobt - yd) ** 2) + (lamda / 2) * np.sum(b1 ** 2)
    grafica.append(J)

    # Actualización de parámetros
    b0_new = b0 - lr * (1 / m) * np.sum(Yobt - yd)
    b1_new = b1 - lr * (1 / m) * np.sum((Yobt - yd) * X_norm) + (lamda / m) * b1

    # Verificar Early Stopping
    if epoch > 0 and abs(grafica[-1] - grafica[-2]) < epsilon:
        print(f"Early Stopping activado en la época {epoch + 1}")
        epoch_count = epoch + 1
        break

    # Actualizar parámetros
    b0, b1 = b0_new, b1_new
else:
    epoch_count = epocas_max

# Resultados finales
print("Parámetro b0: ", b0)
print("Parámetro b1: ", b1)
print("Épocas utilizadas: ", epoch_count)

# Graficar función de costo
plt.figure(figsize=(8, 6))
plt.plot(range(len(grafica)), grafica, label="Función de costo")
plt.xlabel("Épocas")
plt.ylabel("Función de costo")
plt.title("Función de costo vs Épocas")
plt.legend()
plt.show()

# Graficar datos y regresión
plt.figure(figsize=(8, 6))
for i in range(m):
    plt.scatter(X_norm[i], yd[i], color="blue")

x_val = [min(X_norm), max(X_norm)]
y_val = [b0 + b1 * X for X in x_val]
plt.plot(x_val, y_val, color="red")
plt.title("Regresión Lineal")
plt.xlabel("X Normalizado")
plt.ylabel("Ventas (millones)")
plt.show()

# Predicción
# X_test = float(input("Introduzca el año a predecir: "))
# X_test_norm = normalizacion_zscore(np.array([X_test]))[0]
# Y_test = b0 + b1 * X_test_norm
# print(f"Para el año {X_test} se estiman {Y_test} millones de ventas")
