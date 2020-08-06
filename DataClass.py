from tkinter import *
try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

# Data class for the simplify imfomation
class simplifyTableInfo:
    def __init__(self, IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User):
        self.IdNumber = IdNumber
        self.Dates = Dates
        self.Times = Times
        self.City = City
        self.Dictrict = Dictrict
        self.Place = Place
        self.Altitude = Altitude
        self.User = User

    def __str__(self):

        return ('\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [Dictrict]: ' + self.Dictrict +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User)

# Data class for DetailedTable infomation
class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User, Latitude, Longitude, SpeciesFamily ,Species, Description):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User)
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Species = Species
        self.SpeciesFamily = SpeciesFamily
        self.Description = Description
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
                '  [Dictrict]: ' + self.Dictrict +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User+
                '  [Latitude]: ' + self.Latitude +
                '  [Longitude]: ' + self.Longitude +
                '  [Species]: ' + self.Species +
                '  [SpeciesFamily]: ' + self.SpeciesFamily +
                '  [Description]: ' + self.Description)

# table class for tk GUI
# reference : https://www.geeksforgeeks.org/create-table-using-tkinter/
class Table:
    def __init__(self, root, list, row_start, column_start):
        for i in range(row_start, len(list)):
            for j in range(column_start, len(list[0])):
                self.e = Entry(root, width=20, fg='blue', font=('Arial', 16, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, list[i][j])


# since tk doesnt have tooltip so use this thied party Method
# reference: https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() - 23  #use minus to make the infobox shown above the cursor
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

