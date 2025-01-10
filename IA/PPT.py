import random

def obtener_eleccion_usuario():
    eleccion = input("Elige piedra, papel o tijera: ").lower()
    while eleccion not in ["piedra", "papel", "tijera"]:
        eleccion = input("Entrada no válida. Elige piedra, papel o tijera: ").lower()
    return eleccion

def obtener_eleccion_maquina():
    opciones = ["piedra", "papel", "tijera"]
    return random.choice(opciones)

def determinar_ganador(usuario, maquina):
    if usuario == maquina:
        return "Empate"
    elif (usuario == "piedra" and maquina == "tijera") or \
         (usuario == "papel" and maquina == "piedra") or \
         (usuario == "tijera" and maquina == "papel"):
        return "Usuario"
    else:
        return "Máquina"

def jugar():
    print("¡Bienvenido al juego de Piedra, Papel o Tijera!")
    usuario = obtener_eleccion_usuario()
    maquina = obtener_eleccion_maquina()
    print(f"El usuario eligió: {usuario}")
    print(f"La máquina eligió: {maquina}")
    
    ganador = determinar_ganador(usuario, maquina)
    if ganador == "Empate":
        print("Es un empate!")
    elif ganador == "Usuario":
        print("¡Felicidades! Ganaste.")
    else:
        print("La máquina ganó. ¡Inténtalo de nuevo!")

if __name__ == "__main__":
    jugar()