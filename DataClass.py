from tkinter import *

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



class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User, Latitude, Longitude, Species, Description):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User)
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Species = Species
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

        
