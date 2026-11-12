# Modular Arithmetic and RSA Library

A number-theory library and an RSA implementation written in Python, with an interactive command interpreter, two attacks on RSA and a small encrypted chat. Course project for Discrete Mathematics.

## What is inside

| File | Content |
|---|---|
| `code/modular.py` | Modular arithmetic library |
| `code/rsa.py` | RSA key generation, encryption, decryption and attacks |
| `code/imatlab.py` | IMAT-LAB: command interpreter (interactive and batch) for `modular.py` |
| `code/criptochat.py` | Encrypted command-line chat between two users |
| `docs/` | Reports (in Spanish) |

## `modular.py`

| Function | Idea |
|---|---|
| `es_primo` | Miller–Rabin primality test (20 rounds) |
| `lista_primos`, `factorizar` | Primes in an interval; factorization with **Pollard's rho** |
| `mcd`, `bezout`, `mcd_n`, `bezout_n`, `coprimos` | Euclid's algorithm, extended Euclid, versions for lists |
| `potencia_mod_p` | Fast modular exponentiation (square-and-multiply), also for negative exponents |
| `inversa_mod_p`, `euler` | Modular inverse, Euler's totient |
| `legendre` | Legendre symbol |
| `resolver_sistema_congruencias` | Systems of linear congruences with the **Chinese Remainder Theorem**, including non-coprime moduli |
| `raiz_mod_p`, `ecuacion_cuadratica` | Modular square roots (**Cipolla's algorithm**) and quadratic equations modulo p |

Impossible problems raise custom exceptions (`SinSolucionError`, `RaizNoExisteError`). The first version used trial division; Miller–Rabin and Pollard's rho make it possible to factor moduli of more than 20 digits.

## `rsa.py`

- `generar_claves` – key generation from two random primes in an interval.
- `cifrar_cadena_rsa` / `descifrar_cadena_rsa` – character-by-character text encryption, with optional random decimal padding.
- `romper_clave` – recovers the private key by factoring `n`.
- `ataque_texto_elegido` – **chosen-plaintext attack** on text encrypted with unpadded RSA.
- `ataque_opcional` – attack on padded messages with unknown padding length.

## IMAT-LAB (`imatlab.py`)

Evaluates one command per line: `primo`, `primos`, `factorizar`, `mcd`, `coprimos`, `pow`, `inv`, `euler`, `legendre`, `resolverSistema`, `raiz` and `ecCuadratica`. It answers `NE` when there is no solution and `NOP` for an invalid command.

```bash
cd code
python imatlab.py                 # interactive mode
python imatlab.py input.txt out.txt   # batch mode
```

## Encrypted chat (`criptochat.py`)

```bash
cd code
python criptochat.py alice bob
```

It reads `Usuarios/pub_<user>.txt` and `Usuarios/priv_<user>.txt`. A public key file has three lines (`n`, `e`, number of padding digits); a private key file has one line (`d`). These files are not included. Option `C` encrypts a message with the other user's public key, `D` decrypts one with your private key and `S` exits.

## Using the library

```python
import modular, rsa

modular.factorizar(360)                                         # {2: 3, 3: 2, 5: 1}
modular.resolver_sistema_congruencias([1, 4], [1, 7], [3, 11])  # (10, 33)

n, e, d = rsa.generar_claves(10**12, 10**12 + 400)
c = rsa.cifrar_cadena_rsa("Hola", n, e, 2)
rsa.descifrar_cadena_rsa(c, n, d, 2)                            # 'Hola'
```

`generar_claves(min, max)` tests every number in the interval, so keep it narrow. Requires Python 3.8 or newer.
