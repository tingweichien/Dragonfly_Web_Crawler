# use the split Windows

import tkinter as tk 
from tkinter import ttk
from tkinter import *
from Dragonfly import *
from tkinter import messagebox
from tkinter.messagebox import *
import os
import os.path
import PySimpleGUI as PYGUI
from gmplot import *
import webbrowser
from Index import *
from Save2File import *
import time
import threading
  
LARGEFONT =("Verdana", 35) 
   
Username = ''

##################################################################
#\ arguement
current_dropdown_index = 0 
Login_Response = 0
Login_state = False


# global the Stringvar to replace the XXX,get() mehtod in the previos version
var_family = None
var_species = None
      



################################################################
# change page 
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):
        if __name__ == '__main__':
            
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
        tk.Tk.wm_geometry(self, MainPageGeometry)
        tk.Tk.iconbitmap(self, default=ico_image_path)
        frame.tkraise()


    
# first window frame LoginPage 
   
class LoginPage(tk.Frame): 
    def __init__(self, parent, controller):  
        if __name__ == '__main__':
            tk.Frame.__init__(self, parent, bg="white")
            
            # label of frame Layout 2 
            self.Loginlabel = tk.Label(self, text="Login", font=LARGEFONT, bg="white")
            self.AccountLabel = tk.Label(self, text="Account", bg="white")
            self.StatementLabel = tk.Label(self, text=copyright_text,
                                        bg="white", fg = "gray", font = ("Arial", 8))
            
            # putting the grid in its place by using 
            VarName = StringVar(self, value='')
            VarPwd = StringVar(self, value='')
            self.accountFrame =Frame(self, bg="black", borderwidth = 1, relief = "sunken")
            self.accountEntry = Entry(self.accountFrame, textvariable=VarName, relief=FLAT)
            self.password_eyeFrame = Frame(self, bg='white')
            self.passwordFrame =Frame(self.password_eyeFrame, bg="black", borderwidth = 1, relief = "sunken")
            self.passwordEntry = Entry(self.passwordFrame, textvariable=VarPwd, relief=FLAT, show="*")
            self.PasswordPadLabel = tk.Label(self.password_eyeFrame, bg="white")
            self.PasswordLabel = tk.Label(self.password_eyeFrame, text="Password", bg="white")
            

            # button
            self.Loginbutton = Button(self, text="Login", font=("Arial", 9, "bold"), bg="lime green", fg='white',
                                activebackground = "green2", activeforeground = "white",
                                relief='groove', pady = 0.5, padx =54,
                                command=lambda: self.LoginButton(controller, VarName.get(), VarPwd.get()))
            self.ViewPWbuttonIMG = PhotoImage(file=Image_path + "\\view.png")
            self.NotViewPWbuttonIMG = PhotoImage(file=Image_path + "\\viewhidden.png")

            #photoimage = ViewPWbuttonIMG.subsample(3, 3)
            self.viewcheck = BooleanVar(self.password_eyeFrame, True)
            self.ViewPWbutton = Button(self.password_eyeFrame, text="view", command=self.ViewPWButtonfunc, bg='white', relief=FLAT, image=self.ViewPWbuttonIMG)
        
            # putting the button in its place by 
            self.Loginlabel.pack(pady=20)
            self.AccountLabel.pack()
            self.accountFrame.pack()
            self.accountEntry.pack()


            self.password_eyeFrame.pack()
            self.PasswordLabel.pack(side=TOP)
            self.PasswordPadLabel.pack(side=LEFT, padx=14)
            self.ViewPWbutton.pack(side=RIGHT)
            self.passwordFrame.pack(side=RIGHT)
            self.passwordEntry.pack() 
            
            self.Loginbutton.pack(pady=20)
            self.StatementLabel.pack(pady=20)

            

            # Check password and account and the ID
            self.LoginlnputList = [VarName.get(), VarPwd.get()]
            
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
            return ['', '']
            

    # Check if the user have entered the info (account and password) or not
    def Check(self):
        InputArgumentsLabel = ["Account", "Password"]
        index = 0
        string = ""
        for Input in self.LoginlnputList:
            if (Input == ''):
                string += "[" + InputArgumentsLabel[index] + "] "
            index += 1
        if (len(string) > 0):
            messagebox.showwarning('Warning!!!', string + "should not be empty!!!!")
        return len(string)

    
    #\ Login action
    def LoginButton(self, controller, Account, Password):
        global Login_Response, Login_state, Username 
        [session, Login_Response, Login_state] = Login_Web(Account, Password)
        if (Login_state == False):    
            main.title("蜻蜓資料庫經緯度查詢 --請登入--")
            messagebox.showwarning('Warning!!!', 'Account' + " or " + 'Password' + " might be incorrect!!!!")  #incorrect account or password
        else:   
            Username = Account
            controller.show_frame(MainPage)
            # and write the account and password to the Login_Filename
            with open(Login_Filename, 'w') as fp:
                fp.write(','.join((Account, Password)))

    def ViewPWButtonfunc(self):
        if self.viewcheck.get() == True:
            self.passwordEntry.config(show="")
            self.ViewPWbutton.config(image=self.NotViewPWbuttonIMG)
            self.viewcheck.set(False)
        else:
            self.passwordEntry.config(show="*")
            self.ViewPWbutton.config(image=self.ViewPWbuttonIMG)
            self.viewcheck.set(True)

   


   
# second window frame MainPage  
class MainPage(tk.Frame):   
    def __init__(self, parent, controller):   
        if __name__ == '__main__':
            tk.Frame.__init__(self, parent, bg="white")

            # label frame
            labelframe_font_size = 10
            LabelFrame_font = ("Arial", labelframe_font_size, "bold")
            LabelFrame_Canvas = LabelFrame(self)
            LabelFrame_Canvas.pack()

            ID_LabelFrame_bg = "white"
            LabelFrame_ID_Find = LabelFrame(self, text='ID Find', font=LabelFrame_font, bg=ID_LabelFrame_bg)
            LabelFrame_ID_Find.pack(fill="both", expand="yes")
            Species_Find_LabelFrame_bg = "white"
            LabelFrame_Species_Find = LabelFrame(self, text='Species Find', font=LabelFrame_font, bg=Species_Find_LabelFrame_bg)
            LabelFrame_Species_Find.pack(fill="both", expand="yes")
            Save2file_LabelFrame_bg = "white"
            LabelFrame_Save2file = LabelFrame(self, text='Crawling data', font=LabelFrame_font, bg=Save2file_LabelFrame_bg)
            LabelFrame_Save2file.pack(fill="both", expand="yes")        
            

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
            Save2file_label = Label(LabelFrame_Save2file, text="Update the database", font=label_font_style , bg=Save2file_LabelFrame_bg, anchor='w')


            # Entry
            self.var_LAT = StringVar(LabelFrame_ID_Find)
            self.var_LNG = StringVar(LabelFrame_ID_Find)
            self.var_APIKEY = StringVar(LabelFrame_ID_Find)
            APIKEY_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
            APIKEY = Entry(APIKEY_border, textvariable=self.var_APIKEY)
            ID_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
            ID = Entry(ID_border)
            LNG_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")
            blank_LNG = Entry(LNG_border, textvariable=self.var_LNG)
            LAT_border = Frame(LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")
            blank_LAT = Entry(LAT_border, textvariable=self.var_LAT)


            #\ drop down menu
            # species
            global var_species
            var_species = StringVar(LabelFrame_Species_Find)
            var_species.set(Calopterygidae_Species[0])
            self.Species_drop_down_menu = ttk.Combobox(LabelFrame_Species_Find, width=12, textvariable=var_species, values=Species_Name_Group[current_dropdown_index])

            # family
            global var_family
            var_family = StringVar(LabelFrame_Species_Find)
            var_family.set(Species_Family_Name[0])
            self.Family_drop_down_menu = ttk.Combobox(LabelFrame_Species_Find, width=10, textvariable=var_family, values=Species_Family_Name)
            self.Family_drop_down_menu.bind("<<ComboboxSelected>>", self.changeCombobox)

            #\ check box
            self.VarDatacheckbox = BooleanVar(LabelFrame_Species_Find)
            self.Datacheckbox = Checkbutton(LabelFrame_Species_Find, text="SQL", variable = self.VarDatacheckbox, bg="white")



            # Button(self, text='Quit', command=self.destroy).grid(row=5, column=0, sticky=W, pady=4)
            id_enter_button = Button(LabelFrame_ID_Find,
                            text='ID Enter\b',
                            justify = 'center',
                            bg='gray80',
                            command=lambda: self.IDEnterButton(ID.get()))
                            # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png


            species_find_button = Button(LabelFrame_Species_Find,
                                        text='Find Species',
                                        justify='center',
                                        command=lambda:self.SpeciesFindButton(var_family.get(), var_species.get()))

            Save2file_button = Button(LabelFrame_Save2file,
                                        text='Update',
                                        justify='center',
                                        command=self.Save2FileButton)                                   

            # slider
            self.Save2file_slider = Scale(LabelFrame_Save2file, from_=1, to=maxcpus, label="Crawling speed",
                                        orient=HORIZONTAL, bg=Save2file_LabelFrame_bg, tickinterval=1,
                                        length=250, sliderrelief=GROOVE, troughcolor="black", command=self.Save2FileSliderValue)
            #self.Save2file_slider.set(int(maxcpus / 2))
            self.Save2file_slider.set(maxcpus)


            # grid
            canvas.grid(row=0, column=0, columnspan=2)
            
            APIKEY_label.grid(row=3)
            id_label.grid(row=4)
            latitude_label.grid(row=5)
            longitude_label.grid(row=6)
            Species_label.grid(row=7, columnspan=2)
            Save2file_label.grid(row=9) 

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
            self.Datacheckbox.grid(row=8, column=2, padx=3)

            id_enter_button.grid(row=4, column=2, columnspan=1, padx = 5)
            species_find_button.grid(row=8, column=3, columnspan=1, padx=5)
            Save2file_button.grid(row=10, column=3, columnspan=1, padx = 5)

            self.Save2file_slider.grid(row=10, column=0, columnspan=2, padx=5)


            # some initializing
            self.Place_select_value = ''
            self.User_select_value = ''
            self.Map_spec_method_or_and = ''

    ###################################################################################
    #\ Method
    #\ ID find
    def IDEnterButton(self, ID):
        # CHECK IF THE USER ENTER THE id OR NOT
        if (ID == ''):
            messagebox.showwarning('Warning!!!','ID should not be empty')
            return

        # Check if this data do not contain the Longitude and Latitude infomation
        map_key = True
        [_ID_find_result, _overflow, _Max_ID_Num] = DataCrawler(Login_Response, ID)
        if (_overflow):
            messagebox.showwarning('Warning!!!', "ID" + " number is out of range!!!! \nShoud be in the range of 0 ~ " + _Max_ID_Num)  #ID number overflow
            return
        else :
            if (_ID_find_result.Longitude == '' or _ID_find_result.Latitude == ''):
                _ID_find_result.Longitude = 'No Data'
                _ID_find_result.Latitude = 'No Data'
                map_key = False

        self.var_LNG.set(_ID_find_result.Longitude)
        self.var_LAT.set(_ID_find_result.Latitude)
        if (map_key):
            msg = messagebox.askyesno("info", "Do you want to plot it on map?")
            if (msg):
                self.Show_on_map([_ID_find_result])



    # \ Species find to plot info inthe table and plot on the map
    def SpeciesFindButton(self, var_family, var_species):
        if self.VarDatacheckbox.get() == True:
            map_result_list = ReadFromFile(folder_all_crawl_data + Species_class_key[var_family] + "\\" + Species_class_key[var_family] + Species_key[var_species] + ".csv")
        else:
            map_result_list = SpeiciesCrawler(Login_Response, var_family, var_species)

        if len(map_result_list) == 0:
            messagebox.showinfo("Infomation", "The selected species does not have any record")
            return
        else:
            self.New_table(map_result_list) 



    # dont forget to add the 'event' as input args
    def changeCombobox(self, event):
        global current_dropdown_index, var_species, var_family
        tmp = Species_Name_Group[self.Family_drop_down_menu.current()]
        self.Species_drop_down_menu['value'] = tmp
        var_species.set(tmp[0]) #init the dropdown list in the first element
        print(var_family.get())
        print(self.Family_drop_down_menu.current())


    #
    def Save2FileSliderValue(self, event):
        cpus = self.Save2file_slider.get()
        print("crawling speed : {}".format(cpus))
            
    def pbLabel_text(self):
        self.progressbar_label['text'] = str(self.pbVar.get()) + "%"


    def INameLabel_text(self, speciesfamily, species):
        self.Info_Name_label['text'] = '[Start Crawing] {}  {}'.format(speciesfamily, species)

    def IFileNameLabel_text(self, filename):
        self.Info_FileName_label['text'] = '[File Name]: {}'.format(filename) 

    def IUpdateNumLabel_text(self, updateInfo):
        self.Info_UpdateNum_label['text'] = updateInfo

    def ICurrentNumLabel_text(self, currentNum):
        self.Info_CurrentNum_label['text'] = '[Current total crawl]: {}'.format(currentNum)

    def IStateLabel_text(self, state_text):
        self.Info_State_label['text'] = state_text

    def IFinishStateLabel_text(self, finish_text):
        self.Info_FinishState_label['text'] = finish_text

    def set_all_to_empty(self):
        self.Info_FinishState_label['text'] = ""
        self.Info_State_label['text'] = ""
        self.Info_CurrentNum_label['text'] = ""
        self.Info_UpdateNum_label['text'] = ""
        self.Info_FileName_label['text'] = ""
        self.Info_Name_label['text'] = ""
    
    def UpdateGIF(self, index):
        if self.check == True :
            if index < GIFMAXFRAME-1:
                index += 1
            elif index == GIFMAXFRAME-1:
                index = 0
            frame = self.Load_image[index] 
            self.loading_label.config(image=frame)
            #self.progressbarFrame.after(100, self.UpdateGIF,(index, True))
            self.progressbarFrame.after(100, lambda:self.UpdateGIF(index,))
        else:
            self.loading_label.config(image=self.Load_image[10])
            return


    # very important!!! using thread makes the progressbar move outside the main thread
    def start_button(self):
        def start_multithread():
            self.check = True
            self.Info_Name_label['text'] = "Updating~"
            savefile(self, parse_type)
            self.pbVar.set(100)
            self.progressbar_label['text'] = '100%'
            self.progressbar.stop()
            self.button_popup['text'] = 'Finish'
            self.check = False
            
        self.button_popup['state'] = 'disabled'
        UpdateGIF_thread = threading.Thread(target=self.UpdateGIF, args=(0,)).start()
        threading.Thread(target=start_multithread).start()

    #pop up windows for progress
    def popup(self):
        self.check = True
        self.NewWindow = tk.Toplevel(app)
        self.NewWindow.title("Update data")
        self.NewWindow.geometry(updateWinGeometry)

        self.progressLabelFrame = Frame(self.NewWindow)
        self.progressLabelFrame.pack(side=TOP)
        self.progressbarFrame = Frame(self.NewWindow)
        self.progressbarFrame.pack()
        self.ButtonFrame = Frame(self.NewWindow)
        self.ButtonFrame.pack()

        progressbar_label = Label(self.progressLabelFrame, text="Progress")
        progressbar_label.pack(side=LEFT)
        self.Load_image = [PhotoImage(file="image\LOAD.gif", format="gif -index %i" %(i)) for i in range(GIFMAXFRAME)] # base on how many frame the gif file have
        self.loading_label = Label(self.progressLabelFrame,)
        self.loading_label.pack(side=RIGHT)

        self.pbVar = IntVar(self.NewWindow)
        self.progressbar = ttk.Progressbar(self.progressbarFrame, orient=HORIZONTAL, length=300, mode="determinate", variable=self.pbVar, maximum=100)
        self.progressbar.pack(side=LEFT, pady=10)
        self.progressbar_label = Label(self.progressbarFrame, text="0%")
        self.progressbar_label.pack(side=RIGHT, padx=5)
        
        button_popup_label = Label(self.ButtonFrame, text="Ready to update?")
        button_popup_label.pack()
        self.button_popup = Button(self.ButtonFrame, text="start", command=self.start_button)
        self.button_popup.pack(pady=2)


        TextLabelFrame = LabelFrame(self.NewWindow, text="Info", padx=40)
        TextLabelFrame.pack(pady=10)
        self.Info_Name_label = Label(TextLabelFrame, text="Ready to start Updating......", width=30, anchor='w')
        self.Info_Name_label.pack(pady=3)
        self.Info_FileName_label = Label(TextLabelFrame, anchor='w')
        self.Info_FileName_label.pack(pady=3)
        self.Info_UpdateNum_label = Label(TextLabelFrame, anchor='w')
        self.Info_UpdateNum_label.pack(pady=3)
        self.Info_CurrentNum_label = Label(TextLabelFrame, anchor='w')
        self.Info_CurrentNum_label.pack(pady=3)        
        self.Info_State_label = Label(TextLabelFrame, anchor='w')
        self.Info_State_label.pack(pady=3)
        self.Info_FinishState_label = Label(TextLabelFrame, anchor='w')
        self.Info_FinishState_label.pack(pady=3)        

         
    #\ crawl data 
    # read the flow from here to the top of the method in this class
    def Save2FileButton(self):
        self.popup()




    #\ Table
    # bad since the flexibility of the option are limited
    # this coded in PySimpleGUI library

    def New_table(self, map_result_list):
        global var_species, var_family, map_plot_max_data_num
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
            PYGUI.Text("-- " + str(var_species.get()) + " --", text_color="black",font=("Ststem", 14)),
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
            PYGUI.Text("Select the place", auto_size_text=True, justification="center"),
            PYGUI.Text("\tlimit", auto_size_text=True, justification="center"),
            PYGUI.Input(default_text='100',key='-IN-',size = (5,2),justification='center')
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
            PYGUI.Button(button_text='Show on map',size=(12,3))      
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
        
        self.window = PYGUI.Window("Show Species info", layout=layout)

         # Event Loop
        while True:             
            event, values = self.window.Read()
            if event in (None, 'Exit'):
                PYGUI.popup_animated(None) 
                break
            elif event == PYGUI.WIN_CLOSED or event == 'Quit':
                PYGUI.popup_animated(None) 
                break
            elif event == 'Show on map':
                map_plot_max_data_num = int(values['-IN-'])
                Spec_DATA = self.Show_on_map(map_result_list)         
                self.window['Spec_Table'].update(values=[[index.Place,
                                                    index.Dates + "-" + index.Times,
                                                    index.User,
                                                    index.Latitude,
                                                    index.Longitude,
                                                    index.Altitude] for index in Spec_DATA],
                                            visible=True)
                self.window['Spec_Table_Label'].update(visible=True)                                        
            elif event == 'User_select':
                self.User_select_value = values['User_select']
            elif event == 'Place_select':
                self.Place_select_value = values['Place_select']
            elif event == 'or':
                self.Map_spec_method_or_and = 'or'
                self.window['or'].update(button_color=("black","green"))
                self.window['and'].update(button_color=("black","white"))
            elif event == 'and':
                self.Map_spec_method_or_and = 'and'
                self.window['and'].update(button_color=("black","green"))
                self.window['or'].update(button_color=("black","white"))
        self.window.Close()

    #\ map
    # https://github.com/gmplot/gmplot/blob/master/gmplot/google_map_plotter.py
    # https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python/40905794
    # https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
    # marker title has some problem
    def Show_on_map(self, input_map_list):
        map_list = []
        map_file_path = os.path.realpath(mapfilename)
        # specify by selected item
        for tmp in input_map_list:
            PYGUI.PopupAnimated(PYGUI.DEFAULT_BASE64_LOADING_GIF, background_color="white", time_between_frames=1)

            if (len(self.Place_select_value) > 0):
                if (len(self.User_select_value) > 0):
                    if (self.Map_spec_method_or_and == 'or'):
                        if ((tmp.Place in self.Place_select_value) or (tmp.User in self.User_select_value)):
                            map_list.append(tmp)
                    elif (self.Map_spec_method_or_and == 'and'):
                        if ((tmp.Place in self.Place_select_value) and (tmp.User in self.User_select_value)):
                            map_list.append(tmp)
                    else:
                        PYGUI.popup_animated(None)
                        messagebox.showwarning("warning", "Please select the method (or , and) between two spec")
                        return []
                else:
                    if (tmp.Place in self.Place_select_value):
                        map_list.append(tmp)
            else:
                if (len(self.User_select_value) > 0):
                    if (tmp.User in self.User_select_value):
                        map_list.append(tmp)
                else:
                    map_list = input_map_list
                    break

        # the gmplot have some problem on plotting too many data
        if (len(map_list) > map_plot_max_data_num):
            #del map_list[0: len(map_list) - map_plot_max_data_num]
            limit_map_list = map_list[0: map_plot_max_data_num]
        elif (len(map_list) == 0):  # make sure the map data is not empty
            PYGUI.popup_animated(None)
            messagebox.showinfo("Info", "No data match the spec")
            return []
        else:
            limit_map_list = map_list


        # LOOP until finding the non empty LAT and LNG
        index = 0
        for index in range(len(limit_map_list)):
            if (limit_map_list[index].Latitude == "" and limit_map_list[index].Longitude == ""):
                index += 1
            else:
                break

        gmp = gmplot.GoogleMapPlotter(float(limit_map_list[index].Latitude), float(limit_map_list[index].Longitude), 13, apikey=self.var_APIKEY.get(),
                                        title= limit_map_list[index].Species.encode('utf-8'))
        gmp.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"


        for index in limit_map_list:
            PYGUI.PopupAnimated(PYGUI.DEFAULT_BASE64_LOADING_GIF,background_color="white", time_between_frames=1)
            if not(index.Latitude == "" or index.Longitude == ""):
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
        PYGUI.PopupAnimated(None)
        return limit_map_list



    







# Driver Code
if __name__ == '__main__':
    app = tkinterApp()
    app.geometry(Login_geometry)
    app.title(" Please Login")
    app.mainloop() 