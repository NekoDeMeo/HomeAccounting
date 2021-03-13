import dataset
import pandas as pd

# open db
db = dataset.connect('sqlite:///Preparation//testQuery.db')

expenseLibTable = db['ExpenseLib']
transactionTable = db['rakuten_transaction']

transactionTable.create_column('info', db.types.string, nullable=True)
transactionTable.create_column('category', db.types.string, nullable=True)

transactions = transactionTable.all()

for transaction in transactions:

    payAt = transaction['where']
    libData = expenseLibTable.find_one(where=payAt)

    if (libData != None):
        transaction['info'] = libData['what']
        transaction['category'] = libData['category']
        print(transaction)
    else:
        print('Could not find data for transaction:', payAt)

###########################
# Open points
###########################