import numpy as np
import matplotlib.pyplot as plt
import math

# Definimos la función objetivo
def funcion_objetivo(x):
    return 2*math.sin(x)-0.5*x**2

########## Apartado A #################

# Definimos los parametros
num_particulas = 2
dim = 1  
cantidad_iteraciones = 80  
c1 = 2.0  # componente cognitivo
c2 = 2.0  # componente social
w = 0.7  # factor de inercia
limite_inf = 0  
limite_sup = 4  

def solucion(num_particulas):
    # inicializacion
    particulas = np.random.uniform(limite_inf, limite_sup, (num_particulas, dim))  

    velocidades = np.zeros((num_particulas, dim))

    # inicializacion de pbest y gbest
    pbest = particulas.copy()  

    fitness_pbest = np.empty(num_particulas)  # mejores fitness personales iniciales
    for i in range(num_particulas):
        fitness_pbest[i] = funcion_objetivo(particulas[i])

    gbest = pbest[np.argmax(fitness_pbest)]  
    fitness_gbest = np.max(fitness_pbest)  

    # Inicializamos para grabar los datos
    gbests = []

    # busqueda
    for iteracion in range(cantidad_iteraciones):
        for i in range(num_particulas):  
            r1, r2 = np.random.rand(), np.random.rand()  

            # actualizacion de la velocidad de la particula en cada dimension
            velocidades[i] = (w * velocidades[i] + c1 * r1 * (pbest[i] - particulas[i]) + c2 * r2 * (gbest - particulas[i]))        
            particulas[i] = particulas[i] + velocidades[i]  

            # mantenimiento de las partículas dentro de los limites
            particulas[i] = np.clip(particulas[i], limite_inf, limite_sup)

            fitness = funcion_objetivo(particulas[i])

            # actualizacion el mejor personal
            if fitness > fitness_pbest[i]:
                fitness_pbest[i] = fitness  # actualizacion del mejor fitness personal
                pbest[i] = particulas[i].copy()  # actualizacion de la mejor posicion personal

                # actualizacion del mejor global
                if fitness > fitness_gbest:
                    fitness_gbest = fitness  # actualizacion del mejor fitness global
                    gbest = particulas[i].copy()  # actualizacion de la mejor posicion global

        # imprimir el mejor global en cada iteracion
        #print(f"Iteración {iteracion + 1}: Mejor posición global {gbest}, Valor {fitness_gbest}")
        gbests.append(fitness_gbest)

    # resultado
    solucion_optima = gbest  
    valor_optimo = fitness_gbest

    return solucion_optima, valor_optimo, gbests

# Primera parte
solucion_optima, valor_optimo, gbests = solucion(2)
print("\nSolucion optima (x):", solucion_optima)
print("Valor optimo:", valor_optimo)

# Realizamos la gráfica
x_values = np.linspace(limite_inf, limite_sup, 100)

plt.plot(x_values, [funcion_objetivo(x) for x in x_values], label="Función Objetivo(x)")
plt.scatter(solucion_optima, valor_optimo, color="green", marker="o", label=f"óptima: {solucion_optima[0]:.2f}")
plt.xlabel("x")
plt.ylabel("Función Obj(x)")
plt.title("Función Objetivo(x)")
plt.legend()
plt.grid()
plt.show()

# Rrealizamos el gráfico de gbest
plt.plot(gbests)
plt.xlabel("Iteraciones")
plt.ylabel("gbest")
plt.title("Mejores gbests encontradas en cada iteración")
plt.grid()
plt.show()

# Apartado F
_, _, gbests_4 = solucion(4)
_, _, gbests_10 = solucion(10)
_, _, gbests_100 = solucion(100)
_, _, gbests_200 = solucion(200)
_, _, gbests_400 = solucion(400)

# Realizamos el gráfico de gbest
plt.plot(gbests_4, label="4 particulas")
plt.plot(gbests_10, label="10 particulas")
plt.plot(gbests_100, label="100 particulas")
plt.plot(gbests_200, label="200 particulas")
plt.plot(gbests_400, label="400 particulas")
plt.xlabel("Iteraciones")
plt.ylabel("gbest")
plt.legend()
plt.title("Mejores gbests encontradas en cada iteración por número de partículas")
plt.grid()
plt.show()