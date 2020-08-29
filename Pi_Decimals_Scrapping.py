import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re


# Extrae el HTMl, las wikitablas y las recorre una a una y luego fila a fila
# Luego extrae el primero y quinto valor (fecha y decimales de pi) y los añade a su lista correspondiente
# Constantes que indican la columna de la que se extraen los datos
col1 = 0
col2 = 4
max_col = col2 + 1


def extract_from_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all(class_='wikitable')
    years = []
    decimals = []
    for i in range(len(all_tables)):
        table = all_tables[i]
        rows = table.find_all('tr')
        for j in range(len(rows)):
            row = rows[j]
            if not row.find_all('td') or len(row.find_all('td')) < max_col:
                first_cell = None
                fifth_cell = None
            else:
                first_cell = row.find_all('td')[col1].get_text().replace('\n', '')
                fifth_cell = row.find_all('td')[col2].get_text().replace('\n', '')
                years.append(first_cell)
                decimals.append(fifth_cell)
    return years, decimals


# Eliminar lo que no son fechas de cuatro dígitos
# Todo eliminar dias y meses si la fecha tiene 4 digitos de año
def clean_numbers(list):
    four_digit_list = []
    for i in list:
        new_i = re.findall(r'\d+', i)
        if new_i:
            four_digit_list.append(new_i)
    return four_digit_list


# WIP: Funcion para eliminar un par de cosas de wikipedia que están entre corchetes
def remove_citations(list):
    for i in list:
        re.sub(r'[.+?]', '', i)


# Imprimir los datos con una gráfica escalonada
def plot_values(x, y):
    plt.step(x, y)
    plt.ylabel('Number of decimal digits')
    plt.xlabel('Year')
    plt.xticks(rotation=45, ha="right")
    plt.show()


data = extract_from_table('https://en.wikipedia.org/wiki/Chronology_of_computation_of_π')

new_dates = clean_numbers(data[0])

# Prueba de plot con valores inventados
some_years = [150, 250, 1000, 1230, 1495, 1700, 1800, 2000, 2020]
some_decimals = [1, 3, 5, 10, 20, 2000, 30000, 100000, 200000]
plot_values(some_years, some_decimals)

# Pruebas: Imprimir las fechas, los decimales y asegurarse de que cada lista mide lo mismo.
print(new_dates)
print(data[1])
assert len(new_dates) == len(data[1])
