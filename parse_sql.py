#!/usr/bin/env python3

from sql_parser import SqlParser
from normalizer import Normalizer

import json
import sys

if __name__ == "__main__":

    # Weryfikacja, czy podano pliki jako parametry programu:
    if len(sys.argv) < 3:
        print("Nie podano plików SQL")
        exit(2)

    norm_level = int(sys.argv[1])
    if norm_level < 1 and norm_level > 3:
        print("Błędny poziom normalizacji")
        exit(1)

    parser = SqlParser()

    # Wczytanie i parsowanie plików SQL:
    for filename in sys.argv[2:]:
        with open(filename, 'r') as file:
            sql_script = file.read()
            parser.parse(sql_script)

    # Wyświetlenie wyników i zapis wstępnych jsonów:
    tables_structure_filename = "tables_structure.json"
    tables_content_filename = "tables_content.json"

    tab_struct = parser.get_tables_structure()
    with open(tables_structure_filename, "w") as file:
        file.write(json.dumps(tab_struct, indent=4))
    print(f"Struktura tabel zapisana w pliku {tables_structure_filename}")

    tab_cont = parser.get_tables_content()
    with open(tables_content_filename, "w") as file:
        file.write(json.dumps(tab_cont, indent=4))
    print(f"Zawartość tabel zapisana w pliku {tables_content_filename}")

    # Tworzenie docelowych jsonów w zależności od poziomu normalizacji:
    normalizer = Normalizer(norm_level)
    normalized_database = normalizer.normalize(tab_struct, tab_cont)

    normalized_file_name = f"normalized_{norm_level}.json"
    with open(normalized_file_name, "w") as file:
        file.write(json.dumps(normalized_database, indent=4))
    print(f"Znormalizowana baza zpisana w pliku {normalized_file_name}")
