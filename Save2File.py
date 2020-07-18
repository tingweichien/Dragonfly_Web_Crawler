# reference:
# https://stackoverflow.com/questions/28162358/append-a-header-for-csv-file
# https://stackoverflow.com/questions/50701023/insert-new-line-in-csv-at-second-row-via-python
# http://zetcode.com/python/csv/
# https://blog.csdn.net/chuatony/article/details/71436582
# https://www.itread01.com/content/1547720842.html
# https://stackoverflow.com/questions/4897359/output-to-the-same-line-overwriting-previous-output

from tkinter import filedialog
from tkinter import *
import csv
import os.path
from os import path
from Index import *
from Dragonfly import *
import codecs



# state which have been crwal
#"脊紋鼓蟌" "朱環鼓蟌" "棋紋鼓蟌"
# 黃肩洵蟌 黃腹洵蟌
# 芽痣蹣蟌 青紋絲蟌 隱紋絲蟌 長痣絲蟌
# 慧眼弓蜓 岷峨弓蜓 褐面弓蜓 海神弓蜓 耀沂弓蜓 天王弓蜓 黃尾弓蜓 臺灣弓蜓
# 白痣珈蟌 細胸珈蟌 中華珈蟌南臺亞種 中華珈蟌指名亞種
# 短尾幽蟌 短腹幽蟌
# 青黑琵蟌 黃尾琵蟌 環紋琵蟌
# 烏齒樸蟌 朱背樸蟌
# 短痣勾蜓 斑翼勾蜓 褐翼勾蜓 無霸勾蜓
# 
 


# setting
Input_species_famliy = "勾蜓科"
Input_species = "無霸勾蜓"
limit_cnt = 6000
folder = 'Crawl_Data\\' + Species_class_key[Input_species_famliy]
File_name = folder + "\\" + Species_class_key[Input_species_famliy] + Species_key[Input_species] +'.csv'
oldID = 0

print("--Start crawl-- " + Input_species_famliy + " " + Input_species)
print("[folder]: " + folder)




# --main--

# check the file exist or not
file_check = path.exists(current_path + "\\" + File_name)

# get the Old ID
if file_check:
    file_size = os.stat(current_path + "\\" + File_name).st_size
    if not file_size == 0:
        with open(File_name, newline='', errors = "ignore") as F:
            R = csv.reader(F)
            oldData = [line for line in R]
            oldID = oldData[0][0]

# login     
Login_Web(myaccount, mypassword)

# find the total number of the parsing species_input (expect executed one time)
Species_total_num_Dict = Find_species_total_data()


# get the data
Total_num = int(Species_total_num_Dict[Input_species])
[datatmpList, page] = crawl_all_data(Input_species_famliy, Input_species, Total_num, limit_cnt, oldID)

Data = []
for Data_tmp in datatmpList:
    Data.append([Data_tmp.SpeciesFamily,
            Data_tmp.Species,
            Data_tmp.IdNumber,
            Data_tmp.Dates,
            Data_tmp.Times,
            Data_tmp.User,
            Data_tmp.City,
            Data_tmp.Dictrict,
            Data_tmp.Place,
            Data_tmp.Altitude,
            Data_tmp.Latitude,
            Data_tmp.Longitude,
            Data_tmp.Description
            ])

#auto make the directories
newDir = current_path + "\\" + folder
if (not os.path.isdir(newDir)):
    os.mkdir(newDir)



# 'a' stands for append, which can append the new data to old one
with open(File_name, mode='a', newline='', errors = "ignore") as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    # init , for there is no file exists or the file is empty
    if ((not file_check) or (file_size == 0)):
        employee_writer.writerow(CSV_Head)
        employee_writer.writerows(Data)

    # for insert the data to the old one    
    else:
        for i in range(0, len(Data)):
            oldData.insert(i, Data[i])
        employee_writer.writerows(oldData)
      



'''import csv
ToAdd = [["Add1","Add2"],["Add3","Add4"]]
with open('file.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    print(data[1][0])
    for i in range(0,len(ToAdd)):
        data.insert(i+1, ToAdd[i])
with open('file.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(data)'''

