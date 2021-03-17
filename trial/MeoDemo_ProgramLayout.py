import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use('TkAgg')

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'

x = 15
y = 30
z = 45
t = 10

sizes = [x, y, z, t]
#sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

layout = [[sg.Text('Plot test')],
          [sg.Canvas(key='-PieChart-')],
          [sg.Button('Process Credit Logs')]]

def make_window(theme):
    sg.theme(theme)

    YearList = '2020', '2021'
    MonthList = 'All', '01', '02', '03', '04'

    TableDataList = [['Task01', 'Value01'], ['Task02', 'Value02']]
    headings = ["Name", "Score"]

    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']]]

    right_click_menu_def = [[], ['Nothing', 'More Nothing', 'Exit']]

    main_layout = [[sg.Menu(menu_def, key='-MENU-')],
                    [sg.Text('Enter File Link')],
                    [sg.Input(key='-INTPUT'), sg.Button('Select File')],
                    [sg.Button('Process Credit Logs'), sg.Button('Process Manual Data')],
                    [sg.Listbox(values=YearList), sg.Listbox(values=MonthList)],
                    [sg.Canvas(key='-PieChart-'), sg.Table(values=TableDataList, headings=headings),
                     sg.Canvas(key='-GraphChart-')]
                    ]

    return sg.Window('All Elements Demo', main_layout, right_click_menu=right_click_menu_def)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def main():
    global y, z
    #window = make_window(sg.theme())

    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True,
                       element_justification='center', font='Helvetica 18')

    # add the plot to the window
    fig_canvas_agg = draw_figure(window['-PieChart-'].TKCanvas, fig1)

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

            y = y + 1
            z = z - 1

            fig_canvas_agg = draw_figure(window['-PieChart-'].TKCanvas, fig1)
            #TODO: how to update canvas live?

            sg.popup("You pressed a Process Credit Logs button!")
            print("[LOG] Dismissing Popup!")
        elif event == 'Process Manual Data':
            print("[LOG] Clicked Process Manual Data Button!")
            y = y - 1
            z = z + 1

            sg.popup("You pressed a Process Manual Data button!")
            print("[LOG] Dismissing Popup!")

    window.close()
    exit(0)


if __name__ == '__main__':
    main()