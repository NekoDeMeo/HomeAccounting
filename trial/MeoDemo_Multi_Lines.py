#!/usr/bin/env python
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Paste your Pyplot code into the section marked below.

Do all of your plotting as you normally would, but do NOT call plt.show(). 
Stop just short of calling plt.show() and let the GUI do the rest.

The remainder of the program will convert your plot and display it in the GUI.
If you want to change the GUI, make changes to the GUI portion marked below.

"""

# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




#values_to_plot = (20, 35, 30, 35, 27)
#ind = np.arange(len(values_to_plot))
#width = 0.4

# p1 = plt.bar(ind, values_to_plot, width)
#
# plt.ylabel('Y-Axis Values')
# plt.title('Plot Title')
# plt.xticks(ind, ('Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'))
# plt.yticks(np.arange(0, 81, 10))
# plt.legend((p1[0],), ('Data Group 1',))


# ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# ------------------------------- Beginning of Matplotlib helper code -----------------------

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# ------------------------------- Beginning of GUI CODE -------------------------------




def declare_window():

    sg.theme('Light Brown 3')

    # sample data
    raw_data = {'x_values': range(1, 13),
                'y1_values': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000 ],
                'y2_values': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
                'y3_values': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
                }

    df = pd.DataFrame(raw_data, columns = ['x_values', 'y1_values', 'y2_values', 'y3_values'])

    # define the window layout
    layout = [[sg.Text('Plot test', font='Any 18')],
              [sg.Canvas(key='-CANVAS-')],
              [sg.OK(size=(4, 2))],
              [sg.Button('Button')]
              ]

    # create the form and show it without the plot
    window = sg.Window('CreditReport_RAW Multiple chart',
                       layout, force_toplevel=True, finalize=True)


    return window, df

def init_window(window, df):
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas


    # multiple line plots
    plt.plot('x_values', 'y1_values', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue',
             linewidth=4)
    plt.plot('x_values', 'y2_values', data=df, marker='', color='olive', linewidth=2)
    plt.plot('x_values', 'y3_values', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    # show legend
    plt.legend()

    fig = plt.gcf()  # if using Pyplot then get the figure from the plot

    fig_agg = draw_figure(canvas, fig)

    return fig_agg

def update_chart(fig_agg, df):
    df.at[0, 'y3_values'] += 100

    plt.cla()
    plt.plot('x_values', 'y1_values', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue',
             linewidth=4)
    plt.plot('x_values', 'y2_values', data=df, marker='', color='olive', linewidth=2)
    plt.plot('x_values', 'y3_values', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")

    plt.legend()

    fig_agg.draw()

def declare_window_1():
    sg.theme('Light Brown 3')

    # sample data
    raw_data = {'x_values': range(1, 13),
                'y1_values': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000],
                'y2_values': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
                'y3_values': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
                }

    df = pd.DataFrame(raw_data, columns=['x_values', 'y1_values', 'y2_values', 'y3_values'])

    # define the window layout
    layout = [[sg.Text('Plot test', font='Any 18')],
              [sg.Canvas(key='-CANVAS-')],
              [sg.Button('Button')]
              ]

    # create the form and show it without the plot
    window = sg.Window('CreditReport_RAW Multiple chart',
                       layout, force_toplevel=True, finalize=True)

    return window, df

def init_window_1(window, df):
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas

    # add the plot to the window
    fig = Figure(figsize=(6,6))
    ax1 = fig.add_subplot(111)

    df.plot(kind = 'line', x='x_values', y='y1_values', ax=ax1, marker='o', markerfacecolor='blue', markersize=12, color='skyblue',
             linewidth=4)

    df.plot(kind='line', x='x_values', y='y2_values', ax=ax1, marker='', color='olive', linewidth=2)

    df.plot(kind='line', x='x_values', y='y3_values', ax=ax1, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")

    # show legend
    ax1.legend()

    # plot chart
    ax1.grid()
    fig_agg = draw_figure(canvas, fig)

    return fig_agg, ax1

def update_chart_1(fig_agg, df, ax1):

    df.at[0, 'y3_values'] += 100

    ax1.cla()

    df.plot(kind = 'line', x='x_values', y='y1_values', ax=ax1, marker='o', markerfacecolor='blue', markersize=12, color='skyblue',
             linewidth=4)

    df.plot(kind='line', x='x_values', y='y2_values', ax=ax1, marker='', color='olive', linewidth=2)

    df.plot(kind='line', x='x_values', y='y3_values', ax=ax1, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")

    ax1.legend()
    ax1.grid()
    fig_agg.draw()


def main():

    # create the form and show it without the plot
    # window, df = declare_window()
    # fig_agg = init_window(window, df)

    window, df = declare_window_1()

    fig_agg, ax1 = init_window_1(window, df)

    # show it all again and get buttons
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
        elif event == 'Button':
            print("[LOG] Clicked Button!")
            #update_chart(fig_agg, df)
            update_chart_1(fig_agg, df, ax1)

    window.close()
    exit(0)


if __name__ == '__main__':
    main()