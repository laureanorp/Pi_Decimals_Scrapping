import requests
from bs4 import BeautifulSoup
import matplotlib as mpl
import matplotlib.pyplot as plt
import re


# Extrae el HTML, las wikitablas y las recorre una a una y luego fila a fila
# Luego extrae el primero y último valor (fecha y decimales de pi) y los añade a su lista correspondiente
# Estas constantes indican la columna de la que se extraen los datos
col1 = 0
col2 = -1


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
            if row.find_all('td'):
                first_cell = row.find_all('td')[col1].get_text().replace('\n', '')
                last_cell = row.find_all('td')[col2].get_text().replace('\n', '')
                if first_cell != last_cell and last_cell != '':
                    years.append(first_cell)
                    decimals.append(last_cell)
    return years, decimals


# WIP: Simplificar todas las fechas a solo el año, cogiendo solo el último número
def clean_dates(raw_list):
    year_digit_list = []
    for i in raw_list:
        new_i = re.findall(r'\d+', i)
        if new_i:
            new_i = new_i[-1]
            year_digit_list.append(new_i)
    return year_digit_list


# Eliminar varios elementos de wikipedia que están entre corchetes, las comas y varias fórmulas
def clean_decimals(raw_list):
    clean_list = []
    for i in raw_list:
        i = i.replace(',', '')
        clean_list.append(re.split("[=[:]+", i)[0])
    return clean_list


# Imprimir los datos con una gráfica escalonada
def plot_values(x, y):
    mpl.rcParams["figure.figsize"] = [10, 7]
    plt.step(x, y)
    plt.ylabel('Number of decimal digits')
    plt.xlabel('Year')
    plt.xticks(rotation=45, ha="right")
    plt.yscale('log')
    plt.show()


# Entragable inicial de un plot con valores inventados
# some_years = [150, 250, 1000, 1230, 1495, 1700, 1800, 2000, 2020]
# some_decimals = [1, 3, 5, 10, 20, 2000, 30000, 100000, 20000000]

# Pruebas: Imprimir las fechas, los decimales y asegurarse de que cada lista sigue midiendo lo mismo.
data = extract_from_table('https://en.wikipedia.org/wiki/Chronology_of_computation_of_π')
final_dates = clean_dates(data[0])
final_decimals = clean_decimals(data[1])
print(final_dates)
print(final_decimals)
assert len(final_dates) == len(final_decimals)

# Prueba de plot con valores reales a partir del año 150 d.C (para evitar "negativos")
plot_values(final_dates[11:], final_decimals[11:])
