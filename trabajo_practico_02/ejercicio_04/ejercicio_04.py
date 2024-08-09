import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from pyswarm import pso


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

# Definición de las funciones del sistema de ecuaciones
def f1(x):
    x1, x2 = x
    return x1 * 3 + x2 * 2 - 9  # Ejemplo de una ecuación


def f2(x):
    x1, x2 = x
    return x1 - x2 * 5 - 4  # Ejemplo de otra ecuación

# Expresión despejada
expression = "(x*3 + y*2 - 9)**2 + (x - y*5 - 4)**2"

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

imprimir_resultados(xopt, fopt, limite_inf, limite_sup, w)
