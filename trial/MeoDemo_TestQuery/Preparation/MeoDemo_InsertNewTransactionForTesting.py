import dataset
from datetime import datetime

# Transaction Datas

TranDate = datetime.now()
TranWhere = 'New Transaction'
TranWhose = 'Me'
TransTotalPay = 999

rakuten_keyCols = ['date', 'where', 'whose', 'totalPayment']

#open db
db = dataset.connect('sqlite:///testQuery.db')

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

