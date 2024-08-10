"""
Utilidad (z)
------------
z = 375*a + 275*b + 475*c +325*d

Restricciones
-------------
g1) 2.5*a + 1.5*b + 2.75*c + 2*d  < 640
g2) 3.5*a + 3*b + 3*c + 2*d < 960

"""

from restricted_pso import RestrictedPSO
import matplotlib.pyplot as plt


def plot_vector(vector, num_part):
    fig, ax = plt.subplots()

    if vector is not None:
        x_vector = list(range(len(vector)))
        ax.plot(x_vector, vector, marker='o', linestyle='-', color='b', label='Iteración')
        ax.set_xlabel('Iteración')
        ax.set_ylabel('Valor de GBest')
        ax.set_title(f'Gráfica de GBest para {num_part} partículas')
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()


def f(x):
    return 375 * x[0] + 275 * x[1] + 475 * x[2] + 325 * x[3]


# Parametros
n_particles = 20  # numero de particulas en el enjambre
n_dimensions = 4  # dimensiones del espacio de busqueda (a, b, c y d)
max_iterations = 50  # numero máximo de iteraciones para la optimizacion
c1 = c2 = 1.4944  # coeficientes de aceleracion
w = 0.6  # factor de inercia

variables = ['a', 'b', 'c', 'd']
inequalities = ['2.5*a + 1.5*b + 2.75*c + 2*d  <= 640', '3.5*a + 3*b + 3*c + 2*d <= 960']
restricted_pso = RestrictedPSO()
gbest, gbest_fit, gbest_fit_hist = restricted_pso.run(n_particles, n_dimensions, max_iterations, f, w, c1, c2,
                                                      inequalities, variables)

# Se imprime la mejor solucion encontrada y también su valor optimo
print(f"Mejor solucion: [{gbest[0]:.4f}, {gbest[1]:.4f}, {gbest[2]:.4f}, {gbest[3]:.4f}]")
print(f"Valor optimo: {gbest_fit}")
plot_vector(gbest_fit_hist, n_particles)
