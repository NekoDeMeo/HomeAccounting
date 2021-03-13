import dataset
import pandas as pd
from datetime import datetime

#read csv
rakuten_usedColumns = ['利用日', '利用店名・商品名', '利用者', '支払総額']
rakuten_colsDict = {'利用日': 'date', '利用店名・商品名': 'where', '利用者': 'whose', '支払総額': 'totalPayment'}
rakuten_keyCols = ['date', 'where', 'whose', 'totalPayment']

###########################
# Read Rakuten Data
###########################

rakuten_data = pd.read_csv('Rakuten202102.csv', usecols=rakuten_usedColumns)

# Handle dummy row section
rakuten_df = pd.DataFrame(rakuten_data).dropna()

#rename column for future use
rakuten_df = rakuten_df.rename(columns=rakuten_colsDict)

print(rakuten_df)

###########################
# Store to db (ignore duplicates)
###########################

#create new db
db = dataset.connect('sqlite:///testQuery.db')

transactionTable = db['rakuten_transaction']

for row in rakuten_df.itertuples():
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
# Open points
###########################

