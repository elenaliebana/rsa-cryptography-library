"""
imatlab.py

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin par´ametros,
lanzará la interfaz de usuario para el modo interactivo.
"""

from typing import TextIO
from typing import Tuple, List, Dict
import modular
import sys

def leer_comando(linea:str) -> Tuple[str, list]:
    """ Lee el comando y lo separa en función y argumentos
    
        Args:
            linea (str): Línea con un comando.
    
        Returns:
            str: Nombre de la función
            list: lista con los argumentos
    """
    linea = linea.strip()
    
    # Leer comando
    pos1 = linea.find("(")   # posición del primer "("
    pos2 = linea.rfind(")")    # posición del último ")"

    funcion = linea[:pos1].strip()
    args_str = linea[pos1 + 1 : pos2] 
    args = args_str.split(",") # argumentos en una lista

    return funcion, args

def procesar_comando(funcion: str, args: list) -> str:
    """ Procesa el comando

    Args:
        funcion (str): Funcion a procesar
        args (list): argumentos para la función

    Returns:
        str: Resultado del comando, o "NE" si no existe solución, o "NOP" si el
        comando no existe o hay un error en la llamada.
    """

    try:
        if funcion == "primo":
            n = int(args[0])
            if modular.es_primo(n):
                return "Sí"
            else:
                return "No"
           
        elif funcion == "primos":
            a = int(args[0])
            b = int(args[1])
            lista = modular.lista_primos(a, b)

            if not lista: # Lista vacía
                return "NE"
            
            lista_str = ""
            for i in lista:
                lista_str += str(i) + ", "

            lista_str = lista_str[:-2]  # quita la ", " sobrante del final

            return lista_str

        elif funcion == "factorizar":
            n = int(args[0])

            if n in (-1, 0, 1):
                return str(n)
            
            fact = modular.factorizar(n)

            result = ""
            for k, v in fact.items():
                result += str(k) + ": " + str(v) + ", "

            result = result[:-2]  
            return result

        elif funcion == "mcd":
            numeros = []
            for i in args:
                numeros.append(int(i))

            return str(modular.mcd_n(numeros))

        elif funcion == "coprimos":
            a = int(args[0])
            b = int(args[1])
            if modular.coprimos(a,b):
                return "Sí"
            else:
                return "No"

        elif funcion == "pow":
            base = int(args[0])
            exp = int(args[1])
            p = int(args[2])
            return str(modular.potencia_mod_p(base, exp, p))

        elif funcion == "inv":
            n = int(args[0])
            p = int(args[1])
            return str(modular.inversa_mod_p(n, p))

        elif funcion == "euler":
            n = int(args[0])
            return str(modular.euler(n))

        elif funcion == "legendre":
            n = int(args[0])
            p = int(args[1])

            return str(modular.legendre(n, p))

        elif funcion == "resolverSistema":
            alist, blist, plist = [], [], []
            for entrada in args:
                entrada = entrada[1:-1] # quitar los corchetes de cada lista
                lst = entrada.split(";")
                alist.append(int(lst[0]))
                blist.append(int(lst[1]))
                plist.append(int(lst[2]))

            r, m = modular.resolver_sistema_congruencias(alist, blist, plist)
            return f"{r} (mod {m})"

        elif funcion == "raiz":
            n = int(args[0])
            p = int(args[1])
            x1 = modular.raiz_mod_p(n, p)
            x2 = (p - x1) % p
            menor, mayor = min(x1, x2), max(x1, x2)
            if menor == mayor:
                return f"{menor}"
            return f"{menor}, {mayor}"

        elif funcion == "ecCuadratica":
            a = int(args[0])
            b = int(args[1])
            c = int(args[2])
            p = int(args[3])
            x1, x2 = modular.ecuacion_cuadratica(a, b, c, p)

            if x1 == x2:
                return str(x1)
            menor, mayor = min(x1, x2), max(x1, x2)
            return f"{menor}, {mayor}"

        else: # No existe el comando
            return "NOP"

    except modular.IncompatibleEquationError: # IncompatibleEquationError --> No existe solución
        return "NE"
    except ZeroDivisionError:
        return "NE"
    except Exception: # Cualquier otra excepción --> Error en la llamada
        return "NOP"

def run_commands(fin:TextIO,fout:TextIO):
    """ Recibe un manejador fin de un fichero de texto ya abierto para lectura y otro de un fichero de salida
    ya abierto para escritura y ejecuta línea por línea los comandos proporcionados por fin, escribiendo los resultados en fout.
    Si fin y fout no corresponden con la entrada y salida esáandar, esta función ejecuta el modo de procesamiento
    por lotes de IMAT-LAB para la entrada fin, guardando el resultado en el fichero fout.

    Args:
        fin (TextIO): Fichero de entrada. Manejador de un fichero de texto ya abierto para lectura.
        fout (TextIO): Fichero de salida. Manejador de un fichero de texto ya abierto para escritura.
    
    Returns: None
    
    Raises: None
    
    Examples:
        run_commands(sys.stdin,sys.stdout) lanza el modo interactivo y ejecuta línea por línea los comandos que
            el usuario lanza desde la entrada estándar.
    """
    
    for linea in fin:
        linea = linea.strip()
        if linea == "": # Final del fichero
            return
        funcion, args = leer_comando(linea)
        resultado = procesar_comando(funcion, args)
        fout.write(resultado + "\n") # Escribe el resultado en fout
        
if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_commands(sys.stdin, sys.stdout)
    else:
        with open(sys.argv[1], "r") as fin, open(sys.argv[2], "w") as fout:
            run_commands(fin, fout)