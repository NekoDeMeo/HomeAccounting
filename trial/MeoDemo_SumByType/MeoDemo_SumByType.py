import dataset
import pandas as pd

import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

csvName = 'ExpenseCategories.csv'
csvPath = os.path.join(__location__, csvName)

dbName = 'testQuery.db'
dbPath = os.path.join(__location__, dbName)

# read csv
expenseCat_usedColumns = ['Category']

###########################
# Read CSV Data
###########################

expenseCat_data = pd.read_csv(csvPath, usecols=expenseCat_usedColumns)

# Handle dummy row section
expenseCat_df = pd.DataFrame(expenseCat_data).dropna()

print(expenseCat_df)

# open db
db = dataset.connect('sqlite:///' + dbPath)

confirmedTransactionTable = db['confirmed_transaction']

#transactions = confirmedTransactionTable.all()

for row in expenseCat_df.itertuples():
    refcat = row.Category

    transactions = confirmedTransactionTable.find(category=refcat)
    sum = 0
    for transaction in transactions:
        sum += transaction['totalPayment']

    print('Sum for Category',  refcat, sum)

###########################
# Open points
###########################