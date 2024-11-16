prisionero1="traicionar"
prisionero2="traicionar"


def evaluacion_prisionero(prisionero1,prisionero2):
	if prisionero1 == "Cooperar" and prisionero2=="Cooperar" :
		return(3,3)
	elif prisionero1 == "Cooperar" and prisionero2=="Traicionar" :
		return(5,0)
	elif prisionero1 == "Traicionar" and prisionero2=="Cooperar" :
		return(0,5)
	else:
		return(10,10)

sentencia=evaluacion_prisionero(prisionero1,prisionero2)

##print(evaluacion_prisionero(prisionero1,prisionero2))
print(f"El prisionero 1 tiene una condena de: {sentencia[0]} años")
print(f"El prisionero 2 tiene una condena de: {sentencia[1]} años")
