import numpy as np


class RestrictedPSO:
    def __init__(self):
        pass

    def run(self, n_particles, n_dimensions, max_iterations, f, w, c1, c2, inequalities, variables):

        # inicialización de particulas
        x = np.zeros((n_particles, n_dimensions))  # matriz para las posiciones de las particulas
        v = np.zeros((n_particles, n_dimensions))  # matriz para las velocidades de las particulas
        pbest = np.zeros((n_particles, n_dimensions))  # matriz para los mejores valores personales
        pbest_fit = -np.inf * np.ones(
            n_particles)  # mector para las mejores aptitudes personales (inicialmente -infinito)
        gbest = np.zeros(n_dimensions)  # mejor solución global
        gbest_fit = -np.inf  # mejor aptitud global (inicialmente -infinito)

        # inicializacion de particulas factibles
        for i in range(n_particles):
            while True:  # bucle para asegurar que la particula sea factible
                x[i] = np.random.uniform(0, 10, n_dimensions)  # inicializacion posicion aleatoria en el rango [0, 10]
                # if g1(x[i]) and g2(x[i]) and g3(x[i]):  # se comprueba si la posicion cumple las restricciones
                if self._check_restrictions(inequalities, x[i], variables):
                    break  # Salir del bucle si es factible
            v[i] = np.random.uniform(-1, 1, n_dimensions)  # inicializar velocidad aleatoria
            pbest[i] = x[i].copy()  # ee establece el mejor valor personal inicial como la posicion actual
            fit = f(x[i])  # calculo la aptitud de la posicion inicial
            if fit > pbest_fit[i]:  # si la aptitud es mejor que la mejor conocida
                pbest_fit[i] = fit  # se actualiza el mejor valor personal

        # Optimizacion
        gbest_fit_hist = np.zeros(max_iterations)
        for j in range(max_iterations):  # Repetir hasta el número máximo de iteraciones
            for i in range(n_particles):
                fit = f(x[i])  # Se calcula la aptitud de la posicion actual
                # Se comprueba si la nueva aptitud es mejor y si cumple las restricciones
                # if fit > pbest_fit[i] and g1(x[i]) and g2(x[i]) and g3(x[i]):
                if fit > pbest_fit[i] and self._check_restrictions(inequalities, x[i], variables):
                    pbest_fit[i] = fit  # Se actualiza la mejor aptitud personal
                    pbest[i] = x[i].copy()  # Se actualizar la mejor posicion personal
                    if fit > gbest_fit:  # Si la nueva aptitud es mejor que la mejor global
                        gbest_fit = fit  # Se actualizar la mejor aptitud global
                        gbest = x[i].copy()  # Se actualizar la mejor posicion global

                # actualizacion de la velocidad de la particula
                v[i] = w * v[i] + c1 * np.random.rand() * (pbest[i] - x[i]) + c2 * np.random.rand() * (gbest - x[i])
                x[i] += v[i]  # Se actualiza la posicion de la particula

                # se asegura de que la nueva posicion esté dentro de las restricciones
                # if not (g1(x[i]) and g2(x[i]) and g3(x[i])):
                if not self._check_restrictions(inequalities, x[i], variables):
                    # Si la nueva posicion no es válida, revertir a la mejor posicion personal
                    x[i] = pbest[i].copy()
            gbest_fit_hist[j] = gbest_fit
        return gbest, gbest_fit, gbest_fit_hist

    def _check_restrictions(self, inequalities, point, variables):
        variable_dict = dict(zip(variables, point))

        for inequality in inequalities:
            try:
                # Evaluación de la inecuación
                if not eval(inequality, {}, variable_dict):
                    return False
            except Exception as e:
                raise ValueError(f"Error al evaluar la inecuación '{inequality}': {e}")

        return True

