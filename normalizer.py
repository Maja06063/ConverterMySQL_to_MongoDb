class Normalizer:

    def __init__(self, norm_level: int) -> None:
        self.norm_level = norm_level

    def normalize1(self, tables_structure: dict, tables_content: list) -> dict:

        normalized_dict = {}
        for old_element in tables_content:
            
            new_element = {}
            table_name = old_element["table_name"]
            if not table_name in normalized_dict:
                normalized_dict[table_name] = []

            attributes = old_element["attributes"]

            # Pomijanie ID (będzie dodane automatycznie w mongo):
            for table_attribute in tables_structure[table_name]:
                if table_attribute["name"] in attributes:
                    new_element[table_attribute["name"]] = attributes[table_attribute["name"]]

            normalized_dict[table_name].append(new_element)

        return normalized_dict
    
    def normalize2(self, tables_structure: dict, tables_content: list) -> list:

        return []
    
    def normalize3(self, tables_structure: dict, tables_content: list) -> list:

        return []

    def normalize(self, tables_structure: dict, tables_content: list):

        if self.norm_level == 1:
            return self.normalize1(tables_structure, tables_content)
        
        elif self.norm_level == 2:
            return self.normalize2(tables_structure, tables_content)
        
        elif self.norm_level == 3:
            return self.normalize3(tables_structure, tables_content)


if __name__ == "__main__":
    print("To jest plik klasy Normalizer. Uruchom proszę skrypt parse_sql.")
