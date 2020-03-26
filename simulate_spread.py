import numpy as np
from country_network import form_nodes
from disease_model import Node, DiseaseModel

# Simulation parameters
delta_t = 1
steps = 365

T = np.zeros([steps])

countries, airports = form_nodes()
disease_model = DiseaseModel()
country = [c for c in countries.list if c.iso == 'IT'][0]

print(country)
node = Node(steps, country, disease_model)
for i in range(1, steps):
    time = delta_t * i
    T[i] = time

    node.step(i, delta_t)
node.show(T)
