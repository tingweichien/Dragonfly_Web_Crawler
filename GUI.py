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

# state the wanted spec for plotting on the map
Place_select_value = ''
User_select_value = ''
Map_spec_method_or_and = ''

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
def IDEnterButton():
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
    tmp_key = True
    if (LoginInput_Empty_Or_Not == 0):
        [Output_LNG, Output_LAT, Output_Detailed_Info] = DataCrawler(Login_Response, ID.get())
        if (Output_LNG == '' or Output_LAT == ''):
            Output_LNG = 'No Data'
            Output_LAT = 'No Data'
            tmp_key = False
        elif (Output_LNG == -2):
            messagebox.showwarning('Warning!!!', "ID" + " number is out of range!!!! \nShoud be in the range of 0 ~ " + Output_LAT)  #ID number overflow
            return 
        blank_LNG.delete(0, END)
        blank_LAT.delete(0, END)    
        blank_LNG.insert(0, Output_LNG)
        blank_LAT.insert(0, Output_LAT)
        if (tmp_key):
            msg = messagebox.askyesno("info", "Do you want to plot it on map?")
            if (msg):
                Show_on_map([Output_Detailed_Info])





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
        main.title("蜻蜓資料庫經緯度查詢 -- " + account.get() + "已登入")
        # and write the account and password to the filename
        with open(filename, 'w') as fp:
            fp.write(','.join((LoginlnputList[0], LoginlnputList[1])))



#################################################################################
# \ Species find to plot info inthe table and plot on the map
def SpeciesFindButton(*args):
     #login and ID Check
    if (Login_state == False):
        messagebox.showwarning('Warning!!!','Please Login first')
        return
    map_result_list = SpeiciesCrawler(Login_Response, var_family.get(), var_species.get())
    if len(map_result_list) == 0:
        messagebox.showinfo("Infomation", "The selected species does not have any record")
        return
    else:
        New_table(map_result_list)
        

        

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

def Show_on_map(input_map_list):
    global mapfilename, map_plot_max_data_num, Map_spec_method_or_and
    map_list = []
    file_path = os.path.realpath(mapfilename)
    # specify by selected item
    for tmp in input_map_list:
        if (len(Place_select_value) > 0):
            if (len(User_select_value) > 0):
                if (Map_spec_method_or_and == 'or'):
                    if ((tmp.Place in Place_select_value) or (tmp.User in User_select_value)):
                        map_list.append(tmp)
                elif (Map_spec_method_or_and == 'and'):
                    if ((tmp.Place in Place_select_value) and (tmp.User in User_select_value)):
                        map_list.append(tmp)
                else:
                    PYGUI.popup_animated(None)
                    messagebox.showwarning("warning", "Please select the method (or , and) between two spec")
                    return []
            else:
                if (tmp.Place in Place_select_value):
                    map_list.append(tmp)
        else:
            if (len(User_select_value) > 0):
                if (tmp.User in User_select_value):
                    map_list.append(tmp)
            else:
                map_list = input_map_list
                break


    # the gmplot have some problem on plotting too many data
    if (len(map_list) > map_plot_max_data_num):
        del map_list[0: len(map_list) - map_plot_max_data_num]
    elif (len(map_list) == 0):  # make sure the map data is not empty
        PYGUI.popup_animated(None)
        messagebox.showinfo("Info", "No data match the spec")
        return []
        
    gmp = gmplot.GoogleMapPlotter(float(map_list[0].Latitude), float(map_list[0].Longitude), 13)
    for index in map_list:
        context = index.User + " / " + index.Dates + " / " + index.Times + " / " + index.Place + " / "  + index.Altitude + "m / " + index.Latitude + ", "  + index.Longitude          
        gmp.marker(float(index.Latitude), float(index.Longitude),
                    color="red",
                    label= index.Place.encode('unicode_escape').decode("utf-8"),
                    info_window=context.encode('unicode_escape').decode("utf-8"))
        gmp.draw(file_path)
    webbrowser.open(file_path)
    return map_list



############################################################
#\ Table
# bad since the flexibility of the option are limited
# this coded in PySimpleGUI library
def New_table(map_result_list):
    global Table_scroll_num, User_select_value, Place_select_value, Map_spec_method_or_and
    Data = [
        [index.Place,
        index.Dates + "-" + index.Times,
        index.User,
        index.Latitude,
        index.Longitude,
        index.Altitude] for index in map_result_list
    ]

    layout = [
        [
        PYGUI.Text("--" + str(var_species.get()) + "--", text_color="black"),
            ],
        [
        PYGUI.Table(Data,
                headings=["Place", "Date-Time", "Recorder",
                                "Latitude", "Longitude", "Altitude"],
                justification="center",
                num_rows=Table_scroll_num,
                display_row_numbers=True)
            ],
        [
        PYGUI.Text("Select the user", auto_size_text=True, justification="center"),
        PYGUI.Text("\tSelect the method", auto_size_text = True, justification="center"),
        PYGUI.Text("Select the place", auto_size_text = True, justification="center"),
            ],
        [
        PYGUI.Listbox(values=list({User_List.User for User_List in map_result_list}),
            enable_events=True,
            size=(None, 5),
            auto_size_text=True,
            select_mode=PYGUI.LISTBOX_SELECT_MODE_MULTIPLE,
            key='User_select'),
        PYGUI.Button(button_text="or",size=(5,3)),
        PYGUI.Button(button_text="and",size=(5,3)),
        PYGUI.Listbox(values=list({Place_List.Place for Place_List in map_result_list}),
            enable_events=True,
            size=(None, 5),
            auto_size_text=True,
            select_mode=PYGUI.LISTBOX_SELECT_MODE_MULTIPLE,
            key='Place_select'),
        PYGUI.Button(button_text='Show on map')      
            ],
        [
        PYGUI.Text("Result after choosing the specs", auto_size_text=True, justification="center", visible=False, key="Spec_Table_Label")
            ],
        [
        PYGUI.Table(values=[[" "," "," "," "," "," "]],
                headings=["Place", "Date-Time", "Recorder",
                                "Latitude", "Longitude", "Altitude"],
                justification="center",
                display_row_numbers=True,
                hide_vertical_scroll=True,
                auto_size_columns=False,
                visible=False,
                num_rows=5,
                key='Spec_Table',
                col_widths = 40)
            ]  
    ]
    
    window = PYGUI.Window("Show Species info", layout=layout)

    while True:             # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Show on map':
            PYGUI.popup_animated(os.getcwd() + "\Loading.gif")
            Spec_DATA = Show_on_map(map_result_list)
            PYGUI.popup_animated(None)             
            window['Spec_Table'].update(values=[
                                                [index.Place,
                                                index.Dates + "-" + index.Times,
                                                index.User,
                                                index.Latitude,
                                                index.Longitude,
                                                index.Altitude] for index in Spec_DATA],
                                        visible=True)
            window['Spec_Table_Label'].update(visible=True)                                        
        elif event == 'User_select':
            User_select_value = values['User_select']
        elif event == 'Place_select':
            Place_select_value = values['Place_select']
        elif event == 'or':
            Map_spec_method_or_and = 'or'
            window['or'].update(button_color=("black","green"))
            window['and'].update(button_color=("black","white"))
        elif event == 'and':
            Map_spec_method_or_and = 'and'
            window['and'].update(button_color=("black","green"))
            window['or'].update(button_color=("black","white"))
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
main.geometry('380x400')  # Width*Height
#main.config(bg='white')


# Label frames
LabelFrame_Canvas = LabelFrame(main)
LabelFrame_Canvas.pack()
LabelFrame_Login = LabelFrame(main, text='Login')
LabelFrame_Login.pack(fill="both", expand="yes")  
LabelFrame_ID_Find = LabelFrame(main, text='ID Find')
LabelFrame_ID_Find.pack(fill="both", expand="yes")  
LabelFrame_Species_Find = LabelFrame(main, text='Species Find')
LabelFrame_Species_Find.pack(fill="both", expand="yes")
LabelFrame_CopyRight = LabelFrame(main)




# 設定圖片
# directory from where script was ran
canvas = Canvas(LabelFrame_Canvas, height=100, width=200)
image_path = current_path + "\dragonfly_picture.gif"
image_file = PhotoImage(file = image_path)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
main.iconphoto(False, image_file)
#main.iconbitmap(current_path+"\dragonfly_ico.ico")

# label
account_label = Label(LabelFrame_Login, text = "Account:")
password_label = Label(LabelFrame_Login, text = "Password:")
id_label = Label(LabelFrame_ID_Find, text = "ID:")
latitude_label = Label(LabelFrame_ID_Find, text = "The Latitude is:")
longitude_label = Label(LabelFrame_ID_Find, text="The Longitude is:")
Species_label = Label(LabelFrame_Species_Find, text="Select the Family and Species")


# Entry
VarName = StringVar(LabelFrame_Login, value='')
VarPwd = StringVar(LabelFrame_Login, value='')
account = Entry(LabelFrame_Login, textvariable = VarName)
password = Entry(LabelFrame_Login, textvariable = VarPwd)
ID = Entry(LabelFrame_ID_Find)
blank_LNG = Entry(LabelFrame_ID_Find)
blank_LAT = Entry(LabelFrame_ID_Find)


#\ drop down menu
# family
var_family = StringVar(LabelFrame_Species_Find)
var_family.set(Species_Family_Name[0])
Family_drop_down_menu = ttk.Combobox(LabelFrame_Species_Find, width=10, textvariable=var_family, values=Species_Family_Name)
Family_drop_down_menu.bind("<<ComboboxSelected>>", Family_drop_down_menu_callback)


# species
var_species = StringVar(LabelFrame_Species_Find)
var_species.set(Calopterygidae_Species[0])
Species_drop_down_menu = ttk.Combobox(LabelFrame_Species_Find, width=10, textvariable=var_species, values=Species_Name_Group[current_dropdown_index])
#Species_drop_down_menu.bind("<<ComboboxSelected>>", Species_drop_down_menu_callback)   # As soon as the dropdown list been selected, the table will automatically pop up  


# try to auto fill the account and password
[n, p] = Auto_Fill()
VarName.set(n)
VarPwd.set(p)   

# Check password and account and the ID
LoginlnputList = [account.get(), password.get()]

# button
login_button = Button(LabelFrame_Login,
                text='Login',
                justify='center',
                bg='red',
                command=LoginButton)

# Button(main, text='Quit', command=main.destroy).grid(row=5, column=0, sticky=W, pady=4)
id_enter_button = Button(LabelFrame_ID_Find,
                text='ID Enter\b',
                command=IDEnterButton,
                justify = 'center',
                bg='gray80')
                # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png

#
# id_plot_map_button = Button( main,
#                 text='ID plot on map',
#                 command=IdPlotMapButton,
#                 justify = 'center')
#
species_find_button = Button(LabelFrame_Species_Find,
                            text='Find Species',
                            command=SpeciesFindButton,
                            justify='center')



# grid
canvas.grid(row = 0, column = 0, columnspan = 2)

account_label.grid(row=1)
password_label.grid(row=2)
id_label.grid(row=3)
latitude_label.grid(row=4)
longitude_label.grid(row=5)
Species_label.grid(row=6, columnspan=2)

account.grid(row=1, column=1)
password.grid(row=2, column=1)
ID.grid(row=3, column=1)
blank_LAT.grid(row=4, column=1)
blank_LNG.grid(row=5, column=1)

Family_drop_down_menu.grid(row=7, column=0)
Species_drop_down_menu.grid(row=7, column=1)

login_button.grid(row=2, column=2, pady=2)
id_enter_button.grid(row=3, column=2, columnspan=1, pady=2)
species_find_button.grid(row=7, column=2, columnspan=1)
# id_plot_map_button.grid(row=4,column=2)

mainloop()




