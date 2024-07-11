from collections import defaultdict

# Crear diccionarios para almacenar sumas y conteos por año
sums = defaultdict(float)
counts = defaultdict(int)

# Leer datos desde el archivo de texto
with open('datosMetano.txt', 'r') as file:
    for line in file:
        year, value = line.split()
        year = int(year)
        value = float(value)
        sums[year] += value
        counts[year] += 1

# Calcular el promedio por año
averages = {year: sums[year] / counts[year] for year in sums}

# Mostrar los promedios anuales
for year in sorted(averages):
    print(f"{year}: {averages[year]:.2f}")
