import dataset
import pandas as pd
from datetime import datetime

#read csv
rakuten_columns = ['date',
                   'where',
                   'where',
                   'paymentMethod_unused',
                   'amount',
                   'serviceFee_unused',
                   'totalPayment_unused',
                   'paymentThisMont_unused',
                   'paymentNextMonth_unused',
                   'verified_unused']

rakuten_usedColumns = ['利用日', '利用店名・商品名', '利用者', '支払総額']
rakuten_colsDict = {'利用日': 'date', '利用店名・商品名': 'where', '利用者': 'whose', '支払総額': 'totalPayment'}
rakuten_keyCols = ['date', 'where', 'whose', 'totalPayment']

###########################
# Read CSV section
###########################

#method1: read whole csv then filter needed data to DataFrame and store to db
#data = pd.read_csv('enavi202102(1312).csv', encoding="utf_8")
#df = pd.DataFrame(data, columns=rekuten_usedColumns)

#print(df)

#method2: read only use columns
data = pd.read_csv('enavi202102(1312).csv', usecols=rakuten_usedColumns)
#print(data)

###########################
# Handle dummy row section
###########################
df = pd.DataFrame(data).dropna()

#rename column for future use
df = df.rename(columns=rakuten_colsDict)

print(df)

###########################
# Store to db (ignore duplicates)
###########################

#create new db
db = dataset.connect('sqlite:///testdb.db')

transactionTable = db['transaction']

for row in df.itertuples():
    transactionTable.insert_ignore(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                        where=row.where,
                                        whose=row.whose,
                                        totalPayment=int(row.totalPayment)
                                        ),
                                   rakuten_keyCols
                                   )

transactions = transactionTable.all()

for transaction in transactions:
    print(transaction)


###########################
# TODO
###########################

