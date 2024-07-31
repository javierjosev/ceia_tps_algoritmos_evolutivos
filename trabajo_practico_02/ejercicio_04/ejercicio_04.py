from pyswarm import pso
import numpy as np


# Definición de las funciones del sistema de ecuaciones
def f1(x):
    x1, x2 = x
    return x1 * 3 + x2 * 2 - 9  # Ejemplo de una ecuación


def f2(x):
    x1, x2 = x
    return x1 - x2 * 5 - 4  # Ejemplo de otra ecuación


# Funcion objetivo: Distancia cuadratica del sistema de ecuaciones lineales
def funcion_objetivo(x):
    return f1(x) ** 2 + f2(x) ** 2


# Parámetros del algoritmo
num_particulas = 20  # numero de particulas
cantidad_iteraciones = 200  # maximo numero de iteraciones
c1 = 2.0  # componente cognitivo
c2 = 2.0  # componente social
w = 0.7  # factor de inercia
limite_inf = [-10, -10]  # limite inferior de busqueda
limite_sup = [10, 10]  # limite superior de busqueda

# Ejecutar PSO para encontrar la solución
xopt, fopt = pso(
    funcion_objetivo,
    limite_inf,
    limite_sup,
    swarmsize=num_particulas,
    maxiter=cantidad_iteraciones,
    phip=c1,
    phig=c2,
    omega=w,
)

print("Solución encontrada:")
print("x1 =", xopt[0])
print("x2 =", xopt[1])
