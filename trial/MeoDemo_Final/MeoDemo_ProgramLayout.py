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


    acc_table1 = {'Account': ['Yucho 1 (Meo)', 'Yucho 2 (Vit)', 'Vietcombank', 'USD', 'Cash'],
                'Value': [9999, 8888, 7777, 6666, 5555]}

    acc_table2 = {'Account': ['Meo Yucho', 'Meo Cash', 'Vit Yucho', 'Vit Cash'],
                  'Value': [9999, 8888, 7777, 6666]}

    acc_table3 = {'Account': ['Sum Yucho 1', 'Sum Yucho 2', 'Sum Meo', 'Sum Vit'],
                  'Value': [9999, 8888, 7777, 6666]}

    df_tb1 = pd.DataFrame(acc_table1, columns = ['Account', 'Value'])
    df_tb2 = pd.DataFrame(acc_table2, columns=['Account', 'Value'])
    df_tb3 = pd.DataFrame(acc_table3, columns=['Account', 'Value'])

    food = 4
    eatOut = 24
    housing = 31
    medical = 2
    others = 3

    # sample data
    raw_data = {'Category': ['Food', 'EatingOut', 'Housing', 'Medical', 'Others'],
                'Payment': [food, eatOut, housing, medical, others]}

    df = pd.DataFrame(raw_data, columns = ['Category', 'Payment'])

    YearList = '2020', '2021'
    MonthList = 'All', '01', '02', '03', '04'

    main_layout = [[sg.Text('Enter File Link')],
                   [sg.Input(key='-INPUT-'), sg.FileBrowse('Select File')],
                   [    sg.Button('Process Rakuten'),
                        sg.Button('Process Amazon'),
                        sg.Button('Process Yahoo'),
                        sg.Button('Process Correction Sheet'),
                        sg.Button('Process Manual Data')
                    ],
                   [sg.Combo(values=YearList), sg.Combo(values=MonthList)],
                   [sg.Canvas(key='-AccountSummary-')],
                   [sg.Canvas(key='-PieChartWithTable-'), sg.Canvas(key='-GraphChart-')]
                ]

    window = sg.Window('Home Accounting Tool Test', main_layout, finalize=True)

    return window, df, df_tb1, df_tb2, df_tb3

def init_window_up(window, df_tb1, df_tb2, df_tb3):
    canvas_elem = window['-AccountSummary-']
    canvas = canvas_elem.TKCanvas

    # add the plot to the window
    fig = Figure(figsize=(6.4,2))

    ax_tb1 = fig.add_subplot(131, aspect='equal')
    ax_tb1.axis('off')
    tbl1 = table(ax_tb1, df_tb1, loc='center')
    # tbl.auto_set_font_size(True)

    ax_tb2 = fig.add_subplot(132, aspect='equal')
    ax_tb2.axis('off')
    tbl2 = table(ax_tb2, df_tb2, loc='center')

    ax_tb3 = fig.add_subplot(133, aspect='equal')
    ax_tb3.axis('off')
    tbl3 = table(ax_tb3, df_tb3, loc='center')

    fig_agg = draw_figure(canvas, fig)

    return fig_agg, ax_tb1, ax_tb2, ax_tb3

def init_window_down(window, df):
    canvas_elem = window['-PieChartWithTable-']
    canvas = canvas_elem.TKCanvas

    # add the plot to the window
    fig = Figure()
    ax1 = fig.add_subplot(121, aspect='equal')

    df.plot(kind='pie', y='Payment', ax=ax1, autopct='%1.1f%%',
            startangle=90, shadow=False, labels=df['Category'], legend=False, fontsize=14)

    ax2 = fig.add_subplot(122, aspect='equal')
    ax2.axis('off')
    tbl = table(ax2, df, loc='center')
    # tbl.auto_set_font_size(True)

    # plot chart
    ax1.grid()
    fig_agg = draw_figure(canvas, fig)

    return fig_agg, ax1, ax2

def update_account_tables(fig_agg, df_tb1, df_tb2, df_tb3, ax_tb1, ax_tb2, ax_tb3):

    ax_tb1.cla()
    ax_tb1.axis('off')
    tbl1 = table(ax_tb1, df_tb1, loc='center')

    ax_tb2.cla()
    ax_tb2.axis('off')
    tbl2 = table(ax_tb2, df_tb2, loc='center')

    ax_tb3.cla()
    ax_tb3.axis('off')
    tbl3 = table(ax_tb3, df_tb3, loc='center')

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

def process_import_Rakuten(csvPath):

    #############
    # DB path
    # TODO: handling this bullshit (pass table does not work)
    #############
    dbName = 'Preparation//ExpenseLibrary.db'
    dbPath = os.path.join(__location__, dbName)

    # open db
    db = dataset.connect('sqlite:///' + dbPath)

    expenseLibTable = db['ExpenseLib']

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
    rakuten_keyCols = ['date', 'info', 'whose', 'totalPayment', 'category', 'note']

    strange_CatDict = ['Pocket Money', 'Income', 'Income', 'Adjustment', 'Return', 'Others', 'Unknown', 'Need Confirmed']

    rakuten_data = pd.read_csv(csvPath, usecols=rakuten_usedColumns)

    # Handle dummy row section
    rakuten_df = pd.DataFrame(rakuten_data).dropna()

    # rename column for future use
    rakuten_df = rakuten_df.rename(columns=rakuten_colsDict)

    ###########################
    # Store to db (ignore duplicates)
    ###########################

    needModifiedRow_cols = ['date', 'where', 'whose', 'totalPayment', 'info', 'category', 'note']
    needModifiedRow = []

    for row in rakuten_df.itertuples():

        payAt = row.where
        libData = expenseLibTable.find_one(where=payAt)

        if (libData != None):

            category = libData['category']
            info = libData['what']

            if category in strange_CatDict:
                print('Strange Data - Need Handle', libData)
                needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                            where=row.where,
                                            whose=row.whose,
                                            totalPayment=int(row.totalPayment),
                                            info=info,
                                            category=category,
                                            note='Need correction due to strange category'
                                            )
                                       )
            else:
                #print('Normal Data - Imported', libData)
                rakutenTable.insert_ignore(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                                info=info,
                                                whose='Home',
                                                totalPayment=int(row.totalPayment),
                                                note='Automatically imported'
                                                ),
                                           rakuten_keyCols
                                           )
        else:
            print('New Item - Need Hanlde', libData)
            needModifiedRow.append(dict(date=datetime.strptime(row.date, '%Y/%m/%d').date(),
                                        where=row.where,
                                        whose=row.whose,
                                        totalPayment=int(row.totalPayment),
                                        info='No info',
                                        category='No catefory',
                                        note='New Data'
                                        )
                                   )

    #print(needModifiedRow)

    needModifiedRow_df = pd.DataFrame(needModifiedRow, columns=needModifiedRow_cols)

    modCsvName = 'Output//tobeConfirmed_Rakuten_{date:%Y%m%d_%H%M%S}.csv'.format(date=datetime.now())
    modCsvPath = os.path.join(__location__, modCsvName)

    needModifiedRow_df.to_csv(modCsvPath)

def main():

    # create the form and show it without the plot
    window, df, df_tb1, df_tb2, df_tb3 = declare_window()

    fig_agg_down, ax1, ax2 = init_window_down(window, df)
    fig_agg_up, ax_tb1, ax_tb2, ax_tb3 = init_window_up(window, df_tb1, df_tb2, df_tb3)

    #rakutenDB, rakutenTable = get_expenseLibTable()
    #expenseLibDB, expenseLibTable = get_rakutenTable()



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
            update_pilechart_and_table(fig_agg_down, df, ax1, ax2)
            update_account_tables(fig_agg_up, df_tb1, df_tb2, df_tb3, ax_tb1, ax_tb2, ax_tb3)
        elif event == 'Process Manual Data':
            print("[LOG] Clicked Process Manual Data Button!")

    window.close()
    exit(0)


if __name__ == '__main__':
    main()