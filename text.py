import PySimpleGUI as sg

data = [
    [11,12,13,14],
    [21,22,23,24],
    [31,32,33,34],
    [41,42,43,44],
    [51,52,53,54]
    ]

print(data[0])
print([a[0] for a in data])


layout = [
    [sg.Table(data, headings=["col1", "col2", "col3", "col4"],
    background_color= "green",
    alternating_row_color="gray",
    num_rows=3)]
    ]

window = sg.Window("Scroll Test", layout=layout)

window.read()