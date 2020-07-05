## GUI

from tkinter import *
from tkinter.messagebox import *
from Dragonfly import DataCrawler

def show_answer():
    [Output_LNG, Output_LAT] = DataCrawler(account.get(), password.get(), ID.get()) 
    blank_LNG.insert(0, Output_LNG)
    blank_LAT.insert(0, Output_LAT)
    

main = Tk()
Label(main, text = "account:").grid(row=0)
Label(main, text="password:").grid(row=1)
Label(main, text = "ID:").grid(row=2)
Label(main, text="The Longitude is:").grid(row=3)
Label(main, text="The Lateral is:").grid(row=4)


account = Entry(main)
password = Entry(main)
ID = Entry(main)
blank_LNG = Entry(main)
blank_LAT = Entry(main)


account.grid(row=0, column=1)
password.grid(row=1, column=1)
ID.grid(row=2, column=1)
blank_LNG.grid(row=3, column=1)
blank_LAT.grid(row=4, column=1)


Button(main, text='Quit', command=main.destroy).grid(row=5, column=0, sticky=W, pady=4)
Button(main, text='Enter', command=show_answer).grid(row=5, column=1, sticky=W, pady=4)

mainloop()