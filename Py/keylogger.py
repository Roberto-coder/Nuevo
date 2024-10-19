#import keyboard
#keys = keyboard.record(until ='ENTER')
#keyboard.play(keys)

import keyboard

# Registrar las teclas hasta que se presione "ENTER"
keys = keyboard.record(until='ENTER')

# Guardar las teclas registradas en un archivo .txt
with open('teclas_registradas.txt', 'w') as f:
    for key in keys:
        f.write(f"{key.name}\n")

# Reproducir las teclas registradas
keyboard.play(keys)
