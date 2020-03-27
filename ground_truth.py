import datetime
from country_network import form_nodes
from disease_model import Node, DiseaseModel
import csv
import numpy as np
import pandas as pd

countries, airports = form_nodes()
disease_model = DiseaseModel()
start_date = datetime.date(2019, 11, 30)

future_steps = 15
nodes = []
with open('data/COVID-19-geographic-disbtribution-worldwide-2020-03-24.csv') as covid:
    data = csv.reader(covid, delimiter=',')
    next(data)
    current_country = None
    for row in data:
        date, _, _, _, new_cases, new_deaths, _, iso = row

        # If new country
        if iso != current_country:
            # And it's not the first one
            if current_country is not None:
                # Find the associated country
                country = countries.find(lambda c: c.iso == current_country)
                # If we can't find the country then skip
                if country is None:
                    current_country = iso
                    continue
                # Otherwise create the node for the previous country
                data_real = {"Time": np.array([0] + T[::-1]),
                            "Cases": np.cumsum(np.array([0] + cases[::-1])),
                            "Dead": np.cumsum([0] + deaths[::-1])}
                P_real = pd.DataFrame(data_real)
                node = Node(max(data_real["Time"]) + future_steps, country, disease_model)
                node.set_real_data(P_real)
                nodes.append(node)
            # And reset for the next one
            T, cases, deaths = [], [], []
            current_country = iso

        t = (datetime.datetime.strptime(date, '%d/%m/%Y').date() - start_date).days
        T.append(t)
        cases.append(int(new_cases))
        deaths.append(int(new_deaths))

italy = [n for n in nodes if n.country.iso == 'IT'][0]
china = [n for n in nodes if n.country.iso == 'CN'][0]

delta_t = 1
for i in range(1, italy.steps):
    italy.step(i, delta_t)

# italy.show()
italy.compare(mask_sim = ['Infected (symptomatic)', 'Dead'], mask_real = ['Cases', 'Dead'])
