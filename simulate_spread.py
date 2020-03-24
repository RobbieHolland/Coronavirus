import numpy as np
import matplotlib.pyplot as plt
from country_network import form_nodes
from disease_model import Node, DiseaseModel

# Simulation parameters
delta_t = 1
steps = 365

T = np.zeros([steps])

countries, airports = form_nodes()
disease_model = DiseaseModel()
country = countries.list[0]
print(country)
node = Node(steps, country, disease_model)
for i in range(1, steps):
    time = delta_t * i
    T[i] = time

    node.step(i, delta_t)

plt.plot(T, node.P[:,0], label = "Susceptible")
plt.plot(T, node.P[:,1], label = "Infected (asymptomatic)")
plt.plot(T, node.P[:,2], label = "Infected (symptomatic)")
plt.plot(T, node.P[:,3], label = "Recovered")
plt.plot(T, node.P[:,4], label = "Dead")
plt.plot(T, country.population - node.P[:,4], label = "Population")
# plt.plot(T, N - np.sum(P, axis=1), label = "Recovered")
plt.legend()
plt.xlabel('Days')
plt.ylabel('Individuals')
plt.title(f'Disease progression for {country}')
plt.show()
