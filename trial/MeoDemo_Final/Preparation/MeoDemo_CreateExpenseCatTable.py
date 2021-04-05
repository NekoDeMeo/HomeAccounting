import dataset
import pandas as pd
from datetime import datetime

import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

csvName = 'ExpenseCategories.csv'
csvPath = os.path.join(__location__, csvName)

dbName = 'ExpenseLibrary.db'
dbPath = os.path.join(__location__, dbName)

# read csv
expenseCat_usedColumns = ['Category', 'Classification', 'Direction', 'Explain']

###########################
# Read CSV Data
###########################

expenseCat_data = pd.read_csv(csvPath, usecols=expenseCat_usedColumns)

# Handle dummy row section
expenseCat_df = pd.DataFrame(expenseCat_data).dropna()

print(expenseCat_df)

###########################
# Store to db (ignore duplicates)
###########################

# create new db
db = dataset.connect('sqlite:///' + dbPath)

expenseCatTable = db['ExpenseCat']

for row in expenseCat_df.itertuples():
    expenseCatTable.insert_ignore(dict(Category=row.Category,
                                       Classification=row.Classification,
                                       Direction=row.Direction,
                                       Explain=row.Explain,
                                       ),
                                  expenseCat_usedColumns
                                  )

libs = expenseCatTable.all()

for lib in libs:
    print(lib)

###########################
# Open points
###########################
