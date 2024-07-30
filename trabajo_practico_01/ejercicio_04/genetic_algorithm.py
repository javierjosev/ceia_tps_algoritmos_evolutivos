import numpy as np
import random


class GeneticAlgorithm:

    def __init__(self, expression, num_individuals, bits_x, bits_y, num_generations, prob_crossover, prob_mutation,
                 x_min, x_max, y_min, y_max):
        # Parámetros del algoritmo
        self.expression = expression
        self.num_individuals = num_individuals
        self.bits_x = bits_x
        self.bits_y = bits_y
        self.total_bits = bits_x + bits_y
        self.num_generations = num_generations
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation

        # Límites de las variables
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

        self.best_fitness_value_per_gen = []

        # Inicialización de la población
        total_bits = bits_x + bits_y
        self.population = [''.join(random.choices(['0', '1'], k=total_bits)) for _ in range(num_individuals)]

    def _fitness_function(self, **kwargs):
        # Evalúa la expresión, permitiendo variables locales
        return eval(self.expression, {"__builtins__": None}, kwargs)

    def _decode_chromosome(self, chromosome):
        x_bin = chromosome[:self.bits_x]
        y_bin = chromosome[self.bits_y:]
        x = self.x_min + (self.x_max - self.x_min) * int(x_bin, 2) / (2 ** self.bits_x - 1)
        y = self.y_min + (self.y_max - self.y_min) * int(y_bin, 2) / (2 ** self.bits_y - 1)
        x = round(x, 3)
        y = round(y, 3)
        return x, y

    # Evaluar población
    def _evaluate_population(self, population):
        fitness = []
        for chromosome in population:
            x, y = self._decode_chromosome(chromosome)
            fitness.append(self._fitness_function(x=x, y=y))
        return np.array(fitness)

    # Selección por ruleta
    def _roulette_wheel_selection(self, population, fitness):
        total_fitness = np.sum(fitness)
        probabilities = fitness / total_fitness
        selected_population = []
        for _ in range(len(population)):
            selected_index = np.random.choice(len(population), p=probabilities)
            # "probabilities" es un array de probabilidades asociadas a cada índice.
            # Define la probabilidad de seleccionar cada índice en la secuencia
            # para la función np.random.choice(..).
            selected_population.append(population[selected_index])
        return selected_population

    # Cruce de un punto
    def _crossover(self, parent1, parent2):
        if random.random() < self.prob_crossover:
            point = random.randint(1, self.total_bits - 1)
            # El bit de cruce se selecciona de forma aleatoria
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        else:
            return parent1, parent2

    # Mutación
    def _mutate(self, chromosome):
        chromosome = list(chromosome)
        for i in range(len(chromosome)):
            if random.random() < self.prob_mutation:
                chromosome[i] = '1' if chromosome[i] == '0' else '0'
        return ''.join(chromosome)

    def run(self):
        population = self.population
        # Algoritmo genético
        for generation in range(self.num_generations):
            fitness = self._evaluate_population(population)
            population = self._roulette_wheel_selection(population, fitness)

            # Se guarda el mejor valor de fitness para cada generación
            self.best_fitness_value_per_gen.append(np.max(fitness))

            new_population = []
            for i in range(0, len(population), 2):
                parent1, parent2 = population[i], population[i + 1]
                child1, child2 = self._crossover(parent1, parent2)
                new_population.append(self._mutate(child1))
                new_population.append(self._mutate(child2))

            population = new_population

        # Evaluar la última población
        fitness = self._evaluate_population(population)

        # Encontrar el mejor individuo
        best_index = np.argmax(fitness)

        best_chromosome = population[best_index]
        best_x, best_y = self._decode_chromosome(best_chromosome)
        best_fitness = fitness[best_index]

        return best_chromosome, best_x, best_y, best_fitness, self.best_fitness_value_per_gen
