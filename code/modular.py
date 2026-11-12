"""
modular.py

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict
import random

class IncompatibleEquationError(Exception):
    pass

class SinSolucionError(IncompatibleEquationError):
    """ La ecuación o el sistema no tiene solución. """
    pass

class RaizNoExisteError(IncompatibleEquationError):
    """ El número no es un cuadrado módulo p, por lo que no tiene raíz. """
    pass


def es_primo(n:int)->bool:
    """ Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None
    
    Examples:
        es_primo(5)=True
        es_primo(4)=False
    """
    if n < 2:
        return False
    elif n == 2 or n == 3:
        return True
    elif n % 2 == 0:
        return False

    # Test de Miller-Rabin (utilizando el pseudocódigo de las fuentes citadas)
    # n - 1 = 2^s * d con d impar
    d = n - 1 
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1

    k = 20 # 20 rondas
    for i in range(k):
        a = random.randrange(2, n)

        fpp = False
        x = potencia_mod_p(a, d, n)            
        if x == 1:
            fpp = True
        else:
            r = 0
            while r < s and fpp == False:
                if n-1 == potencia_mod_p(a, 2**r * d, n):                  
                    fpp = True              
                r += 1

        if fpp == False:                        
            return False

    return True                                 
   

def lista_primos(a,b)-> List[int]:
    """ Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
    """
    lista_primos = []
    for n in range(a, b):
        if es_primo(n):
            lista_primos.append(n)

    return lista_primos

def factorizar(n:int)->Dict[int,int]:
    """ Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    """

    if n in (-1, 0, 1):
        return {}

    dict_factores = {}
    n = abs(n)

    # Quitamos antes las potencias de 2 para que funcione mejor
    while n % 2 == 0:
        if 2 in dict_factores:
            dict_factores[2] += 1
        else:
            dict_factores[2] = 1
        n = n // 2

    nums = [] # guarda los números que aún no sabemos si son primos o compuestos
    if n > 1:
        nums.append(n)

    while len(nums) > 0:
        m = nums.pop()

        if es_primo(m):
            # m es primo: lo apuntamos como factor
            if m in dict_factores:
                dict_factores[m] += 1
            else:
                dict_factores[m] = 1
        else:
            # Algoritmo rho de Pollard (utilizando el pseudocódigo de las fuentes citadas)
            c = 0
            d = m

            while d == m: # si d = m, el algoritmo falla y hay que probar con otra funcion
                c += 1
                x = 2               
                y = x
                d = 1

                # g(x) = (x^2 + c) mod m
                while d == 1:
                    x = (x * x + c) % m # x <- g(x)

                    y = (y * y + c) % m 
                    y = (y * y + c) % m # y <- g(g(y))

                    d = mcd(abs(x - y), m) # d <- mcd(|x - y|, m)

            # d es un divisor de m: estudiamos por separado d y m / d
            nums.append(d)
            nums.append(m // d)

    return dict_factores
             


def mcd(a:int,b:int)->int:
    """ Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples:
        mcd(10,15)=5
    """
    a, b = abs(a), abs(b)

    while b != 0:
        a, b = b, a % b

    return a


def bezout(n:int, m:int) -> Tuple[int,int,int]:
    """ Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
            d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples:
        bezout(6,10)=(2,2,-1)
    """

    x0, y0 = 1, 0 # n = (1,0)
    x1, y1 = 0, 1 # m = (0,1)

    while m != 0:
        c = n // m
        r = n % m

        n, m = m, r

        x0, x1 = x1, x0 - c*x1
        y0, y1 = y1, y0 - c*y1

    if n < 0: # el mcd debe ser positivo
        n, x0, y0 = -n, -x0, -y0
    return(n, x0, y0)

def mcd_n(nlist:List[int])->int:
    """ Dados una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples:
        mcd([4,10,14])=2
    """
    d = nlist[0]
    for a in nlist[1:]:
        d = mcd(d,a)

    return d


def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    """ Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    d, x, y = bezout(nlist[0], nlist[1])
    coefs = [x, y]

    for a in nlist[2:]:
        d, x, y = bezout(d, a)
        new_coefs = []
        for c in coefs:
            new_coefs.append(c*x)

        coefs = new_coefs
        coefs.append(y)

    return d, coefs


def coprimos(n:int,m:int)->bool:
    """ Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True
    """
    divisor = mcd(n,m)
    return divisor == 1
    
def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """ Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si la base y el exponente
        son ambos 0 al mismo tiempo.

    Examples:
        potencia_mod_p(2,3,7)=1
    """
    if base == 0 and exp == 0:
        raise ZeroDivisionError("0^0 no está definido")
    
    base = base % p

    if base == 0:
        if exp > 0:
            return 0
        else:
            return 1 % p

    if exp < 0 and es_primo(p): # Pequeño teorema de Fermat 
        exp = exp % (p - 1)

    if exp < 0:
        # base^(-k) mod p = (inversa de base mod p)^k mod p
        base = inversa_mod_p(base, p)
        exp = -exp

    # En lugar de utilizar el operador **, hemos investigado una técnica de exponenciación modular más rápida
    resultado = 1
    while exp > 0:
        if exp % 2 == 1:         
            resultado = (resultado * base) % p   
        base = (base * base) % p  
        exp //= 2                 

    return resultado


def inversa_mod_p(n:int,p:int)->int:
    """ Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    """
    d, x, y = bezout(p, n)

    if d != 1:
        raise ZeroDivisionError(f"No existe inversa de {n} módulo {p}")

    return y % p

def euler(n:int)->int:
    """ Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8
    """
    primo = es_primo(n)

    if primo:
        phi = n-1
    else:
        fact = factorizar(n)
        phi = 1
        for p, k in fact.items():
            phi *= (p - 1) * p**(k-1)

    return phi


def legendre(n:int,p:int)->int:
    """ Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0
    """

    n_mod = n % p

    if n_mod == 0:
        return 0

    # Si encuentra un k / n ≡ k^2 (mod p) --> 1
    for k in range(1, p):
        if (k * k) % p == n_mod:
            return 1

    return -1


def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    """ Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.

    Examples:
        resolver_sistema_congruencias([2],[3],[5]])=(4,5)
        resolver_sistema_congruencias([2],[4],[6])=(2,3)
        resolver_sistema_congruencias([1,4],[1,7],[3,11])=(10,33)
    """
    num = len(alist)
    clist = []
    plist_new = []

    # Calcular los coeficientes nuevos para que x tenga coeficiente 1
    for i in range(num):
        a, b, p = alist[i], blist[i], plist[i]
        d = mcd(a,p) # Ver si a y p son coprimos

        if b % d != 0:
            raise SinSolucionError(f"La ecuación {i + 1} no tiene solución")# Si a y bo no son coprimos y b no divide a d no hay solución
        
        a_new, b_new, p_new = a // d, b // d, p // d # Si b divide a d dividimos todo por d
        plist_new.append(p_new) # Utilizamos los nuevos módulos

        c = (inversa_mod_p(a_new, p_new) * b_new) % p_new # Calculamos el nuevo coeficiente
        clist.append(c)


    # Ejercicio 12: módulos no coprimos entre sí (referencia en Bibliografía)
    # Separamos los módulos en potencias de primos y para cada primo q nos quedamos con la ecuación de mayor potencia.
    mejor = {} 
    for i in range(num):
        factores = factorizar(plist_new[i]) # Factorizamos el módulo
        for q in factores:
            m = q ** factores[q] # Potencia 
            r = clist[i] % m # Usamos el resto para tener un número menor que el módulo
            if q not in mejor:
                mejor[q] = (m, r) # Primera ecuación con ese primo
            else:
                m_viejo, r_viejo = mejor[q]
                if m > m_viejo: # La nueva ecuación es más fuerte que la guardada
                    if r % m_viejo != r_viejo: # Si no coinciden los restos, hay contradicción
                        raise SinSolucionError("El sistema no tiene solución")
                    mejor[q] = (m, r) # Guardamos la nueva
                elif r_viejo % m != r: # La guardada es más fuerte. Comprobamos que no contradice a la nueva
                    raise SinSolucionError("El sistema no tiene solución")

    # Ahora los módulos son coprimos
    clist = []
    plist_new = []
    for q in mejor:
        plist_new.append(mejor[q][0])
        clist.append(mejor[q][1])
    num = len(plist_new) # Número de ecuaciones que quedan

    # M (módulo de la solución) = p1*...*pn
    M = 1
    for mod in plist_new:
        M *= mod

    # Construir la solución: a1*N1*x1 + ... + an*Nn*xn
    sol = 0
    for j in range(num):
        a = clist[j]
        N = M // plist_new[j]
        try:
            x = inversa_mod_p(N, plist_new[j])
        except ZeroDivisionError:
            raise SinSolucionError("Los módulos no son coprimos entre sí: el sistema no tiene solución")

        sol += a*N*x

    return sol % M, M

def raiz_mod_p(n:int,p:int)->int:
    """ Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.

    Examples:
        raiz_mod_p(2,7)=3
    """
    # Usando el algoritmo de Cipolla: referencia en Bibliografía
    n = n % p
    if n == 0:
        return 0
    if p == 2:
        return n

    # Criterio de Euler. Si n^((p-1)/2) no es 1, n no tiene raíz
    if potencia_mod_p(n, (p - 1) // 2, p) != 1:
        raise RaizNoExisteError(f"{n} no es un cuadrado módulo {p}, no tiene raíz cuadrada")

    # Buscar a > 0 tal que a^2 - n no sea un cuadrado: (a^2 - n | p) ≡ -1
    a = 1
    w2 = (a * a - n) % p            
    while potencia_mod_p(w2, (p - 1) // 2, p) != p - 1:
        a += 1
        w2 = (a * a - n) % p

    # Calcular (a + w)^((p+1)/2) 
    c, d = 1, 0                     
    e, f = a, 1                    
    exp = (p + 1) // 2
    while exp > 0:
        if exp % 2 == 1:
            # [c, d] * [e, f] = [c*e + w^2*d*f, d*e + c*f]
            c, d = (c * e + w2 * d * f) % p, (d * e + c * f) % p
        # [e, f] * [e, f] = [e*e + w^2*f*f, 2*e*f]
        e, f = (e * e + w2 * f * f) % p, (2 * e * f) % p
        exp //= 2

    return c

def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->Tuple[int,int]:
    """ Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación.

    Examples:
        ecuacion_cuadratica(4,1,3,11)
        ecuacion_cuadratica(4,1,5,11)=(3, 5)
        ecuacion_cuadratica(1,2,1,11)=(10,10)
    """
    try:
        D = raiz_mod_p(b * b - 4 * a * c, p)
    except RaizNoExisteError:
        raise SinSolucionError("La ecuación no tiene solución: el discriminante no es un cuadrado módulo p")
    
    d = inversa_mod_p(2 * a, p)

    x1 = ((-b + D) * d) % p
    x2 = ((-b - D) * d) % p

    return x1, x2