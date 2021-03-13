import dataset
from datetime import datetime

import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

dbName = 'testQuery.db'
dbPath = os.path.join(__location__, dbName)

# Transaction Datas

TranDate = datetime.now()
TranWhere = 'New Transaction'
TranWhose = 'Me'
TransTotalPay = 999

rakuten_keyCols = ['date', 'where', 'whose', 'totalPayment']

#open db
db = dataset.connect('sqlite:///' + dbPath)

transactionTable = db['rakuten_transaction']

transactionTable.insert_ignore(dict(date=TranDate.date(),
                                    where=TranWhere,
                                    whose=TranWhose,
                                    totalPayment=int(TransTotalPay)
                                    ),
                               rakuten_keyCols
                               )

transactions = transactionTable.all()

for transaction in transactions:
    print(transaction)


###########################
# Open points
###########################

