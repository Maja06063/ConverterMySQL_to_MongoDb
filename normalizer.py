class Normalizer:

    def __init__(self, norm_level: int) -> None:
        self.norm_level = norm_level

    # Brak relacji między kolekcjami:
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

    def does_table_have_ref(self, table_list: list) -> bool:

        for attribute in table_list:
            if "ref_table" in attribute:
                return True

        return False

    # Dodanie references (odniesienia) do docelowego dokumentu:    
    def add_reference_to_document(self, document: dict, reference: dict) -> None:

        if not "references" in document:
            document["references"] = []
        document["references"].append(reference)

    # Odniesienie między kolekcjami:
    def normalize2(self, tables_structure: dict, tables_content: list) -> dict:

        normalized_dict = self.normalize1(tables_structure, tables_content)

        # Znajdź tabele z kluczami obcymi: 
        tables_with_ref = {}
        for table_name in tables_structure.keys():
            if self.does_table_have_ref(tables_structure[table_name]):
                tables_with_ref[table_name] = tables_structure[table_name]

        # Na podstawie refa dodaj id do kolekcji, gdzie prowadzi:
        for table_name in tables_with_ref.keys():
            for attribute in tables_with_ref[table_name]:
                
                # Szukamy atrybutu, do którego prowadzi klucz obcy:
                if "ref_table" in attribute:
                    ref_table = attribute["ref_table"]
                    name = attribute["name"]
                    base_table = table_name

                    # Obsługa sytuacji, w której mamy dostęp do klucza głównego:
                    if name in normalized_dict[ref_table][0]:
                        for document in normalized_dict[ref_table]:
                            for record in normalized_dict[base_table]:

                                if document[name] == record[name]:
                                    self.add_reference_to_document(document, {table_name: record})

                    # Obsługa sytuacji, w której kluczem głównym jest autoinkrementowane id:
                    else:
                        for record in normalized_dict[base_table]:
                            index = int(record[name]) - 1
                            document = normalized_dict[ref_table][index]
                            self.add_reference_to_document(document, {table_name: record})

        return normalized_dict

    # Osadzenie kolekcji:
    def normalize3(self, tables_structure: dict, tables_content: list) -> list:

        normalized_dict = self.normalize1(tables_structure, tables_content)

        # Znajdź tabele z kluczami obcymi: 
        tables_with_ref = {}
        for table_name in tables_structure.keys():
            if self.does_table_have_ref(tables_structure[table_name]):
                tables_with_ref[table_name] = tables_structure[table_name]

        # Na podstawie refa dodaj id do kolekcji, gdzie prowadzi:
        for table_name in tables_with_ref.keys():
            for attribute in tables_with_ref[table_name]:
                
                # Szukamy atrybutu, do którego prowadzi klucz obcy:
                if "ref_table" in attribute:
                    ref_table = attribute["ref_table"]
                    name = attribute["name"]
                    base_table = table_name

                    # Obsługa sytuacji, w której mamy dostęp do klucza głównego:
                    if name in normalized_dict[ref_table][0]:
                        for document in normalized_dict[ref_table]:
                            for record in normalized_dict[base_table]:

                                print(document)
                                print(record)
                                if document[name] == record[name]:
                                    self.add_reference_to_document(document, {table_name: record})
                                    #document["references"][-1][table_name].pop(name)

                    # Obsługa sytuacji, w której kluczem głównym jest autoinkrementowane id:
                    else:
                        for record in normalized_dict[base_table]:
                            index = int(record[name]) - 1
                            document = normalized_dict[ref_table][index]
                            self.add_reference_to_document(document, {table_name: record})
                            record.pop(name)

        return normalized_dict

    def normalize(self, tables_structure: dict, tables_content: list):

        if self.norm_level == 1:
            return self.normalize1(tables_structure, tables_content)
        
        elif self.norm_level == 2:
            return self.normalize2(tables_structure, tables_content)
        
        elif self.norm_level == 3:
            return self.normalize3(tables_structure, tables_content)


if __name__ == "__main__":
    print("To jest plik klasy Normalizer. Uruchom proszę skrypt parse_sql.")
