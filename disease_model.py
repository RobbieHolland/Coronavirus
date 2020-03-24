import numpy as np

class Node():
    def __init__(self, steps, country, disease_model):
        self.country = country
        self.disease_model = disease_model
        # S, E, I, R, D
        P_0 = np.array([country.population, 0, 0, 0, 0])
        P = np.zeros([steps, P_0.shape[0]])
        P[0,:] = P_0
        self.P = P

    def step(self, i, delta_t):
        d = self.disease_model.derivative(self.P[i - 1], i * delta_t)
        self.P[i] = self.P[i - 1] + delta_t * d

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
