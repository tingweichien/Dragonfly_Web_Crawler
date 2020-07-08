## GUI
# Reference:
# https://www.geeksforgeeks.org/python-os-path-exists-method/
# https://www.tutorialspoint.com/python/tk_message.htm
# https://www.itread01.com/content/1548486187.html
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/anchors.html
# https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
# https://www.youtube.com/watch?v=UZX5kH72Yx4
# https://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-attribute-name

from Dragonfly import *
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk 
from tkinter.messagebox import *
import os
import os.path

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
def show_result_button():
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
        messagebox.showwarning('Warning!!!', InputArgumentsLabel[0] + " or " + InputArgumentsLabel[1] + " might be incorrect!!!!")    #incorrect account or password

        
#############################################################
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

   

################################################################### main
################################################################### start
# 建立一個視窗物件
main = Tk()

# 視窗基本設定
main.title("蜻蜓資料庫經緯度查詢")
main.geometry('380x480') # Width*Height

# 設定圖片
current_path = os.getcwd()  # directory from where script was ran
canvas = Canvas(main, height=300, width=380)
image_path = current_path + "\dragonfly_picture.gif"
image_file = PhotoImage(file = image_path)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.grid(row = 0, column = 0, columnspan = 2)

# label
Label(main, text = "Account:").grid(row=1)
Label(main, text = "Password:").grid(row=2)
Label(main, text = "ID:").grid(row=3)
Label(main, text = "The Latutude is:").grid(row=5)
Label(main, text = "The Longitude is:").grid(row=6)

# Entry
VarName = StringVar(main, value='')
VarPwd = StringVar(main, value='')
account = Entry(main, textvariable = VarName)
password = Entry(main, textvariable = VarPwd)
ID = Entry(main)
blank_LNG = Entry(main)
blank_LAT = Entry(main)


account.grid(row=1, column=1)
password.grid(row=2, column=1)
ID.grid(row=3, column=1)
blank_LAT.grid(row=5, column=1)
blank_LNG.grid(row=6, column=1)


# drop down menu
# family
var_family = StringVar(main)
var_family.set(Species_Family_Name[0])
Family_drop_down_menu = ttk.Combobox(main, width=10, textvariable=var_family, values=Species_Family_Name)
Family_drop_down_menu.bind("<<ComboboxSelected>>", Family_drop_down_menu_callback)
Family_drop_down_menu.grid(row=2, column=3)


# species
var_species = StringVar(main)
var_species.set(Calopterygidae_Species[0])
Species_drop_down_menu = ttk.Combobox(main, width=10, textvariable=var_species, values=Species_Name_Group[current_dropdown_index])
Species_drop_down_menu.bind("<<ComboboxSelected>>", Species_drop_down_menu_callback)
Species_drop_down_menu.grid(row=2, column=4)
tmp = Entry(main, textvariable=var_family).grid(row=3, column=3)


# try to auto fill the account and password
[n, p] = auto_fill()
VarName.set(n)
VarPwd.set(p)   


Button(main,
        text='Login',
        command=LoginButton).grid(row=4, column=2, sticky=W, pady=4)

# Button(main, text='Quit', command=main.destroy).grid(row=5, column=0, sticky=W, pady=4)
Button( main,
        text='Enter\b',
        command=show_result_button,
        height=2,
        width=53,
        bg="gray80").grid(row=4, column=0, columnspan=2, sticky=W, pady=4)
        # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png

mainloop()




