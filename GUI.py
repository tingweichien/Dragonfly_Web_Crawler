## GUI
# Reference:
# https://www.geeksforgeeks.org/python-os-path-exists-method/
# https://www.tutorialspoint.com/python/tk_message.htm
# https://www.itread01.com/content/1548486187.html
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/anchors.html
# https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
#https://www.youtube.com/watch?v=UZX5kH72Yx4

from Dragonfly import DataCrawler
from ColorClass import color 
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.messagebox import *
import os
import os.path

##################################################################
#\ arguement
InputArgumentsLabel = ["Account", "Password", "ID"]

# auto save account and password file
path = os.getenv('temp')
filename = os.path.join(path, 'info.txt')
    
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
def show_result():
    InputList = [account.get(), password.get(), ID.get()]

    # check if the user enter the info properly
    empty_or_not = check(InputList)

    # this datd do not contain the Longitude and Latitude infomation
    if (empty_or_not == 0):
        [Output_LNG, Output_LAT] = DataCrawler(InputList[0], InputList[1], InputList[2])
        if (Output_LNG == '' or Output_LAT == ''):
            Output_LNG = 'No Data'
            Output_LAT = 'No Data'
        elif (Output_LNG == -1):    
            messagebox.showwarning('Warning!!!', InputArgumentsLabel[0] + " or " + InputArgumentsLabel[1] + " might be incorrect!!!!")    #incorrect account or password
        elif (Output_LNG == -2):
            messagebox.showwarning('Warning!!!', InputArgumentsLabel[2] + " number is out of range!!!!")    #ID number overflow

        blank_LNG.delete(0, END)
        blank_LAT.delete(0, END)    
        blank_LNG.insert(0, Output_LNG)
        blank_LAT.insert(0, Output_LAT)

    # and write the account and password to the filename
    with open(filename, 'w') as fp:
        fp.write(','.join((InputList[0],InputList[1])))
    

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
Label(main, text = "The Longitude is:").grid(row=5)
Label(main, text = "The Lateral is:").grid(row=6)

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
blank_LNG.grid(row=5, column=1)
blank_LAT.grid(row=6, column=1)


# try to auto fill the account and password
[n, p] = auto_fill()
VarName.set(n)
VarPwd.set(p)   


# Button(main, text='Quit', command=main.destroy).grid(row=5, column=0, sticky=W, pady=4)
Button( main,
        text='Enter\b',
        command=show_result,
        height=2,
        width=53,
        bg="gray80").grid(row=4, column=0, columnspan=2, sticky=W, pady=4)
        # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png

mainloop()




