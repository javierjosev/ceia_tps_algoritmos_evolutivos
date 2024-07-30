from pso import PSO

# Definición de los parametros
num_particles = 2
dim = 1
num_iterations = 30
c1 = 1.49  # Componente cognitivo
c2 = 1.49  # Componente social
w = 0.5  # Factor de inercia
lower_bound = 0
upper_bound = 10

expression = "math.sin(x) + math.sin(x**2)"

pso = PSO(expression, num_particles, lower_bound, upper_bound, dim, num_iterations, w, c1, c2)
solucion_optima, valor_optimo, gbests = pso.run()
print("\nSolución óptima (x):", solucion_optima)
print("Valor óptimo:", valor_optimo)



