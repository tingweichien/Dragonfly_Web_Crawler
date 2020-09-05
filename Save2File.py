#\ save the file to csv
#\ reference:
# https://stackoverflow.com/questions/28162358/append-a-header-for-csv-file
# https://stackoverflow.com/questions/50701023/insert-new-line-in-csv-at-second-row-via-python
# http://zetcode.com/python/csv/
# https://blog.csdn.net/chuatony/article/details/71436582
# https://www.itread01.com/content/1547720842.html
# https://stackoverflow.com/questions/4897359/output-to-the-same-line-overwriting-previous-output
# https://stackoverflow.com/questions/29244286/how-to-flatten-a-2d-list-to-1d-without-using-numpy

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import csv
import os.path
from os import path
#from Index import *
import Index
from Dragonfly import *
import codecs
from functools import reduce
from operator import add
from multiprocessing import Process, Value, Pool
import time
import json

TotalSpeciesNumber = 0

# read data from csv file
def Read_check_File(File_name):
    oldData = []
    oldData_len = 0
    oldID = 0
    file_size = -1 #means no such file
    # check the file exist or not
    file_check = path.exists(Index.current_path + "\\" + File_name)

    # get the Old ID
    if file_check:
        file_size = os.stat(Index.current_path + "\\" + File_name).st_size
        if not file_size == 0:
            with open(File_name, newline='', errors = "ignore") as F:
                R = csv.reader(F)
                oldData = [line for line in R]
                oldID = oldData[0][0]
                oldData_len = len(oldData) - 1
    return [oldData, oldData_len, oldID, file_check, file_size]


#\ write data to csv file
def Write2File(File_path, folder, file_check, file_size, CSV_Header, Data, oldData):
    #\ auto make the directories
    newDir = Index.current_path + "\\" + folder
    if (not os.path.isdir(newDir)):
        os.mkdir(newDir)

    #\ 'a' stands for append, which can append the new data to old one
    with open(File_path, mode='w', newline='', errors = "ignore") as Save_File:
        File_writer = csv.writer(Save_File, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # init , for there is no file exists or the file is empty
        if ((not file_check) or (file_size == 0)):
            File_writer.writerow(CSV_Header)
            File_writer.writerows(Data)
            #print("\n[write type]: First write")

        #\ for inserting the data into the old one
        else:
            for i in range(0, len(Data)):
                oldData.insert(i+1, Data[i])
            File_writer.writerows(oldData)
            #print('\n[write type]: Insert')


#\ write species number to json file
def writeTotalNum2Json(inputDict, filepath):
    with open(filepath, 'w', encoding='utf-8') as outputfile:
        json.dump(inputDict, outputfile, ensure_ascii=False, indent = 4) #ident =4 use for pretty print, write inputDict to the outputfile

#\ read json file
def ReadTotalNum2Json(filepath):
    global TotalSpeciesNumber
    try:
        with open(filepath, 'r', errors='ignore', encoding='utf-8') as readfile:
            return_dict = json.load(readfile)
            TotalSpeciesNumber = len(return_dict)
            return return_dict
    except:
        return []

#\ check if there is any species need to be update by comparing the new species number in the web with old Snumber from json file
def checkUpdateSpecies(NewNumberData, filepath):
    Update = []
    OldNumberData = ReadTotalNum2Json(filepath)
    if not OldNumberData == []:
        for key in NewNumberData:
            if key in OldNumberData and OldNumberData[key] < NewNumberData[key]:
                Update.append(key)
    return Update

#\ remove the empty data and duplicate data in csv database
def removeEmpty():
    Data = []
    for spec_family in Index.Species_Family_Name:
        for spec in Index.Species_Name_Group[Index.Species_Family_Name.index(spec_family)]:
            Save_File = "Crawl_Data\\" + Index.Species_class_key[spec_family] + "\\" + Index.Species_class_key[spec_family] + Index.Species_key[spec]
            #print(Save_File)
            #print(spec)
            if os.path.exists(Save_File+ ".csv"):
                with open(Save_File + ".csv", "r", newline='', errors="ignore") as r:
                    with open("Crawl_Data\\Record_Num_each_species.txt", "r", newline='', errors="ignore", encoding='utf-8') as js:
                        totalNum = json.load(js)
                    R = list(csv.reader(r))
                    #print("Total: " + str(totalNum[spec]))
                    #print("lens: " + str(len(R)))
                    with open(Save_File+ ".csv", "w", newline='', errors="ignore") as w:
                        for read in R:
                            if (not len(read[0]) == 0) and (not read[2] in [data[2] for data in Data]):
                                Data.append(read)
                        #print("will write {} data\n".format(len(Data)))
                        File_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                        File_writer.writerows(Data)
                        Data = []


#\ main program
def Save2File(self, Input_species_famliy, Input_species, session_S2F, Species_total_num_Dict, File_name, folder):
    if __name__ == 'Save2File':
    #if __name__ == '__main__':
        # setting
        oldID = 0
        oldData_len = 0
        file_size = 0
        DataTmpList = []
        oldData = []
        global DataCNT, TotalCount


        self.INameLabel_text(Input_species_famliy, Input_species)#print("\n--Start crawling-- " + Input_species_famliy + " " + Input_species)

        self.IFileNameLabel_text(File_name)#print("[File name]: " + File_name)

        # <timing>
        start = time.time()

        [oldData, oldData_len, oldID, file_check, file_size] = Read_check_File(File_name)

        # make sure the loop method will not redo this again and again
        if Index.parse_type == 'parse_one':
            # login
            [session_S2F, Login_Response_S2F, Login_state_S2F] = Login_Web(myaccount, mypassword)

            # find the total number of the species_input (expect executed one time)
            Species_total_num_Dict = Find_species_total_data()


        # get the data
        Total_num = int(Species_total_num_Dict[Input_species])

        # choose to do the multiprocessing or not
        if Index.do_multiprocessing :
            expecting_CNT = Total_num - oldData_len  # get the total number of data need to be update ot crawl

            self.IUpdateNumLabel_text("[Update]: {}, CurrentData: {}, OldData: {}".format(expecting_CNT, Total_num, oldData_len))#print("[Update]: {}, CurrentData: {}, OldData: {}".format(expecting_CNT, Total_num, oldData_len))
            if expecting_CNT <= 0:
                self.IStateLabel_text("No Data need to update~")#print("No Data need to update~")
                return False

            expecting_page = int(expecting_CNT / Index.data_per_page)  # since it starts form page 0
            renmaind_data_Last_page = expecting_CNT % Index.data_per_page
            pool = Pool(Index.cpus,
                        initializer=init,
                        initargs=(DataCNT,))
            func = partial( crawl_all_data_mp2,
                            session_S2F, Input_species_famliy, Input_species, Total_num, expecting_CNT, expecting_page, renmaind_data_Last_page) # combine the not iterable value
            returnList = pool.map_async(func, list(range(expecting_page + 1)))
            DataCNT_lock = Lock()
            with DataCNT_lock:
                TotalCount += DataCNT.value
                DataCNT.value = 0


            self.ICurrentNumLabel_text(TotalCount)#print("[current total crawl]: {} data".format(TotalCount))

            #\ check if the total counts over the limit
            if TotalCount <= Index.limit_cnt:
                if not (len(returnList.get()) == 0) :
                    DataTmpList = reduce(add, returnList.get())
                else:
                    #print("No Data need to update\n")
                    return False
            else:

                self.IStateLabel_text("!!!Meet the limit for data counts!!!!")#print("!!!Meet the limit for data counts!!!!\n")
                pool.terminate()
                return True  #End the program

        # without multiprocessing
        else:
            [DataTmpList, page] = crawl_all_data(Input_species_famliy, Input_species, Total_num, Index.limit_cnt, oldID)


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

            self.IStateLabel_text("No Data need to update")#print("No Data need to update")
            return False

        #\ write the data to file
        Write2File(File_name, folder, file_check, file_size, Index.CSV_Head, Data, oldData)

        if Index.do_multiprocessing :
            #\ make sure whe main is finished, subfunctions still keep rolling on
            pool.close()
            pool.join()

        #\ <timing>
        end = time.time()
        derivation = end - start

        self.IStateLabel_text('Finished crawling data ~  spend: {} min {} s'.format(int(derivation/60), round(derivation%60), 1))#print('Finished crawling data ~  spend: {} min {} s'.format(int(derivation/60), round(derivation%60), 1))


#\ parse all species
def parse_all(self):
    program_stop_check = False
    [Session_S2F, Login_Response_S2F, Login_state_S2F] = Login_Web(myaccount, mypassword)   # login
    Species_total_num_Dict = Find_species_total_data()  # find the total number of the species_input (expect executed one time)
    Update = checkUpdateSpecies(Species_total_num_Dict, Index.TotalNumberOfSpecies_filepath)
    writeTotalNum2Json(Species_total_num_Dict, Index.TotalNumberOfSpecies_filepath)
    self.ICurrentNumLabel_text(0)
    #\ if there is no json file at the first time
    if len(Update) == 0:
        for species_family_loop in Index.Species_Family_Name:
            for species_loop in Index.Species_Name_Group[Index.Species_Family_Name.index(species_family_loop)]:
                folder = 'Crawl_Data\\' + Index.Species_class_key[species_family_loop]
                File_name = folder + "\\" + Index.Species_class_key[species_family_loop] + Index.Species_key[species_loop] + '.csv'
                program_check = Save2File(self, species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                self.progressbar.step(100 / TotalSpeciesNumber)
                self.pbLabel_text()
                if program_stop_check:
                    return

            self.IFinishStateLabel_text("---Finishing crawling {} --- ".format(species_family_loop))#print("\n---Finishing crawling {} --- ".format(species_family_loop))
    else:
        for species_family_loop in Index.Species_Family_Name:
            for species_loop in Index.Species_Name_Group[Index.Species_Family_Name.index(species_family_loop)]:
                folder = 'Crawl_Data\\' + Index.Species_class_key[species_family_loop]
                File_name = folder + "\\" + Index.Species_class_key[species_family_loop] + Index.Species_key[species_loop] + '.csv'
                file_check = path.exists(Index.current_path + "\\" + File_name) # check the file exist or not
                self.progressbar.step(100 / TotalSpeciesNumber)
                self.pbLabel_text()
                if (species_loop in Update) or (not file_check): # if the species is in the update list or the file doesn't exist
                    program_check = Save2File(self, species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                    if program_stop_check:
                        return

            self.IFinishStateLabel_text("---Finishing crawling {} --- ".format(species_family_loop))#print("\n---Finishing crawling {} --- ".format(species_family_loop))


#\ read the file from csv database
def ReadFromFile(file):
    ReadFileList = []
    if (os.path.exists(file) == True):
        with open(file, 'r', newline="", errors='ignore') as r:
            ReadFile = csv.reader(r)
            for line in ReadFile:
                ReadFileList.append(
                    DetailedTableInfo(line[2],line[3],line[4], line[6],line[7],line[8],line[9], line[5], line[10], line[11], line[0], line[1], line[12])
                )
            del ReadFileList[0:1]
            if len(ReadFileList) == 0:
                messagebox.showinfo("info", "No record")
    return ReadFileList

#\ transfer to clear data with no data that has no latitude and longitutde information
def CleanDataTF(*args):
    for name in Index.Species_Family_Name:
        folder = Index.current_path + "\\Crawl_Data_clean\\" + Index.Species_class_key[name]
        os.makedirs(folder, exist_ok=True)
        for species in Index.Species_Name_Group[Index.Species_Family_Name.index(name)]:
            filepath = folder + "\\" + Index.Species_class_key[name] + Index.Species_key[species] + "_clean.csv"
            oldfilepath = ".\Crawl_Data\\" + Index.Species_class_key[name] + "\\" +Index.Species_class_key[name] + Index.Species_key[species] + ".csv"
            old = ReadFromFile(oldfilepath)
            newData = []
            for row in old:
                if not (row.Latitude == '' and row.Longitude == ''):
                    newData.append([row.SpeciesFamily,
                                    row.Species,
                                    row.IdNumber,
                                    row.Times,
                                    row.Dates,
                                    row.User,
                                    row.City,
                                    row.Dictrict,
                                    row.Place,
                                    row.Altitude,
                                    row.Latitude,
                                    row.Longitude,
                                    row.Description
                                    ])

            with open(filepath, 'w', newline='', errors="ignore") as w:
                File_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                File_writer.writerow(Index.CSV_Head)
                File_writer.writerows(newData)




#########################################################################
#\ select the parsing type : all family or one
def savefile(self, parsetype):
    # --main--
    if __name__ == 'Save2File':
        # start timer
        Start = time.time()

        if parsetype == 'parse_all':
            parse_all(self)
        elif parsetype == 'parse_one':
            Save2File(self, Index.parse_one_family_name, Index.parse_one_species_name, None, None)
            #print("\n---Finishing crawling {} ---".format(parse_family_name))
        else:
            print("!!!! No parse type define !!!!!")

        #\ End timer
        End = time.time()
        self.pbLabel_text()
        Time_interval = End - Start
        self.set_all_to_empty()
        self.IUpdateNumLabel_text("--- Finished crawling all the data ---  Totally spend: {}m {}s".format(int(Time_interval / 60), round(Time_interval % 60), 1))
        #print("\n--- Finished crawling all the data ---  Totally spend: {}m {}s".format(int(Time_interval / 60), round(Time_interval % 60), 1))


