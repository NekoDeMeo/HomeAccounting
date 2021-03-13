import dataset
import pandas as pd

confirmedTransaction_keyCols = ['date', 'info', 'whose', 'totalPayment', 'category']

# open db
db = dataset.connect('sqlite:///Preparation//testQuery.db')

expenseLibTable = db['ExpenseLib']
transactionTable = db['rakuten_transaction']

confirmedTransactionTable = db['confirmed_transaction']


transactionTable.create_column('info', db.types.string, nullable=True)
transactionTable.create_column('category', db.types.string, nullable=True)

transactions = transactionTable.all()

for transaction in transactions:

    payAt = transaction['where']
    libData = expenseLibTable.find_one(where=payAt)

    if (libData != None):
        transaction['info'] = libData['what']
        transaction['category'] = libData['category']
        #print(transaction)

        confirmedTransactionTable.insert_ignore(dict(date=transaction['date'],
                                                     info=transaction['info'],
                                                     whose=transaction['whose'],
                                                     totalPayment=transaction['totalPayment'],
                                                     category=transaction['category']
                                                     ),
                                                confirmedTransaction_keyCols
                                                )

    else:
        print('Could not find data for transaction:', payAt)

for confirmedTrans in confirmedTransactionTable.all():
    print(confirmedTrans)

###########################
# Open points
###########################