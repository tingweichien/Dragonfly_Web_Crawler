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
import colorama

##################################################################
#\ arguement
InputArgumentsLabel = ["Account", "Password"]

# auto save account and password file
path = os.getenv('temp')
filename = os.path.join(path, 'info.txt')

current_dropdown_index = 0 
Login_Response = 0
Login_state = False

LoginlnputList = []

# init text color
colorama.init()

##################################################################
# Check if the user have entered  the info (account and password) or not
def Check(LoginlnputList):
    index = 0
    string = ""
    for Input in LoginlnputList:
        if (Input == ''):
            string += "[" + InputArgumentsLabel[index] + "] "
        index += 1
    if (len(string) > 0):
        messagebox.showwarning('Warning!!!', string + "should not be empty!!!!")
    return len(string)


#################################################################
# 嘗試自動填寫使用者名稱和密碼
def Auto_Fill():
    try:
        with open(filename) as fp:
            n, p = fp.read().strip().split(',')
            return [n, p]
    except:
        return['', '']


##################################################################
def Enter_button():
    global LoginlnputList, Login_state

    # Check if the user enter the info properly
    LoginInput_Empty_Or_Not = Check(LoginlnputList)
    
    #login and ID Check
    if (Login_state == False):
        messagebox.showwarning('Warning!!!','Please Login first')
        return
    elif (ID.get() == ''):
        messagebox.showwarning('Warning!!!','ID should not be empty')
        return

    # Check if this data do not contain the Longitude and Latitude infomation
    if (LoginInput_Empty_Or_Not == 0):
        [Output_LNG, Output_LAT] = DataCrawler(Login_Response, ID.get())
        if (Output_LNG == '' or Output_LAT == ''):
            Output_LNG = 'No Data'
            Output_LAT = 'No Data'
        elif (Output_LNG == -2):
            messagebox.showwarning('Warning!!!', "ID" + " number is out of range!!!! \nShoud be in the range of 0 ~ " + Output_LAT)  #ID number overflow
            return 

        blank_LNG.delete(0, END)
        blank_LAT.delete(0, END)    
        blank_LNG.insert(0, Output_LNG)
        blank_LAT.insert(0, Output_LAT)

    # and write the account and password to the filename
    with open(filename, 'w') as fp:
        fp.write(','.join((LoginlnputList[0], LoginlnputList[1])))


###################################################################################
#\ Login action
def LoginButton():
    global Login_Response, Login_state 
    [Login_Response, Login_state] = Login_Web(account.get(), password.get())
    if (Login_state == False):    
        messagebox.showwarning('Warning!!!', InputArgumentsLabel[0] + " or " + InputArgumentsLabel[1] + " might be incorrect!!!!")  #incorrect account or password
    else:
        login_button.config(bg='green')
        #messagebox.showinfo('Login success', 'Hi~ ' + account.get() + ' welcome')
        main.title("蜻蜓資料庫經緯度查詢 -- "  + account.get() + "已登入")  



#################################################################################
# \ Species find to plot info inthe table and plot on the map
def SpeciesFindButton(*args):
     #login and ID Check
    if (Login_state == False):
        messagebox.showwarning('Warning!!!','Please Login first')
        return
    map_result_List = SpeiciesCrawler(Login_Response, var_family.get(), var_species.get())
    if len(map_result_List) == 0:
        messagebox.showinfo("Infomation", "The selected species does not have any record")
        return
    else:
        New_table(map_result_List)            
        

############################################################
#\ map
# https://github.com/gmplot/gmplot/blob/master/gmplot/google_map_plotter.py
# https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python/40905794
# https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
# marker title has some problem
'''
apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)
'''

def Show_on_map(map_list):
    global mapfilename, map_plot_max_data_num
    file_path = os.path.realpath(mapfilename)
    if (len(map_list) > map_plot_max_data_num):
        del map_list[0: len(map_list) - map_plot_max_data_num]
        
    gmp = gmplot.GoogleMapPlotter(float(map_list[0].Latitude), float(map_list[0].Longitude), 13)
    for index in map_list:
        context = "[User]: " + index.User + "  [Time]: " + index.Dates + index.Times + "  [Place]: " + index.Place + "  [Altitude]: " + index.Altitude          
        gmp.marker(float(index.Latitude), float(index.Longitude),
                    color="red",
                    label= index.Place.encode('unicode_escape').decode("utf-8"),
                    info_window=context.encode('unicode_escape').decode("utf-8"))
        gmp.draw(file_path)
    webbrowser.open(file_path) 




############################################################
#\ Table
# bad since the flexibility of the option are limited
# this coded in PySimpleGUI library
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
            Show_on_map(map_result_List)
    window.Close()



#############################################################
#\ dropdown list
def Family_drop_down_menu_callback(*args): 
    global current_dropdown_index
    current_dropdown_index = Family_drop_down_menu.current()
    tmp = Species_Name_Group[current_dropdown_index]
    Species_drop_down_menu['value'] = tmp
    var_species.set(tmp[0])
    print (var_family.get())
    print (Family_drop_down_menu.current())

'''    
def Species_drop_down_menu_callback(*args):
    # when the species been selected the new table will be created and display
'''
   



################################################################### main
################################################################### start
# 建立一個視窗物件
main = Tk()

# 視窗基本設定
main.title("蜻蜓資料庫經緯度查詢")
main.geometry('500x300')  # Width*Height
#main.config(bg='white')

# 設定圖片
current_path = os.getcwd()  # directory from where script was ran
canvas = Canvas(main, height=100, width=200)
image_path = current_path + "\dragonfly_picture.gif"
image_file = PhotoImage(file = image_path)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)

# label
account_label = Label(main, text = "Account:")
password_label = Label(main, text = "Password:")
id_label = Label(main, text = "ID:")
latitude_label = Label(main, text = "The Latitude is:")
longitude_label = Label(main, text="The Longitude is:")
Species_label = Label(main, text="Select the Family and Species")

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
#Species_drop_down_menu.bind("<<ComboboxSelected>>", Species_drop_down_menu_callback)   # As soon as the dropdown list been selected, the table will automatically pop up  
Family_drop_down_menu.grid(row=2, column=3)
Species_drop_down_menu.grid(row=2, column=4)


# try to auto fill the account and password
[n, p] = Auto_Fill()
VarName.set(n)
VarPwd.set(p)   

# Check password and account and the ID
LoginlnputList = [account.get(), password.get()]

# button
login_button = Button(main,
                text='Login',
                justify='center',
                bg='red',
                command=LoginButton)

# Button(main, text='Quit', command=main.destroy).grid(row=5, column=0, sticky=W, pady=4)
enter_button = Button( main,
                text='ID Enter\b',
                command=Enter_button,
                height=2,
                width=15,
                justify = 'center',
                bg='gray80')
                # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png

species_find_button = Button(main,
                            text='Find Species',
                            command=SpeciesFindButton,
                            height=2,
                            width=15,
                            justify='center')
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
Species_label.grid(row=1, column=3, columnspan=2)

account.grid(row=1, column=1)
password.grid(row=2, column=1)
ID.grid(row=3, column=1)
blank_LAT.grid(row=5, column=1)
blank_LNG.grid(row=6, column=1)

Family_drop_down_menu.grid(row=2, column=3)
Species_drop_down_menu.grid(row=2, column=4)

login_button.grid(row=4, column=0, pady=2)
enter_button.grid(row=4, column=1, columnspan=1, pady=2)
species_find_button.grid(row=4, column=3, columnspan=2)

mainloop()




