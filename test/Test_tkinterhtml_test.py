import tkinter as tk
from tkinter import messagebox
from cefpython3 import cefpython as cef
import threading
import sys


'''def test_thread(frame):
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), rect)
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='http://www.google.com')
    cef.MessageLoop()
    cef.Shutdown()


def on_closing():
    print('closing')
    root.destroy()


root = tk.Tk()
root.geometry('800x600')
root.protocol('WM_DELETE_WINDOW', on_closing)
frame = tk.Frame(root, bg='blue', height=200)
frame2 = tk.Frame(root, bg='white', height=200)
frame.pack(side='top', fill='x')
frame2.pack(side='top', fill='x')

tk.Button(frame2, text='Exit', command=on_closing).pack(side='left')
tk.Button(frame2, text='Show something',
          command=lambda: messagebox.showinfo('TITLE', 'Shown something')).pack(side='right')

rect = [0, 0, 800, 200]
print('browser: ', rect[2], 'x', rect[3])

thread = threading.Thread(target=test_thread, args=(frame,))
thread.start()

root.mainloop()'''

##########################################################################################
'''# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.

from cefpython3 import cefpython as cef
import platform
import sys


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="https://www.google.com/",
                          window_title="Hello World!")
    cef.MessageLoop()
    cef.Shutdown()


def check_versions():
    ver = cef.GetVersion()
    print("[hello_world.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[hello_world.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[hello_world.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[hello_world.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


if __name__ == '__main__':
    main()'''


#######################################################################################!/usr/bin/env python
# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.

'''from cefpython3 import cefpython as cef
import platform
import sys
import tkinter as tk


def open_link(url):
    print(url)
    root.destroy()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url=url,
        window_title=url)
    cef.MessageLoop()
    main()

def main():
    global root
    root = tk.Tk()
    root.geometry("400x100")
    l = tk.Label(root, text="Press Enter to browse Internet", fg="blue", font="Arial 20")
    l.pack(fill=tk.X)
    v = tk.StringVar()
    e = tk.Entry(root, textvariable=v, font="Arial 14")
    e.pack(fill=tk.X)
    v.set("https://www.google.com/")
    e.focus()
    e.bind("<Return>", lambda x: open_link(e.get()))
    root.mainloop()
    cef.Shutdown()


if __name__ == '__main__':
    main()
'''


###################################################################################
from cefpython3 import cefpython as cef
import platform
import sys
import tkinter as tk
import threading

def htmlfunction(frame):
    print("this is the html function")
    rect = [0, 0, 960, 540]
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), rect)
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='http://www.google.com')
    cef.MessageLoop()
    cef.Shutdown()


def b1funciton(frame, t):
    t.start()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1800x1080")
    f1 = tk.Frame(root, bg = "blue", height=200)
    f2 = tk.Frame(root, bg = "green", height=800)
    f1.pack(side='top', fill='x')
    f2.pack(side='top', fill='x')
    thread = threading.Thread(target=htmlfunction, args=(f2,))
    b1 = tk.Button(f1, text="Button", command=lambda: b1funciton(f2, thread))
    b1.pack()
    root.mainloop()



