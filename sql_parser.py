import re

class SqlParser():

    # Inicjalizacja słownika na strukturę i listy na zawartość tabel
    tables_structure = {} # słownik
    tables_content = [] # lista
    foreign_keys = []

    def get_tables_structure(self) -> dict:
        return self.tables_structure

    def get_tables_content(self) -> list:
        return self.tables_content

    def parse_foreign_key(self, foreign_key_string):

        pattern = r'FOREIGN KEY \((\w+)\) REFERENCES (\w+) \((\w+)\)'
        match = re.search(pattern, foreign_key_string)

        if match:
            foreign_key = {}
            foreign_key['name'] = match.group(1)
            foreign_key['ref_table'] = match.group(2)
            foreign_key['ref_name'] = match.group(3)
            self.foreign_keys.append(foreign_key)

            return foreign_key
        return None

    # Funkcja tekst między przecinkami i zwraca słownik z nazwą i typem zmiennej oraz jej dodatkowymi parametrami
    def parse_attribute(self, attribute_string):

        if "FOREIGN KEY" in attribute_string:
            return self.parse_foreign_key(attribute_string)

        attribute = {}
        attribute["name"] = attribute_string.split(" ")[0]
        attribute["isPrimary"] = "PRIMARY KEY" in attribute_string

        return attribute

    def find_table_name(self, query):
        # Regex pattern to match the table name
        pattern = r'(CREATE TABLE\s+(IF NOT EXISTS\s+)?|INSERT INTO\s+)(\w+)'
        match = re.search(pattern, query, re.IGNORECASE)

        return match.group(3)

    def extract_table_attributes(self, query):
        # Regex pattern to match the part inside the parentheses
        pattern = r'CREATE TABLE\s+(IF NOT EXISTS\s+)?\w+\s*\((.+)\)'
        match = re.search(pattern, query, re.IGNORECASE | re.DOTALL)

        attributes_str = match.group(2).strip()

        # Initialize variables
        attributes = []
        current_attribute = []
        inside_parentheses = 0

        # Parse the attributes string
        for char in attributes_str:
            if char == ',' and inside_parentheses == 0:
                # If we are at a comma and not inside parentheses, it's a delimiter
                attribute_dict = self.parse_attribute(''.join(current_attribute).strip())
                attributes.append(attribute_dict)
                current_attribute = []
            else:
                if char == '(':
                    inside_parentheses += 1
                elif char == ')':
                    inside_parentheses -= 1
                current_attribute.append(char)

        # Append the last attribute
        if current_attribute:
            attribute_dict = self.parse_attribute(''.join(current_attribute).strip())
            attributes.append(attribute_dict)

        return attributes

    def parse_create_table(self, query):
        # Funkcja do parsowania definicji tabeli
        table_name = self.find_table_name(query)
        attributes = self.extract_table_attributes(query)

        return table_name, attributes

    def extract_insert_attributes(self, query):
        # Regex pattern to match the attributes part inside the parentheses after INSERT INTO
        pattern = r'INSERT INTO\s+\w+\s*\(([^)]+)\)'
        match = re.search(pattern, query, re.IGNORECASE)

        attributes_str = match.group(1).strip()
        # Split the attributes by comma and strip any extra whitespace
        attributes = [attr.strip() for attr in attributes_str.split(',')]

        return attributes

    def extract_values_from_string(self, values_str):
        # Split the values by comma, considering quotes for strings
        values = []
        current_value = []
        inside_quotes = False

        for char in values_str:
            if char == ',' and not inside_quotes:
                # If we are at a comma and not inside quotes, it's a delimiter
                value = ''.join(current_value).strip()
                # Remove enclosing quotes
                if value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                values.append(value)
                current_value = []
            else:
                if char in ("'", '"'):
                    inside_quotes = not inside_quotes
                current_value.append(char)

        # Append the last value
        if current_value:
            value = ''.join(current_value).strip()
            # Remove enclosing quotes
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            values.append(value)

        return values

    def extract_insert_values(self, query):
        # Regex pattern to match the values part inside the parentheses after VALUES
        pattern = r'VALUES\s*\(([^)]+)\)(?:\s*,\s*\(([^)]+)\))*'
        matches = re.finditer(pattern, query, re.IGNORECASE)

        all_values = []

        for match in matches:
            for group_num in range(1, len(match.groups()) + 1):
                values_str = match.group(group_num)
                if values_str:

                    values = self.extract_values_from_string(values_str)
                    all_values.append(values)

        return all_values

    def parse_insert_into(self, query) -> list:
        # Funkcja do parsowania instrukcji INSERT INTO zwraca liste
        table_name = self.find_table_name(query)
        attibutes_list = self.extract_insert_attributes(query)
        values_list = self.extract_insert_values(query)

        final_list = []
        for current_value in values_list:

            record = {
                "table_name": table_name,
                "attributes": {}
            }
            for i in range(len(attibutes_list)):
                record["attributes"][attibutes_list[i]]=current_value[i]

            final_list.append(record)

        return final_list

    def parse(self, sql_script: str):

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
                # Jeśli instrukcja rozpoczyna się od "CREATE TABLE", parsujemy definicję tabeli
                table_name, attributes = self.parse_create_table(instruction)
                if table_name and attributes:
                    # Dodajemy informacje o strukturze tabeli do słownika tables_structure
                    self.tables_structure[table_name] = attributes
            elif instruction.startswith('INSERT INTO'):
                # Jeśli instrukcja rozpoczyna się od "INSERT INTO", parsujemy instrukcję wstawiania
                records = self.parse_insert_into(instruction)
                if records:
                    self.tables_content.extend(records)


if __name__ == "__main__":
    print("To jest plik klasy SqlParser. Uruchom proszę skrypt parse_sql.")
