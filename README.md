# basic-web-scraper
Basic web scraper example with python.

## How to run the entire process
In the root of the project run
```
python pipeline.py
```

## How to run individual steps
### Extraction
In this step, the scraper gets raw data from posts in the specified news portal and loads it in a .csv file. The news portal and the selectors must be previously loaded in the .yaml file.
```
cd ./extract
python main.py site_name
```

### Transformation
In this step, the data is cleaned and transformed for its posterior analysis. The command takes the .csv generated in the previous step as input and saves the result in a new .csv file.
```
cd ./transform
python main.py file_name.csv
```

### Load
In this step, the clean data is saved into a SQLite database. The command takes the .csv generated in the previous step as input and generates a .db file with the data stored in tables.
```
cd ./load
python main.py file_name.csv
```
