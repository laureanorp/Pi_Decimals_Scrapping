import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re


# Extrae el HTMl, las wikitablas y las recorre una a una, fila a fila
# Luego extrae el primero y quinto valor (fecha y decimales de pi) y los añade a un diccionario
# Constantes que indican la columna de la que se extraen los datos
I1 = 4
I = 0
I2 = I1 + 1


def extract_from_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all(class_='wikitable')
    clean_data = {}
    for i in range(len(all_tables)):
        table = all_tables[i]
        rows = table.find_all('tr')
        for j in range(len(rows)):
            row = rows[j]
            if not row.find_all('td') or len(row.find_all('td')) < I2:
                first_cell = None
                fifth_cell = None
            else:
                first_cell = row.find_all('td')[I].get_text().replace('\n', '')
                fifth_cell = row.find_all('td')[I1].get_text().replace('\n', '')
                clean_data[first_cell] = fifth_cell
    return clean_data


# Convertir el diccionario en dos listas
def dict_to_lists(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    (keys, values) = zip(*dict.items())
    return keys, values

# Eliminar todo lo que eno son fechas de cuatro dígitos
def leave_just_numbers(list):
    re.findall(r'\d+', 'list')


# Imprimir los datos con una gráfica escalonada, WIP, desastre en los ejes
def plot_values(x, y):
    # plt.plot(x, y)
    plt.step(x, y)
    plt.ylabel('Number of decimal digits')
    plt.xlabel('Year')
    plt.show()

clean_data = extract_from_table('https://en.wikipedia.org/wiki/Chronology_of_computation_of_π')
print(dict_to_lists(clean_data)[0])
plot_values(dict_to_lists(clean_data)[0], dict_to_lists(clean_data)[1])
