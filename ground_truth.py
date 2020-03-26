import datetime
from country_network import form_nodes
from disease_model import Node, DiseaseModel
import csv
import numpy as np

countries, airports = form_nodes()
disease_model = DiseaseModel()
start_date = datetime.date(2019, 12, 30)

nodes = []
with open('data/COVID-19-geographic-disbtribution-worldwide-2020-03-24.csv') as covid:
    data = csv.reader(covid, delimiter=',')
    next(data)
    current_country = None
    for row in data:
        date, _, _, _, new_cases, new_deaths, _, iso = row
        if iso != current_country:
            if current_country is not None:
                cases = np.cumsum(np.array([0] + cases[::-1]))
                deaths = np.cumsum(np.array([0] + deaths[::-1]))
                T = np.array([0] + T[::-1])
                country = countries.find(lambda c: c.iso == current_country)
                node = Node(len(T), country, disease_model)
                node.P[:,0] = node.country.population - np.cumsum(np.array(cases[::-1]))
                node.P[:,4] = np.cumsum(deaths[::-1])
                node.show(T[::-1])
                nodes.append(node)
                # print(node.P)
                break
            T, cases, deaths = [], [], []
            current_country = iso

        t = (datetime.datetime.strptime(date, '%d/%m/%Y').date() - start_date).days
        T.append(t)
        print(T)
        cases.append(int(new_cases))
        deaths.append(int(new_deaths))
