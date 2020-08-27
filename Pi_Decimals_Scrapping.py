import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

# Errores graves a corregir
# Un diccionario no es buena idea para meter los valores originales porque hay varios valores para la misma fecha
# Tal y como esta el script, hay mas datos para un eje que para el otro
# Esto quiere decir que el pulido de las fechas tiene que ser anterior a convertirlo a dos listas...


# Extrae el HTMl, las wikitablas y las recorre una a una y luego fila a fila
# Luego extrae el primero y quinto valor (fecha y decimales de pi) y los añade a un diccionario
# Constantes que indican la columna de la que se extraen los datos
col1 = 0
col2 = 4
max_col = col2 + 1


def extract_from_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all(class_='wikitable')
    data = {}
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
                data[first_cell] = fifth_cell
    return data


# Convertir el diccionario en dos listas con los numeros filtrados
def dict_to_lists(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    (keys, values) = zip(*dict.items())
    return keys, values


# Eliminar lo que no son fechas de cuatro dígitos
def leave_just_numbers(list):
    four_digit_list = []
    for i in list:
        new_i = re.findall(r'\d{4}', i)
        if new_i:
            four_digit_list.append(new_i)
    return four_digit_list


# Imprimir los datos con una gráfica escalonada, WIP [desastre en los ejes]
def plot_values(x, y):
    plt.step(x, y)
    plt.ylabel('Number of decimal digits')
    plt.xlabel('Year')
    plt.xticks(rotation=45, ha="right")
    plt.show()


data = extract_from_table('https://en.wikipedia.org/wiki/Chronology_of_computation_of_π')

plot_values(dict_to_lists(data)[0], dict_to_lists(data)[1])
