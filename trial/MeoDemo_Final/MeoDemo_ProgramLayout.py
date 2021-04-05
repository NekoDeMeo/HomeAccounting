import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandas.plotting import table
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import dataset
from pathlib import Path
from datetime import datetime

matplotlib.use('TkAgg')

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))




def declare_window():

    df_tb1, df_tb2, df_tb3 = update_balance_data()

    df = get_expense_data()

    YearList = '2020', '2021'
    MonthList = 'All', '01', '02', '03', '04'

    main_layout = [[sg.Text('Enter File Link')],
                   [sg.Input(key='-INPUT-'), sg.FileBrowse('Select File')],
                   [    sg.Button('Process Rakuten'),
                        sg.Button('Process Amazon'),
                        sg.Button('Process Yahoo'),
                        sg.Button('Process Correction Sheet'),
                        sg.Button('Process Manual Data'),
                        sg.Button('Reload Table'),
                    ],
                   [sg.Canvas(key='-AccountSummary-')],
                   [sg.Combo(values=YearList), sg.Combo(values=MonthList), sg.Button('Show')],
                   [sg.Canvas(key='-PieChartWithTable-'), sg.Canvas(key='-GraphChart-')]
                ]

    window = sg.Window('Home Accounting Tool Test', main_layout, finalize=True, location = (500, 100))

    return window, df, df_tb1, df_tb2, df_tb3

def init_window_up(window, df_tb1, df_tb2, df_tb3):
    canvas_elem = window['-AccountSummary-']
    canvas = canvas_elem.TKCanvas

    # add the plot to the window
    fig = Figure(figsize=(12.4,2))

    ax_tb1 = fig.add_subplot(131, aspect='equal')
    ax_tb1.axis('off')
    tbl1 = ax_tb1.table(cellText=df_tb1.values, colLabels=df_tb1.keys(), loc='center')
    tbl1.auto_set_font_size(False)
    tbl1.set_fontsize(12)
    tbl1.scale(2, 2)

    ax_tb2 = fig.add_subplot(132, aspect='equal')
    ax_tb2.axis('off')
    tbl2 = ax_tb2.table(cellText=df_tb2.values, colLabels=df_tb2.keys(), loc='center')
    tbl2.auto_set_font_size(False)
    tbl2.set_fontsize(12)
    tbl2.scale(2, 2)

    ax_tb3 = fig.add_subplot(133, aspect='equal')
    ax_tb3.axis('off')
    tbl3 = ax_tb3.table(cellText=df_tb3.values, colLabels=df_tb3.keys(), loc='center')
    tbl3.auto_set_font_size(False)
    tbl3.set_fontsize(12)
    tbl3.scale(2, 2)

    fig_agg = draw_figure(canvas, fig)

    return fig_agg, ax_tb1, ax_tb2, ax_tb3

def init_window_down(window, df):
    canvas_elem = window['-PieChartWithTable-']
    canvas = canvas_elem.TKCanvas

    # add the plot to the window
    fig = Figure(figsize=(12.4,8))
    ax1 = fig.add_subplot(121, aspect='equal')

    df.plot(kind='pie', y='Value', ax=ax1, autopct='%1.1f%%',
            startangle=90, shadow=False, labels=df['Category'], legend=False, fontsize=14)

    ax2 = fig.add_subplot(122, aspect='equal')
    ax2.axis('off')

    tbl = ax2.table(cellText=df.values, colLabels=df.keys(), loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 2) #width, heigth

    # plot chart
    ax1.grid()
    fig_agg = draw_figure(canvas, fig)

    return fig_agg, ax1, ax2

def update_account_tables(fig_agg, df_tb1, df_tb2, df_tb3, ax_tb1, ax_tb2, ax_tb3):

    ax_tb1.cla()
    ax_tb1.axis('off')
    tbl1 = ax_tb1.table(cellText=df_tb1.values, colLabels=df_tb1.keys(), loc='center')

    ax_tb2.cla()
    ax_tb2.axis('off')
    tbl2 = ax_tb2.table(cellText=df_tb2.values, colLabels=df_tb2.keys(), loc='center')

    ax_tb3.cla()
    ax_tb3.axis('off')
    tbl1 = ax_tb3.table(cellText=df_tb3.values, colLabels=df_tb3.keys(), loc='center')

    tbl1.auto_set_font_size(False)
    tbl1.set_fontsize(12)
    tbl1.scale(2, 2)
    tbl2.auto_set_font_size(False)
    tbl2.set_fontsize(12)
    tbl2.scale(2, 2)
    tbl3.auto_set_font_size(False)
    tbl3.set_fontsize(12)
    tbl3.scale(2, 2)

    fig_agg.draw()

def update_pilechart_and_table(fig_agg, df, ax1, ax2):
    df.at[0, 'Payment'] += 1
    ax1.cla()
    ax1.axis('off')
    df.plot(kind='pie', y='Payment', ax=ax1, autopct='%1.1f%%',
            startangle=90, shadow=False, labels=df['Category'], legend=False, fontsize=14)

    ax2.cla()
    ax2.axis('off')
    tbl = table(ax2, df, loc='center')

    fig_agg.draw()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def get_expenseLibTable():

    dbName = 'Preparation//ExpenseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    expenseLibTable = db['ExpenseLib']

    #libs = expenseLibTable.all()

    #for lib in libs:
    #    print(lib)

    return db, expenseLibTable


def get_rakutenTable():

    dbName = 'CreditDB.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    rakutenTable = db['Rakuten']

    #libs = rakutenTable.all()

    #for lib in libs:
    #    print(lib)

    return db, rakutenTable

def search_lib_for_cat_info_classification_direction_whose(payAt):

    dbName = 'Preparation//ExpenseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    expenseLibTable = db['ExpenseLib']
    expenseCatTable = db['ExpenseCat']

    category = None
    classification = None
    info = None
    direction = None
    whose = None

    libData = expenseLibTable.find_one(where=payAt)

    if (libData != None):
        category = libData['category']
        info = libData['what']
        whose = libData['whose']

        catData = expenseCatTable.find_one(Category=category)

        if (catData != None):
            classification = catData['Classification']
            direction = catData['Direction']

    return category, info, classification, direction, whose

def from_cat_to_classification(category):

    dbName = 'Preparation//ExpenseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    expenseLibTable = db['ExpenseLib']
    expenseCatTable = db['ExpenseCat']

    classification = None

    catData = expenseCatTable.find_one(Category=category)

    if (catData != None):
        classification = catData['Classification']
    else:
        print('Error: could not find classification')

    return classification

def check_valid_category(category):

    dbName = 'Preparation//ExpenseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    expenseCatTable = db['ExpenseCat']

    classification = None

    catData = expenseCatTable.find_one(Category=category)

    if (catData != None):
        ret = True
        classification = catData['Classification']
        direction = catData['Direction']
    else:
        ret = False
        print('Error: could not find classification')

    return ret, classification, direction

def getCycle_Rakuten(csvPath, type):

    filename = os.path.basename(csvPath)

    cycle = None

    if type == 'Rakuten':
        cycle = filename[5:11]

    if type == 'Yahoo':
        cycle = filename[6:12]

    if type == 'Amazon':
        cycle = filename[0:6]

    return cycle

def process_import_Rakuten(csvPath):

    #############
    # DB path
    # TODO: handling this bullshit (pass table does not work)
    #############

    dbName = 'CreditDB.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    rakutenTable = db['Rakuten']

    #############
    # CSV Definition
    #############

    # read csv
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
    rakuten_keyCols = ['date', 'info', 'whose', 'totalPayment', 'category', 'classification', 'direction', 'cycle', 'note']

    strange_CatDict = ['Pocket Money', 'Income', 'Income', 'Adjustment', 'Return', 'Others', 'Unknown', 'Need Confirmed']

    rakuten_data = pd.read_csv(csvPath, usecols=rakuten_usedColumns)

    # Handle dummy row section
    rakuten_df = pd.DataFrame(rakuten_data).dropna()

    # rename column for future use
    rakuten_df = rakuten_df.rename(columns=rakuten_colsDict)

    ###########################
    # Store to db (ignore duplicates)
    ###########################

    needModifiedRow_cols = ['date', 'where', 'whose', 'totalPayment', 'info', 'category', 'type', 'cycle', 'note']
    needModifiedRow = []

    cycle = getCycle_Rakuten(csvPath, 'Rakuten')

    if cycle == None:
        print('Error: File name error')

    for row in rakuten_df.itertuples():

        payAt = row.where

        category, info, classification, direction, whose = search_lib_for_cat_info_classification_direction_whose(payAt)

        if whose == 'Not sure':
            whose = row.whose

        if (category != None):

            if (classification != None):

                if category in strange_CatDict:
                    print('Strange Data - Need Handle', payAt, category)
                    needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                                where=row.where,
                                                whose=whose,
                                                totalPayment=float(row.totalPayment),
                                                info=info,
                                                category=category,
                                                type = 'Rakuten',
                                                cycle = cycle,
                                                note='Manual confirmed unclear transaction'
                                                )
                                           )
                else:
                    # print('Normal Data - Imported', libData)
                    # print('Classification = ', classification)
                    rakutenTable.insert_ignore(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                                    info=info,
                                                    whose=whose,
                                                    totalPayment=float(row.totalPayment),
                                                    category=category,
                                                    classification=classification,
                                                    direction=direction,
                                                    cycle = cycle,
                                                    note='Automatically imported'
                                                    ),
                                               rakuten_keyCols
                                               )

            else:
                print('Error: could not get classification for category', category)

        else:
            print('New Item - Need Hanlde', payAt)
            needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                        where=row.where,
                                        whose=row.whose,
                                        totalPayment=float(row.totalPayment),
                                        info='No info',
                                        category='No catefory',
                                        type='Rakuten',
                                        cycle= cycle,
                                        note='Confirmed new transaction data'
                                        )
                                   )

    for tran in rakutenTable.all():
        print(tran)

    needModifiedRow_df = pd.DataFrame(needModifiedRow, columns=needModifiedRow_cols)

    folderName = 'Output'
    folderpath = os.path.join(__location__, folderName)
    modCsvName = 'tobeConfirmed_' + cycle + '_Rakuten_{date:%Y%m%d_%H%M%S}.csv'.format(date=datetime.now())
    modCsvPath = os.path.join(folderpath, modCsvName)

    needModifiedRow_df.to_csv(modCsvPath)

def process_import_Yahoo(csvPath):

    #############
    # DB path
    # TODO: handling this bullshit (pass table does not work)
    #############

    dbName = 'CreditDB.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    yahooTable = db['Yahoo']

    #############
    # CSV Definition
    #############

    yahoo_usedColumns = ['利用日', '利用店名・商品名', '利用者', '支払総額']
    yahoo_colsDict = {'利用日': 'date', '利用店名・商品名': 'where', '利用者': 'whose', '支払総額': 'totalPayment'}
    yahoo_keyCols = ['date', 'info', 'whose', 'totalPayment', 'category', 'classification', 'direction', 'cycle', 'note']

    strange_CatDict = ['Pocket Money', 'Income', 'Income', 'Adjustment', 'Return', 'Others', 'Unknown', 'Need Confirmed']

    yahoo_data = pd.read_csv(csvPath, encoding='cp932', usecols=yahoo_usedColumns)

    # Handle dummy row section
    yahoo_df = pd.DataFrame(yahoo_data).dropna()

    # rename column for future use
    yahoo_df = yahoo_df.rename(columns=yahoo_colsDict)

    ###########################
    # Store to db (ignore duplicates)
    ###########################

    needModifiedRow_cols = ['date', 'where', 'whose', 'totalPayment', 'info', 'category', 'type', 'cycle', 'note']
    needModifiedRow = []

    cycle = getCycle_Rakuten(csvPath, 'Yahoo')

    if cycle == None:
        print('Error: File name error')

    for row in yahoo_df.itertuples():

        payAt = row.where

        category, info, classification, direction, whose = search_lib_for_cat_info_classification_direction_whose(payAt)

        if whose == 'Not sure':
            whose = row.whose

        if (category != None):

            if (classification != None):

                if category in strange_CatDict:
                    print('Strange Data - Need Handle', payAt, category)
                    needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                                where=row.where,
                                                whose=row.whose,
                                                totalPayment=float(row.totalPayment),
                                                info=info,
                                                category=category,
                                                type='Yahoo',
                                                cycle=cycle,
                                                note='Manually confirmed unclear transaction'
                                                )
                                           )
                else:
                    # print('Normal Data - Imported', libData)
                    # print('Classification = ', classification)
                    yahooTable.insert_ignore(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                                    info=info,
                                                    whose='Home',
                                                    totalPayment=float(row.totalPayment),
                                                    category=category,
                                                    classification=classification,
                                                    direction=direction,
                                                    cycle=cycle,
                                                    note='Automatically imported'
                                                    ),
                                               yahoo_keyCols
                                               )

            else:
                print('Error: could not get classification for category', category)

        else:
            print('New Item - Need Hanlde', payAt)
            needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                        where=row.where,
                                        whose=row.whose,
                                        totalPayment=float(row.totalPayment),
                                        info='No info',
                                        category='No category',
                                        type='Yahoo',
                                        cycle=cycle,
                                        note='New Data'
                                        )
                                   )

    for tran in yahooTable.all():
        print(tran)

    needModifiedRow_df = pd.DataFrame(needModifiedRow, columns=needModifiedRow_cols)

    modCsvName = 'Output//tobeConfirmed_' + cycle + '_Yahoo_{date:%Y%m%d_%H%M%S}.csv'.format(date=datetime.now())
    modCsvPath = os.path.join(__location__, modCsvName)

    needModifiedRow_df.to_csv(modCsvPath)

def process_import_Amazon(csvPath):

    #############
    # CSV Definition
    #############

    amazon_usedColumns = ['ファンタン　ミン　様', '5334-9114-6839-5***', 'Ａｍａｚｏｎマスタークラシック']
    amazon_colsDict = {'ファンタン　ミン　様': 'date', '5334-9114-6839-5***': 'where', 'Ａｍａｚｏｎマスタークラシック': 'totalPayment'}

    amazon_data = pd.read_csv(csvPath, encoding='cp932', usecols=amazon_usedColumns)
    #amazon_data = pd.read_csv(csvPath)

    # Handle dummy row section
    amazon_df = pd.DataFrame(amazon_data).dropna()

    #print(amazon_df)

    # rename column for future use
    amazon_df = amazon_df.rename(columns=amazon_colsDict)

    ###########################
    # Store to db (ignore duplicates)
    ###########################

    needModifiedRow_cols = ['date', 'where', 'whose', 'totalPayment', 'info', 'category', 'type', 'cycle', 'note']
    needModifiedRow = []

    cycle = getCycle_Rakuten(csvPath, 'Amazon')

    if cycle == None:
        print('Error: File name error')

    for row in amazon_df.itertuples():

        # All amazon items need manual modification

        needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                    where=row.where,
                                    whose='Need Check',
                                    totalPayment=float(row.totalPayment),
                                    info='No info',
                                    category='No Cat',
                                    type='Amazon',
                                    cycle=cycle,
                                    note='Manually confirmed Amazon Transaction'
                                    )
                               )

    needModifiedRow_df = pd.DataFrame(needModifiedRow, columns=needModifiedRow_cols)

    modCsvName = 'Output//tobeConfirmed_' + cycle + '_Amazon_{date:%Y%m%d_%H%M%S}.csv'.format(date=datetime.now())
    modCsvPath = os.path.join(__location__, modCsvName)

    needModifiedRow_df.to_csv(modCsvPath)

def process_import_Modified(csvPath):

    #############
    # DB path
    # TODO: handling this bullshit (pass table does not work)
    #############

    dbName = 'CreditDB.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    #############
    # CSV Definition
    #############

    needModifiedRow_cols = ['date', 'where', 'whose', 'totalPayment', 'info', 'category', 'type', 'cycle', 'note']

    credit_keyCols = ['date', 'info', 'whose', 'totalPayment', 'category', 'classification', 'direction', 'cycle', 'note']

    modified_data = pd.read_csv(csvPath, usecols=needModifiedRow_cols)

    # Handle dummy row section
    modified_df = pd.DataFrame(modified_data).dropna()

    ###########################
    # Store to db (ignore duplicates)
    ###########################

    for row in modified_df.itertuples():

        tableName = row.type
        targetTable = db[tableName]

        ret, classification, direction = check_valid_category(row.category)

        if (ret == True):

            validWhose = ['Home', 'Vit', 'Meo']
            if row.whose in validWhose:
                targetTable.insert_ignore(dict(date=datetime.strptime(row.date, '%Y-%m-%d').date(),
                                                info=row.info,
                                                whose=row.whose,
                                                totalPayment=float(row.totalPayment),
                                                category=row.category,
                                                classification=classification,
                                                direction=direction,
                                                cycle=row.cycle,
                                                note=row.note
                                                ),
                                           credit_keyCols
                                           )
            else:
                print('Error: invalid User', row.category)

        else:
            print('Error: invalid Category', row.category)


    #for tran in targetTable.all():
    #    print(tran)


def get_DB_Source(DBName):

    dbName = 'Prepare_Manual//DatabaseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    mapTable = db['DBMappingList']

    targetDB = None
    targetSource = None

    catData = mapTable.find_one(Name=DBName)

    if (catData != None):
        targetDB = catData['Database']
        targetSource = catData['Source']
    else:
        print('Error: could not find DB Name')

    return targetDB, targetSource

def import_Manual_Data(csvPath):

    #############
    # CSV Definition
    #############

    cols = ['date', 'info', 'totalPayment', 'processDB', 'category']

    data = pd.read_csv(csvPath, usecols=cols)

    # Handle dummy row section
    df = pd.DataFrame(data).dropna()

    ###########################
    # Store to db (ignore duplicates)
    ###########################

    for row in df.itertuples():

        tableName = row.processDB
        targetDB, targetSource = get_DB_Source(tableName)

        #############
        # DB path
        # TODO: handling this bullshit (pass table does not work)
        #############

        dbFileName = 'Database//' + targetDB + '.db'
        dbPath = os.path.join(__location__, dbFileName)

        # open db
        db = dataset.connect('sqlite:///' + dbPath)

        targetTable = db[tableName]

        ret, classification, direction = check_valid_category(row.category)

        if (ret == True):

            keyCols = ['date', 'info', 'totalPayment', 'category', 'classification', 'direction', 'note']

            targetTable.insert_ignore(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                           info=row.info,
                                           totalPayment=float(row.totalPayment.replace(',', '')),
                                           category=row.category,
                                           classification=classification,
                                           direction=direction,
                                           note='Imported Manual Input data'
                                           ),
                                      keyCols
                                      )
        else:
            print('Error: invalid Category', row.category)

        db.commit()
        db.close()

    # for tran in targetTable.all():
    #    print(tran)

def calc_all_transaction_in_table(dbPath, tableName):

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    table = db[tableName]

    balance = 0

    for tran in table.all():
        direction = tran['direction']
        if direction == 'In':
            balance += tran['totalPayment']
        elif  direction == 'Out':
            balance -= tran['totalPayment']
        else:
            print('Error: wrong direction at DB:', tableName, ', transaction: ', tran, ', direction: ', direction)

    return balance

def calc_HomeBalance():

    homeBalance = 0
    HomeYB_Main = 0
    HomeYB_Saving = 0
    HomeCash = 0

    dbName = 'Database//Home.db'
    dbPath = os.path.join(__location__, dbName)

    HomeYB_Main = calc_all_transaction_in_table(dbPath, 'HomeYB_Main')
    HomeYB_Saving = calc_all_transaction_in_table(dbPath, 'HomeYB_Saving')
    HomeCash = calc_all_transaction_in_table(dbPath, 'HomeCash')

    homeBalance= HomeYB_Main + HomeYB_Saving + HomeCash

    return homeBalance, HomeYB_Main, HomeYB_Saving, HomeCash

def calc_PersonalBalance():

    meoYB = 0
    vitYB = 0

    meodbName = 'Database//Meo.db'
    meodbPath = os.path.join(__location__, meodbName)

    vitdbName = 'Database//Vit.db'
    vitdbPath = os.path.join(__location__, vitdbName)

    meoYB = calc_all_transaction_in_table(meodbPath, 'MeoYB')
    vitYB = calc_all_transaction_in_table(vitdbPath, 'VitYB')

    return meoYB, vitYB

def calc_OptionalBalance():

    usd = 0
    yb1 = 0
    yb2 = 0
    vcb = 0

    HomeDBName = 'Database//Home.db'
    homeDBPath = os.path.join(__location__, HomeDBName)

    usd = calc_all_transaction_in_table(homeDBPath, 'HomeUSD')

    MomDBName = 'Database//Mom.db'
    MomDBPath = os.path.join(__location__, MomDBName)

    momYB = calc_all_transaction_in_table(MomDBPath, 'MomYB')
    momVCB = calc_all_transaction_in_table(MomDBPath, 'MomVCB')

    homeBalance, HomeYB_Main, HomeYB_Saving, HomeCash = calc_HomeBalance()
    meoYB, vitYB = calc_PersonalBalance()

    yb1 = HomeYB_Main + momYB
    yb2 = HomeYB_Saving + meoYB + vitYB
    vcb = momVCB

    return usd, yb1, yb2, vcb

def remove_zero(str):

    return str[0:len(str)-2]

def update_balance_data():

    # ----------------------
    # Calc Home Balance
    # ----------------------

    homeBalance, HomeYB_Main, HomeYB_Saving, HomeCash = calc_HomeBalance()

    acc_table1 = {'Account': ['Home Balance', '- Yucho Main', '- Yucho Saving', '- Cash'],
                  'Value': [remove_zero(f'{homeBalance:,}'),
                            remove_zero(f'{HomeYB_Main:,}'),
                            remove_zero(f'{HomeYB_Saving:,}'),
                            remove_zero(f'{HomeCash:,}')
                            ]
                  }

    df_tb1 = pd.DataFrame(acc_table1, columns = ['Account', 'Value'])

    # ----------------------
    # Calc Personal Balance
    # ----------------------

    meoBalance, vitBalance = calc_PersonalBalance()

    acc_table2 = {'Account': ['Vit In Bank', 'Meo In Bank'],
                  'Value': [remove_zero(f'{vitBalance:,}'),
                            remove_zero(f'{meoBalance:,}')
                            ]
                  }

    df_tb2 = pd.DataFrame(acc_table2, columns=['Account', 'Value'])

    # ----------------------
    # Calc Optional Balance
    # ----------------------

    usd, yb1, yb2, vcb = calc_OptionalBalance()

    acc_table3 = {'Account': ['USD', 'Yucho 1', 'Yucho 2', 'VCB'],
                  'Value': [remove_zero(f'{usd:,}'),
                            remove_zero(f'{yb1:,}'),
                            remove_zero(f'{yb2:,}'),
                            remove_zero(f'{vcb:,}')
                            ]
                  }

    df_tb3 = pd.DataFrame(acc_table3, columns=['Account', 'Value'])

    return df_tb1, df_tb2, df_tb3

def get_list_by_classification(classification):

    lst = []

    dbName = 'Preparation//ExpenseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    mapTable = db['ExpenseCat']

    result = mapTable.find(Classification=classification)

    for ret in result:
        lst.append(ret['Category'])

    return lst


def get_expense_category_list():

    lst = []

    lst = get_list_by_classification('Expense')
    print(lst)

    return lst


def get_df_by_year_month(year, month, dbPath, tableName):

    expense = []

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    tbl = db[tableName]

    for tran in tbl:

        tmonth = tran['date'].strftime('%m')
        tyear = tran['date'].strftime('%Y')

        if (tmonth == month) and (tyear == year):
            expense.append(dict(totalPayment=float(tran['totalPayment']),
                           category=tran['category']
                            )
                        )

    df = pd.DataFrame(expense, columns=['totalPayment', 'category'])

    return df

def get_all_expense_df_by_year_month(year, month):

    CreditDbName = 'CreditDB.db'
    CreditDBPath = os.path.join(__location__, CreditDbName)

    HomeDbName = 'Database//Home.db'
    HomeDBPath = os.path.join(__location__, HomeDbName)

    df_Rakuten = get_df_by_year_month(year, month, CreditDBPath, 'Rakuten')
    df_Amazon = get_df_by_year_month(year, month, CreditDBPath, 'Amazon')
    df_Yahoo = get_df_by_year_month(year, month, CreditDBPath, 'Yahoo')
    df_HomeYB_Main = get_df_by_year_month(year, month, HomeDBPath, 'HomeYB_Main')
    df_HomeYB_Saving = get_df_by_year_month(year, month, HomeDBPath, 'HomeYB_Saving')

    df = pd.concat([df_Rakuten,
                    df_Amazon,
                    df_Yahoo,
                    df_HomeYB_Main,
                    df_HomeYB_Saving
                    ],
                   ignore_index=True,
                   sort=False
                   )

    return df

def get_filter_expense(display_df, expense_df):

    # TODO: find a way to do this smarter - pandas data frame query/index

    cnt = 0

    for row in display_df.itertuples():
        cat = row.Category
        display_df.at[cnt, 'Value'] = expense_df[expense_df['category'] == cat].sum()['totalPayment']
        cnt += 1

    return display_df

def get_expense_data():

    expenseLst = get_list_by_classification('Expense')
    tbl = {'Category': expenseLst, 'Value': 0}

    display_df = pd.DataFrame(tbl, columns=['Category', 'Value'])

    expense_df = get_all_expense_df_by_year_month('2021', '02')

    df = get_filter_expense(display_df, expense_df)

    return df

def main():

    # create the form and show it without the plot
    window, df, df_tb1, df_tb2, df_tb3 = declare_window()

    fig_agg_up, ax_tb1, ax_tb2, ax_tb3 = init_window_up(window, df_tb1, df_tb2, df_tb3)
    fig_agg_down, ax1, ax2 = init_window_down(window, df)


    # This is an Event Loop
    while True:
        event, values = window.read(timeout=100)

        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
        elif event == 'Process Rakuten':
            print("[LOG] Clicked Rakuten Button!")
            csvPath = values['-INPUT-']
            if ((csvPath != "") and (Path(csvPath).exists())):
                #print('Csvpath = ', csvPath)
                process_import_Rakuten(csvPath)
            else:
                print('Invalid path')

        elif event == 'Process Amazon':
            print("[LOG] Clicked Amazon Button!")
            csvPath = values['-INPUT-']
            if ((csvPath != "") and (Path(csvPath).exists())):
                #print('Csvpath = ', csvPath)
                process_import_Amazon(csvPath)
            else:
                print('Invalid path')

        elif event == 'Process Yahoo':
            print("[LOG] Clicked Yahoo Button!")
            csvPath = values['-INPUT-']
            if ((csvPath != "") and (Path(csvPath).exists())):
                #print('Csvpath = ', csvPath)
                process_import_Yahoo(csvPath)
            else:
                print('Invalid path')

        elif event == 'Process Correction Sheet':
            print("[LOG] Clicked Correction Button!")
            csvPath = values['-INPUT-']
            if ((csvPath != "") and (Path(csvPath).exists())):
                #print('Csvpath = ', csvPath)
                process_import_Modified(csvPath)
            else:
                print('Invalid path')

        elif event == 'Process Manual Data':
            print("[LOG] Clicked Manual Button!")
            csvPath = values['-INPUT-']
            if ((csvPath != "") and (Path(csvPath).exists())):
                #print('Csvpath = ', csvPath)
                import_Manual_Data(csvPath)
            else:
                print('Invalid path')

        elif event == 'Reload Table':
            print("[LOG] Clicked Reload Table!")
            df_tb1, df_tb2, df_tb3 = update_balance_data()
            update_account_tables(fig_agg_up, df_tb1, df_tb2, df_tb3, ax_tb1, ax_tb2, ax_tb3)
        elif event == 'Process Manual Data':
            print("[LOG] Clicked Process Manual Data Button!")

    window.close()
    exit(0)


if __name__ == '__main__':
    main()