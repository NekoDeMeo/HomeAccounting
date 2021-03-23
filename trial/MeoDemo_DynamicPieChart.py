import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


food = 4
eatOut = 24
housing = 31
medical = 2
others = 3

# sample data
raw_data = {'Category': ['Food', 'EatingOut', 'Housing', 'Medical', 'Others'],
            'Payment': [food, eatOut, housing, medical, others]}
df = pd.DataFrame(raw_data, columns = ['Category', 'Payment'])


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# ------------------------------- Beginning of GUI CODE -------------------------------

# define the window layout
layout = [[sg.Text('Plot test')],
          [sg.Canvas(key='-CANVAS-')],
            [sg.Button('Increase1'),
             sg.Button('Increase2'),
             sg.Button('Increase3'),
             sg.Button('Increase4'),
             sg.Button('Increase5'),]
          ]

def update_table(fig_agg, df, ax1, ax2):
    df.at[0, 'Payment'] += 1
    ax1.cla()
    ax1.axis('off')
    df.plot(kind='pie', y='Payment', ax=ax1, autopct='%1.1f%%',
            startangle=90, shadow=False, labels=df['Category'], legend=False, fontsize=14)

    ax2.cla()
    ax2.axis('off')
    tbl = table(ax2, df, loc='center')

    fig_agg.draw()


def main():
    global fig_agg, canvas, fig, df, ax1, ax2

# create the form and show it without the plot
window = sg.Window('Dynamic PierChart with Table', layout, finalize=True)

canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas

# add the plot to the window
fig = Figure()
ax1 = fig.add_subplot(121, aspect='equal')

df.plot(kind='pie', y='Payment', ax=ax1, autopct='%1.1f%%',
 startangle=90, shadow=False, labels=df['Category'], legend = False, fontsize=14)

ax2 = fig.add_subplot(122, aspect='equal')
ax2.axis('off')
tbl = table(ax2, df, loc='center')
tbl.auto_set_font_size(True)

# plot chart
ax1.grid()
fig_agg = draw_figure(canvas, fig)

while True:

    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Increase1':
        update_table(fig_agg, df, ax1, ax2)

    elif event == 'Increase2':
        eatOut += 1
    elif event == 'Increase3':
        housing += 1
    elif event == 'Increase4':
        medical += 1
    elif event == 'Increase5':
        others += 1

window.close()

if __name__ == '__main__':
    main()