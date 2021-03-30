import dataset
import pandas as pd
from datetime import datetime

import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

csvName = 'ExpenseLibrary.csv'
csvPath = os.path.join(__location__, csvName)

dbName = 'ExpenseLibrary.db'
dbPath = os.path.join(__location__, dbName)

# read csv
expenseLib_usedColumns = ['PaymentAt', 'Information', 'Category']

###########################
# Read CSV Data
###########################

expenseLib_data = pd.read_csv(csvPath, usecols=expenseLib_usedColumns)

# Handle dummy row section
expenseLib_df = pd.DataFrame(expenseLib_data).dropna()

print(expenseLib_df)

###########################
# Store to db (ignore duplicates)
###########################

# create new db
db = dataset.connect('sqlite:///' + dbPath)

expenseLibTable = db['ExpenseLib']

for row in expenseLib_df.itertuples():
    expenseLibTable.insert_ignore(dict(where=row.PaymentAt,
                                       what=row.Information,
                                       category=row.Category,
                                       ),
                                  expenseLib_usedColumns
                                  )

libs = expenseLibTable.all()

for lib in libs:
    print(lib)

###########################
# Open points
###########################
