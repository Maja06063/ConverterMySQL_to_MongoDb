# MySQL--MongoDb
Converter relative base to NoSQL database.
There are 2 modules:
 - `parse_sql` to convert SQL file to JSON file,
 - `create_mongodb_from_json` to upload JSON to the local MongoDb database.

## Requirements

1. Make sure you installed MongoDb server,
2. Download `pymongo` Python library using pip (prefferably in venv):
```Bash
python3 -m venv .venv
source .venv/bin/activate
pip install pymongo
```
3. Restard MongoDb service if needed:
 - Linux:
```Bash
rm /tmp/mongodb-27017.sock
sudo systemctl start mongod
```
 - Mac:
```Bash
rm /tmp/mongodb-27017.sock
brew services start mongodb-community
```

## Parsing SQL

Use `parse_sql.py` script:
```Bash
python parse_sql.py <SQL files>
```

for example:
```Bash
python parse_sql.py *.sql
```

The following result files should be created:
 - `tables_content.json` - temporary,
 - `tables_structure.json` - temporary,
 - `normalized_X.json`, where `X` is the choosen normalization number (1 or 2) - actual the result.

## Uploading JSON

Use `create_mongodb_from_json.py` script:
```Bash
python create_mongodb_from_json.py <JSON file>
```

for example:
```Bash
python create_mongodb_from_json.py normalized_1.json | more
```

In result the data from JSON will be uploaded to local MongoDb.
