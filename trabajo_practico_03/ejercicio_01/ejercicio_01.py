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


def experiment(num_particles):
    gbest_e, gbest_fit_e, _ = restricted_pso.run(n_particles=num_particles, n_dimensions=n_dimensions,
                                                              max_iterations=max_iterations, f=f, w=w, c1=c1, c2=c2,
                                                              inequalities=inequalities, variables=variables)
    print(f"Cantidad de partículas: {num_particles}")
    print(f"Valor optimo: {gbest_fit_e}")
    print(f"Mejor solucion: [{gbest_e[0]:.4f}, {gbest_e[1]:.4f}, {gbest_e[2]:.4f}, {gbest_e[3]:.4f}]")


def f(x):
    return 375 * x[0] + 275 * x[1] + 475 * x[2] + 325 * x[3]


# Parametros
n_particles = 20  # numero de particulas en el enjambre
n_dimensions = 4  # dimensiones del espacio de busqueda (a, b, c y d)
max_iterations = 50  # numero máximo de iteraciones para la optimizacion
c1 = c2 = 1.4944  # coeficientes de aceleracion
w = 0.6  # factor de inercia

variables = ['a', 'b', 'c', 'd']
inequalities = ['a >= 0', 'b >= 0', 'c >= 0', 'd >= 0',
                '2.5*a + 1.5*b + 2.75*c + 2*d  <= 640', '3.5*a + 3*b + 3*c + 2*d <= 960']
restricted_pso = RestrictedPSO()
gbest, gbest_fit, gbest_fit_hist = restricted_pso.run(n_particles, n_dimensions, max_iterations, f, w, c1, c2,
                                                      inequalities, variables)
# Se imprime la mejor solucion encontrada y también su valor optimo
print(f"Mejor solucion: [{gbest[0]:.4f}, {gbest[1]:.4f}, {gbest[2]:.4f}, {gbest[3]:.4f}]")
print(f"Valor optimo: {gbest_fit}")
plot_vector(gbest_fit_hist, n_particles)


# Que sucede si se reduce en 1 unidad el tiempo de acabado de la parte B.
inequalities_b_reduced = ['2.5*a + 1.5*b + 2.75*c + 2*d  <= 640', '3.5*a + 2*b + 3*c + 2*d <= 960']
gbest, gbest_fit, gbest_fit_hist = restricted_pso.run(n_particles, n_dimensions, max_iterations, f, w, c1, c2,
                                                      inequalities_b_reduced, variables)
# Se imprime la mejor solucion encontrada y también su valor optimo
print("Reducción en 1 unidad el tiempo de acabado de B")
print(f"Mejor solucion: [{gbest[0]:.4f}, {gbest[1]:.4f}, {gbest[2]:.4f}, "
      f"{gbest[3]:.4f}]")
print(f"Valor optimo: {gbest_fit}")
plot_vector(gbest_fit_hist, n_particles)


# Test para identificar la mínima cantidad de partículas
experiment(num_particles=1)
experiment(num_particles=2)
experiment(num_particles=3)
experiment(num_particles=4)
experiment(num_particles=5)
experiment(num_particles=10)
experiment(num_particles=15)
experiment(num_particles=20)

