"""
Crear en Python un vector columna A de 20 individuos binarios aleatorios de tipo
string. Crear un segundo vector columna B de 20 números aleatorios comprendidos
en el intervalo (0, 1). Mutar un alelo aleatorio a aquellos genes pertenecientes a los
cromosomas de A que tengan en su i-ésima fila un correspondiente de B inferior a
0.09. Almacenar los cromosomas mutados en un vector columna C y mostrarlos por
consola.
"""

import random
import numpy as np

chromosome_dim = 10  # No especifica la dimensión en el enunciado. Se establece en 10.
population_size = 20
threshold = 0.09


# Mostrar los cromosomas de una población
def print_population(population):
    for i, chromosome in enumerate(population):
        print(f"Cromosoma {i + 1}: {chromosome}")


def generate_chromosome(length=10):
    return ''.join(random.choice('01') for _ in range(length))


A = [generate_chromosome(length=chromosome_dim) for _ in range(population_size)]

# Crea un vector columna B con valores aleatorios en el intervalo (0, 1)
B = np.random.rand(population_size)


# Muta un alelo aleatorio en los genes del cromosoma
def mutate_chromosome(chromosome):
    mutation_position = random.randint(0, len(chromosome) - 1)
    if chromosome[mutation_position] == '0':
        chromosome = chromosome[:mutation_position] + '1' + chromosome[mutation_position + 1:]
    else:
        chromosome = chromosome[:mutation_position] + '0' + chromosome[mutation_position + 1:]
    return chromosome


# Se aplica la mutación si el valor en B es menor al threshold
C = [mutate_chromosome(individual) if value < threshold else individual for individual, value in zip(A, B)]

print('\n Población A:')
print_population(A)

print('\n Conjunto B:')
print_population(B)

print('\n Población C:')
print_population(C)
