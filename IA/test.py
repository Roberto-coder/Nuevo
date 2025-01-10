
## Definicion de los daros de entrada
X = np.array([1.0,3.0,6.0,9.0,11.0,15.0,16.0,19.0,24.0])
## Dataset: Datos ocupados para hacer el entrenamiento
 yd = np.array([4.0,5.0,6.5,7.0,8.5,12.0,13.0,16.0,22.0])

## Definir ahora dataTEST
X_test = float(input("Ingrese el valor de X: "))
Y_test =b0 + b1*X_test
print("El valor de Y es: ",Y_test)

##Clasificacion
X_test_clas = float(input("Ingrese el valor de X: "))
Y_test_clas = float(input("Ingrese el valor de Y: "))
Y_obt_clas = b0 + b1*X_test_clas

if Y_obt_clas > Y_test_clas:
    print("El valor de Y es mayor al esperado")
else:
    print("El valor de Y es menor al esperado")
    
##############################################################

X = np.array([2019, 2020, 2021, 2022, 2023, 2024])
yd = np.array([4.0, 5.0 ,6.5 ,7.0 ,8.5 ,12.0])

X_norm = normalizacion(X)

def normalizacion(X):
    X_max = max(X)
    X_min = min(X)
    return (X-X_min)/(X_max-X_min)

X_test = float(input("Introdusca el año a predecir"))
X_norm= normalizacion(X_test)
Y_test = b0 + b1*X_norm
print("Para el año {X_test} se estiman {Y_test} millones de ventas")

X = X_norm
