import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Node():
    def __init__(self, steps, country, disease_model):
        self.steps = steps
        self.country = country
        self.disease_model = disease_model
        # S, E, I, R, D
        self.P = pd.DataFrame(0, index=np.arange(steps), columns=
            ["Time", "Susceptible", "Infected (asymptomatic)", "Infected (symptomatic)", "Recovered", "Dead"])
        self.P["Susceptible"][0] = country.population
        self.P_real = None

    def step(self, i, delta_t):
        d = self.disease_model.derivative(self.P.loc[i - 1], i * delta_t)
        self.P.loc[i] = self.P.loc[i - 1] + delta_t * d
        self.P["Time"][i] = self.P["Time"][i - 1] + delta_t

    def add_column(self, c, name):
        self.P[name] = c

    def set_real_data(self, P_real):
        self.P_real = P_real

    def show(self, real = False, mask = None):
        self.add_column(self.country.population - self.P["Dead"], "Population")

        P = self.P_real if real else self.P
        if mask is None:
            mask = P.columns
        P[mask].plot(x = "Time")

        plt.xlabel('Days')
        plt.ylabel('Individuals')
        plt.title(f'Disease progression for {self.country}')
        plt.show()

    def compare(self, mask_sim = None, mask_real = None):
        print(f'Total deaths: {self.country.population - self.P["Dead"]}')
        assert(len(mask_sim) == len(mask_real))
        n = len(mask_sim)

        fig, axs = plt.subplots(n, constrained_layout=True)

        P = self.P[['Time'] + mask_sim]
        P_real = self.P_real[['Time'] + mask_real]
        for i in range(n):
            l1, l2 = mask_sim[i], mask_real[i]
            axs[i].plot(P['Time'], P[l1], '--', label = 'Simulated')
            axs[i].plot(P_real['Time'], P_real[l2], label = 'Real data')
            axs[i].set_title(f'Real {l2} and simulated {l1}')
            axs[i].set_xlabel('Days')
            axs[i].set_ylabel('Individuals')
            axs[i].legend()

        fig.suptitle(f'Simulation accuracy for {self.country}', fontsize=20)
        plt.show()

class DiseaseModel():
    def __init__(self):
        self.R_0 = 2.5
        self.D_E = 5.1 # Time infected (asymptomatic)
        self.D_I = 15 # Time infected (symptomatic)
        self.gamma = 0.05 # Mortality rate
        self.z = 86 # Zoonotic force

    def derivative(self, P, t):
        z = self.z * (P["Time"] < 15)
        N = P.sum() - P[-1]
        _, S, E, I, R, _ = P
        conversions = (self.R_0 / (N * self.D_I)) * S * (I + z)
        prop_latent_to_infected = E / self.D_E
        prop_infected_to_removed = I / self.D_I
        dS = -conversions
        dE = conversions - prop_latent_to_infected
        dI = prop_latent_to_infected - prop_infected_to_removed
        dR = (1 - self.gamma) * prop_infected_to_removed
        dD = self.gamma * prop_infected_to_removed
        return np.array([0, dS, dE, dI, dR, dD])
