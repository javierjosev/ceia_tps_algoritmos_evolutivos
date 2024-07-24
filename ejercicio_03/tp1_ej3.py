"""
La tasa de crecimiento g de una levadura que produce cierto antibiotico es una función
del nivel de concentración del alimento c en el intervalo [0, 10], siendo:

g = 2*c /(4+0.8*c+c**2+0.2c**3)

Mediante un algoritmo escrito en Python con representación de individuos
binarios, con operador de por torneo, probabilidad de cruce Pc=0.85 y
probabilidad de mutación Pm=0.07, realizar las siguientes consignas:
a. Encontrar el valor aproximado de c para el cual g es máximo. Utilizar precisión de 2 decimales.
b. Transcribir el algoritmo comentando brevemente las secciones de código que sean relevantes.
c. Graficar g en función de c en el intervalo [-1, 20] y agregar un punto rojo en la gráfica
en donde el algoritmo haya encontrado el valor máximo. El gráfico debe contener título, leyenda y etiquetas en los ejes.
d. Graficar las mejores aptitudes encontradas en función de cada generación. El grácfico debe contener título, leyenda y
etiquetas en los ejes.
"""
import random
import numpy as np
import matplotlib.pyplot as plt

# Definimos las funciones de uso de g con c y las auxiliares binarias
def g(c):
    return 2 * c / (4 + 0.8 * c + c**2 + 0.2 * c**3)

def codificar_binario(c, n_bits):
    binario = np.binary_repr(int(c * 2**n_bits), width=n_bits)
    return binario

def decodificar_binario(binario):
    c = int(binario, 2) / (2**len(binario))
    return c

# Definimos la función aptitud que va a depender de g
def aptitud(individuo):
    c = decodificar_binario(individuo)
    return g(c)

# Definimos método de selección por torneo
def seleccion_torneo(poblacion, k):
    padres = []
    for i in range(2):
        seleccionados = np.random.choice(len(poblacion), k, replace=False)
        mejor_indice = np.argmax([aptitud(poblacion[i]) for i in seleccionados])
        padres.append(poblacion[seleccionados[mejor_indice]])
    return padres

# Definimos la función de cruce a 1 punto
def cruce_un_punto(progenitor1, progenitor2, tasa_cruce):
    if random.random() < tasa_cruce:
        punto_cruce = random.randint(1, len(progenitor1) - 1)
        descendiente1 = progenitor1[:punto_cruce] + progenitor2[punto_cruce:]
        descendiente2 = progenitor2[:punto_cruce] + progenitor1[punto_cruce:]
    else:
        descendiente1, descendiente2 = progenitor1, progenitor2
    return descendiente1, descendiente2

# Definimos la función de mutación
def mutacion(cromosoma, tasa_mutacion):
    cromosoma_mutado = ""
    for bit in cromosoma:
        if random.random() < tasa_mutacion:
            cromosoma_mutado = cromosoma_mutado+str(int(not int(bit)))
        else:
            cromosoma_mutado = cromosoma_mutado+bit
    return cromosoma_mutado

# Definimos el algoritmo genético
def algoritmo_genetico(n_individuos, n_bits, n_generaciones, pc, pm):
    poblacion = []
    for i in range(n_individuos):
        individuo = ''.join(np.random.choice(['0', '1'], size=n_bits))
        poblacion.append(individuo)

    mejor_c = None
    mejor_g = float('-inf') # ponemos el máximo valor infinito

    mejores_aptitudes = []

    for generacion in range(n_generaciones):
        # Selección de padres
        padres = []
        for i in range(int(n_individuos / 2)):
            padre1, padre2 = seleccion_torneo(poblacion, k=2)
            padres.extend([padre1, padre2])

        # Cruce y mutación
        nueva_poblacion = []
        for i in range(0, len(padres), 2):
            hijo1, hijo2 = cruce_un_punto(padres[i], padres[i+1], pc)
            hijo1 = mutacion(hijo1, pm)
            hijo2 = mutacion(hijo2, pm)
            nueva_poblacion.extend([hijo1, hijo2])

        # Evaluación de la aptitud y selección de la siguiente generación
        aptitudes = []
        for individuo in poblacion:
            aptitud_individuo = aptitud(individuo)
            aptitudes.append(aptitud_individuo)
            if aptitud_individuo > mejor_g:
                mejor_c = decodificar_binario(individuo)
                mejor_g = aptitud_individuo

        mejores_aptitudes.append(max(aptitudes))
        poblacion = nueva_poblacion

    return mejor_c, mejor_g, mejores_aptitudes

# Parámetros del algoritmo
n_individuos = 50
n_bits = 18
n_generaciones = 100
pc = 0.85
pm = 0.07

# Ejecutar el algoritmo genético
mejor_c, mejor_g, mejores_aptitudes = algoritmo_genetico(n_individuos, n_bits, n_generaciones, pc, pm)

print("Valor máximo de c:", mejor_c)
print("Valor máximo de g:", mejor_g)

# Graficar g(c)
c_values = np.linspace(-1, 20, 100)
g_values = [g(c) for c in c_values]

plt.plot(c_values, g_values, label="g(c)")
plt.scatter(mejor_c, mejor_g, color="red", marker="o", label=f"c máximo: {mejor_c:.2f}")
plt.xlabel("c")
plt.ylabel("g(c)")
plt.title("Función g(c)")
plt.legend()
plt.grid()
plt.show()

# Graficar las mejores aptitudes
plt.plot(mejores_aptitudes)
plt.xlabel("Generación")
plt.ylabel("Mejor aptitud")
plt.title("Mejores aptitudes encontradas en cada generación")
plt.grid()
plt.show()


