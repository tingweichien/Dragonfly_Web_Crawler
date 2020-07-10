
'''
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
'''





# import gmplot package 
import gmplot
import os
import webbrowser
from Index import *
  
# GoogleMapPlotter return Map object 
# Pass the center latitude and 
# center longitude 
gmap1 = gmplot.GoogleMapPlotter(30.3164945, 
                                78.03219179999999, 13)#Zoom

for i in range(0, 5):                            
    gmap1.marker(30.3164945, 78.03219179999999+i*0.1,
                    color='cornflowerblue',
                    title="test",
                    label="test-label",
                    info_window="info_window")
                                      
  
# Pass the absolute path
path = os.path.realpath(mapfilename)
gmap1.draw(path)
webbrowser.open(path)


'''

import PySimpleGUI as sg

def func(message):
    print(message)

layout = [[sg.Button(button_text = '11 22'), sg.Button('2'), sg.Exit()] ]

window = sg.Window('ORIGINAL').Layout(layout)

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == '11 22':
        func('Pressed button 1')
    elif event == '2':
        func('Pressed button 2')
window.Close()

'''