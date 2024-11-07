#!/usr/bin/env python3

from mongo_uploader import MongoUploader

import json
import sys

if __name__ == "__main__":

    # Weryfikacja, czy podano plik jako parametr programu:
    if len(sys.argv) < 1:
        print("Nie podano pliku znormalizowanego json.")
        exit(2)

    with open(sys.argv[1], 'r') as file:
        json_dict = json.loads(file.read())

    mongoUploader = MongoUploader()
    mongoUploader.remove_all_collections()

    for collection in json_dict.keys():
        for collection_data in json_dict[collection]:
            mongoUploader.upload_collection_data(collection, collection_data)

    # Test:
    print("Odczyt danych zapisanych w bazie. Lista nazw kolekcji:")
    collections_from_database = mongoUploader.get_collections()
    print(collections_from_database)

    for collection in collections_from_database:
        print("Kolekcja:")
        print(collection)
        print(json.dumps(mongoUploader.get_collection_data(collection), indent=4, default=str))
