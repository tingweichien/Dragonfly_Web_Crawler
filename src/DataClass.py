try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

# Data class for the simplify imfomation
class simplifyTableInfo:
    def __init__(self, IdNumber:str="", Dates:str="", Times:str="", City:str="", District:str="", Place:str="",
                Altitude:str="", User:str=""):
        self.IdNumber = IdNumber
        self.Dates = Dates
        self.Times = Times
        self.City = City
        self.District = District
        self.Place = Place
        self.Altitude = Altitude
        self.User = User

    def __str__(self):
        return ('\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [District]: ' + self.District +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User)


# Data class for DetailedTable infomation
class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber:str="", Dates:str="", Times:str="", City:str="", District:str="", Place:str="",
                Altitude:str="", User:str="", Latitude:str="", Longitude:str="", SpeciesFamily:str="",
                Species:str="", Description:str="", weather=None):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, District, Place, Altitude, User)
        self.Latitude       = Latitude
        self.Longitude      = Longitude
        self.SpeciesFamily  = SpeciesFamily
        self.Species        = Species
        self.Description    = Description
        self.weather        = weather
    def __str__(self):
        '''
        return (super(DetailedTableInfo, self).__str__()+
                '\t[Latitude]: ' + self.Latitude +
                '\t[Longitude]: ' + self.Longitude +
                '\t[Species]: ' + self.Species +
                '\t[Description]: ' + self.Description)
        '''
        print(  '\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [District]: ' + self.District +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User+
                '  [Latitude]: ' + self.Latitude +
                '  [Longitude]: ' + self.Longitude +
                '  [SpeciesFamily]: ' + self.SpeciesFamily +
                '  [Species]: ' + self.Species +
                '  [Description]: ' + self.Description +
                '  [weather]: ' + self.weather) # type: ignore


# table class for tk GUI
# reference : https://www.geeksforgeeks.org/create-table-using-tkinter/
class Table:
    def __init__(self, root, list, row_start, column_start):
        for i in range(row_start, len(list)):
            for j in range(column_start, len(list[0])):
                self.e = tk.Entry(root, width=20, fg='blue', font=('Arial', 16, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, list[i][j])



# since tk doesnt have tooltip so use this thied party Method
# reference: https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info', window_x = 25, window_y = -23):
        self.widget = widget
        self.text = text
        self.window_x = window_x
        self.window_y = window_y
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.window_x
        y += self.widget.winfo_rooty() + self.window_y  #use minus to make the infobox shown above the cursor
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background='white', relief='solid', borderwidth=1,
                       font=("times", "10", "normal"))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

