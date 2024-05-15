#!/usr/bin/env python3

from sql_parser import SqlParser

import json
import sys

if __name__ == "__main__":

    # Weryfikacja, czy podano pliki jako parametry programu:
    if len(sys.argv) < 2:
        print("Nie podano plików SQL")
        exit(2)

    parser = SqlParser()

    # Wczytanie i parsowanie plików SQL
    for filename in sys.argv[1:]:
        with open(filename, 'r') as file:
            sql_script = file.read()
            parser.parse(sql_script)

    # Wyświetlenie wyników
    print("Struktura tabel:")
    print(json.dumps(parser.get_tables_structure(), indent=4))
    print("\nZawartość tabel:")
    print(json.dumps(parser.get_tables_content(), indent=4))
