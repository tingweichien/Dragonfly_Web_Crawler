## GUI
# Reference:
# https://www.geeksforgeeks.org/python-os-path-exists-method/
# https://www.tutorialspoint.com/python/tk_message.htm
# https://www.itread01.com/content/1548486187.html
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/anchors.html
# https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
# https://www.youtube.com/watch?v=UZX5kH72Yx4
# https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-attribute-name
# https://stackoverflow.com/questions/31264522/getting-the-selected-value-from-combobox-in-tkinter
# https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
# https://pysimplegui.readthedocs.io/en/latest/call%20reference/?#table-element

from Dragonfly import *
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk 
from tkinter.messagebox import *
import os
import os.path
import PySimpleGUI as PYGUI
import gmplot
import webbrowser
from Index import *


##################################################################
#\ arguement
InputArgumentsLabel = ["Account", "Password", "ID"]

# auto save account and password file
path = os.getenv('temp')
filename = os.path.join(path, 'info.txt')

current_dropdown_index = 0 
Login_Response = 0
Login_state = 0

##################################################################
# check if the user enter the info properly
def check(InputList):
    index = 0
    string = ""
    for Input in InputList:
        if (Input == ''):
            string += "[" + InputArgumentsLabel[index] + "] "
        index += 1
    if (len(string) > 0):
        messagebox.showwarning('Warning!!!', string + "should not be empty!!!!")
    return len(string)


#################################################################
# 嘗試自動填寫使用者名稱和密碼
def auto_fill():
    try:
        with open(filename) as fp:
            n, p = fp.read().strip().split(',')
            return [n, p]
    except:
        return['', '']


##################################################################
def enter_button():
    InputList = [account.get(), password.get(), ID.get()]

    # check if the user enter the info properly
    empty_or_not = check(InputList)
    
    #login
    #[Login_Response, Login_state] = Login_Web(account.get(), password.get())    
    if (Login_state == False):
        messagebox.showwarning('Warning!!!','Please Login first')
        return

    # this datd do not contain the Longitude and Latitude infomation
    if (empty_or_not == 0):
        [Output_LNG, Output_LAT] = DataCrawler(Login_Response, ID.get())
        if (Output_LNG == '' or Output_LAT == ''):
            Output_LNG = 'No Data'
            Output_LAT = 'No Data'
        elif (Output_LNG == -2):
            messagebox.showwarning('Warning!!!', InputArgumentsLabel[2] + " number is out of range!!!!")    #ID number overflow

        blank_LNG.delete(0, END)
        blank_LAT.delete(0, END)    
        blank_LNG.insert(0, Output_LNG)
        blank_LAT.insert(0, Output_LAT)

    # and write the account and password to the filename
    with open(filename, 'w') as fp:
        fp.write(','.join((InputList[0], InputList[1])))


def LoginButton():
    global Login_Response, Login_state
    [Login_Response, Login_state] = Login_Web(account.get(), password.get())
    if (Login_state == False):    
        messagebox.showwarning('Warning!!!', InputArgumentsLabel[0] + " or " + InputArgumentsLabel[1] + " might be incorrect!!!!")  #incorrect account or password
        

############################################################
#\ map
# https://github.com/gmplot/gmplot/blob/master/gmplot/google_map_plotter.py
# https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python/40905794
'''
apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)
'''


def show_on_map(map_list):
    global mapfilename
    file_path = os.path.realpath(mapfilename)
    gmp = gmplot.GoogleMapPlotter(float(map_list[0].Latitude), float(map_list[0].Longitude), 13)
    for index in map_list:
        context = "[User]: " + index.User + "\n[Time]: " + index.Dates + index.Times + "\n[Place]: " + index.Place + "\n[Altitude]: " + index.Altitude          
        gmp.marker(float(index.Latitude), float(index.Longitude),
                    color="red",
                    label= index.Place.encode('unicode_escape').decode("utf-8"),
                    info_window=context.encode('unicode_escape').decode("utf-8"))
        gmp.draw(file_path)
    webbrowser.open(file_path) 



############################################################
#\ Table
def New_table(map_result_List):
    global Table_scroll_num
    Data = [
        [index.Place,
        index.Dates + "-" + index.Times,
        index.User,
        index.Latitude,
        index.Longitude,
        index.Altitude] for index in map_result_List
    ]

    layout = [
        [PYGUI.Text(str(var_species.get()))],
        [PYGUI.Table(Data,
                    headings=["Place", "Date-Time", "Recorder",
                                    "Latitude", "Longitude", "Altitude"],
                    justification="center",
                    num_rows=Table_scroll_num,
                    display_row_numbers=True,)],
        [PYGUI.Button(button_text='Show on map')]]
    
    window = PYGUI.Window("Show Species info", layout=layout)

    while True:             # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Show on map':
            show_on_map(map_result_List)
    window.Close()



#############################################################
# dropdown list
def Family_drop_down_menu_callback(*args):
    
    global current_dropdown_index
    current_dropdown_index = Family_drop_down_menu.current()
    tmp = Species_Name_Group[current_dropdown_index]
    Species_drop_down_menu['value'] = tmp
    var_species.set(tmp[0])
    print (var_family.get())
    print (Family_drop_down_menu.current())

      
def Species_drop_down_menu_callback(*args):
    map_result_List = SpeiciesCrawler(Login_Response, var_family.get(), var_species.get())
    New_table(map_result_List)
   



################################################################### main
################################################################### start
# 建立一個視窗物件
main = Tk()

# 視窗基本設定
main.title("蜻蜓資料庫經緯度查詢")
main.geometry('600x480') # Width*Height

# 設定圖片
current_path = os.getcwd()  # directory from where script was ran
canvas = Canvas(main, height=300, width=380)
image_path = current_path + "\dragonfly_picture.gif"
image_file = PhotoImage(file = image_path)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)

# label
account_label = Label(main, text = "Account:")
password_label = Label(main, text = "Password:")
id_label = Label(main, text = "ID:")
latitude_label = Label(main, text = "The Latitude is:")
longitude_label = Label(main, text="The Longitude is:")
Species_label = Label(main, text="Select the Family anf Species")

# Entry
VarName = StringVar(main, value='')
VarPwd = StringVar(main, value='')
account = Entry(main, textvariable = VarName)
password = Entry(main, textvariable = VarPwd)
ID = Entry(main)
blank_LNG = Entry(main)
blank_LAT = Entry(main)


# drop down menu
# family
var_family = StringVar(main)
var_family.set(Species_Family_Name[0])
Family_drop_down_menu = ttk.Combobox(main, width=10, textvariable=var_family, values=Species_Family_Name)
Family_drop_down_menu.bind("<<ComboboxSelected>>", Family_drop_down_menu_callback)


# species
var_species = StringVar(main)
var_species.set(Calopterygidae_Species[0])
Species_drop_down_menu = ttk.Combobox(main, width=10, textvariable=var_species, values=Species_Name_Group[current_dropdown_index])
Species_drop_down_menu.bind("<<ComboboxSelected>>", Species_drop_down_menu_callback)
Family_drop_down_menu.grid(row=2, column=3)
Species_drop_down_menu.grid(row=2, column=4)


# try to auto fill the account and password
[n, p] = auto_fill()
VarName.set(n)
VarPwd.set(p)   


# button
login_button = Button(main,
                text='Login',
                justify = "center",
                command=LoginButton)

# Button(main, text='Quit', command=main.destroy).grid(row=5, column=0, sticky=W, pady=4)
Enter_button = Button( main,
                text='Enter\b',
                command=enter_button,
                height=2,
                width=15,
                justify = "center",
                bg="gray80")
                # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png

#Table
#table = Table(main, result_list, 3, 1)
'''
layout = [
    [PYGUI.Table(data, headings=["","","","","",""], num_rows=5)]
]
window = PYGUI.Window("Coordinate Info", layout=layout)
window.Read()
'''


# grid
canvas.grid(row = 0, column = 0, columnspan = 2)

account_label.grid(row=1)
password_label.grid(row=2)
id_label.grid(row=3)
latitude_label.grid(row=5)
longitude_label.grid(row=6)
Species_label.grid(row=1, column=3,columnspan=2)

account.grid(row=1, column=1)
password.grid(row=2, column=1)
ID.grid(row=3, column=1)
blank_LAT.grid(row=5, column=1)
blank_LNG.grid(row=6, column=1)

Family_drop_down_menu.grid(row=2, column=3)
Species_drop_down_menu.grid(row=2, column=4)

login_button.grid(row=4, column=0, pady=2)
#Enter_button.grid(row=4, column=1, columnspan=1, sticky=W+E, pady=2)
Enter_button.grid(row=4, column=1, columnspan=1, pady=2)

mainloop()




