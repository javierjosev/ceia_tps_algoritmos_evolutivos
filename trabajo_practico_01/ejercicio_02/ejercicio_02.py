"""
Maximizar mediante un algoritmo genético desarrollado en Python la función
y = x 2 . Los parámetros del algoritmos son:
✓ Selección por ruleta
✓ Cruza monopunto aleatoria
✓ Probabilidad de cruce 0.92
✓ Probabilidad de mutación 0.01
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from genetic_algorithm import GeneticAlgorithm

# Parámetros del algoritmo
num_individuals = 50
# Cálculo de rangos
# límites de –10 ≤ x ≤ 10, 0 ≤ y ≤ 20 y precisión de 3 decimales
# Para x: rango = 20 -> 20*1000 = 20000 -> 2^14 < 20000 < 2^15 => 15 bits
bits_x = 15
num_generations = 100
prob_crossover = 0.92
prob_mutation = 0.01

# Límites de la variable x
x_min, x_max = -10, 10

expression = "x**2"

# Inicialización de la población
population = [''.join(random.choices(['0', '1'], k=bits_x)) for _ in range(num_individuals)]

genetic_algorithm = GeneticAlgorithm(expression, num_individuals, bits_x, num_generations, prob_crossover,
                                     prob_mutation,
                                     x_min, x_max)
best_chromosome, best_x, best_fitness, best_fitness_per_gen = genetic_algorithm.run(population)

print(f'Mejor individuo: {best_chromosome}')
print(f'Valor de x: {best_x}')
print(f'Mejor fitness: {best_fitness}')

