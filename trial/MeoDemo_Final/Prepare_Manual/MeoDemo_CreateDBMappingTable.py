import dataset
import pandas as pd
from datetime import datetime

import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

csvName = 'DBMappingList.csv'
csvPath = os.path.join(__location__, csvName)

dbName = 'DatabaseLibrary.db'
dbPath = os.path.join(__location__, dbName)

# read csv
usedColumns = ['Name', 'Database', 'Source', 'Currency']

###########################
# Read CSV Data
###########################

data = pd.read_csv(csvPath, usecols=usedColumns)

# Handle dummy row section
df = pd.DataFrame(data).dropna()

#print(df)

###########################
# Store to db (ignore duplicates)
###########################

# create new db
db = dataset.connect('sqlite:///' + dbPath)

table = db['DBMappingList']

for row in df.itertuples():
    table.insert_ignore(dict(Name=row.Name,
                                Database=row.Database,
                                Source=row.Source,
                                Currency=row.Currency
                           ),
                      usedColumns
                      )

libs = table.all()

for lib in libs:
    print(lib)

###########################
# Open points
###########################
