import numpy as np
import matplotlib.pyplot as plt

def show(T, P, labels):
    for i, l in enumerate(labels):
        plt.plot(T, P[:,i], label = l)

    plt.legend()
    plt.xlabel('Days')
    plt.ylabel('Individuals')

class Node():
    def __init__(self, steps, country, disease_model):
        self.country = country
        self.disease_model = disease_model
        # S, E, I, R, D
        P_0 = np.array([country.population, 0, 0, 0, 0])
        P = np.zeros([steps, P_0.shape[0]])
        P[0,:] = P_0
        self.P = P

        self.labels = ["Susceptible", "Infected (asymptomatic)", "Infected (symptomatic)", "Recovered", "Dead"]

    def step(self, i, delta_t):
        d = self.disease_model.derivative(self.P[i - 1], i * delta_t)
        self.P[i] = self.P[i - 1] + delta_t * d

    def add_column(self, c, name):
        P = np.zeros([self.P.shape[0], self.P.shape[1] + 1])
        P[:,:-1] = self.P
        P[:,-1] = c
        self.P = P
        self.labels.append(name)

    def show(self, T, mask = None):
        if mask is None:
            mask =
        print(f'Total deaths: {self.country.population - self.P[-1,4]}')
        self.add_column(self.country.population - self.P[:,4], "Population")
        # plt.plot(T, N - np.sum(P, axis=1), label = "Recovered")

        show(T, self.P, self.labels)
        plt.title(f'Disease progression for {self.country}')
        plt.show()

class DiseaseModel():
    def __init__(self):
        self.R_0 = 2.5
        self.D_E = 5.1 # Time infected (asymptomatic)
        self.D_I = 10 # Time infected (symptomatic)
        self.gamma = 0.05 # Mortality rate
        self.z = 86 # Zoonotic force

    def derivative(self, P, t):
        z = self.z * (t < 15)
        N = P.sum() - P[-1]
        S, E, I, R, _ = P
        conversions = (self.R_0 / (N * self.D_I)) * S * (I + z)
        prop_latent_to_infected = E / self.D_E
        prop_infected_to_removed = I / self.D_I
        dS = -conversions
        dE = conversions - prop_latent_to_infected
        dI = prop_latent_to_infected - prop_infected_to_removed
        dR = (1 - self.gamma) * prop_infected_to_removed
        dD = self.gamma * prop_infected_to_removed
        return np.array([dS, dE, dI, dR, dD])
