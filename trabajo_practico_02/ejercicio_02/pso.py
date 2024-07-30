import numpy as np
import math


class PSO:
    def __init__(self, expression, num_particles, limite_inf, limite_sup, dim, cantidad_iteraciones, w, c1, c2):
        self.expression = expression
        self.num_particles = num_particles
        self.limite_inf = limite_inf
        self.limite_sup = limite_sup
        self.dim = dim
        self.cantidad_iteraciones = cantidad_iteraciones
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def _objective_function(self, **kwargs):
        # Evalúa la expresión, permitiendo variables locales
        context = {
            'math': math
        }
        return eval(self.expression, {"__builtins__": None}, {**context, **kwargs})

    def run(self):
        # inicializacion
        particles = np.random.uniform(self.limite_inf, self.limite_sup, (self.num_particles, self.dim))

        velocities = np.zeros((self.num_particles, self.dim))

        # inicializacion de pbest y gbest
        pbest = particles.copy()

        fitness_pbest = np.empty(self.num_particles)  # mejores fitness personales iniciales
        for i in range(self.num_particles):
            # fitness_pbest[i] = funcion_objetivo(particles[i])
            fitness_pbest[i] = self._objective_function(x=particles[i].item())

        gbest = pbest[np.argmax(fitness_pbest)]
        fitness_gbest = np.max(fitness_pbest)

        # Inicializamos para grabar los datos
        gbests = []

        # busqueda
        for iteracion in range(self.cantidad_iteraciones):
            for i in range(self.num_particles):
                r1, r2 = np.random.rand(), np.random.rand()

                # actualizacion de la velocidad de la particula en cada dimension
                velocities[i] = (self.w * velocities[i] + self.c1 * r1 * (pbest[i] - particles[i]) + self.c2 * r2 * (
                        gbest - particles[i]))
                particles[i] = particles[i] + velocities[i]

                # mantenimiento de las partículas dentro de los limites
                particles[i] = np.clip(particles[i], self.limite_inf, self.limite_sup)

                # fitness = funcion_objetivo(particles[i])
                fitness = self._objective_function(x=particles[i].item())

                # actualizacion el mejor personal
                if fitness > fitness_pbest[i]:
                    fitness_pbest[i] = fitness  # actualizacion del mejor fitness personal
                    pbest[i] = particles[i].copy()  # actualizacion de la mejor posicion personal

                    # actualizacion del mejor global
                    if fitness > fitness_gbest:
                        fitness_gbest = fitness  # actualizacion del mejor fitness global
                        gbest = particles[i].copy()  # actualizacion de la mejor posicion global

            # imprimir el mejor global en cada iteracion
            # print(f"Iteración {iteracion + 1}: Mejor posición global {gbest}, Valor {fitness_gbest}")
            gbests.append(fitness_gbest)

        # resultado
        solucion_optima = gbest
        valor_optimo = fitness_gbest

        return solucion_optima, valor_optimo, gbests
