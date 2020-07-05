## GUI

from tkinter import *
from tkinter.messagebox import *

def show_answer():
    
    Ans = 0
    blank.insert(0, Ans)


main = Tk()
Label(main, text = "account:").grid(row=0)
Label(main, text="password:").grid(row=1)
Label(main, text = "ID:").grid(row=2)
Label(main, text = "The Sum is:").grid(row=3)


account = Entry(main)
password = Entry(main)
ID = Entry(main)
blank = Entry(main)


account.grid(row=0, column=1)
password.grid(row=1, column=1)
ID.grid(row=2, column=)
blank.grid(row=3, column=1)


Button(main, text='Quit', command=main.destroy).grid(row=4, column=0, sticky=W, pady=4)
Button(main, text='Enter', command=show_answer).grid(row=4, column=1, sticky=W, pady=4)

mainloop()