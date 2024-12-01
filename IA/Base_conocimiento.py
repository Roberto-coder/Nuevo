#Base de conocimientos ampliada con oraciones positivas y negativas
oraciones = [
    ["Juan", "ama","Maria"],
    ["Maria", "ama", "Pedro"],
    ["Pedro", "odia", "Luis"],
    ["Luis", "admira", "Juan"],
    ["Ana", "ayuda", "Maria"],
    ["El gato", "persigue", "el raton"],
    ["El raton", "come", "queso"],
    ["El queso", "es", "amarillo"],
    ["Luis", "visita", "Ana"],
    ["Ana", "trabaja", "en la biblioteca"],
    ["Carlos", "enseña", "Matemáticas"],
    ["Sara", "no lee", "un libro"],
    ["Un libro", "es", "interesante"],
    ["La niña", "no come", "una manzana"],
    ["El perro", "persigue", "el gato"]
]

# Pacientes con sus sintomas asociados 
pacientes = [
    ["Juan", ["tos", "fiebre", "dificultad para respirar"]],
    ["Ana", ["diarrea", "dolor abdominal","vómitos"]],
    ["Carlos", ["sed excesiva", "orinar frecuentemente", "visión borrosa"]],
    ["Luis", ["tos", "fiebre", "escalofrios"]],
    ["Maria", ["calambres abdominales", "nauseas", "pérdida de apetito"]], 
    ["Sofia", ["fatiga", "pérdida de peso", "heridas que no cicatrizan"]], 
    ["Pedro", ["dalor de pecho", "dificultad para respirar", "escalofrios"]],
    ["Laura", ["diarrea", "calambres abdominales", "fatiga"]],
    ["Diego", ["sed excesiva", "visión borrosa", "heridas que no cicatrizan"]],
    ["Carmen", ["fiebre", "dolor de cabeza", "tos"]]
]

# Enfermedades con sus sintomas caracteristicos
enfermedades = [
    ["infección respiratoria", ["tos", "fiebre", "dificultad para respirar", "escalofrios"]],
    ["gastroenteritis", ["diarrea", "dolor abdominal", "nauseas", "vomitos"]],
    ["diabetes", ["sed excesiva", "orinar frecuentemente", "visión borrosa", "fatiga"]]
]

diagnosticos = []

for i in range(len(pacientes)):
    nombre_paciente = pacientes[i][1]
    paciente_sintomas = pacientes[i][0]
    
    coincidencias_total = 0
    enfermedad_diagnosticada = "No se"
    for j in range(len(enfermedades)):
        nombre_enfermedad = enfermedades[j][1]
        nombre_sintoma= enfermedades[j][0]
        
        coincidencias = 0
        for k in range(len(paciente_sintomas)):
            for l in range(len(nombre_sintoma)):
                if paciente_sintomas[k] == nombre_sintoma[l]:
                    coincidencias += 1
        
        if coincidencias > coincidencias_total :
            coincidencias_total = coincidencias
            enfermedad_diagnosticada = nombre_enfermedad
    
    diagnosticos = diagnosticos + [(nombre_paciente, enfermedad_diagnosticada)]
    
for m in range(len(diagnosticos)) :
    print(f"{diagnosticos[m][0]}: Diagnostico probable -> {diagnosticos[m][1]}")