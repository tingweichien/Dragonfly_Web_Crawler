@echo off  
D:  
cd D:\DragonflyData  
call pip install PySimpleGUI
call pip install --upgrade PySimpleGUI
call pip install selenium
call pip install gmplot
call pip install bs4
call pip install requests
call pip install fake-useragent

start pythonw GUI_split.py  
exit  