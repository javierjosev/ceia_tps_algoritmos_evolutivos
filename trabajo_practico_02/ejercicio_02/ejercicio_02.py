"""
Escribir un algoritmo PSO para la maximización de la función:
y = sin(x) + sin(x 2 )
En el intervalo de 0 ≤ x ≤ 10 y que cumpla con las siguientes consignas:
A. Transcribir el algoritmo en Python con los siguientes parámetros: número de
partículas = 2, máximo número de iteraciones = 30, coeficientes de aceleración
c1 = c2 = 1.49, peso de inercia w = 0.5.
B. Indicar la URL del repositorio en donde se encuentra el algoritmo PSO.
C. Graficar usando matplotlib la función objetivo y agregar un punto negro en
donde el algoritmo haya encontrado el valor máximo. El gráfico debe contener
etiquetas en los ejes, leyenda y un título.
D. Realizar un gráfico de línea que muestre gbest en función de las iteraciones
E. Transcribir la solución óptima encontrada (dominio) y el valor objetivo óptimo
(imagen).
F. Incrementar el número de partículas a 4, ejecutar la rutina, transcribir la
solución óptima encontrada, transcribir el valor objetivo óptimo y realizar
nuevamente los gráficos solicitados en C y D.
G. Incrementar el número de partículas a 6, ejecutar la rutina, transcribir la
solución óptima encontrada, transcribir el valor objetivo óptimo y realizar
nuevamente los gráficos solicitados en C y D.
H. Incrementar el número de partículas a 10, ejecutar la rutina, transcribir la
solución óptima encontrada, transcribir el valor objetivo óptimo y realizar
nuevamente los gráficos solicitados en C y D.
I. Realizar observaciones/comentarios/conclusiones sobre los resultados
obtenidos.
"""
import numpy as np
import sympy as sp
from pso import PSO
import matplotlib.pyplot as plt


def plot_function_gbest(expression_str, x_min_bound, x_max_bound, x_point=None, num_part=None, vector=None):
    # Definir la variable independiente
    x = sp.symbols('x')

    # Reemplazo la función de math
    expression_str = expression_str.replace('math.sin', 'sin').replace('math.cos', 'cos')

    # Conversión de la cadena en una expresión simbólica
    expression = sp.sympify(expression_str)

    # Convertir la expresión simbólica en una función numérica
    func = sp.lambdify(x, expression, 'numpy')

    # Creación de un rango de valores para x
    x_vals = np.linspace(x_min_bound, x_max_bound, 400)

    # Evaluación de la función en los valores de x
    y_vals = func(x_vals)

    # Se crea la figura y los subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico de la función en el primer subplot
    ax1.plot(x_vals, y_vals, label=f'f(x) = {expression_str}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title(f'Gráfica de f(x) = {expression_str}')
    ax1.grid(True)
    ax1.legend()

    # Marcar el punto específico, si es pasado por parámetro
    if x_point is not None:
        # Evaluar y en el punto x especificado
        y_point = func(x_point)
        ax1.scatter(x_point, y_point, color='black', s=100, zorder=5,
                    label=f'Punto ({x_point}, {y_point})')
        ax1.legend()

    # Gráfico del gbest en el segundo subplot, si es pasado por parámetro
    if vector is not None:
        x_vector = list(range(len(vector)))
        ax2.plot(x_vector, vector, marker='o', linestyle='-', color='b', label='Iteración')
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('Valor de GBest')
        ax2.set_title(f'Gráfica de GBest para {num_part} partículas')
        ax2.grid(True)
        ax2.legend()

    # Mostrar la figura con ambos subplots
    plt.tight_layout()
    plt.show()


def experiment(expression, num_particles, lower_bound, upper_bound, dim, num_iterations, w, c1, c2):
    pso = PSO(expression, num_particles, lower_bound, upper_bound, dim, num_iterations, w, c1, c2)
    solucion_optima, valor_optimo, gbests = pso.run()
    print("\nNúmero de partículas:", num_particles)
    print("\nSolución óptima (x):", solucion_optima)
    print("Valor óptimo:", valor_optimo)
    #Gráficos
    plot_function_gbest(expression, lower_bound, upper_bound, x_point=solucion_optima, num_part=num_particles,
                        vector=gbests)


# A. Transcribir el algoritmo en Python con los siguientes parámetros: número de
# partículas = 2, máximo número de iteraciones = 30, coeficientes de aceleración
# c1 = c2 = 1.49, peso de inercia w = 0.5.
# B. Indicar la URL del repositorio en donde se encuentra el algoritmo PSO.
# C. Graficar usando matplotlib la función objetivo y agregar un punto negro en
# donde el algoritmo haya encontrado el valor máximo. El gráfico debe contener
# etiquetas en los ejes, leyenda y un título.
# D. Realizar un gráfico de línea que muestre gbest en función de las iteraciones
# E. Transcribir la solución óptima encontrada (dominio) y el valor objetivo óptimo
# (imagen).

# Definición de los parametros comunes a todos los experimentos
# num_particles = 2
dim = 1
num_iterations = 30
c1 = 1.49  # Componente cognitivo
c2 = 1.49  # Componente social
w = 0.5  # Factor de inercia
lower_bound = 0
upper_bound = 10

expression = "math.sin(x) + math.sin(x**2)"

experiment(expression=expression, num_particles=2, lower_bound=lower_bound, upper_bound=upper_bound, dim=dim,
           num_iterations=num_iterations, w=w, c1=c1, c2=c2)

# E. Transcribir la solución óptima encontrada (dominio) y el valor objetivo óptimo (imagen).

# F. Incrementar el número de partículas a 4, ejecutar la rutina, transcribir la
# solución óptima encontrada, transcribir el valor objetivo óptimo y realizar
# nuevamente los gráficos solicitados en C y D.
experiment(expression=expression, num_particles=4, lower_bound=lower_bound, upper_bound=upper_bound, dim=dim,
           num_iterations=num_iterations, w=w, c1=c1, c2=c2)

# G. Incrementar el número de partículas a 6, ejecutar la rutina, transcribir la
# solución óptima encontrada, transcribir el valor objetivo óptimo y realizar
# nuevamente los gráficos solicitados en C y D.
experiment(expression=expression, num_particles=6, lower_bound=lower_bound, upper_bound=upper_bound, dim=dim,
           num_iterations=num_iterations, w=w, c1=c1, c2=c2)

# H. Incrementar el número de partículas a 10, ejecutar la rutina, transcribir la
# solución óptima encontrada, transcribir el valor objetivo óptimo y realizar
# nuevamente los gráficos solicitados en C y D.
experiment(expression=expression, num_particles=10, lower_bound=lower_bound, upper_bound=upper_bound, dim=dim,
           num_iterations=num_iterations, w=w, c1=c1, c2=c2)
