


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


# ###################################################################################
# from cefpython3 import cefpython as cef
# import platform
# import sys
# import tkinter as tk
# import threading

# def htmlfunction(frame):
#     print("this is the html function")
#     rect = [0, 0, 960, 540]
#     sys.excepthook = cef.ExceptHook
#     window_info = cef.WindowInfo(frame.winfo_id())
#     window_info.SetAsChild(frame.winfo_id(), rect)
#     cef.Initialize()
#     browser = cef.CreateBrowserSync(window_info, url='http://www.google.com')
#     cef.MessageLoop()
#     cef.Shutdown()


# def b1funciton(frame, t):
#     t.start()

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.geometry("1800x1080")
#     f1 = tk.Frame(root, bg = "blue", height=200)
#     f2 = tk.Frame(root, bg = "green", height=800)
#     f1.pack(side='top', fill='x')
#     f2.pack(side='top', fill='x')
#     thread = threading.Thread(target=htmlfunction, args=(f2,))
#     b1 = tk.Button(f1, text="Button", command=lambda: b1funciton(f2, thread))
#     b1.pack()
#     root.mainloop()


# from tkinter import *

# root = Tk()
# sv = StringVar()

# def callback():
#     print(sv.get())
#     print("change")
#     return True

# e = Entry(root, textvariable=sv, validate="all", validatecommand=callback)
# e.grid()

# root.mainloop()



########################################################################
# import io
# # allows for image formats other than gif
# from PIL import Image, ImageTk
# import tkinter as tk
# from urllib.request import urlopen



# # find yourself a picture on an internet web page you like
# # (right click on the picture, under properties copy the address)
# url = "http://www.google.com/intl/en/images/logo.gif"
# url3="https://i.ibb.co/3mQF3Jt/32585369723-e87b06b042-c.jpg"
# url4="https://i.ibb.co/z5jBfvN/34077780896-32c563c964-c.jpg"
# url5="https://i.ibb.co/G7r55jC/gradonfly-2.jpg"
# url6="https://i.ibb.co/bWTSXdg/gragonfly-3.jpg"
# # or use image previously downloaded to tinypic.com
# #url = "http://i48.tinypic.com/w6sjn6.jpg"
# #url = "http://i50.tinypic.com/34g8vo5.jpg"

# url_list = [url, url3, url4, url5, url6]




# class App():
#     def __init__(self):
#         self.root = tk.Tk()
#         self.counter = 0
#         # put the image on a typical widget
#         self.label = tk.Label(self.root, bg='brown')
#         self.label.pack(padx=5, pady=5)
#         self.update_img()
#         self.root.mainloop()


#     def update_img(self):
#         image_bytes = urlopen(url_list[self.counter % len(url_list)]).read()
#         # internal data file
#         data_stream = io.BytesIO(image_bytes)
#         # open as a PIL image object
#         pil_image = Image.open(data_stream)
#         # optionally show image info
#         # get the size of the image
#         w, h = pil_image.size
#         # split off image file name
#         fname = url_list[self.counter % len(url_list)].split('/')[-1]
#         sf = "{} ({}x{})".format(fname, w, h)
#         self.root.title(sf)
#         # convert PIL image object to Tkinter PhotoImage object
#         pil_image = pil_image.resize((800, 534), Image.ANTIALIAS)
#         self.tk_image = ImageTk.PhotoImage(pil_image)
#         self.label.config(image=self.tk_image)
#         self.counter += 1
#         self.root.after(5*1000, self.update_img)



# app=App()



########################################################################################
try:
  import Tkinter              # Python 2
  import ttk
except ImportError:
  import tkinter as Tkinter   # Python 3
  import tkinter.ttk as ttk


def main():

  root = Tkinter.Tk()
  ttk.Style().theme_use('xpnative') # <--- Change default to whichever theme you want to use.

  ft = ttk.Frame()
  fb = ttk.Frame()

  ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  fb.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

  pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate', phase=20, maximum=50)
  pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
  pb_vd = ttk.Progressbar(fb, orient='vertical', mode='determinate')
  pb_vD = ttk.Progressbar(fb, orient='vertical', mode='indeterminate')

  pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  pb_hD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  pb_vd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)
  pb_vD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)

  pb_hd.start(50)
  pb_hD.start(50)
  pb_vd.start(50)
  pb_vD.start(50)


  root.mainloop()
  


if __name__ == '__main__':
  main()