import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandas.plotting import table
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


def declare_window():
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
                   [sg.Input(key='-INTPUT'), sg.FileBrowse('Select File')],
                   [sg.Button('Process Credit Logs'), sg.Button('Process Manual Data')],
                   [sg.Combo(values=YearList), sg.Combo(values=MonthList)],
                   [sg.Canvas(key='-PieChartWithTable-'), sg.Canvas(key='-GraphChart-')]
                ]

    window = sg.Window('Home Accounting Tool CreditReport_RAW', main_layout, finalize=True)

    return window, df

def init_window(window, df):
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

def main():

    # create the form and show it without the plot
    window, df = declare_window()

    fig_agg, ax1, ax2 = init_window(window, df)



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
        elif event == 'Process Credit Logs':
            print("[LOG] Clicked Process Credit Logs Button!")
            update_pilechart_and_table(fig_agg, df, ax1, ax2)
        elif event == 'Process Manual Data':
            print("[LOG] Clicked Process Manual Data Button!")

    window.close()
    exit(0)


if __name__ == '__main__':
    main()