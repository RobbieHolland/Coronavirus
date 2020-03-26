import re
import csv
import numpy as np
import unidecode

class Table():
    def __init__(self):
        self.list = []

    def filter(self, condition):
        return [a for a in self.list if condition(a)]

    def find(self, condition):
        matching = self.filter(condition)
        if len(matching) == 1:
            return matching[0]
        else:
            return None

    def add(self, item):
        self.list.append(item)

    def __len__(self):
        return len(self.list)

class Country():
    def __init__(self, net_id, iso, name, continent, population):
        self.net_id = net_id
        self.iso = iso
        self.name = name
        self.continent = continent
        self.population = int(population.replace(',', ''))

    def __str__(self):
        return self.name

class Airport():
    def __init__(self, iata, country_iso):
        self.net_id = None
        self.iata = iata
        self.country_iso = country_iso

    def set_network_id(self, id):
        self.net_id = id

    def __str__(self):
        return f'{self.iata}\t{self.country_iso}'

def form_nodes():
    airports = Table()
    with open('data/iata_codes.csv', encoding = "ISO-8859-1") as iata_codes:
        data = csv.reader(iata_codes, delimiter=',')
        for row in data:
            # ident, type, name, elevation, continent, iso_country, iso_region, municipality, gps_code, iata_code, local_code, coords
            iso_country, iata_code = row[5], row[9]
            airports.add(Airport(iata_code, iso_country))

    countries = Table()
    with open('data/iso_pop.csv') as iso_pop:
        data = csv.reader(iso_pop, delimiter=',')
        next(data)
        for i, row in enumerate(data):
            # iso, ?, ?, fips, country, capital, area, population, continent
            iso, name, population, continent = row[0], row[1], row[2], row[3]
            countries.add(Country(i, iso, name, continent, population))

    with open("airports/global-cities.dat", "r") as filestream:
        for line in filestream:
            iata, id, city = line.rstrip().split('|')
            matching_airport = airports.find(lambda a: a.iata == iata)
            if matching_airport is not None:
                matching_airport.set_network_id(int(id))
    airports.list = airports.filter(lambda a: a.net_id is not None)

    return countries, airports

def form_network(countries, airports):
    max_id = max([a.net_id for a in airports.list])
    network = np.zeros([max_id + 1, max_id + 1])
    with open("airports/global-net.dat", "r") as filestream:
        for line in filestream:
            node_1, node_2 = [int(node) for node in line.rstrip().split(' ')]
            network[node_1, node_2] += 1

    country_network = np.zeros([len(countries), len(countries)])
    missed = 0
    total = 0
    for country in countries.list:
        country_airports = airports.filter(lambda a: a.country_iso == country.iso)
        for a in country_airports:
            for other_net_id, link in enumerate(network[a.net_id]):
                if link:
                    total += 1
                    matching_airport = airports.find(lambda a: a.net_id == other_net_id)
                    if matching_airport is not None:
                        b_country = countries.find(lambda c: c.iso == matching_airport.country_iso)
                        country_network[country.net_id, b_country.net_id] += 1
                    else:
                        missed += 1

    print(total, missed)
    print(country_network[1:10,1:10])
    np.save('data/country_network.npy', country_network)

if __name__ == "__main__":
    countries, airports = form_nodes()
    form_network(countries, airports)
