#!/usr/bin/env python3

import re
import json

# Funkcja bierze to co między , i zwraca słownik z nazwą i typem zmiennej oraz jej dodatkowymi parametrami
def parse_attribute(attribute_string):
    print(attribute_string)
    attribute = {}
    attribute["name"] = attribute_string.split(" ")[0]
    attribute["type"] = attribute_string.split(" ")[1]
    #attribute["info"] = attribute_string.split(" ")[2:]
    attribute["info"] = " ".join(attribute_string.split(" ")[2:])
    return attribute

# Funkcja do parsowania definicji tabeli
def parse_create_table(query):

    # Wyszukiwanie nazwy tabeli za pomocą metody split
    table_name = query.split("(")[0].strip().split(" ")[-1]
    if table_name:
        print(table_name)
        # Parsowanie atrybutów tabeli również za pomocą wyrażenia regularnego
        attributes = []
        #print("*********THIS******")
        attributes_begin_index = query.find("(") # szuka numeru na którym stoi ( w liście query (bo string to lista znakow)
        attributes_string_list = query[attributes_begin_index+1:-2].split(",") # bierze tylko elementy w nawiasie (+1 i -1 by nie brac nawiasow) i dzieli je po ,
        for i in range (len(attributes_string_list)-1):
            if "(" in attributes_string_list[i] and ")" not in attributes_string_list[i]:
                for j in range(i+1, len(attributes_string_list)):
                    attributes_string_list[i]+="," + attributes_string_list[j]
                    attributes_string_list[j]=""
                    if ")" in attributes_string_list[i+1]:
                        break
        attributes_string_list = [i for i in attributes_string_list if i] # usuwanie pustych stringów z listy


        for attribute_string in attributes_string_list:

            attribute_string = attribute_string.strip()
            if attribute_string.startswith("PRIMARY KEY") or attribute_string.startswith("FOREIGN KEY"):
                continue

            attributes.append(parse_attribute(attribute_string))

        # Zwracamy nazwę tabeli i listę atrybutów
        return table_name, attributes
    # Jeśli nie udało się znaleźć nazwy tabeli, zwracamy None
    return None, None

# Funkcja do parsowania instrukcji INSERT INTO
def parse_insert_into(query):
    # Wyszukiwanie nazwy tabeli za pomocą wyrażenia regularnego
    table_name_match = re.search(r'INSERT INTO `([^`]+)`', query)
    if table_name_match:
        # Jeśli znajdziemy pasujące grupy, pobieramy nazwę tabeli
        table_name = table_name_match.group(1)
        # Wyszukiwanie wartości do wstawienia za pomocą wyrażenia regularnego
        values_match = re.search(r'VALUES \((.*?)\)', query)
        if values_match:
            # Jeśli znajdziemy wartości, dzielimy je i otrzymujemy listę
            values = values_match.group(1).split(',')
            # Zwracamy nazwę tabeli i listę wartości
            return table_name, values
    # Jeśli nie udało się znaleźć nazwy tabeli lub wartości, zwracamy None
    return None, None

# Inicjalizacja słowników na strukturę i zawartość tabel
tables_structure = {}
tables_content = {}

# Wczytanie pliku SQL
with open('test_file.sql', 'r') as file:
    sql_script = file.read()

# Podział skryptu na instrukcje
sql_instructions = sql_script.split(';')

# Parsowanie i budowanie słowników
for instruction in sql_instructions:
    # Usunięcie białych znaków z początku i końca instrukcji
    instruction = instruction.strip()
    
    # Usuwanie komentarzy: (kończą się znakiem końca linii)
    lines = instruction.split("\n")
    instruction = ""
    for line in lines:
        if not line.startswith("--"):
            instruction += line + "\n"

    if instruction.startswith('CREATE TABLE'):
        #print("Wykryto CREATE TABLE")
        # Jeśli instrukcja rozpoczyna się od "CREATE TABLE", parsujemy definicję tabeli
        table_name, attributes = parse_create_table(instruction)
        if table_name and attributes:
            # Dodajemy informacje o strukturze tabeli do słownika tables_structure
            tables_structure[table_name] = attributes
    elif instruction.startswith('INSERT INTO'):
        print("Wykryto INSERT INTO")
        # Jeśli instrukcja rozpoczyna się od "INSERT INTO", parsujemy instrukcję wstawiania
        table_name, values = parse_insert_into(instruction)
        if table_name and values:
            # Jeśli udało się sparsować nazwę tabeli i wartości, dodajemy wartości do słownika tables_content
            if table_name not in tables_content:
                # Tworzymy listę wartości dla danej tabeli, jeśli jeszcze jej nie ma
                tables_content[table_name] = []
            # Dodajemy wartości do listy dla danej tabeli
            tables_content[table_name].append(values)

# Wyświetlenie wyników
print("Struktura tabel:")
print(json.dumps(tables_structure, indent=4))
print("\nZawartość tabel:")
print(tables_content)
