# this is GUI split program

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from PySimpleGUI.PySimpleGUI import RELIEF_FLAT, RELIEF_GROOVE, RELIEF_SUNKEN
import Dragonfly
import DataClass
import os
import PySimpleGUI as PYGUI
import gmplot
import webbrowser
import Index
import Save2File
from datetime import datetime
import threading
import gmplot
import Chromedriver.update_chromedriver
from dateutil.relativedelta import relativedelta
import Plot_from_database as PFD
from urllib.request import urlopen
import io
from PIL import Image, ImageTk
import random
import time



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





################################################################################
#\ main GUI
#\ change page
class tkinterApp(tk.Tk):

    #\ __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        if __name__ == '__main__':

            #\ __init__ function for class Tk
            tk.Tk.__init__(self, *args, **kwargs)

            #\ ---Menu Bar---
            self.menubar = tk.Menu(self)
            self.Emptymenubar = tk.Menu(self)
            self.config(menu=self.menubar)

            # creating a container
            container = tk.Frame(self)
            container.pack(side = "top", fill = "both", expand = True)

            container.grid_rowconfigure(0, weight = 1)
            container.grid_columnconfigure(0, weight = 1)

            #\ initializing frames to an empty array
            self.frames = {}

            # iterating through a tuple consisting
            # of the different page layouts
            for F in (LoginPage, MainPage, SettingPage):

                frame = F(container, self)

                #\ initializing frame of that object from
                #\ LoginPage, MainPage respectively with
                #\ for loop
                self.frames[F] = frame

                frame.grid(row = 0, column = 0, sticky ="nsew")

            self.show_frame(LoginPage)

    #\ to display the current frame passed as
    #\ parameter
    def show_frame(self, cont):
        global Username
        frame = self.frames[cont]

        #\ menu setting
        if frame._name == "!loginpage":
            self.config(menu=self.Emptymenubar)
        else:
            self.config(menu=self.menubar)


        print(frame._name)
        tk.Tk.wm_title(self, "蜻蜓經緯度查詢-- {} 已登入".format(Username))
        tk.Tk.wm_geometry(self, Index.MainPageGeometry)
        tk.Tk.iconbitmap(self, default=Index.ico_image_path)
        frame.tkraise()


    #\ define the action when mouse hover on the button
    #\ but it can be replace by ttk widget
    def B_HoverOn(self, event, color):
        event.widget['background'] = color

    def BHoverOn(self, w:tk, colorList:list):
        w.bind("<Leave>", lambda event, color=colorList[0]: self.B_HoverOn(event, color))
        w.bind("<Enter>", lambda event, color=colorList[1]: self.B_HoverOn(event, color))

    def B_HoverOnGroup(self, event, color, groupmember:list):
         event.widget['background'] = color
         for i in range(len(groupmember)):
            groupmember[i]['background'] = color

    def BHoverOnGroup(self, trigger:tk, beenTrigger:list, colorList:list):
        trigger.bind("<Leave>", lambda event, color=colorList[0], groupmember=beenTrigger: self.B_HoverOnGroup(event, color, groupmember))
        trigger.bind("<Enter>", lambda event, color=colorList[1], groupmember=beenTrigger: self.B_HoverOnGroup(event, color, groupmember))





#\ --- Login Page ---
#\ first window frame LoginPage
#\ controller is the parent class
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        if __name__ == '__main__':
            tk.Frame.__init__(self, parent, bg="white")

            #\ check and update the chromedriver
            Chromedriver.update_chromedriver.check_chromedriver()

            #\ label of frame Layout 2
            self.Loginlabel = tk.Label(self, text="Login", font=LARGEFONT, bg="white")
            self.AccountLabel = tk.Label(self, text="Account", bg="white")
            self.StatementLabel = tk.Label(self, text=Index.copyright_text,
                                        bg="white", fg = "gray", font = ("Arial", 8))

            #\ putting the grid in its place by using
            self.VarName = tk.StringVar(self, value='')
            self.VarPwd = tk.StringVar(self, value='')
            self.accountFrame = tk.Frame(self, bg="black", borderwidth = 1, relief = "sunken")
            self.accountEntry = tk.Entry(self.accountFrame, textvariable=self.VarName, relief=tk.FLAT)
            self.password_eyeFrame = tk.Frame(self, bg='white')
            self.passwordFrame = tk.Frame(self.password_eyeFrame, bg="black", borderwidth = 1, relief = "sunken")
            self.passwordEntry = tk.Entry(self.passwordFrame, textvariable=self.VarPwd, relief=tk.FLAT, show="*")
            self.PasswordPadLabel = tk.Label(self.password_eyeFrame, bg="white")
            self.PasswordLabel = tk.Label(self.password_eyeFrame, text="Password", bg="white")


            #\ --Button--
            #\ log in
            self.Loginbutton = tk.Button(self,
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
            self.ViewPWbuttonIMG = tk.PhotoImage(file=Index.Image_path + "\\view.png")
            self.ViewPWbutton = tk.Button(self.password_eyeFrame,
                                        text="view",
                                        command=self.ViewPWButtonfunc,
                                        bg='white',
                                        activebackground="white",
                                        relief=tk.FLAT,
                                        image=self.ViewPWbuttonIMG)
            controller.BHoverOn(self.ViewPWbutton, ["white", "grey87"])

            #\ --Image--
            self.NotViewPWbuttonIMG = tk.PhotoImage(file=Index.Image_path + "\\viewhidden.png")
            #photoimage = ViewPWbuttonIMG.subsample(3, 3)

            #\ --checkbox--
            self.viewcheck = tk.BooleanVar(self.password_eyeFrame, True)

            #\ --Putting the button in its place by--
            self.Loginlabel.pack(pady=20)
            self.AccountLabel.pack()
            self.accountFrame.pack()
            self.accountEntry.pack()

            self.password_eyeFrame.pack()
            self.PasswordLabel.pack(side=tk.TOP)
            self.PasswordPadLabel.pack(side=tk.LEFT, padx=14)
            self.ViewPWbutton.pack(side=tk.RIGHT)
            self.passwordFrame.pack(side=tk.RIGHT)
            self.passwordEntry.pack()

            self.Loginbutton.pack(pady=20)
            self.StatementLabel.pack(pady=20)

            #\ --try to auto fill the account and password--
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


    #\ Check if the user have entered the info (account and password) or not
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
        threading.Thread(target=self.LoginButtonFuncthread(controller)).start()

    #\ Login thread
    def LoginButtonFuncthread(self, controller):
        global Login_Response, Login_state, Username
        Index.myaccount = self.VarName.get()
        Index.mypassword = self.VarPwd.get()
        if self.Check_empty() > 0:
            return
        else:
            [_, Login_Response, Login_state] = Dragonfly.Login_Web(Index.myaccount, Index.mypassword)
            if (Login_state == False):
                messagebox.showwarning('Warning!!!', 'Account' + " or " + 'Password' + " might be incorrect!!!!")  #incorrect account or password
            elif Login_Response == None and Login_state == None:
                messagebox.showwarning('Warning!!!',"No connection to server, check the internet connection!!!")
            else:
                Username = Index.myaccount
                controller.show_frame(MainPage)
                #\ and write the account and password to the Login_Filename
                with open(Index.Login_Filename, 'w') as fp:
                    fp.write(','.join((Index.myaccount, Index.mypassword)))


    #\ the eye button that can hide the PW or show it
    def ViewPWButtonfunc(self):
        if self.viewcheck.get() == True:
            self.passwordEntry.config(show="")
            self.ViewPWbutton.config(image=self.NotViewPWbuttonIMG)
            self.viewcheck.set(False)
        else:
            self.passwordEntry.config(show="*")
            self.ViewPWbutton.config(image=self.ViewPWbuttonIMG)
            self.viewcheck.set(True)



#\ --- Setting Page ---
class SettingPage(tk.Frame):
    def __init__(self, parent, controller):
        if __name__ == '__main__':
            tk.Frame.__init__(self, parent, bg="white")
            self.SettingTitle = tk.Label(self, text="Setting", background="white")
            self.returnbutton = ttk.Button(self, text="Return", command=lambda: controller.show_frame(MainPage))
            self.SettingTitle.pack()
            self.returnbutton.pack()




#\ --- Main Page ---
#\ second window frame MainPage
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        if __name__ == '__main__':
            tk.Frame.__init__(self, parent, bg="white")

            #\ ---Menu Bar---
            self.filemenu = tk.Menu(controller.menubar, tearoff=0)
            self.filemenu.add_command(label="API&Key", command=lambda : controller.show_frame(SettingPage))
            self.filemenu.add_command(label="Image url", command=self.donothing)
            self.filemenu.add_separator()
            self.filemenu.add_command(label="Exit", command=self.quit)
            controller.menubar.add_cascade(label="Settings", menu=self.filemenu)

            self.helpmenu = tk.Menu(controller.menubar, tearoff=0)
            self.helpmenu.add_command(label="Help Index", command=self.donothing)
            self.helpmenu.add_command(label="About...", command=self.donothing)
            controller.menubar.add_cascade(label="Help", menu=self.helpmenu)



            #\ Label frame and label setting
            labelframe_font_size = 10
            LabelFrame_font = ("Arial", labelframe_font_size, "bold")
            label_font_size = 10
            label_font_style = ("Arial", label_font_size)


            #\ ---Image Frame---
            #####################
            #\ 設定圖片
            #\ directory from where script was ran
            self.img_counter = 0
            self.previous_img = None
            #\ put the image on a typical widget
            self.imglabel = tk.Label(self, bg='white',relief=tk.FLAT, borderwidth=0, highlightthickness=0)
            self.imglabel.pack(padx=5, pady=5)
            self.init_while = False
            self.update_img()


            #\ ---ID Find Frame---
            ######################
            #\ label frame
            ID_LabelFrame_bg = "white"
            self.LabelFrame_ID_Find = tk.LabelFrame(self, text='ID Find', fg="red", font=LabelFrame_font, bg=ID_LabelFrame_bg, highlightbackground="red", takefocus=True)

            #\ Label
            self.APIKEY_label = tk.Label(self.LabelFrame_ID_Find, text = "API-Key:", font=label_font_style, bg=ID_LabelFrame_bg)
            self.id_label = tk.Label(self.LabelFrame_ID_Find, text = "ID:", font=label_font_style, bg=ID_LabelFrame_bg)
            self.latitude_label = tk.Label(self.LabelFrame_ID_Find, text = "(LAT, LNG): ", font=label_font_style, bg=ID_LabelFrame_bg)

            #\ Entry
            self.var_APIKEY = tk.StringVar(self.LabelFrame_ID_Find)
            self.APIKEY_border = tk.Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
            self.APIKEY = tk.Entry(self.APIKEY_border, textvariable=self.var_APIKEY)
            self.APIKEY_TLTP = DataClass.CreateToolTip(self.APIKEY, "This is the apikey for google map to remove the watermark of \" for develop purpose only\"")

            self.ID_border = tk.Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief="sunken")  # to make a border for the entry
            self.ID = tk.Entry(self.ID_border)

            self.var_LNGLAT = tk.StringVar(self.LabelFrame_ID_Find)
            self.LNGLAT_border = tk.Frame(self.LabelFrame_ID_Find, bg="black", borderwidth=1, relief=RELIEF_FLAT)
            self.blank_LNGLAT = tk.Entry(self.LNGLAT_border, textvariable=self.var_LNGLAT)


            self.LabelFrame_ID_Find.pack(fill="both", expand="yes")

            self.id_enter_button = ttk.Button(self.LabelFrame_ID_Find,
                            text='ID Enter\b',
                            #justify = 'center',
                            #bg='gray80',
                            cursor="hand2",
                            command=lambda: self.IDEnterButton(self.ID.get()))
                            #\ color info : http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png


            #\ list to get the label and labelfrme in ID Find frame
            self.IDFindLabelList = [self.LabelFrame_ID_Find, self.APIKEY_label, self.id_label, self.latitude_label]



            #\ ---Species Find Frame---
            ###########################
            Species_Find_LabelFrame_bg = "white"
            self.LabelFrame_Species_Find = tk.LabelFrame(self, text='Species Find', fg="orange", font=LabelFrame_font, bg=Species_Find_LabelFrame_bg, highlightbackground="red", takefocus=True)
            self.LabelFrame_Species_Find.pack(fill="both", expand="yes")

            #\ Label
            self.Species_label = tk.Label(self.LabelFrame_Species_Find, text="Select the Family and Species", font=label_font_style , bg=Species_Find_LabelFrame_bg)

            #\ drop down menu
            #\ species
            global var_species
            var_species = tk.StringVar(self.LabelFrame_Species_Find)
            var_species.set(Index.Calopterygidae_Species[0])
            self.Species_drop_down_menu = ttk.Combobox(self.LabelFrame_Species_Find, width=14, textvariable=var_species, values=Index.Species_Name_Group[current_dropdown_index])

            #\ family
            global var_family
            var_family = tk.StringVar(self.LabelFrame_Species_Find)
            var_family.set(Index.Species_Family_Name[0])
            self.Family_drop_down_menu = ttk.Combobox(self.LabelFrame_Species_Find, width=10, textvariable=var_family, values=Index.Species_Family_Name)
            self.Family_drop_down_menu.bind("<<ComboboxSelected>>", self.changeCombobox)

            #\ check box
            self.VarDatacheckbox = tk.BooleanVar(self.LabelFrame_Species_Find)
            self.Datacheckbox = tk.Checkbutton(self.LabelFrame_Species_Find, text="EXCEL-SQL", variable=self.VarDatacheckbox, bg="white")
            self.DatacheckboxTLTP = DataClass.CreateToolTip(self.Datacheckbox, "This will import data from database")

            #\ Button
            self.species_find_button = ttk.Button(self.LabelFrame_Species_Find,
                                        text='Find Species',
                                        #justify='center',
                                        #bg='gray80',
                                        cursor="hand2",
                                        command=lambda:self.SpeciesFindButton(var_family.get(), var_species.get()))


            #\ list to get the label and labelfrme in Species Find frame
            self.SpeciesFindLabelList = [self.LabelFrame_Species_Find, self.Species_label, self.Datacheckbox]



            #\ ---Save2file Frame---
            ########################
            #\ frame
            Save2file_LabelFrame_bg = "white"
            self.LabelFrame_Save2file = tk.LabelFrame(self, text='Crawling data', fg="green", font=LabelFrame_font, bg=Save2file_LabelFrame_bg, highlightbackground="red", takefocus=True)

            #\ Label
            self.Save2file_label = tk.Label(self.LabelFrame_Save2file, text="Update the database", font=label_font_style , bg=Save2file_LabelFrame_bg, anchor='w')
            self.MaxCrawling_label = tk.Label(self.LabelFrame_Save2file, text="Max Crawling NO", font=label_font_style , bg=Species_Find_LabelFrame_bg)
            self.LabelFrame_Save2file.pack(fill="both", expand="yes") # fill both horizon and vertically

            #\ Entry
            self.var_MC = tk.StringVar(self.LabelFrame_Save2file)
            self.var_MC.set(str(Index.limit_cnt))
            self.MaxCrawling_width = 10
            self.MaxCrawling_border = tk.Frame(self.LabelFrame_Save2file, bg="black", borderwidth=1, relief="sunken", width=self.MaxCrawling_width)
            self.MaxCrawling = tk.Entry(self.MaxCrawling_border, textvariable=self.var_MC, width=self.MaxCrawling_width, justify="center")
            self.MaxCrawlingTLTP = DataClass.CreateToolTip(self.MaxCrawling, "This will limit the max number of data shown")

            #\ Button
            self.Save2file_button = ttk.Button(self.LabelFrame_Save2file,
                                        text='Update',
                                        #justify='center',
                                        #bg='gray80',
                                        style='Fun.TButton',
                                        cursor="hand2",
                                        command=self.Save2FileButton)

            #\ Slider
            self.Save2file_slider = tk.Scale(self.LabelFrame_Save2file, from_=1, to=Index.maxcpus, label="Crawling speed",
                                        orient=tk.HORIZONTAL, bg=Save2file_LabelFrame_bg, tickinterval=1, cursor="hand2",
                                        length=250, sliderrelief=tk.GROOVE, troughcolor="black", command=self.Save2FileSliderValue)
            self.Save2file_slider.set(Index.maxcpus)#self.Save2file_slider.set(int(maxcpus / 2))


            #\ list to get the label and labelfrme in Save2file frame
            self.Save2fileLabelList = [self.LabelFrame_Save2file, self.Save2file_label, self.MaxCrawling_label, self.Save2file_slider]



            #\ ---Plot Chart---
            ###################
            #\ Label Frame
            Plot_LabelFrame_bg = "white"
            self.LabelFrame_Plot = tk.LabelFrame(self, text="Plot Chart", font=LabelFrame_font, bg=Plot_LabelFrame_bg, fg="blue", highlightbackground="red", takefocus=True)
            self.LabelFrame_Plot.pack(fill="both", expand="yes") # fill both horizon and vertically

            #\ Label
            self.Time_range_from_label = tk.Label(self.LabelFrame_Plot, text="From", bg=Plot_LabelFrame_bg)
            self.Time_range_to_label = tk.Label(self.LabelFrame_Plot, text="to", bg=Plot_LabelFrame_bg)
            self.Time_Duration_Year_label = tk.Label(self.LabelFrame_Plot, text="Year", bg=Plot_LabelFrame_bg)
            self.Time_Duration_Month_label = tk.Label(self.LabelFrame_Plot, text="Month", bg=Plot_LabelFrame_bg)


            #\ Drop down menu
            #\ species
            self.Plot_var_species = tk.StringVar(self.LabelFrame_Plot, value=Index.Calopterygidae_Species[0])
            self.Plot_Species_drop_down_menu = ttk.Combobox(self.LabelFrame_Plot, width=14, textvariable=self.Plot_var_species, values=Index.Species_Name_Group[current_dropdown_index])

            #\ family
            self.Plot_var_family = tk.StringVar(self.LabelFrame_Plot, value=Index.Species_Family_Name[0])
            self.Plot_Family_drop_down_menu = ttk.Combobox(self.LabelFrame_Plot, width=10, textvariable=self.Plot_var_family, values=Index.Species_Family_Name)
            self.Plot_Family_drop_down_menu.bind("<<ComboboxSelected>>", self.changeCombobox)

            #\ Button
            self.MatplotlibPlot_button = tk.Button(self.LabelFrame_Plot,
                                        text='Matplotlib',
                                        justify='center',
                                        bg='White',
                                        cursor="hand2",
                                        relief=RELIEF_GROOVE,
                                        command=self.MatplotlibPlotButton)
            controller.BHoverOn(self.MatplotlibPlot_button, ['White','gray70'])
            self.MatplotlibPlot_button_logo = tk.PhotoImage(file=Index.Matplotlib_img_path)
            self.MatplotlibPlot_button.config(image=self.MatplotlibPlot_button_logo)



            self.PyechartsPlot_button = tk.Button(self.LabelFrame_Plot,
                                        text='Pyecharts',
                                        justify='center',
                                        bg='White',
                                        cursor="hand2",
                                        relief=RELIEF_GROOVE,
                                        command=self.PyechartsPlotButton)
            controller.BHoverOn(self.PyechartsPlot_button, ['White','gray70'])
            self.PyechartsPlot_button_logo = tk.PhotoImage(file=Index.Echarts_img_path)
            self.PyechartsPlot_button.config(image=self.PyechartsPlot_button_logo)

            #\ Entry
            today = datetime.today()
            shift_year_age = today - relativedelta(years = Index.Plot_chart_init_delta_years)  #\ shift the time back to the previous year
            self.var_Time_end = tk.StringVar(self.LabelFrame_Plot, value=today.strftime("%Y-%m-%d"))
            self.var_Time_start = tk.StringVar(self.LabelFrame_Plot, value=shift_year_age.strftime("%Y-%m-%d"))
            self.Time_range_width = 10
            self.Time_range_start_border = tk.Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.Time_range_width)
            self.Time_range_start = tk.Entry(self.Time_range_start_border, width=self.Time_range_width, textvariable=self.var_Time_start, justify="center")
            self.Time_range_end_border = tk.Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.Time_range_width)
            self.Time_range_end = tk.Entry(self.Time_range_end_border, width=self.Time_range_width, textvariable=self.var_Time_end, justify="center")


            #\ time selector
            self.VarTimeDuration_ckeckbox = tk.BooleanVar(self.LabelFrame_Plot, value=False)
            self.TimeDuration_checkbox = tk.Checkbutton(self.LabelFrame_Plot, text="--", variable=self.VarTimeDuration_ckeckbox, bg="white", cursor= "arrow", command=self.TimeDuration_checkbox_callback)
            self.TimeDuration_checkboxTLTP = DataClass.CreateToolTip(self.TimeDuration_checkbox, "Use the time adjest or not")

            self.var_Duration_month = tk.StringVar(self.LabelFrame_Plot, value=str(0))
            self.var_Duration_month.trace_add("write", self.Time_Duration_month_callback)
            self.var_Duration_year = tk.StringVar(self.LabelFrame_Plot, value=str(0))
            self.var_Duration_year.trace_add("write", self.Time_Duration_year_callback)
            self.TimeDuration_range_width = 5
            self.Time_Duration_year_border = tk.Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.TimeDuration_range_width)
            self.Time_Duration_year =tk.Entry(   self.Time_Duration_year_border,
                                                width=self.TimeDuration_range_width,
                                                textvariable=self.var_Duration_year,
                                                justify="center",
                                                # validate='all',
                                                # validatecommand=self.Time_Duration_year_callback
                                            )
            self.Time_Duration_month_border = tk.Frame(self.LabelFrame_Plot, bg="black", borderwidth=1, relief="sunken", width=self.TimeDuration_range_width)
            self.Time_Duration_month = tk.Entry( self.Time_Duration_month_border,
                                            width=self.TimeDuration_range_width,
                                            textvariable=self.var_Duration_month,
                                            justify="center",
                                            # validate='all',
                                            # validatecommand=self.Time_Duration_month_callback
                                         )


            #\ list to get the label and labelfrme in Save2file frame
            self.PlotChartLabelList = [self.LabelFrame_Plot, self.Time_range_from_label, self.Time_range_to_label, self.Time_Duration_Year_label,
                                        self.Time_Duration_Month_label, self.TimeDuration_checkbox]



            #\ ---The link to my Github and doc---
            ########################################
            #\ frame
            Hub_LabelFrame_bg = "White"
            self.Hub_Frame = tk.LabelFrame(self, text="", font=LabelFrame_font, bg=Hub_LabelFrame_bg, highlightbackground="red", takefocus=True)
            self.Hub_Frame.pack(fill="both", expand="yes")
            self.Hub_parentF = tk.Frame(self.Hub_Frame, bg=Hub_LabelFrame_bg)

            #\ Github Label Image
            self.githubImg = tk.PhotoImage(file=Index.github_img_path)
            Label_bg_color = "white"
            self.Hub_Label = tk.Label(self.Hub_parentF, text="github", cursor="hand2", image=self.githubImg, bg=Label_bg_color)
            self.Hub_Label.bind("<Button-1>", lambda e: self.Hub_callback("https://github.com/tingweichien/Dragonfly_Web_Crawler"))
            self.Hub_Label_tooltip = DataClass.CreateToolTip(self.Hub_Label, "Go to Github", window_y=-15)

            #\ Web-version Label Image
            self.web_versionImg = tk.PhotoImage(file=Index.web_version_img_path)
            self.Web_version_Label = tk.Label(self.Hub_parentF, text="web version", cursor="hand2", image=self.web_versionImg, bg=Label_bg_color)
            self.Web_version_Label.bind("<Button-1>", lambda e: self.Hub_callback("https://flask-web-training.herokuapp.com/"))
            self.Web_version_tooltip = DataClass.CreateToolTip(self.Web_version_Label, "Go to Web version of this app", window_y=-15)

            #\ ReadtheDoc Label Image
            self.ReadthedocsImg = tk.PhotoImage(file=Index.Readthedocs_img_path)
            self.Readthedocs_Label = tk.Label(self.Hub_parentF, text="read the docs", cursor="hand2", image=self.ReadthedocsImg, bg=Label_bg_color)
            self.Readthedocs_Label.bind("<Button-1>", lambda e: self.Hub_callback("https://dragonfly-web-crawler.readthedocs.io/en/latest/"))
            self.Readthedocs_tooltip = DataClass.CreateToolTip(self.Readthedocs_Label, "Go to read the docs for more detail info", window_y=-10)

            #\ list to get the label and labelfrme in Save2file frame
            # self.LinkLabelList = [self.Hub_Frame, self.Hub_parentF]


            #\ ---grid---
            #############

            #\ ID Find
            self.APIKEY_label.grid(row=3)
            self.id_label.grid(row=4)
            self.latitude_label.grid(row=5)

            self.id_enter_button.grid(row=4, column=2, columnspan=1, padx = 5)

            self.APIKEY.grid(row=3, column=1)
            self.APIKEY_border.grid(row=3, column=1)
            self.ID.grid(row=4, column=1)
            self.ID_border.grid(row=4, column=1)
            self.blank_LNGLAT.grid(row=5, column=1)
            self.LNGLAT_border.grid(row=5, column=1)

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
            self.MaxCrawling.grid(row=10, column=3, sticky=tk.N)
            self.MaxCrawling_border.grid(row=10, column=3, sticky=tk.N)

            #\ Plot Chart
            self.Plot_Family_drop_down_menu.grid(row=11, column=0, columnspan=2, padx=3)
            self.Plot_Species_drop_down_menu.grid(row=11, column=2, columnspan=2, padx=3)
            self.MatplotlibPlot_button.grid(row=11, column=5, columnspan=2, pady=3, padx=20, sticky=tk.E)
            self.PyechartsPlot_button.grid(row=12, rowspan=2, column=5, columnspan=2, padx=20, sticky=tk.E)
            self.Time_range_from_label.grid(row=12, column=0)
            self.Time_range_start.grid(row=12, column=1)
            self.Time_range_start_border.grid(row=12, column=1)
            self.Time_range_to_label.grid(row=12, column=2)
            self.Time_range_end.grid(row=12, column=3)
            self.Time_range_end_border.grid(row=12, column=3, pady=3)

            self.TimeDuration_checkbox.grid(row=13, column=1, sticky=tk.W)
            self.Time_Duration_year.grid(row=13, column=1, sticky=tk.E)
            self.Time_Duration_year_border.grid(row=13, column=1, sticky=tk.E)
            self.Time_Duration_Year_label.grid(row=13, column=2, sticky=tk.W)
            self.Time_Duration_month.grid(row=13, column=3, sticky=tk.W)
            self.Time_Duration_month_border.grid(row=13, column=3, sticky=tk.W)
            self.Time_Duration_Month_label.grid(row=13, column=3, sticky=tk.E)

            #\ Hub and docs
            self.Hub_Label.pack(side=tk.LEFT, padx=15)
            self.Readthedocs_Label.pack(side=tk.RIGHT, padx=15)
            self.Web_version_Label.pack(side=tk.RIGHT, padx=15)
            self.Hub_parentF.pack(expand=True)



            #\ some initialization
            ####################
            self.Place_select_value = ''
            self.User_select_value = ''
            self.Map_spec_method_or_and = ''

            #\ All of the label, checkboxes, Labelframe List
            #\ remember when you add new group here, also add the corresponding color at the Index.py
            self.MainPageLabelList:list =  [ self.IDFindLabelList,
                                        self.SpeciesFindLabelList,
                                        self.Save2fileLabelList,
                                        self.PlotChartLabelList,
                                        # self.LinkLabelList
                                        ]

            #\ make the label and label frame change background when mouse hover on it
            self.Hover_ChangeBackgroundColor(controller)




    ###################################################################################
    #\ ---Method---
    #\ make the label and label frame change background when mouse hover on it
    def Hover_ChangeBackgroundColor(self, controller):
        for idx, FrameLabelList in enumerate(self.MainPageLabelList):
            #\ the last args in the BHoverOn is list of the color for original and changed
            #\ the second arg is to pass all the elements in this Frame-list without the element pass in the first args.
            #\ get the current widget backgroundcolor : use b.cget("bg") or b["bg"] where i.e. b = Label(self, .....)
            tmpList = []
            for element in FrameLabelList:
                tmpList = FrameLabelList.copy()
                tmpList.remove(element)
                controller.BHoverOnGroup(element, tmpList, [element["bg"], Index.var_HCNgColorList[idx]])

    #\ Menu Bar
    def donothing(self):
        print("menu bar")



    #\ ID find
    def IDEnterButton(self, ID:str):
        # CHECK IF THE USER ENTER THE id OR NOT
        if ID == '':
            messagebox.showwarning('Warning!!!','ID should not be empty')
            return

        # Check if this data do not contain the Longitude and Latitude infomation
        map_key = True
        [_ID_find_result, _overflow, _Max_ID_Num] = Dragonfly.DataCrawler(Login_Response, ID)
        if _overflow:
            messagebox.showwarning('Warning!!!', "ID" + " number is out of range!!!! \nShoud be in the range of 0 ~ " + str(_Max_ID_Num))  #ID number overflow
            return
        else :
            if (_ID_find_result.Longitude == '' or _ID_find_result.Latitude == ''):
                _ID_find_result.Longitude = 'No Data'
                _ID_find_result.Latitude = 'No Data'
                map_key = False

        self.var_LNGLAT.set(f"({_ID_find_result.Longitude}, {_ID_find_result.Latitude})")
        if map_key:
            msg = messagebox.askyesno("info", "Do you want to plot it on map?")
            if msg:
                self.Show_on_map([_ID_find_result])


    # \ Species find to plot info inthe table and plot on the map
    def SpeciesFindButton(self, var_family, var_species):
        if self.VarDatacheckbox.get() == True:
            map_result_list = Save2File.ReadFromFile(Index.folder_all_crawl_data + Index.Species_class_key[var_family] + "\\" + Index.Species_class_key[var_family] + Index.Species_key[var_species] + ".csv")
        else:
            map_result_list = Dragonfly.SpeiciesCrawler(var_family, var_species)

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

    #\ progress bar percentage
    def pbLabel_text(self):
        self.progressbar_label['text'] = f'{self.pbVar.get()}% '

    #\ text in line 1
    def INameLabel_text(self, speciesfamily:str, species:str):
        self.Info_Name_label['text'] = '[Start Crawing] {}  {}'.format(speciesfamily, species)

    #\ text in line 2
    def IFileNameLabel_text(self, filename):
        self.Info_FileName_label['text'] = '[File Name]: {}'.format(filename)

    #\ text in line 3
    def IUpdateNumLabel_text(self, updateInfo):
        self.Info_UpdateNum_label['text'] = updateInfo

    #\ text in line 4
    def ICurrentNumLabel_text(self, currentNum):
        self.Info_CurrentNum_label['text'] = '[Current total crawl]: {}'.format(currentNum)

    #\ text in line 5
    def IStateLabel_text(self, state_text):
        self.Info_State_label['text'] = state_text

    #\ text in line 6
    def IFinishStateLabel_text(self, finish_text):
        self.Info_FinishState_label['text'] = finish_text

    #\ clear all the block
    def Update_Block_set_all_to_empty(self):
        self.Info_FinishState_label['text'] = ""
        self.Info_State_label['text'] = ""
        self.Info_CurrentNum_label['text'] = ""
        self.Info_UpdateNum_label['text'] = ""
        self.Info_FileName_label['text'] = ""
        self.Info_Name_label['text'] = ""


    #\ update the sub-progressbar
    #\ return the sub-progressbar label
    def set_sub_progressbar(self)->str:
        if self.update_section == "Save2File":
            self.SpinLabelIndex += 1
            return Index.SpinLabel[self.SpinLabelIndex % len(Index.SpinLabel)]
        else:
            if self.expecting_CNT != 0:
                self.pbVar_partial.set(100*Dragonfly.DataCNT.value/self.expecting_CNT)
                return f"({Dragonfly.DataCNT.value}/{self.expecting_CNT})"
            else:
                return "(0/0)"



    #\ thread to update gif
    #\ also for update the update timer
    #\ the sub-progressbar will also included
    def UpdateGIF(self, index):
        if self.GIFcheck == True :
            if index < Index.GIFMAXFRAME-1:
                index += 1
            elif index == Index.GIFMAXFRAME-1:
                index = 0
            frame = self.Load_image[index]
            self.loading_label.config(image=frame)

            #\ update the timer
            if self.update_timer_flag:
                delta_time = datetime.now() - self.start_time
                sec = delta_time.seconds
                milisec = delta_time.microseconds
                self.progressbar_label_time["text"] = f"({str(sec//60).zfill(2)}:{str(sec%60).zfill(2)}.{str(milisec//10**(Index.pb_microsecond_ndigits-Index.pb_showing_digit)).zfill(Index.pb_showing_digit)})"

            #\update the sub progressbar for value and label
            text = self.set_sub_progressbar()
            print(text)
            self.progressbar_partial_label["text"] = text

            #\ Update updating image
            self.progressbarFrame.after(100, lambda:self.UpdateGIF(index,))
        else:
            self.loading_label.config(image=self.Load_image[10])
            return


    #\ very important!!! using thread makes the progressbar move outside the main thread
    #\ Var_MySQL_enable : Update the crawling data from csv to MySQL
    #\ Var_weather_enable :　Update the weather data
    #\ Var_UpdatefWeb_enable : Update the data from web and save to the csv
    def start_button(self):
        self.start_time = datetime.now()
        def start_multithread():
            self.GIFcheck = True
            self.Info_Name_label['text'] = "Updating~"
            self.NewWindow.title = "Update data - updating~"
            Save2File.savefile(self, Index.parse_type, [self.Var_MySQL_enable.get(), self.Var_weather_enable.get(), self.Var_UpdatefWeb_enable.get()])
            self.GIFcheck = False

        #\ disable the button1
        self.button_popup['state'] = 'disabled'

        #\ start the timer
        self.update_timer_flag = True

        #\ start the thread
        threading.Thread(target=self.UpdateGIF, args=(0,)).start()
        threading.Thread(target=start_multithread).start()



    #\ Save2File pop up windows for progress
    def Save2File_popup(self):
        #\ new root window
        self.GIFcheck = True
        self.NewWindow = tk.Toplevel(app)
        self.NewWindow.title("Update data")
        self.NewWindow.geometry(Index.updateWinGeometry)
        self.NewWindow.config(bg="white")


        #\ Frame
        self.progressLabelFrame = tk.Frame(self.NewWindow, bg="white")
        self.progressLabelFrame.pack(side=tk.TOP)
        self.progressbarFrame = tk.Frame(self.NewWindow, bg="white")
        self.progressbarFrame.pack()
        self.progressbarSubFrame = tk.Frame(self.NewWindow, bg="white")
        self.progressbarSubFrame.pack()
        self.ButtonFrame = tk.Frame(self.NewWindow, bg="white")
        self.ButtonFrame.pack()


        #\ Progress layer
        progressbar_label = tk.Label(self.progressLabelFrame, text="Progress", bg="white")
        progressbar_label.pack(side=tk.LEFT)
        self.Load_image = [tk.PhotoImage(file=Index.updateGIF, format="gif -index %i" %(i)) for i in range(Index.GIFMAXFRAME)] # base on how many frame the gif file have
        self.loading_label = tk.Label(self.progressLabelFrame, bg="white")
        self.loading_label.pack(side=tk.RIGHT)

        self.pbVar = tk.IntVar(self.NewWindow)
        self.progressbar = ttk.Progressbar(self.progressbarFrame, orient=tk.HORIZONTAL, phase=1, length=350, mode="determinate", variable=self.pbVar, maximum=100)
        self.progressbar.pack(side=tk.LEFT, pady=10)

        self.progressbar_label_time = tk.Label(self.progressbarFrame, text="00:00", bg="white")
        self.progressbar_label_time.pack(side=tk.RIGHT, padx=5)
        self.progressbar_label = tk.Label(self.progressbarFrame, text="0%", bg="white")
        self.progressbar_label.pack(side=tk.RIGHT, padx=5)


        #\ Button layer
        button_popup_label = tk.Label(self.ButtonFrame, text="Ready to update?", bg="white")
        button_popup_label.pack()
        self.button_popup = ttk.Button(self.ButtonFrame, text="start", command=self.start_button)
        self.button_popup.pack(pady=2)


        #\ Check button
        #\ Color
        self.default_fg_color = "black"
        self.default_bg_color = "white"
        self.selected_fg_color = "green"
        self.updating_bg_color = "light sky blue"
        self.updating_fg_color = "black"
        self.finished_bg_color = "pale green"
        self.ChangeDefaultColor1 = False
        self.ChangeDefaultColor2 = False
        self.ChangeDefaultColor3 = False
        #\ this specify whether to update from web and save it to excel or not
        self.Var_UpdatefWeb_enable = tk.BooleanVar(self.ButtonFrame, value=True)
        self.checkbox_UpdatefWeb = tk.Checkbutton(self.ButtonFrame, text="UpdateWebData-Enable", fg=self.selected_fg_color, variable=self.Var_UpdatefWeb_enable, bg=self.default_bg_color, cursor= "arrow",command=self.checkbox_UpdatefWeb_callback)
        self.checkbox_UpdatefWeb.pack(side="left")
        #\ this specify whether to update MySQL database or not
        self.Var_MySQL_enable = tk.BooleanVar(self.ButtonFrame, value=True)
        self.checkbox_MySQL = tk.Checkbutton(self.ButtonFrame, text="MySQL-Enable", fg=self.selected_fg_color, variable=self.Var_MySQL_enable, bg=self.default_bg_color, cursor= "arrow", command=self.checkbox_MySQL_callback)
        self.checkbox_MySQL.pack(side="left")
        #\ this specify whether to update weather from online weather api or not
        self.Var_weather_enable = tk.BooleanVar(self.ButtonFrame, value=True)
        self.checkbox_weather = tk.Checkbutton(self.ButtonFrame, text="Weather-Enable", fg=self.selected_fg_color, variable=self.Var_weather_enable, bg=self.default_bg_color, cursor= "arrow",command=self.checkbox_weather_callback)
        self.checkbox_weather.pack(side="left")


        #\ Update progress infomation
        self.TextLabelFrame = tk.LabelFrame(self.NewWindow, text="Info", padx=40, bg="white")
        self.TextLabelFrame.pack(pady=10)
        self.Info_Name_label_Var = tk.StringVar(self.TextLabelFrame)
        self.Info_Name_label = tk.Label(self.TextLabelFrame, text="Ready to start Updating......", width=30, anchor='w', bg="white", textvariable=self.Info_Name_label_Var)
        self.Info_Name_label.pack(pady=3)
        self.Info_FileName_label = tk.Label(self.TextLabelFrame, anchor='w', bg="white")
        self.Info_FileName_label.pack(pady=3)
        self.Info_UpdateNum_label = tk.Label(self.TextLabelFrame, anchor='w', bg="white")
        self.Info_UpdateNum_label.pack(pady=3)
        self.Info_CurrentNum_label = tk.Label(self.TextLabelFrame, anchor='w', bg="white")
        self.Info_CurrentNum_label.pack(pady=3)
        self.Info_State_label = tk.Label(self.TextLabelFrame, anchor='w', bg="white")
        self.Info_State_label.pack(pady=3)
        self.Info_FinishState_label = tk.Label(self.TextLabelFrame, anchor='w', bg="white")
        self.Info_FinishState_label.pack(pady=3)

        #\ the sub bar for the progress bar
        # s = ttk.Style()
        # s.theme_use('clam')
        # s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.SubProgressbarFrame = tk.Frame(self.NewWindow, padx=40, bg="white")
        self.SubProgressbarFrame.pack(pady=10)

        self.progressbar_partial_label = tk.Label(self.SubProgressbarFrame, text="0/0", bg="white")
        self.progressbar_partial_label.pack(side=tk.RIGHT, padx=5)
        self.expecting_CNT = 0
        self.pbVar_partial = tk.IntVar(self.NewWindow)
        self.progressbar_partial = ttk.Progressbar(self.SubProgressbarFrame, orient=tk.HORIZONTAL,
                                                    phase=1, length=300, mode="determinate",
                                                    # style="red.Horizontal.TProgressbar",
                                                    variable=self.pbVar_partial, maximum=100)
        self.progressbar_partial.pack(side=tk.RIGHT, padx=5)


        #\sub progress bar spin label effect
        self.update_section = ""
        self.SpinLabelIndex = 0



    #\ Save2File_popup close window event
    def Save2File_popup_closeWindow(self):

        #\ stop the update timer
        self.update_timer_flag = False

        #\ destroy the window
        self.NewWindow.destroy()




    #\ progreebar portion base on the number of checkbox that indicates different update type you choose
    def progressbar_portion_calc(self)->dict:
        result = dict()
        result["MySQL_portion"] = 1 - int(self.Var_weather_enable.get()) * Index.Var_weather_enable_percentage \
                                    - int(self.Var_UpdatefWeb_enable.get()) * Index.Var_UpdatefWeb_enable_percentage
        result["weather_portion"] = 1 - int(self.Var_MySQL_enable.get()) * Index.Var_MySQL_enable_percentage \
                                        - int(self.Var_UpdatefWeb_enable.get()) * Index.Var_UpdatefWeb_enable_percentage
        result["UpdatefWeb_portion"] = 1 - int(self.Var_MySQL_enable.get()) * Index.Var_MySQL_enable_percentage \
                                        - int(self.Var_weather_enable.get()) * Index.Var_weather_enable_percentage
        return result



    #\ Button to open pop up window for checkupdating
    #\ read the flow from here to the top of the method in this class
    def Save2FileButton(self):
        Index.limit_cnt = int(self.var_MC.get())
        print(f"limit count is {Index.limit_cnt}")

        #\ pop up window
        self.Save2File_popup()


    #\ checkbox callback function for changing color
    def checkbox_MySQL_callback(self):
        if self.ChangeDefaultColor1:
            self.checkbox_MySQL["fg"] =  self.selected_fg_color
            self.ChangeDefaultColor1= False
        else :
            self.checkbox_MySQL["fg"] =  self.default_fg_color
            self.ChangeDefaultColor1 = True

    def checkbox_weather_callback(self):
        if self.ChangeDefaultColor2:
            self.checkbox_weather["fg"] =  self.selected_fg_color
            self.ChangeDefaultColor2 = False
        else :
            self.checkbox_weather["fg"] =  self.default_fg_color
            self.ChangeDefaultColor2 = True

    def checkbox_UpdatefWeb_callback(self):
        if self.ChangeDefaultColor3:
            self.checkbox_UpdatefWeb["fg"] =  self.selected_fg_color
            self.ChangeDefaultColor3 = False
        else :
            self.checkbox_UpdatefWeb["fg"] =  self.default_fg_color
            self.ChangeDefaultColor3 = True




    #\ Table
    #\ bad since the flexibility of the option are limited
    #\ these are coded in PySimpleGUI library
    def New_table(self, map_result_list:list):
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

        #\ Event Loop
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
    def Show_on_map(self, input_map_list:list):
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


    #\ gitHub open
    def Hub_callback(self, link:list):
        webbrowser.open(link)


    #\ Blending the image
    def blending_img(self):
        try:
            #\ random the number of picture
            self.img_counter = random.randrange(0, 9, 1)

            #\ limit the image counter within the range
            self.img_counter %= len(Index.img_url_list)

            #\ open the image from url
            image_bytes = urlopen( Index.img_url_list[self.img_counter], timeout=Index.Img_timeout).read()

            #\ internal data file
            data_stream = io.BytesIO(image_bytes)

            #\ open as a PIL image object
            self.pil_image = Image.open(data_stream)

            #\ convert PIL image object to Tkinter PhotoImage object
            self.pil_image = self.pil_image.resize((Index.coverImagWidth, Index.coverImagHeight), Image.ANTIALIAS)

            #\ Blending
            if (self.init_while):
                alpha = 0
                while(alpha < 1.0):
                    self.previous_img = self.previous_img if self.previous_img != None else self.pil_image
                    blendImg = Image.blend(self.previous_img, self.pil_image, alpha)
                    self.tk_image = ImageTk.PhotoImage(blendImg)
                    alpha += Index.BlendingPrecision #\ decide how precise the blending is
                    time.sleep(Index.BlendingTime) #\ decide how long between each frame
                    self.imglabel.config(image=self.tk_image)
                    self.imglabel.update()

                # \ set the current image as previous
                self.previous_img = self.pil_image

        except:
            print("[Warning] Blending failed~")
            self.tk_image  = tk.PhotoImage(file = Index.Image_path + "\\dragonfly_picture.gif")
            self.imglabel.config(image=self.tk_image)



    #\ update the image cover
    #\ this is because recalling this function by after or use the thread for this function
    #\ will cause the program to hang. Apply the thread to it will cause the error showing that
    #\ the mian thread is not in the main loop, so I add a wrap up function for it to let this work
    def update_img(self):
        threading.Thread(target=self.update_img_thread()).start()



    #\ update image thread to call the finction again by using after function
    def update_img_thread(self):
        if (self.init_while):
            #\ blending the picture in another thread
            threading.Thread(target=self.blending_img()).start()

        #\ for init
        else:
            self.tk_image  = tk.PhotoImage(file = Index.Image_path + "\\dragonfly_picture.gif")
            self.init_while = True
            self.imglabel.config(image=self.tk_image)

        #\ rerun the function every XXX second
        self.after(Index.img_change_time*1000, self.update_img_thread)



# Driver Code
if __name__ == '__main__':
    app = tkinterApp()
    app.geometry(Index.Login_geometry)

    #\ set the title
    app.title(" Please Login")

    #\ Specify the style1
    style = ThemedStyle(app)
    style.set_theme("xpnative")

    #\ Let the main loop running
    app.mainloop()