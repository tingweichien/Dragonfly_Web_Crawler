

import PySimpleGUI as sg

data = [
    [11,12,13,14],
    [21,22,23,24],
    [31,32,33,34],
    [41,42,43,44],
    [51,52,53,54]
    ]
data2 = [["","","",""]]

print(data[0])
print([a[0] for a in data])


layout = [
    [sg.Table(data, headings=["col1", "col2", "col3", "col4"],
    visible_column_map=[True,True,False,True],
    background_color= "green",
    alternating_row_color="gray",
    #visible=False,
    num_rows=3)],
    [sg.Text("test",relief=sg.RELIEF_SOLID,text_color="red")],
    [sg.Text("test",relief=sg.RELIEF_RIDGE), sg.Text("test",relief=sg.RELIEF_GROOVE),sg.Text("test",relief=sg.RELIEF_RIDGE), sg.Text("test",relief=sg.RELIEF_RAISED)],
    [sg.Table(data, headings=["col1", "col2", "col3", "col4"],
    background_color= "green",
    alternating_row_color="gray",
    visible=False,
    num_rows=3)],
    [sg.Text("test",relief=sg.RELIEF_FLAT)],
    [sg.Text("test",relief=sg.RELIEF_SUNKEN)],
    [sg.Table(data2, headings=["col1", "col2", "col3", "col4"],
    visible=False,
    num_rows=3)],   
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

for i in range(0, 892):                            
    gmap1.marker(30.3164945, 78.03219179999999+i*0.5,
                    color='cornflowerblue',
                    title="test",
                    label="test-label",
                    info_window="info_window")
                                      
  
# Pass the absolute path
path = os.path.realpath(mapfilename)
gmap1.draw(path)
webbrowser.open(path)
'''

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

'''
import colorama
colorama.init()
start = "\033[1;31m"
end = "\033[0;0m"
print("File is: " + start + "<placeholder>" + end)
'''


'''
import gmaps
gmaps.configure(api_key='AI...')
nuclear_power_plants = [
{'name': 'Atucha', 'location': (-34.0, -59.167), 'active_reactors': 1},
{'name': 'Embalse', 'location': (-32.2333, -64.4333), 'active_reactors': 1},
{'name': 'Armenia', 'location': (40.167, 44.133), 'active_reactors': 1},
{'name': 'Br', 'location': (51.217, 5.083), 'active_reactors': 1},
{'name': 'Doel', 'location': (51.333, 4.25), 'active_reactors': 4},
{'name': 'Tihange', 'location': (50.517, 5.283), 'active_reactors': 3}
]
plant_locations = [plant['location'] for plant in nuclear_power_plants]
info_box_template = """
<dl>
<dt>Name</dt><dd>{name}</dd>
<dt>Number reactors</dt><dd>{active_reactors}</dd>
</dl>
"""
plant_info = [info_box_template.format(**plant) for plant in nuclear_power_plants]
marker_layer = gmaps.marker_layer(plant_locations, info_box_content=plant_info)
fig = gmaps.figure()
fig.add_layer(marker_layer)
fig
'''
'''
import tkinter as tk 
from tkinter import ttk 
   
  
LARGEFONT =("Verdana", 35) 
   
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
          
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, Page1, Page2): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(StartPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 
   
# first window frame startpage 
   
class StartPage(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
          
        # label of frame Layout 2 
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT) 
          
        # putting the grid in its place by using 
        # grid 
        label.grid(row = 0, column = 4, padx = 10, pady = 10)  
   
        button1 = ttk.Button(self, text ="Page 1", 
        command = lambda : controller.show_frame(Page1)) 
      
        # putting the button in its place by 
        # using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 
   
        ## button to show frame 2 with text layout2 
        button2 = ttk.Button(self, text ="Page 2", 
        command = lambda : controller.show_frame(Page2)) 
      
        # putting the button in its place by 
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 
   
           
   
   
# second window frame page1  
class Page1(tk.Frame): 
      
    def __init__(self, parent, controller): 
          
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
   
        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="StartPage", 
                            command = lambda : controller.show_frame(StartPage)) 
      
        # putting the button in its place  
        # by using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 
   
        # button to show frame 2 with text 
        # layout2 
        button2 = ttk.Button(self, text ="Page 2", 
                            command = lambda : controller.show_frame(Page2)) 
      
        # putting the button in its place by  
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 
   
   
   
   
# third window frame page2 
class Page2(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
   
        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="Page 1", 
                            command = lambda : controller.show_frame(Page1)) 
      
        # putting the button in its place by  
        # using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 
   
        # button to show frame 3 with text 
        # layout3 
        button2 = ttk.Button(self, text ="Startpage", 
                            command = lambda : controller.show_frame(StartPage)) 
      
        # putting the button in its place by 
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 
   
   
# Driver Code 
app = tkinterApp() 
app.mainloop() 
'''

'''
l = ['tt', 'tt', 'tr', 'tc', 'ata', 'tt', 'at']
print(list(set(l)))
import os
import os.path
import PySimpleGUI as sg
for i in range(10000000):
    sg.PopupAnimated(os.getcwd() + "\Waiting.gif", background_color='white', time_between_frames=50)

sg.PopupAnimated(None)  # close all Animated Popups
'''

