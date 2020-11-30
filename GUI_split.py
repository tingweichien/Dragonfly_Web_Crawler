# this is GUI split program

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
import Index
from Save2File import *
from datetime import datetime
import threading
from multiprocessing import Process, Value, Pool
import gmplot
from update_chromedriver import *
#from tkcalendar import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import Plot_from_database as PFD
from PIL import ImageTk, Image


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
# Plot_var_family = None
# Plot_var_species = None


#\ check and update the chromedriver
check_chromedriver()


################################################################################
#\ main GUI
#\ change page
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
        #print(frame._name)
        tk.Tk.wm_title(self, "蜻蜓經緯度查詢-- {} 已登入".format(Username))
        tk.Tk.wm_geometry(self, Index.MainPageGeometry)
        tk.Tk.iconbitmap(self, default=Index.ico_image_path)
        frame.tkraise()

    #\ define the action when mouse hover on the button
    def B_HoverOn(self, event, color):
        event.widget['background'] = color
    def BHoverOn(self, w:tk.Widget, colorList:list):
        w.bind("<Leave>", lambda event, color=colorList[0]: self.B_HoverOn(event, color))
        w.bind("<Enter>", lambda event, color=colorList[1]: self.B_HoverOn(event, color))


# first window frame LoginPage

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        if __name__ == '__main__':
            tk.Frame.__init__(self, parent, bg="white")

            # label of frame Layout 2
            self.Loginlabel = tk.Label(self, text="Login", font=LARGEFONT, bg="white")
            self.AccountLabel = tk.Label(self, text="Account", bg="white")
            self.StatementLabel = tk.Label(self, text=Index.copyright_text,
                                        bg="white", fg = "gray", font = ("Arial", 8))

            # putting the grid in its place by using
            self.VarName = StringVar(self, value='')
            self.VarPwd = StringVar(self, value='')
            self.accountFrame =Frame(self, bg="black", borderwidth = 1, relief = "sunken")
            self.accountEntry = Entry(self.accountFrame, textvariable=self.VarName, relief=FLAT)
            self.password_eyeFrame = Frame(self, bg='white')
            self.passwordFrame =Frame(self.password_eyeFrame, bg="black", borderwidth = 1, relief = "sunken")
            self.passwordEntry = Entry(self.passwordFrame, textvariable=self.VarPwd, relief=FLAT, show="*")
            self.PasswordPadLabel = tk.Label(self.password_eyeFrame, bg="white")
            self.PasswordLabel = tk.Label(self.password_eyeFrame, text="Password", bg="white")


            #\ --Button--
            #\ log in
            self.Loginbutton = Button(self,
                                    text="Login",
                                    font=("Arial", 9, "bold"),
                                    bg="lime green",
                                    fg='white',
                                    activebackground = "green2",
                                    activeforeground = "white",
                                    relief='groove',
                                    pady = 0.5,
                                    padx =54,
                                    command=lambda: self.LoginButtonFunc(controller))
            #\ bind the button with mouse hover to change the background color
            controller.BHoverOn(self.Loginbutton,["lime green", "green2"])


            #\ view password
            self.ViewPWbuttonIMG = PhotoImage(file=Index.Image_path + "\\view.png")
            self.ViewPWbutton = Button(self.password_eyeFrame,
                                        text="view",
                                        command=self.ViewPWButtonfunc,
                                        bg='white',
                                        activebackground="white",
                                        relief=FLAT,
                                        image=self.ViewPWbuttonIMG)
            controller.BHoverOn(self.ViewPWbutton, ["white", "grey87"])

            #\ --Image--
            self.NotViewPWbuttonIMG = PhotoImage(file=Index.Image_path + "\\viewhidden.png")
            #photoimage = ViewPWbuttonIMG.subsample(3, 3)

            #\ --checkbox--
            self.viewcheck = BooleanVar(self.password_eyeFrame, True)

            #\ --Putting the button in its place by--
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

            # --try to auto fill the account and password--
            [n, p] = self.Auto_Fill()
            self.VarName.set(n)
            self.VarPwd.set(p)


    #\ @@ 注意空格，不小心放在init method裡面
    #\ 嘗試自動填寫使用者名稱和密碼
    def Auto_Fill(self):
        try:
            with open(Index.Login_Filename) as fp:
                n, p = fp.read().strip().split(',')
                return [n, p]
        except:
            return ['', '']


    # Check if the user have entered the info (account and password) or not
    def Check_empty(self):
        InputArgumentsLabel = ["Account", "Password"]
        index = 0
        string = ""
        for Input in [self.VarName.get(), self.VarPwd.get()]:
            if (Input == ''):
                string += "[" + InputArgumentsLabel[index] + "] "
            index += 1
        if (len(string) > 0):
            messagebox.showwarning('Warning!!!', string + "should not be empty!!!!")
        return len(string)

    #\ Login action
    def LoginButtonFunc(self, controller):
        global Login_Response, Login_state, Username
        Index.myaccount = self.VarName.get()
        Index.mypassword = self.VarPwd.get()
        if self.Check_empty() > 0:
            return
        else:
            [session, Login_Response, Login_state] = Login_Web(Index.myaccount, Index.mypassword)
            if (Login_state == False):
                messagebox.showwarning('Warning!!!', 'Account' + " or " + 'Password' + " might be incorrect!!!!")  #incorrect account or password
            elif Login_Response == None and Login_state == None:
                messagebox.showwarning('Warning!!!',"No connection to server, check the internet connection!!!")
            else:
                Username = Index.myaccount
                controller.show_frame(MainPage)
                # and write the account and password to the Login_Filename
                with open(Index.Login_Filename, 'w') as fp:
                    fp.write(','.join((Index.myaccount, Index.mypassword)))


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

            #\ Label frame and label setting
            labelframe_font_size = 10
            LabelFrame_font = ("Arial", labelframe_font_size, "bold")
            label_font_size = 10
            label_font_style = ("Arial", label_font_size)


            #\ ---Image Frame---
            #####################
            #\ 設定圖片
            #\ directory from where script was ran
            self.LabelFrame_Canvas = LabelFrame(self)
            self.canvas = Canvas(self.LabelFrame_Canvas, height=180, width=380)
            self.image_path = Index.Image_path + "\dragonfly_picture.gif"
            self.canvas.background = PhotoImage(file = Index.Image_path + "\dragonfly_picture.gif")
            self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.canvas.background)
            self.LabelFrame_Canvas.pack()


            #\ ---ID Find Frame---
            ######################
            ID_LabelFrame_bg = "white"
            self.LabelFrame_ID_Find = LabelFrame(self, text='ID Find', fg="red", font=LabelFrame_font, bg=ID_LabelFrame_bg)

            #\ Label
            self.APIKEY_label = Label(self.LabelFrame_ID_Find, text = "API-Key:", font=label_font_style, bg=ID_LabelFrame_bg)
            self.id_label = Label(self.LabelFrame_ID_Find, text = "ID:", font=label_font_style, bg=ID_LabelFrame_bg)
            self.latitude_label = Label(self.LabelFrame_ID_Find, text = "Latitude:", font=label_font_style, bg=ID_LabelFrame_bg)
            self.longitude_label = Label(self.LabelFrame_ID_Find, text="Longitude:", font=label_font_style, bg=ID_LabelFrame_bg)

            #\ Entry
            self.var_APIKEY = StringVar(self.LabelFrame_ID_Find)
            self.APIKEY_border = Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
            self.APIKEY = Entry(self.APIKEY_border, textvariable=self.var_APIKEY)
            self.APIKEY_TLTP = CreateToolTip(self.APIKEY, "This is the apikey for google map to remove the watermark of \" for develop purpose only\"")

            self.ID_border = Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
            self.ID = Entry(self.ID_border)

            self.var_LNG = StringVar(self.LabelFrame_ID_Find)
            self.LNG_border = Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")
            self.blank_LNG = Entry(self.LNG_border, textvariable=self.var_LNG)

            self.var_LAT = StringVar(self.LabelFrame_ID_Find)
            self.LAT_border = Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")
            self.blank_LAT = Entry(self.LAT_border, textvariable=self.var_LAT)
            self.LabelFrame_ID_Find.pack(fill="both", expand="yes")

            self.id_enter_button = Button(self.LabelFrame_ID_Find,
                            text='ID Enter\b',
                            justify = 'center',
                            bg='gray80',
                            cursor="hand2",
                            command=lambda: self.IDEnterButton(self.ID.get()))
                            # color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png
            controller.BHoverOn(self.id_enter_button, ['gray80','gray70'])


            #\ ---Species Find Frame---
            ###########################
            Species_Find_LabelFrame_bg = "white"
            self.LabelFrame_Species_Find = LabelFrame(self, text='Species Find', fg="orange", font=LabelFrame_font, bg=Species_Find_LabelFrame_bg)
            self.LabelFrame_Species_Find.pack(fill="both", expand="yes")

            #\ Label
            self.Species_label = Label(self.LabelFrame_Species_Find, text="Select the Family and Species", font=label_font_style , bg=Species_Find_LabelFrame_bg)

            #\ drop down menu
            #\ species
            global var_species
            var_species = StringVar(self.LabelFrame_Species_Find)
            var_species.set(Index.Calopterygidae_Species[0])
            self.Species_drop_down_menu = ttk.Combobox(self.LabelFrame_Species_Find, width=14, textvariable=var_species, values=Index.Species_Name_Group[current_dropdown_index])

            #\ family
            global var_family
            var_family = StringVar(self.LabelFrame_Species_Find)
            var_family.set(Index.Species_Family_Name[0])
            self.Family_drop_down_menu = ttk.Combobox(self.LabelFrame_Species_Find, width=10, textvariable=var_family, values=Index.Species_Family_Name)
            self.Family_drop_down_menu.bind("<<ComboboxSelected>>", self.changeCombobox)

            #\ check box
            self.VarDatacheckbox = BooleanVar(self.LabelFrame_Species_Find)
            self.Datacheckbox = Checkbutton(self.LabelFrame_Species_Find, text="EXCEL-SQL", variable=self.VarDatacheckbox, bg="white")
            self.DatacheckboxTLTP = CreateToolTip(self.Datacheckbox, "This will import data from database")

            #\ Button
            self.species_find_button = Button(self.LabelFrame_Species_Find,
                                        text='Find Species',
                                        justify='center',
                                        bg='gray80',
                                        cursor="hand2",
                                        command=lambda:self.SpeciesFindButton(var_family.get(), var_species.get()))
            controller.BHoverOn(self.species_find_button, ['gray80','gray70'])


            #\ ---Save2file Frame---
            ########################
            Save2file_LabelFrame_bg = "white"
            self.LabelFrame_Save2file = LabelFrame(self, text='Crawling data', fg="green", font=LabelFrame_font, bg=Save2file_LabelFrame_bg)
            self.Save2file_label = Label(self.LabelFrame_Save2file, text="Update the database", font=label_font_style , bg=Save2file_LabelFrame_bg, anchor='w')
            self.MaxCrawling_label = Label(self.LabelFrame_Save2file, text="Max Crawling NM", font=label_font_style , bg=Species_Find_LabelFrame_bg)
            self.LabelFrame_Save2file.pack(fill="both", expand="yes") # fill both horizon and vertically

            #\ Entry
            self.var_MC = StringVar(self.LabelFrame_Save2file)
            self.var_MC.set(str(Index.limit_cnt))
            self.MaxCrawling_width = 10
            self.MaxCrawling_border = Frame(self.LabelFrame_Save2file, bg="black", borderwidth=1, relief="sunken", width=self.MaxCrawling_width)
            self.MaxCrawling = Entry(self.MaxCrawling_border, textvariable=self.var_MC, width=self.MaxCrawling_width, justify="center")

            #\ Button
            self.Save2file_button = Button(self.LabelFrame_Save2file,
                                        text='Update',
                                        justify='center',
                                        bg='gray80',
                                        cursor="hand2",
                                        command=self.Save2FileButton)
            controller.BHoverOn(self.Save2file_button, ['gray80','gray70'])

            #\ Slider
            self.Save2file_slider = Scale(self.LabelFrame_Save2file, from_=1, to=Index.maxcpus, label="Crawling speed",
                                        orient=HORIZONTAL, bg=Save2file_LabelFrame_bg, tickinterval=1,
                                        length=250, sliderrelief=GROOVE, troughcolor="black", command=self.Save2FileSliderValue)
            #self.Save2file_slider.set(int(maxcpus / 2))
            self.Save2file_slider.set(Index.maxcpus)


            #\ ---Plot Chart---
            ###################
            #\ Label Frame
            Plot_LabelFrame_bg = "white"
            self.LabelFrame_Plot = LabelFrame(self, text="Plot Chart", font=LabelFrame_font, bg=Plot_LabelFrame_bg, fg="blue")
            self.LabelFrame_Plot.pack(fill="both", expand="yes") # fill both horizon and vertically
            self.Time_range_from_label = Label(self.LabelFrame_Plot, text="From", bg=Plot_LabelFrame_bg)
            self.Time_range_to_label = Label(self.LabelFrame_Plot, text="to", bg=Plot_LabelFrame_bg)
            self.Time_Duration_Year_label = Label(self.LabelFrame_Plot, text="Year", bg=Plot_LabelFrame_bg)
            self.Time_Duration_Month_label = Label(self.LabelFrame_Plot, text="Month", bg=Plot_LabelFrame_bg)


            #\ Drop down menu
            #\ species
            self.Plot_var_species = StringVar(self.LabelFrame_Plot, value=Index.Calopterygidae_Species[0])
            self.Plot_Species_drop_down_menu = ttk.Combobox(self.LabelFrame_Plot, width=14, textvariable=self.Plot_var_species, values=Index.Species_Name_Group[current_dropdown_index])

            #\ family
            self.Plot_var_family = StringVar(self.LabelFrame_Plot, value=Index.Species_Family_Name[0])
            self.Plot_Family_drop_down_menu = ttk.Combobox(self.LabelFrame_Plot, width=10, textvariable=self.Plot_var_family, values=Index.Species_Family_Name)
            self.Plot_Family_drop_down_menu.bind("<<ComboboxSelected>>", self.changeCombobox)

            #\ Button
            self.MatplotlibPlot_button = Button(self.LabelFrame_Plot,
                                        text='Matplotlib',
                                        justify='center',
                                        bg='gray80',
                                        cursor="hand2",
                                        command=self.MatplotlibPlotButton)
            controller.BHoverOn(self.MatplotlibPlot_button, ['gray80','gray70'])

            self.PyechartsPlot_button = Button(self.LabelFrame_Plot,
                                        text='Pyecharts',
                                        justify='center',
                                        bg='gray80',
                                        cursor="hand2",
                                        command=self.PyechartsPlotButton)
            controller.BHoverOn(self.PyechartsPlot_button, ['gray80','gray70'])

            #\ Entry
            today = datetime.today()
            shift_year_age = today - relativedelta(years = Index.Plot_chart_init_delta_years)  #\ shift the time back to the previous year
            self.var_Time_end = StringVar(self.LabelFrame_Plot, value=today.strftime("%Y-%m-%d"))
            self.var_Time_start = StringVar(self.LabelFrame_Plot, value=shift_year_age.strftime("%Y-%m-%d"))
            self.Time_range_width = 10
            self.Time_range_start_border = Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.Time_range_width)
            self.Time_range_start = Entry(self.Time_range_start_border, width=self.Time_range_width, textvariable=self.var_Time_start, justify="center")
            self.Time_range_end_border = Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.Time_range_width)
            self.Time_range_end = Entry(self.Time_range_end_border, width=self.Time_range_width, textvariable=self.var_Time_end, justify="center")


            #\ time selector
            self.VarTimeDuration_ckeckbox = BooleanVar(self.LabelFrame_Plot, value=False)
            self.TimeDuration_checkbox = Checkbutton(self.LabelFrame_Plot, text="-->", variable=self.VarTimeDuration_ckeckbox, bg="white", cursor= "arrow", command=self.TimeDuration_checkbox_callback)
            self.TimeDuration_checkboxTLTP = CreateToolTip(self.TimeDuration_checkbox, "Use the time duration or not")

            self.var_Duration_month = StringVar(self.LabelFrame_Plot, value=str(0))
            self.var_Duration_month.trace_add("write", self.Time_Duration_month_callback)
            self.var_Duration_year = StringVar(self.LabelFrame_Plot, value=str(0))
            self.var_Duration_year.trace_add("write", self.Time_Duration_year_callback)
            self.TimeDuration_range_width = 5
            self.Time_Duration_year_border = Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.TimeDuration_range_width)
            self.Time_Duration_year = Entry(   self.Time_Duration_year_border,
                                                width=self.TimeDuration_range_width,
                                                textvariable=self.var_Duration_year,
                                                justify="center",
                                                # validate='all',
                                                # validatecommand=self.Time_Duration_year_callback
                                            )
            self.Time_Duration_month_border = Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.TimeDuration_range_width)
            self.Time_Duration_month = Entry( self.Time_Duration_month_border,
                                            width=self.TimeDuration_range_width,
                                            textvariable=self.var_Duration_month,
                                            justify="center",
                                            # validate='all',
                                            # validatecommand=self.Time_Duration_month_callback
                                         )


            #\ The link to my Github and doc
            Hub_LabelFrame_bg = "White"
            self.Hub_Frame = LabelFrame(self, text="", font=LabelFrame_font, bg=Hub_LabelFrame_bg)
            self.Hub_Frame.pack(fill="both", expand="yes")
            self.Hub_parentF = Frame(self.Hub_Frame, bg=Hub_LabelFrame_bg)
            self.githubImg = PhotoImage(file=Index.github_img_path)
            Label_bg_color = "white"
            self.Hub_Label = Label(self.Hub_parentF, text="github", cursor="hand2", image=self.githubImg, bg=Label_bg_color)
            self.Hub_Label.bind("<Button-1>", lambda e: self.Hub_callback("https://github.com/tingweichien/Dragonfly_Web_Crawler"))
            self.Hub_Label_tooltip = CreateToolTip(self.Hub_Label, "Go to Github", window_y=-15)

            self.web_versionImg = PhotoImage(file=Index.web_version_img_path)
            self.Web_version_Label = Label(self.Hub_parentF, text="web version", cursor="hand2", image=self.web_versionImg, bg=Label_bg_color)
            self.Web_version_Label.bind("<Button-1>", lambda e: self.Hub_callback("https://flask-web-training.herokuapp.com/"))
            self.Web_version_tooltip = CreateToolTip(self.Web_version_Label, "Go to Web version of this app", window_y=-15)

            self.ReadthedocsImg = PhotoImage(file=Index.Readthedocs_img_path)
            self.Readthedocs_Label = Label(self.Hub_parentF, text="read the docs", cursor="hand2", image=self.ReadthedocsImg, bg=Label_bg_color)
            self.Readthedocs_Label.bind("<Button-1>", lambda e: self.Hub_callback("https://dragonfly-web-crawler.readthedocs.io/en/latest/"))
            self.Readthedocs_tooltip = CreateToolTip(self.Readthedocs_Label, "Go to read the docs for more detail info", window_y=-10)


            #\ ---grid---
            #############
            self.canvas.grid(row=0, column=0, columnspan=2)

            #\ ID Find
            self.APIKEY_label.grid(row=3)
            self.id_label.grid(row=4)
            self.latitude_label.grid(row=5)
            self.longitude_label.grid(row=6)

            self.id_enter_button.grid(row=4, column=2, columnspan=1, padx = 5)

            self.APIKEY.grid(row=3, column=1)
            self.APIKEY_border.grid(row=3, column=1)
            self.ID.grid(row=4, column=1)
            self.ID_border.grid(row=4, column=1)
            self.blank_LAT.grid(row=5, column=1)
            self.LAT_border.grid(row=5, column=1)
            self.blank_LNG.grid(row=6, column=1)
            self.LNG_border.grid(row=6, column=1)

            #\ Species find
            self.Species_label.grid(row=7, columnspan=2)
            self.Family_drop_down_menu.grid(row=8, column=0, padx=3)
            self.Species_drop_down_menu.grid(row=8, column=1, padx=3)
            self.Datacheckbox.grid(row=7, column=2, padx=3)
            self.species_find_button.grid(row=8, column=2, columnspan=1, padx=5)

            #\ Crawling data
            self.Save2file_button.grid(row=10, column=3)
            self.Save2file_label.grid(row=9)
            self.Save2file_slider.grid(row=10, column=0, columnspan=2, padx=5)
            self.MaxCrawling_label.grid(row=9,column=3)
            self.MaxCrawling.grid(row=10, column=3, sticky=N)
            self.MaxCrawling_border.grid(row=10, column=3, sticky=N)

            #\ Plot Chart
            self.Plot_Family_drop_down_menu.grid(row=11, column=0, columnspan=2, padx=3)
            self.Plot_Species_drop_down_menu.grid(row=11, column=2, columnspan=2, padx=3)
            self.MatplotlibPlot_button.grid(row=11, column=5, columnspan=2, pady=3, padx=20, sticky=E)
            self.PyechartsPlot_button.grid(row=12, column=5, columnspan=2, padx=20, sticky=E)
            self.Time_range_from_label.grid(row=12, column=0)
            self.Time_range_start.grid(row=12, column=1)
            self.Time_range_start_border.grid(row=12, column=1)
            self.Time_range_to_label.grid(row=12, column=2)
            self.Time_range_end.grid(row=12, column=3)
            self.Time_range_end_border.grid(row=12, column=3)

            self.TimeDuration_checkbox.grid(row=13, column=1, )
            self.Time_Duration_year.grid(row=13, column=2, sticky=W)
            self.Time_Duration_year_border.grid(row=13, column=2, sticky=W)
            self.Time_Duration_Year_label.grid(row=13, column=3, sticky=W)
            self.Time_Duration_month.grid(row=13, column=3, sticky=E)
            self.Time_Duration_month_border.grid(row=13, column=3, sticky=E)
            self.Time_Duration_Month_label.grid(row=13, column=5, sticky=W)

            #\ Hub and docs
            self.Hub_Label.pack(side=LEFT, padx=15)
            self.Readthedocs_Label.pack(side=RIGHT, padx=15)
            self.Web_version_Label.pack(side=RIGHT, padx=15)
            self.Hub_parentF.pack(expand=True)



            #\ some initializing
            ####################
            self.Place_select_value = ''
            self.User_select_value = ''
            self.Map_spec_method_or_and = ''



    ###################################################################################
    #\ ---Method---
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
            map_result_list = ReadFromFile(Index.folder_all_crawl_data + Index.Species_class_key[var_family] + "\\" + Index.Species_class_key[var_family] + Index.Species_key[var_species] + ".csv")
        else:
            map_result_list = SpeiciesCrawler(Login_Response, var_family, var_species)

        if len(map_result_list) == 0:
            messagebox.showinfo("Infomation", "The selected species does not have any record")
            return
        else:
            self.New_table(map_result_list)


    #\ dont forget to add the 'event' as input args
    def changeCombobox(self, event):
        global current_dropdown_index, var_species

        tmp = Index.Species_Name_Group[self.Family_drop_down_menu.current()]
        tmp1 = Index.Species_Name_Group[self.Plot_Family_drop_down_menu.current()]
        self.Species_drop_down_menu['value'] = tmp
        self.Plot_Species_drop_down_menu['value'] = tmp1
        #\ init the dropdown list in the first element when the family changed
        var_species.set(tmp[0])
        self.Plot_var_species.set(tmp1[0])

        #print(var_family.get())
        #print(self.Family_drop_down_menu.current())

    #\ specify the crawling speed
    def Save2FileSliderValue(self, event):
        Index.cpus = self.Save2file_slider.get()
        #print("crawling speed : {}".format(Index.cpus))

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
            if index < Index.GIFMAXFRAME-1:
                index += 1
            elif index == Index.GIFMAXFRAME-1:
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
            savefile(self, Index.parse_type)
            self.pbVar.set(100)
            self.progressbar_label['text'] = '100%'
            self.progressbar.stop()
            self.button_popup['text'] = 'Finish'
            self.check = False

        self.button_popup['state'] = 'disabled'
        UpdateGIF_thread = threading.Thread(target=self.UpdateGIF, args=(0,)).start()
        threading.Thread(target=start_multithread).start()

    #\ pop up windows for progress
    def popup(self):
        self.check = True
        self.NewWindow = tk.Toplevel(self.app)
        self.NewWindow.title("Update data")
        self.NewWindow.geometry(Index.updateWinGeometry)

        self.progressLabelFrame = Frame(self.NewWindow)
        self.progressLabelFrame.pack(side=TOP)
        self.progressbarFrame = Frame(self.NewWindow)
        self.progressbarFrame.pack()
        self.ButtonFrame = Frame(self.NewWindow)
        self.ButtonFrame.pack()

        progressbar_label = Label(self.progressLabelFrame, text="Progress")
        progressbar_label.pack(side=LEFT)
        self.Load_image = [PhotoImage(file="image\LOAD.gif", format="gif -index %i" %(i)) for i in range(Index.GIFMAXFRAME)] # base on how many frame the gif file have
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
        Index.limit_cnt = int(self.var_MC.get())
        print(f"limit count is {Index.limit_cnt}")
        self.popup()


    #\ Table
    # bad since the flexibility of the option are limited
    # this coded in PySimpleGUI library
    def New_table(self, map_result_list):
        global var_species, var_family
        Data = [
            [index.Place,
            index.Dates,
            index.Times,
            index.User,
            index.Latitude,
            index.Longitude,
            index.Altitude] for index in map_result_list
        ]

        rowcolor = []
        for i in list(range(1, len(Data), 2)):
            rowcolor.append([i, "gray88"])

        layout = [
            [
            PYGUI.Text("-- " + str(var_species.get()) + " --", text_color="black",font=("Ststem", 14)),
                ],
            [
            PYGUI.Table(Data,
                    headings=["Place", "Date", "Time", "Recorder",
                                    "Latitude", "Longitude", "Altitude"],
                    justification="center",
                    num_rows=Index.Table_scroll_num,
                    background_color="white",
                    text_color="black",
                    row_colors=rowcolor,
                    display_row_numbers=True)
                ],
            [
            PYGUI.Text("Select the user", auto_size_text=True, justification="center"),
            PYGUI.Text("\tSelect the method", auto_size_text = True, justification="center"),
            PYGUI.Text("Select the place", auto_size_text=True, justification="center"),
            PYGUI.Text("\tlimit", auto_size_text=True, justification="center"),
            PYGUI.Input(default_text='100', key='-IN-', size=(5, 2), justification='center', enable_events=True, tooltip='Limit the maximum of the plotting data')
                ],
            [
            PYGUI.Listbox(values=list({User_List.User for User_List in map_result_list}),
                enable_events=True,
                size=(15, 5),
                auto_size_text=True,
                pad=(2,2),
                select_mode=PYGUI.LISTBOX_SELECT_MODE_MULTIPLE,
                key='User_select'),
            PYGUI.Button(button_text="or",size=(5,2)), # widthxheight
            PYGUI.Button(button_text="and",size=(5,2)),
            PYGUI.Listbox(values=list({Place_List.Place for Place_List in map_result_list}),
                enable_events=True,
                size=(25, 5),
                auto_size_text=True,
                pad=(4,4),
                select_mode=PYGUI.LISTBOX_SELECT_MODE_MULTIPLE,
                key='Place_select'),
            PYGUI.Button(button_text='Show on map',size=(12,3))
                ],
            [
            PYGUI.Text("Result after choosing the specs", auto_size_text=True, justification="center", visible=False, key="Spec_Table_Label")
                ],
            [
            PYGUI.Table(values=[[" "," "," "," "," "," "," "]],
                    headings=["Place", "Date", "Time", "Recorder",
                                    "Latitude", "Longitude", "Altitude"],
                    justification="center",
                    display_row_numbers=True,
                    hide_vertical_scroll=True,
                    auto_size_columns=False,
                    visible=False,
                    num_rows=5,
                    key='Spec_Table',
                    pad=(2,2),
                    size=(150 ,None))
                ]
        ]

        self.window = PYGUI.Window("Show Species info", layout=layout,resizable=True,)

         # Event Loop
        while True:
            event, values = self.window.Read()
            if event == None:
                PYGUI.popup_animated(None)
                break
            elif event == PYGUI.WIN_CLOSED or event == 'Quit':
                PYGUI.popup_animated(None)
                break
            elif event == 'Show on map':
                Index.map_plot_max_data_num = int(values['-IN-'])
                Spec_DATA = self.Show_on_map(map_result_list)
                self.window['Spec_Table'].update(values=[[index.Place,
                                                    index.Dates,
                                                    index.Times,
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
                self.window['or'].update(button_color=("black", "white"))
            elif event == '-IN-':
                if int(values['-IN-']) <= 0:
                    messagebox.showwarning('Warning!!!', 'Please set the positive integer value')
        self.window.Close()

    #\ map
    # https://github.com/gmplot/gmplot/blob/master/gmplot/google_map_plotter.py
    # https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python/40905794
    # https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
    # marker title has some problem

    #\ show result on map
    def Show_on_map(self, input_map_list):
        map_list = []
        map_file_path = os.path.realpath(Index.mapfilename)

        #\ check the limit number
        if Index.map_plot_max_data_num <= 0:
            messagebox.showwarning('Warning!!!', 'The limit number should be positive integer')
            return []

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
        if (len(map_list) > Index.map_plot_max_data_num):
            #del map_list[0: len(map_list) -Index. map_plot_max_data_num]
            limit_map_list = map_list[0: Index.map_plot_max_data_num]
        elif (len(map_list) == 0):  # make sure the map data is not empty
            PYGUI.popup_animated(None)
            messagebox.showinfo("Info", "No data match the spec")
            return []
        else:
            limit_map_list = map_list


        # LOOP until finding the non empty LAT and LNG
        # and check after looping, the resultant list is emty or not
        index = 0
        for index in range(len(limit_map_list)):
            if (limit_map_list[index].Latitude == "" and limit_map_list[index].Longitude == ""):
                if index < len(limit_map_list)-1:
                    index += 1
                else:
                    messagebox.showinfo("info","All the record have no latitude and longitutde information")
                    return
            else:
                break

        #since ID find will find plenty of species in one record so modify the title
        if limit_map_list[index].Species == "" and limit_map_list[index].SpeciesFamily == "":
            Title = "map"
        else:
            Title = Index.Species_class_key[limit_map_list[index].SpeciesFamily] + Index.Species_key[limit_map_list[index].Species]
        gmp = gmplot.GoogleMapPlotter(float(limit_map_list[index].Latitude), float(limit_map_list[index].Longitude), 13, apikey=self.var_APIKEY.get(),
                                        title=Title)
                                        #title= limit_map_list[index].Species.encode('unicode_escape').decode("utf-8"))
        try:
            for index in limit_map_list:
                PYGUI.PopupAnimated(PYGUI.DEFAULT_BASE64_LOADING_GIF,background_color="white", time_between_frames=1)
                if not(index.Latitude == "" or index.Longitude == ""):
                    tmp_dict = {"User": index.User,
                                "Dates": index.Dates,
                                "Times": index.Times,
                                "Place": index.Place,
                                "Altitude": index.Altitude,
                                "Latitude": index.Latitude,
                                "Longitude": index.Longitude}
                    context =  Index.info_box_template.format(**tmp_dict)
                    gmp.marker(float(index.Latitude), float(index.Longitude),
                                color="red",
                                label= index.Place.encode('unicode_escape').decode("utf-8"),
                                info_window=context.encode('unicode_escape').decode("utf-8"))
                    gmp.draw(map_file_path)
            webbrowser.open(map_file_path)
            PYGUI.PopupAnimated(None)
        except:
            PYGUI.PopupAnimated(None)
            messagebox.showinfo("info", "try to reduce the limit number")

        return limit_map_list


    #\ Plot by Matplotlib
    def MatplotlibPlotButton(self):
        print(f"time start from {self.var_Time_start.get()} to {self.var_Time_end.get()}")
        print(self.Plot_var_species.get())
        PFD.PlotChart("Matplotlib",
                        Index.Species_key_fullname_C2E[self.Plot_var_species.get()],
                        [self.var_Time_start.get(), self.var_Time_end.get()]
                    )

    #\ Plot by Pyechart
    def PyechartsPlotButton(self):
        PFD.PlotChart("Pyecharts",
                            Index.Species_key_fullname_C2E[self.Plot_var_species.get()],
                            [self.var_Time_start.get(), self.var_Time_end.get()]
                        )




    #\ Time duration (Year)
    def Time_Duration_year_callback(self, var, indx, mode):
        if self.VarTimeDuration_ckeckbox.get() and (self.var_Duration_year.get() not in ["", " "]):
            self.var_Time_start.set( (datetime.today() - relativedelta(years = int(self.var_Duration_year.get()))).strftime("%Y-%m-%d"))


    #\ Time duration (Month)
    def Time_Duration_month_callback(self, var, indx, mode):
        if self.VarTimeDuration_ckeckbox.get() and (self.var_Duration_month.get() not in ["", " "]):
            self.var_Time_start.set((datetime.today() - relativedelta(years = int(self.var_Duration_year.get()), months = int(self.var_Duration_month.get()))).strftime("%Y-%m-%d"))

    #\ Time duraiton checkbutton
    def TimeDuration_checkbox_callback(self):
        if self.VarTimeDuration_ckeckbox.get():
            if (self.var_Duration_month.get() not in ['0', "", " "]):
                self.var_Time_start.set((datetime.today() - relativedelta(months = int(self.var_Duration_month.get()))).strftime("%Y-%m-%d"))

            if (self.var_Duration_year.get() not in ['0', "", " "]):
                self.var_Time_start.set( (datetime.today() - relativedelta(years = int(self.var_Duration_year.get()))).strftime("%Y-%m-%d") )

    #\ Hub open
    def Hub_callback(self, link):
        webbrowser.open(link)


# Driver Code
if __name__ == '__main__':
    app = tkinterApp()
    app.geometry(Index.Login_geometry)
    app.title(" Please Login")
    app.mainloop()