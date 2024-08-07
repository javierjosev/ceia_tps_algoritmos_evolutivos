import random

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from pyswarm import pso


def plot_function(
    expression_str,
    x_min_bound,
    x_max_bound,
    y_min_bound,
    y_max_bound,
    x_point=None,
    y_point=None,
):
    # Definir las variables simbólicas
    x, y = sp.symbols("x y")

    # Convertir la cadena en una expresión simbólica
    expression = sp.sympify(expression_str)

    # Convertir la expresión simbólica en una función numérica
    func = sp.lambdify((x, y), expression, "numpy")

    # Crear una malla de puntos (x, y)
    x_vals = np.linspace(x_min_bound, x_max_bound, 100)
    y_vals = np.linspace(y_min_bound, y_max_bound, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = func(X, Y)

    # Crear la figura y los ejes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Graficar la superficie
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.8)

    # Añadir el punto rojo si se proporcionan coordenadas
    if x_point is not None and y_point is not None:
        # Evaluar la función en el punto proporcionado
        z_point = func(x_point, y_point)
        ax.scatter(
            x_point,
            y_point,
            z_point,
            color="red",
            s=100,
            label=f"({x_point}, {y_point}, {z_point})",
        )
        ax.legend()

    # Etiquetas de los ejes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("c(x, y)")

    # Título
    ax.set_title(f"Gráfico de c(x, y) = {expression_str} con w={w}")

    # Mostrar la gráfica
    plt.show()


def plot_vector(vector):
    # Crear un rango de índices para el eje x
    x = list(range(len(vector)))

    # Graficar los valores del vector en el eje y y sus índices en el eje x
    plt.figure(figsize=(10, 6))
    plt.plot(x, vector, marker="o", linestyle="-", color="b", label="Iteración")

    # Etiquetas y título
    plt.xlabel("Iteración")
    plt.ylabel("Mejor valor de Fitness")
    plt.title(f"Gráfica de Fitness con w={w}")
    plt.legend()
    plt.grid(True)

    # Mostrar la gráfica
    plt.show()


def imprimir_resultados(
    solucion_optima, valor_optimo, limite_inf, limite_sup, w, gbests=None
):
    # Gráfica de apartado C
    plot_function(
        expression,
        limite_inf,
        limite_sup,
        limite_inf,
        limite_sup,
        x_point=solucion_optima[0],
        y_point=solucion_optima[1],
    )

    if gbests is not None:
        # Gráfica de apartado D
        plot_vector(gbests)

    # Solución de apartado E
    print(f"Mejor individuo: {solucion_optima} con w={w}")
    print(f"Valor de x: {solucion_optima[0]} con w={w}")
    print(f"Valor de y: {solucion_optima[1]} con w={w}")
    print(f"Mejor fitness: {valor_optimo} con w={w}")


# Parámetros del algoritmo
num_particulas = 20  # numero de particulas
dim = 2  # dimensiones
cantidad_iteraciones = 10  # maximo numero de iteraciones
c1 = 2.0  # componente cognitivo
c2 = 2.0  # componente social
w = 0.7  # factor de inercia
limite_inf = -100  # limite inferior de busqueda
limite_sup = 100  # limite superior de busqueda


# funcion objetivo hiperboloide eliptico
def funcion_objetivo(x, y, a, b):
    return (x - a) ** 2 + (y + b) ** 2


# Generamos las variables a y b
a_ = input("Ingrese el valor de a en el rango [-50,50]: ")
a = int(a_)
b_ = input("Ingrese el valor de b en el rango [-50,50]: ")
b = int(b_)


# Definimos una función para realizar el análisis
def PSO_manual(w):
    # inicializacion
    particulas = np.random.uniform(
        limite_inf, limite_sup, (num_particulas, dim)
    )  # posiciones iniciales de las particulas

    velocidades = np.zeros(
        (num_particulas, dim)
    )  # inicializacion de la matriz de velocidades en cero

    # inicializacion de pbest y gbest
    pbest = particulas.copy()  # mejores posiciones personales iniciales

    fitness_pbest = np.empty(num_particulas)  # mejores fitness personales iniciales
    for i in range(num_particulas):
        fitness_pbest[i] = funcion_objetivo(particulas[i][0], particulas[i][1], a, b)

    gbest = pbest[np.argmin(fitness_pbest)]  # mejor posicion global inicial
    fitness_gbest = np.min(fitness_pbest)  # fitness global inicial

    # Inicializamos los mejores valores
    gbests = []

    # busqueda
    for iteracion in range(cantidad_iteraciones):
        for i in range(num_particulas):  # iteracion sobre cada partícula
            r1, r2 = (
                np.random.rand(),
                np.random.rand(),
            )  # generacion dos numeros aleatorios

            # actualizacion de la velocidad de la particula en cada dimension
            for d in range(dim):
                velocidades[i][d] = (
                    w * velocidades[i][d]
                    + c1 * r1 * (pbest[i][d] - particulas[i][d])
                    + c2 * r2 * (gbest[d] - particulas[i][d])
                )

            for d in range(dim):
                particulas[i][d] = (
                    particulas[i][d] + velocidades[i][d]
                )  # Actualizacion de la posicion de la particula en cada dimension

                # mantenimiento de las partículas dentro de los limites
                particulas[i][d] = np.clip(particulas[i][d], limite_inf, limite_sup)

            fitness = funcion_objetivo(
                particulas[i][0], particulas[i][1], a, b
            )  # Evaluacion de la funcion objetivo para la nueva posicion

            # actualizacion el mejor personal
            if fitness < fitness_pbest[i]:
                fitness_pbest[i] = fitness  # actualizacion del mejor fitness personal
                pbest[i] = particulas[
                    i
                ].copy()  # actualizacion de la mejor posicion personal

                # actualizacion del mejor global
                if fitness < fitness_gbest:
                    fitness_gbest = fitness  # actualizacion del mejor fitness global
                    gbest = particulas[
                        i
                    ].copy()  # actualizacion de la mejor posicion global

        # imprimir el mejor global en cada iteracion
        # print(f"Iteración {iteracion + 1}: Mejor posición global {gbest}, Valor {fitness_gbest}")

        gbests.append(fitness_gbest)

    # Resultado
    solucion_optima = gbest  # mejor posicion global final
    valor_optimo = fitness_gbest  # mejor fitness global final

    return solucion_optima, valor_optimo, gbests


# Expresión despejada
expression = f"(x-{a})**2 + (y+{b})**2"

# Solución apartado A
print("\n-------------------------------------\n")
print(f"Funcion usada: PSO_manual")
solucion_optima, valor_optimo, gbests = PSO_manual(w)
imprimir_resultados(solucion_optima, valor_optimo, limite_inf, limite_sup, w, gbests)

# Apartado F
# Se define un nuevo coeficiente de inercia
w = 0.0
print("\n-------------------------------------\n")
print(f"Funcion usada: PSO_manual")
solucion_optima, valor_optimo, gbests = PSO_manual(w)
imprimir_resultados(solucion_optima, valor_optimo, limite_inf, limite_sup, w, gbests)


# Apartado G
# Realizamos el mismo ejercicio con PSO
# funcion objetivo hiperboloide eliptico
def funcion_objetivo_pso(p):
    x, y = p
    return (x - a) ** 2 + (y + b) ** 2


# Solución apartado A
w = 0.7  # factor de inercia
# Ejecutar PSO para encontrar la solución
print("\n-------------------------------------\n")
print(f"Funcion usada: pyswarm pso")
xopt, fopt = pso(
    funcion_objetivo_pso,
    [limite_inf, limite_inf],
    [limite_sup, limite_sup],
    swarmsize=num_particulas,
    maxiter=cantidad_iteraciones,
    phip=c1,
    phig=c2,
    omega=w,
)

imprimir_resultados(xopt, fopt, limite_inf, limite_sup, w)

# Apartado F
# Se define un nuevo coeficiente de inercia
w = 0.0
print("\n-------------------------------------\n")
print(f"Funcion usada: pyswarm pso")
xopt, fopt = pso(
    funcion_objetivo_pso,
    [limite_inf, limite_inf],
    [limite_sup, limite_sup],
    swarmsize=num_particulas,
    maxiter=cantidad_iteraciones,
    phip=c1,
    phig=c2,
    omega=w,
)
imprimir_resultados(xopt, fopt, limite_inf, limite_sup, w)
