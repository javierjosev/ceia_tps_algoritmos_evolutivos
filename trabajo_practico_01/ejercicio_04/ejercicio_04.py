"""
La distribución de la concentración de cierto contaminante en un canal está descrita por la ecuación:

c(x, y) = 7.7 + 0.15x + 0.22y − 0.05x 2 − 0.016y 2 − 0.007x y

En donde, las variables independientes se encuentran entre los límites de –10 ≤ x ≤ 10, 0 ≤ y ≤ 20.

Para la función de adaptación anterior, escribir y ejecutar un algoritmo genético que utilice el operador de
selección por ruleta con probabilidades de cruza y mutación a elección.

Luego realizar las siguientes consignas:
a. Determinar en forma aproximada la concentración máxima dada la función c(x, y). Utilizar una precisión de 3
decimales.
b. Transcribir el algoritmo genético comentando brevemente las secciones de código que sean relevantes.
c. Graficar c(x, y) para los intervalos de las variables independientes ya mencionados y agregar un punto rojo en la
gráfica en donde el algoritmo haya encontrado el valor máximo. El gráfico debe contener título, leyenda y etiquetas
en los ejes.
d. Graficar las mejores aptitudes encontradas en función de cada generación. El gráfico debe contener
título, leyenda y etiquetas en los ejes.

"""
import random
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from genetic_algorithm import GeneticAlgorithm


def plot_function(expression_str, x_min_bound, x_max_bound, y_min_bound, y_max_bound, x_point=None, y_point=None):
    # Definir las variables simbólicas
    x, y = sp.symbols('x y')

    # Convertir la cadena en una expresión simbólica
    expression = sp.sympify(expression_str)

    # Convertir la expresión simbólica en una función numérica
    func = sp.lambdify((x, y), expression, 'numpy')

    # Crear una malla de puntos (x, y)
    x_vals = np.linspace(x_min_bound, x_max_bound, 100)
    y_vals = np.linspace(y_min_bound, y_max_bound, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = func(X, Y)

    # Crear la figura y los ejes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar la superficie
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

    # Añadir el punto rojo si se proporcionan coordenadas
    if x_point is not None and y_point is not None:
        # Evaluar la función en el punto proporcionado
        z_point = func(x_point, y_point)
        ax.scatter(x_point, y_point, z_point, color='red', s=100, label=f'({x_point}, {y_point}, {z_point})')
        ax.legend()

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('c(x, y)')

    # Título
    ax.set_title(f'Gráfico de c(x, y) = {expression_str}')

    # Mostrar la gráfica
    plt.show()


def plot_vector(vector):
    # Crear un rango de índices para el eje x
    x = list(range(len(vector)))

    # Graficar los valores del vector en el eje y y sus índices en el eje x
    plt.figure(figsize=(10, 6))
    plt.plot(x, vector, marker='o', linestyle='-', color='b', label='Generación')

    # Etiquetas y título
    plt.xlabel('Generación')
    plt.ylabel('Mejor valor de Fitness')
    plt.title('Gráfica de Fitness')
    plt.legend()
    plt.grid(True)

    # Mostrar la gráfica
    plt.show()


# Parámetros del algoritmo
num_individuals = 50
# Cálculo de rangos
# límites de –10 ≤ x ≤ 10, 0 ≤ y ≤ 20 y precisión de 3 decimales
# Para x: rango = 20 -> 20*1000 = 20000 -> 2^14 < 20000 < 2^15 => 15 bits
# Para y: rango = 20 -> 20*1000 = 20000 -> 2^14 < 20000 < 2^15 => 15 bits
bits_x = 15
bits_y = 15
total_bits = bits_x + bits_y
num_generations = 100
prob_crossover = 0.85
prob_mutation = 0.07

# Límites de las variables
x_min, x_max = -10, 10
y_min, y_max = 0, 20

expression = "7.7 + 0.15 * x + 0.22 * y - 0.05 * x ** 2 - 0.016 * y ** 2 - 0.007 * x * y"

genetic_algorithm = GeneticAlgorithm(expression, num_individuals, bits_x, bits_y, num_generations, prob_crossover,
                                     prob_mutation,
                                     x_min, x_max, y_min, y_max)
best_chromosome, best_x, best_y, best_fitness, best_fitness_per_gen = genetic_algorithm.run()

print(f'Mejor individuo: {best_chromosome}')
print(f'Valor de x: {best_x}')
print(f'Valor de y: {best_y}')
print(f'Mejor fitness: {best_fitness}')

plot_function(expression, x_min, x_max, y_min, y_max, x_point=best_x, y_point=best_y)
plot_vector(best_fitness_per_gen)
