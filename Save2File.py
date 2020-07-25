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
import json

 
def Read_check_File(File_name):
    oldData = []
    oldData_len = 0
    oldID = 0
    file_size = -1 #means no such file
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
                oldData_len = len(oldData) - 1
    return [oldData, oldData_len, oldID, file_check, file_size]
      


def Write2File(File_name, folder, file_check, file_size, CSV_Head, Data, oldData):
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



def writeTotalNum2Json(inputDict, filepath):
    #with open(folder_all_crawl_data + 'Record_Num_each_species.txt', 'w') as outputfile:
    with open(filepath, 'w', encoding='utf-8') as outputfile: 
        json.dump(inputDict, outputfile, ensure_ascii=False, indent = 4)


def ReadTotalNum2Json(filepath):
    try:
        with open(filepath, 'r', errors='ignore') as readfile:
            return json.load(readfile)
    except:
        return []


def checkUpdateSpecies(NewNumberData, filepath):
    Update = []
    OldNumberData = ReadTotalNum2Json(filepath)
    if not OldNumberData == []:
        for key in NewNumberData:
            if key in OldNumberData and OldNumberData[key] < NewNumberData[key]:
                #Update.append([key, NewNumberData[key] - OldNumberData[key]])
                Update.append(key)
    return Update





def Save2File(Input_species_famliy, Input_species, session_S2F, Species_total_num_Dict, File_name, folder):
    if __name__ == '__main__':
        # setting
        oldID = 0
        oldData_len = 0
        file_size = 0
        DataTmpList = []
        oldData = []
        global DataCNT, TotalCount, limit_cnt

        print("\n--Start crawling-- " + Input_species_famliy + " " + Input_species)
        print("[File name]: " + File_name)
        
        # <timing>
        start = time.time()

        [oldData, oldData_len, oldID, file_check, file_size] = Read_check_File(File_name)

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
            print("[Update]: {}, CurrentData: {}, OldData: {}".format(expecting_CNT, Total_num, oldData_len))
            if expecting_CNT <= 0:
                print("No Data need to update~")
                return False
            expecting_page = int(expecting_CNT / data_per_page)  # since it starts form page 0
            renmaind_data_Last_page = expecting_CNT % data_per_page
            pool = Pool(cpus,
                        initializer=init,
                        initargs=(DataCNT,))
            func = partial( crawl_all_data_mp2,
                            session_S2F, Input_species_famliy, Input_species, Total_num, expecting_CNT, expecting_page, renmaind_data_Last_page) # combine the not iterable value
            returnList = pool.map_async(func, list(range(expecting_page + 1)))
            DataCNT_lock = Lock()
            with DataCNT_lock:
                TotalCount += DataCNT.value
                DataCNT.value = 0    
            print("[current total crawl]: {} data".format(TotalCount))

            if TotalCount <= limit_cnt:
                if not (returnList.get() == None or len(returnList.get()) == 0) :
                    DataTmpList = reduce(add, returnList.get())
                else:
                    print("No Data need to update\n")
                    return False
            else:
                print("meet the limit for data counts\n")
                pool.terminate()
                return True   #End the program
        # without multiprocessing
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
        if len(Data) == 0:
            print("No Data need to update")
            return False

        #write the data to file
        Write2File(File_name, folder, file_check, file_size, CSV_Head, Data, oldData)            

        if do_multiprocessing :
            # make sure whe main is finished, subfunctions still keep rolling on             
            pool.close()
            pool.join()
            
        # <timing>
        end = time.time()
        derivation = end - start
        print('Finished crawling data ~  spend: {} min {} s'.format(int(derivation/60), round(derivation%60), 1))



#\ parse family
def parse_family():
    program_stop_check = False
    [Session_S2F, Login_Response_S2F, Login_state_S2F] = Login_Web(myaccount, mypassword)   # login 
    Species_total_num_Dict = Find_species_total_data()  # find the total number of the species_input (expect executed one time)
    Species_in_family_total_num_Dict = {key: Species_total_num_Dict[key] for key in Species_total_num_Dict.keys()
                                                                                    & set(Species_total_num_Dict)}
    Update = checkUpdateSpecies(Species_in_family_total_num_Dict, TotalNumberOfSpecies_filepath)
    writeTotalNum2Json(Species_total_num_Dict, TotalNumberOfSpecies_filepath)
    if len(Update) == 0:
        for species_loop in Species_Name_Group[Species_Family_Name.index(parse_family_name)]:
            folder = 'Crawl_Data\\' + Species_class_key[parse_family_name]
            File_name = folder + "\\" + Species_class_key[parse_family_name] + Species_key[species_loop] + '.csv'
            file_check = path.exists(current_path + "\\" + File_name) # check the file exist or not
            program_stop_check = Save2File(parse_family_name, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
            if program_stop_check:
                return
    else:
        for species_loop in Species_Name_Group[Species_Family_Name.index(parse_family_name)]:
            folder = 'Crawl_Data\\' + Species_class_key[parse_family_name]
            File_name = folder + "\\" + Species_class_key[parse_family_name] + Species_key[species_loop] + '.csv'
            file_check = path.exists(current_path + "\\" + File_name) # check the file exist or not
            if (species_loop in Update) or (not file_check):
                program_stop_check = Save2File(parse_family_name, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                if program_stop_check:
                    return


#\ parse all species
def parse_all():
    program_stop_check = False
    [Session_S2F, Login_Response_S2F, Login_state_S2F] = Login_Web(myaccount, mypassword)   # login 
    Species_total_num_Dict = Find_species_total_data()  # find the total number of the species_input (expect executed one time)
    Update = checkUpdateSpecies(Species_total_num_Dict, TotalNumberOfSpecies_filepath)
    writeTotalNum2Json(Species_total_num_Dict, TotalNumberOfSpecies_filepath)
    if len(Update) == 0:
        for species_family_loop in Species_Family_Name:
            for species_loop in Species_Name_Group[Species_Family_Name.index(species_family_loop)]:
                folder = 'Crawl_Data\\' + Species_class_key[species_family_loop]
                File_name = folder + "\\" + Species_class_key[species_family_loop] + Species_key[species_loop] + '.csv'                    
                program_check = Save2File(species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                if program_stop_check:
                    return
            print("---Finishing crawling {} ---".format(species_family_loop))              
    else:
        for species_family_loop in Species_Family_Name:
            for species_loop in Species_Name_Group[Species_Family_Name.index(species_family_loop)]:
                folder = 'Crawl_Data\\' + Species_class_key[species_family_loop]
                File_name = folder + "\\" + Species_class_key[species_family_loop] + Species_key[species_loop] + '.csv'
                file_check = path.exists(current_path + "\\" + File_name) # check the file exist or not
                if (species_loop in Update) or (not file_check): # if the species is in the update list or the file doesn't exist
                    program_check = Save2File(species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                    if program_stop_check:
                        return                              
            print("---Finishing crawling {} ---".format(species_family_loop))   


#########################################################################
# --main--
if __name__ == '__main__':
    # start timer
    Start = time.time()
    
    if parse_type == 'parse_a_family':          
        parse_family()
    elif parse_type == 'parse_all':  
        parse_all()
    elif parse_type == 'parse_one':
        Save2File(parse_family_name, parse_species_name, None, None)
        print("\n---Finishing crawling {} ---".format(parse_family_name))
    else:
        print("!!!! No parse type define !!!!!")

    #End timer
    End = time.time()
    Time_interval = End - Start
    print("---\nFinished crawling all the data---  Totally spend: {}m {}s".format(int(Time_interval/60), round(Time_interval % 60), 1))
