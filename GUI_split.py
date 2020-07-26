# use the split Windows

import tkinter as tk 
from tkinter import ttk
from tkinter import *
import PySimpleGUI as sg
from Dragonfly import *
from tkinter import messagebox
from tkinter.messagebox import *
import os
import os.path
import PySimpleGUI as PYGUI
import gmplot
import webbrowser
from Index import *

  
LARGEFONT =("Verdana", 35) 
   
Username = ''

##################################################################
#\ arguement
InputArgumentsLabel = ["Account", "Password"]

# auto save account and password file
Login_path = os.getenv('temp')
Login_Filename = os.path.join(Login_path, 'Password_Account_info.txt')

current_dropdown_index = 0 
Login_Response = 0
Login_state = False

LoginlnputList = []

# state the wanted spec for plotting on the map
Place_select_value = ''
User_select_value = ''
Map_spec_method_or_and = ''


# global the Stringvar to replace the XXX,get() mehtod in the previos version
var_LAT = None
var_LNG = None
var_family = None
var_species = None
var_APIKEY = None




##################################################################
# Check if the user have entered the info (account and password) or not
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
# def Auto_Fill():
#     try:
#         with open(Login_Filename) as fp:
#             n, p = fp.read().strip().split(',')
#             return [n, p]
#     except:
#         return['', '']


##################################################################+
def IDEnterButton(ID):
    global LoginlnputList, Login_state

    # Check if the user enter the info properly
    LoginInput_Empty_Or_Not = Check(LoginlnputList)
    
    #login and ID Check
    if (Login_state == False):
        messagebox.showwarning('Warning!!!','Please Login first')
        return
    elif (ID == ''):
        messagebox.showwarning('Warning!!!','ID should not be empty')
        return

    # Check if this data do not contain the Longitude and Latitude infomation
    map_key = True
    if (LoginInput_Empty_Or_Not == 0):
        [_ID_find_result, _overflow, _Max_ID_Num] = DataCrawler(Login_Response, ID)
        if (_overflow):
            messagebox.showwarning('Warning!!!', "ID" + " number is out of range!!!! \nShoud be in the range of 0 ~ " + _Max_ID_Num)  #ID number overflow
            return
        else :
            if (_ID_find_result.Longitude == '' or _ID_find_result.Latitude == ''):
                _ID_find_result.Longitude = 'No Data'
                _ID_find_result.Latitude = 'No Data'
                map_key = False

        var_LNG.set(_ID_find_result.Longitude)
        var_LAT.set(_ID_find_result.Latitude)
        if (map_key):
            msg = messagebox.askyesno("info", "Do you want to plot it on map?")
            if (msg):
                Show_on_map([_ID_find_result])



###################################################################################
#\ Login action
def LoginButton(controller, Account, Password):
    global Login_Response, Login_state, Username 
    [session, Login_Response, Login_state] = Login_Web(Account, Password)
    if (Login_state == False):    
        main.title("蜻蜓資料庫經緯度查詢 --請登入--")
        messagebox.showwarning('Warning!!!', InputArgumentsLabel[0] + " or " + InputArgumentsLabel[1] + " might be incorrect!!!!")  #incorrect account or password
    else:   
        Username = Account
        controller.show_frame(MainPage)
        # and write the account and password to the Login_Filename
        with open(Login_Filename, 'w') as fp:
            fp.write(','.join((Account, Password)))



#################################################################################
# \ Species find to plot info inthe table and plot on the map
def SpeciesFindButton(var_family, var_species):
    global Login_Response
     #login and ID Check
    if (Login_state == False):
        messagebox.showwarning('Warning!!!','Please Login first')
        return
    map_result_list = SpeiciesCrawler(Login_Response, var_family, var_species)
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


def Show_on_map(input_map_list):
    global mapfilename, map_plot_max_data_num, Map_spec_method_or_and
    map_list = []
    map_file_path = os.path.realpath(mapfilename)
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
        
    gmp = gmplot.GoogleMapPlotter(float(map_list[0].Latitude), float(map_list[0].Longitude), 13, apikey=var_APIKEY.get(),
                                    title= map_list[0].Species.encode('unicode_escape').decode("utf-8"))
    info_box_template = """
    <dl>
    <dt><b>[User]</b></dt><dt>{User}</dt>
    <dt><b>[Dates]</b></dt><dt>{Dates}</dt>
    <dt><b>[Times]</b></dt><dt>{Times}</dt>
    <dt><b>[Place]</b></dt><dt>{Place}</dt>
    <dt><b>[Altitude]</b></dt><dt>{Altitude}</dt>
    <dt><b>[Latitude]</b></dt><dt>{Latitude}</dt>
    <dt><b>[Longitude]</b></dt><dt>{Longitude}</dt>
    </dl>
    """
    for index in map_list:
        #context = index.User + " / " + index.Dates + " / " + index.Times + " / " + index.Place + " / "  + index.Altitude + "m / " + index.Latitude + ", "  + index.Longitude
        tmp_dict = {"User": index.User, "Dates": index.Dates, "Times": index.Times, "Place": index.Place,
                    "Altitude": index.Altitude, "Latitude": index.Latitude, "Longitude": index.Longitude}
        context =  info_box_template.format(**tmp_dict) 
        gmp.marker(float(index.Latitude), float(index.Longitude),
                    color="red",
                    label= index.Place.encode('unicode_escape').decode("utf-8"),
                    info_window=context.encode('unicode_escape').decode("utf-8"))
        gmp.draw(map_file_path)
    webbrowser.open(map_file_path)
    return map_list



############################################################
#\ Table
# bad since the flexibility of the option are limited
# this coded in PySimpleGUI library
def New_table(map_result_list):
    global Table_scroll_num, User_select_value, Place_select_value, Map_spec_method_or_and, var_species, var_family
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
        PYGUI.Button(button_text="or",size=(5,2)), # widthxheight
        PYGUI.Button(button_text="and",size=(5,2)),
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

    # Event Loop
    while True:             
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Show on map':
            PYGUI.popup_animated(Image_path + "\Loading.gif")
            Spec_DATA = Show_on_map(map_result_list)
            PYGUI.popup_animated(None)             
            window['Spec_Table'].update(values=[[index.Place,
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



################################################################
# change page 
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
        for F in (LoginPage, MainPage): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # LoginPage, MainPage respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(LoginPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont):
        global Username 
        frame = self.frames[cont]
        print(frame._name)
        tk.Tk.wm_title(self, "蜻蜓經緯度查詢-- {} 已登入".format(Username))
        tk.Tk.wm_geometry(self, "380x450")
        tk.Tk.iconbitmap(self, default=ico_image_path)
        frame.tkraise()


    
# first window frame LoginPage 
   
class LoginPage(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent, bg="white")
        
        # label of frame Layout 2 
        Loginlabel = tk.Label(self, text="Login", font=LARGEFONT, bg="white")
        AccountLabel = tk.Label(self, text="Account", bg="white")
        PasswordLabel = tk.Label(self, text="Password", bg="white")
        StatementLabel = tk.Label(self, text=copyright_text,
                                    bg="white", fg = "gray", font = ("Arial", 8))
          
        # putting the grid in its place by using 
        VarName = StringVar(self, value='')
        VarPwd = StringVar(self, value='')
        accountFrame =Frame(self, bg="black", borderwidth = 1, relief = "sunken")
        accountEntry = Entry(accountFrame, textvariable=VarName, relief=FLAT)
        passwordFrame =Frame(self, bg="black", borderwidth = 1, relief = "sunken")
        passwordEntry = Entry(passwordFrame, textvariable=VarPwd, relief=FLAT)
        
        # button
        Loginbutton = Button(self, text="Login", font=("Arial", 9, "bold"), bg="lime green", fg='white',
                            activebackground = "green2", activeforeground = "white",
                            relief='groove', pady = 0.5, padx =54,
                            command = lambda : LoginButton(controller, VarName.get(), VarPwd.get())) 
      
        # putting the button in its place by 
        Loginlabel.pack(pady=20)
        AccountLabel.pack()
        accountFrame.pack()
        accountEntry.pack()
        PasswordLabel.pack()
        passwordFrame.pack() 
        passwordEntry.pack() 
        Loginbutton.pack(pady=20)
        StatementLabel.pack(pady=20)
        

        # Check password and account and the ID
        LoginlnputList = [VarName.get(), VarPwd.get()]
        
        # try to auto fill the account and password
        [n, p] = self.Auto_Fill()
        VarName.set(n)
        VarPwd.set(p)

    # @@ 注意空格，不小心放在init method裡面    
    # 嘗試自動填寫使用者名稱和密碼
    def Auto_Fill(self):
        try:
            with open(Login_Filename) as fp:
                n, p = fp.read().strip().split(',')
                return [n, p]
        except:
            return['', ''] 



   


   
# second window frame MainPage  
class MainPage(tk.Frame): 
      
    def __init__(self, parent, controller):   
        tk.Frame.__init__(self, parent, bg="white")

        # label frame
        labelframe_font_size = 11
        LabelFrame_font = ("Ink Free", labelframe_font_size, "bold")
        LabelFrame_Canvas = LabelFrame(self)
        LabelFrame_Canvas.pack()

        ID_LabelFrame_bg = "white"
        LabelFrame_ID_Find = LabelFrame(self, text='ID Find', font=LabelFrame_font, bg=ID_LabelFrame_bg)
        LabelFrame_ID_Find.pack(fill="both", expand="yes")
        Species_Find_LabelFrame_bg = "white"
        LabelFrame_Species_Find = LabelFrame(self, text='Species Find', font=LabelFrame_font, bg=Species_Find_LabelFrame_bg)
        LabelFrame_Species_Find.pack(fill="both", expand="yes")
        

        # 設定圖片
        # directory from where script was ran
        canvas = Canvas(LabelFrame_Canvas,height=180, width=380)
        image_path = Image_path + "\dragonfly_picture.gif"
        canvas.background = PhotoImage(file = "image\dragonfly_picture.gif")
        image = canvas.create_image(0, 0, anchor='nw', image=canvas.background)
        

        # label
        label_font_size = 10
        label_font_style = ("Arial", label_font_size)
        APIKEY_label = Label(LabelFrame_ID_Find, text = "API-Key:", font=label_font_style, bg=ID_LabelFrame_bg)
        id_label = Label(LabelFrame_ID_Find, text = "ID:", font=label_font_style, bg=ID_LabelFrame_bg)
        latitude_label = Label(LabelFrame_ID_Find, text = "Latitude:", font=label_font_style, bg=ID_LabelFrame_bg)
        longitude_label = Label(LabelFrame_ID_Find, text="Longitude:", font=label_font_style, bg=ID_LabelFrame_bg)
        Species_label = Label(LabelFrame_Species_Find, text="Select the Family and Species", font=label_font_style , bg=Species_Find_LabelFrame_bg)


        # Entry
        global var_LAT, var_LNG, var_APIKEY
        var_LAT = StringVar(LabelFrame_ID_Find)
        var_LNG = StringVar(LabelFrame_ID_Find)
        var_APIKEY = StringVar(LabelFrame_ID_Find)
        APIKEY_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
        APIKEY = Entry(APIKEY_border, textvariable=var_APIKEY)
        ID_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
        ID = Entry(ID_border)
        LNG_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")
        blank_LNG = Entry(LNG_border, textvariable=var_LNG)
        LAT_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")
        blank_LAT = Entry(LAT_border, textvariable=var_LAT)

        #\ drop down menu
        # species
        global var_species
        var_species = StringVar(LabelFrame_Species_Find)
        var_species.set(Calopterygidae_Species[0])
        self.Species_drop_down_menu = ttk.Combobox(LabelFrame_Species_Find, width=10, textvariable=var_species, values=Species_Name_Group[current_dropdown_index])

        # family
        global var_family
        var_family = StringVar(LabelFrame_Species_Find)
        var_family.set(Species_Family_Name[0])
        self.Family_drop_down_menu = ttk.Combobox(LabelFrame_Species_Find, width=10, textvariable=var_family, values=Species_Family_Name)
        # bind to the <<ComboboxSelected>> event which will fire whenever the value of the combobox changes.
        self.Family_drop_down_menu.bind("<<ComboboxSelected>>", self.changeCombobox)


        # Button(self, text='Quit', command=self.destroy).grid(row=5, column=0, sticky=W, pady=4)
        id_enter_button = Button(LabelFrame_ID_Find,
                        text='ID Enter\b',
                        justify = 'center',
                        bg='gray80',
                        command=lambda: IDEnterButton(ID.get()))
                        # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png


        species_find_button = Button(LabelFrame_Species_Find,
                                    text='Find Species',
                                    justify='center',
                                    command=lambda:SpeciesFindButton(var_family.get(), var_species.get()))

        # grid
        canvas.grid(row = 0, column = 0, columnspan = 2)


        APIKEY_label.grid(row=3)
        id_label.grid(row=4)
        latitude_label.grid(row=5)
        longitude_label.grid(row=6)
        Species_label.grid(row=7, columnspan=2)

        APIKEY.grid(row=3, column=1)
        APIKEY_border.grid(row=3, column=1)            
        ID.grid(row=4, column=1)
        ID_border.grid(row=4, column=1)
        blank_LAT.grid(row=5, column=1)
        LAT_border.grid(row=5, column=1)
        blank_LNG.grid(row=6, column=1)
        LNG_border.grid(row=6, column=1)


        self.Family_drop_down_menu.grid(row=8, column=0, padx=5)
        self.Species_drop_down_menu.grid(row=8, column=1, padx=5)

        id_enter_button.grid(row=4, column=2, columnspan=1, padx = 5)
        species_find_button.grid(row=8, column=2, columnspan=1, padx = 5)

    # dont forget to add the 'event' as input args
    def changeCombobox(self, event):
        global current_dropdown_index, var_species, var_family
        tmp = Species_Name_Group[self.Family_drop_down_menu.current()]
        self.Species_drop_down_menu['value'] = tmp
        var_species.set(tmp[0]) #init the dropdown list in the first element
        print(var_family.get())
        print(self.Family_drop_down_menu.current())
    







# Driver Code
app = tkinterApp()
app.geometry(Login_geometry)
app.title(" Please Login")
app.mainloop() 