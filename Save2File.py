# reference:
# https://stackoverflow.com/questions/28162358/append-a-header-for-csv-file
# https://stackoverflow.com/questions/50701023/insert-new-line-in-csv-at-second-row-via-python
# http://zetcode.com/python/csv/
# https://blog.csdn.net/chuatony/article/details/71436582
# https://www.itread01.com/content/1547720842.html
# https://stackoverflow.com/questions/4897359/output-to-the-same-line-overwriting-previous-output
# https://stackoverflow.com/questions/29244286/how-to-flatten-a-2d-list-to-1d-without-using-numpy


from tkinter import filedialog
from tkinter import *
import csv
import os.path
from os import path
from Index import *
from Dragonfly import *
import codecs
from functools import reduce
from operator import add
from multiprocessing import Process, Value, Pool
import time

# state which have been crwal
#"脊紋鼓蟌" "朱環鼓蟌" "棋紋鼓蟌"
# 黃肩洵蟌 黃腹洵蟌
# 芽痣蹣蟌 青紋絲蟌 隱紋絲蟌 長痣絲蟌
# 慧眼弓蜓 岷峨弓蜓 褐面弓蜓 海神弓蜓 耀沂弓蜓 天王弓蜓 黃尾弓蜓 臺灣弓蜓
# 白痣珈蟌 細胸珈蟌 中華珈蟌南臺亞種 中華珈蟌指名亞種
# 短尾幽蟌 短腹幽蟌
# 青黑琵蟌 黃尾琵蟌 環紋琵蟌 脛蹼琵蟌
# 烏齒樸蟌 朱背樸蟌
# 短痣勾蜓 斑翼勾蜓 褐翼勾蜓 無霸勾蜓
# 丹頂細蟌 藍彩細蟌 針尾細蟌 白粉細蟌 橙尾細蟌 黃腹細蟌 亞東細蟌 朝雲細蟌 昧影細蟌 葦笛細蟌 弓背細蟌 青紋細蟌 紅腹細蟌 蔚藍細蟌 瘦面細蟌
# 國姓春蜓 長唇春蜓 雙角春蜓
 
 




def Save2File(Input_species_famliy, Input_species, session_S2F, Species_total_num_Dict):
    if __name__ == '__main__':
    #if __name__ == '__mp_main__':
        # setting
        limit_cnt = 6000
        folder = 'Crawl_Data\\' + Species_class_key[Input_species_famliy]
        File_name = folder + "\\" + Species_class_key[Input_species_famliy] + Species_key[Input_species] +'.csv'
        oldID = 0
        oldData_len = 0
        DataCNT = Value('i', 0)
        DataTmpList = []

        print("\n--Start crawl-- " + Input_species_famliy + " " + Input_species)
        print("[folder]: " + folder)
        
        # <timing>
        start = time.time()

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
                    oldData_len = len(oldData)-1

        # make sure the loop method will not redo this again and again
        if parse_type == 'parse_one':
            # login     
            [session_S2F, Login_Response_S2F, Login_state_S2F] = Login_Web(myaccount, mypassword)

            # find the total number of the species_input (expect executed one time)
            Species_total_num_Dict = Find_species_total_data()


        # get the data
        Total_num = int(Species_total_num_Dict[Input_species])

        # choose to do the multiprocessing or not
        if do_multiprocessing :
            expecting_CNT = Total_num - oldData_len  # get the total number of data need to be update ot crawl
            expecting_page = int(expecting_CNT / data_per_page)  # since it starts form page 0
            renmaind_data_Last_page = expecting_CNT % data_per_page
            pool = Pool(cpus,
                        initializer=init,
                        initargs=(DataCNT,))
            func = partial( crawl_all_data_mp2,
                            session_S2F, Input_species_famliy, Input_species, Total_num, limit_cnt, expecting_page, renmaind_data_Last_page) # combine the not iterable value
            returnList = pool.map_async(func, list(range(expecting_page + 1)))
            if not len(returnList.get()) == 0:
                DataTmpList = reduce(add, returnList.get())
            else:
                print("No Data need to update\n")
                return 
        else:
            [DataTmpList, page] = crawl_all_data(Input_species_famliy, Input_species, Total_num, limit_cnt, oldID)


        Data = []
        for Data_tmp in DataTmpList:
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
        with open(File_name, mode='a', newline='', errors = "ignore") as Save_File:
            File_writer = csv.writer(Save_File, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            # init , for there is no file exists or the file is empty
            if ((not file_check) or (file_size == 0)):
                File_writer.writerow(CSV_Head)
                File_writer.writerows(Data)

            # for inserting the data into the old one    
            else:
                for i in range(0, len(Data)):
                    oldData.insert(i, Data[i])
                File_writer.writerows(oldData)

        if do_multiprocessing :
            # make sure whe main is finished, subfunctions still keep rolling on             
            pool.close()
            pool.join()
            
        # <timing>
        end = time.time()
        derivation = end - start
        print('Finished crawling data ~ Totally spend: {} min {} s'.format(int(derivation/60), round(derivation%60), 1))



#########################################################################
# --main--
if __name__ == '__main__':
    input_species_famliy = "春蜓科"
    input_species = "國姓春蜓"

    if parse_type == 'parse_a_family':
        Start = time.time()           
        [Session_S2F, Login_Response_S2F, Login_state_S2F] = Login_Web(myaccount, mypassword)   # login 
        Species_total_num_Dict = Find_species_total_data()                                      # find the total number of the species_input (expect executed one time)
        for species_loop in Species_Name_Group[Species_Family_Name.index(input_species_famliy)]:
            Save2File(input_species_famliy, species_loop, Session_S2F, Species_total_num_Dict)
        End = time.time()
        Time_interval = End - Start
        print("\n---Finishing crawling {} ---, totally spend: {}m {}s".format(input_species_famliy, int(Time_interval/60), round(Time_interval % 60), 1))
    elif parse_type == 'parse_all': # not sure
        for species_family_loop in Species_Family_Name:
            for species_loop in Species_Name_Group[Species_Family_Name.index(species_family_loop)]:
                Save2File(species_family_loop, Input_species, None, None)
    elif parse_type == 'parse_one':
        Save2File(input_species_famliy, input_species, None, None)



'''
    if parse_type == 'parse_a_family':  
        parse_family_pool = Pool(cpus)
        function = partial(Save2File, input_species_famliy)
        parse_family_pool.map_async(function, Species_Name_Group[Species_Family_Name.index(input_species_famliy)])
        parse_family_pool.close()
        parse_family_pool.join()
    elif parse_type == 'parse_all': # not sure
        for species_family_loop in Species_Family_Name:
            for species_loop in Species_Name_Group[Species_Family_Name.index(species_family_loop)]:
                Save2File(species_family_loop, Input_species)
    elif parse_type == 'parse_one':
        Save2File(input_species_famliy, input_species)

        '''