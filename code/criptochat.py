import os
import sys
import rsa

if len(sys.argv) != 3:
    print("No se han introducido dos usuarios")
    sys.exit()

usuario1 = sys.argv[1]
usuario2 = sys.argv[2]

pub1 = "Usuarios/pub_" + usuario1 + ".txt"
priv1 = "Usuarios/priv_" + usuario1 + ".txt"
pub2 = "Usuarios/pub_" + usuario2 + ".txt"


falta = False
for fichero in [pub1, priv1, pub2]:
    if not os.path.exists(fichero):
        print("No existe el fichero", fichero)
        falta = True
if falta:
    sys.exit()


fichero = open(pub1)
n1 = int(fichero.readline())
e1 = int(fichero.readline())
padding1 = int(fichero.readline())
fichero.close()


fichero = open(priv1)
d1 = int(fichero.readline())
fichero.close()


fichero = open(pub2)
n2 = int(fichero.readline())
e2 = int(fichero.readline())
padding2 = int(fichero.readline())
fichero.close()


opcion = ""
while opcion != "S":

    opcion = input("Introduce una opción (C / D / S): ").strip().upper()

    if opcion == "C":
        texto = input("Escribe un texto a cifrar: ")
        cifrado_lista = rsa.cifrar_cadena_rsa(texto, n2, e2, padding2)

        cifrado_str = ""
        for i in cifrado_lista:
            cifrado_str += str(i) + " "

        print("Texto cifrado:", cifrado_str)

    elif opcion == "D":
        texto = input("Escribe un texto a descifrar: ")
        cifrado_lista = texto.split()

        try:
            numeros = []
            for s in cifrado_lista:
                numeros.append(int(s))

            descifrado = rsa.descifrar_cadena_rsa(numeros, n1, d1, padding1)
            print("Texto descifrado:", descifrado)

        except (ValueError, UnicodeEncodeError):
            print("Error: texto cifrado no válido")

    elif opcion != "S":
        print("Opción no válida")

print("Has salido del programa")     

