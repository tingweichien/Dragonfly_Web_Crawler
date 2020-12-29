#\ save the file to csv
#\ reference:
# https://stackoverflow.com/questions/28162358/append-a-header-for-csv-file
# https://stackoverflow.com/questions/50701023/insert-new-line-in-csv-at-second-row-via-python
# http://zetcode.com/python/csv/
# https://blog.csdn.net/chuatony/article/details/71436582
# https://www.itread01.com/content/1547720842.html
# https://stackoverflow.com/questions/4897359/output-to-the-same-line-overwriting-previous-output
# https://stackoverflow.com/questions/29244286/how-to-flatten-a-2d-list-to-1d-without-using-numpy

from tkinter import messagebox
import csv
import os.path
from os import path
import Index
from Dragonfly import *
from functools import reduce
from operator import add
from multiprocessing import Process, Value, Pool
import time
import json
from Database_function import *


TotalSpeciesNumber = 0

# read data from csv file
def Read_check_File(File_name:str):
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
def Write2File(File_path:str, folder:str, file_check:bool, file_size:int, CSV_Header:List[str], Data:list, oldData:list):
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
            print("\n[write type]: First write")

        #\ for inserting the data into the old one
        else:
            for i in range(0, len(Data)):
                oldData.insert(i+1, Data[i])
            File_writer.writerows(oldData)
            print('\n[write type]: Insert')



#\ write species number to json file
def writeTotalNum2Json(inputDict:dict, filepath:str):
    with open(filepath, 'w', encoding='utf-8') as outputfile:
        json.dump(inputDict, outputfile, ensure_ascii=False, indent = 4) #ident =4 use for pretty print, write inputDict to the outputfile


#\ read json file
def ReadTotalNum2Json(filepath:str):
    global TotalSpeciesNumber
    try:
        with open(filepath, 'r', errors='ignore', encoding='utf-8') as readfile:
            return_dict = json.load(readfile)
            TotalSpeciesNumber = len(return_dict)
            return return_dict
    except:
        return []



#\ check if there is any species need to be update by comparing the new species number in the web with old Snumber from json file
def checkUpdateSpecies(NewNumberData:dict, filepath:str)->list:
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
            print(Save_File)
            #print(spec)
            if os.path.exists(Save_File+ ".csv"):
                with open(Save_File + ".csv", "r", newline='', errors="ignore") as r:
                    with open("Crawl_Data\\Record_Num_each_species.txt", "r", newline='', errors="ignore", encoding='utf-8') as js:
                        totalNum = json.load(js)
                    R = list(csv.reader(r))
                    print("Total: " + str(totalNum[spec]))
                    print("lens: " + str(len(R)))
                    with open(Save_File+ ".csv", "w", newline='', errors="ignore") as w:
                        for read in R:
                            if (not len(read[0]) == 0) and (not read[2] in [data[2] for data in Data]):
                                Data.append(read)
                        print("will write {} data\n".format(len(Data)))
                        File_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                        File_writer.writerows(Data)
                        Data = []



#\ transfer to clear data without dataa that has no latitude and longitutde information
def CleanDataTF(*args):
    print("Transferring to the clean data~")
    for name in Index.Species_Family_Name:
        folder = Index.current_path + "\\Crawl_Data_clean\\" + Index.Species_class_key[name]
        os.makedirs(folder, exist_ok=True)
        for species in Index.Species_Name_Group[Index.Species_Family_Name.index(name)]:
            filepath = folder + "\\" + Index.Species_class_key[name] + Index.Species_key[species] + "_clean.csv"
            oldfilepath = ".\\Crawl_Data\\" + Index.Species_class_key[name] + "\\" +Index.Species_class_key[name] + Index.Species_key[species] + ".csv"
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

            #\ write to the file
            with open(filepath, 'w', newline='', errors="ignore") as w:
                File_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                File_writer.writerow(Index.CSV_Head)
                File_writer.writerows(newData)



#\ main program
#\ 1.get the data by web crawler by single or multi processing
#\ 2.write to the csv file
def Save2File(self, Input_species_famliy:str, Input_species:str, session_S2F, Species_total_num_Dict:dict, File_name:str, folder:str)->bool:
    if __name__ == 'Save2File':
        #\ setting
        oldID = 0
        oldData_len = 0
        file_size = 0
        DataTmpList = []
        oldData = []
        global DataCNT, TotalCount

        #\ For displaying in GUI
        self.INameLabel_text(Input_species_famliy, Input_species)
        print("\n--Start crawling-- " + Input_species_famliy + " " + Input_species)
        self.IFileNameLabel_text(File_name)
        print("[File name]: " + File_name)

        #\ <timing>
        start = time.time()

        #\ Read the old data
        [oldData, oldData_len, oldID, file_check, file_size] = Read_check_File(File_name)

        #\ get the total data number
        Total_num = int(Species_total_num_Dict[Input_species])

        #\ choose to do the multiprocessing or not
        if Index.do_multiprocessing :

            #\ get the total number of data need to be update ot crawl
            expecting_CNT = Total_num - oldData_len

            #\ GUI display
            self.IUpdateNumLabel_text("[Update]: {}, CurrentData: {}, OldData: {}".format(expecting_CNT, Total_num, oldData_len))

            #\ check if the expecting update number is zero, which the don't need to update
            if expecting_CNT <= 0:
                self.IStateLabel_text("No Data need to update~")
                print("[warning] No Data need to update~")
                return False

            #\ change page every ten counts
            expecting_page = int(expecting_CNT / Index.data_per_page)

            #\ since it starts form page 0, control the counter within the range 0~10 in each page
            renmaind_data_Last_page = expecting_CNT % Index.data_per_page

            #\ Multi-processing pool
            pool = Pool(Index.cpus,
                        initializer=init,
                        initargs=(DataCNT,))
            func = partial( crawl_all_data_mp2,
                            session_S2F,
                            Input_species_famliy,
                            Input_species,
                            expecting_CNT,
                            expecting_page,
                            renmaind_data_Last_page) # combine the not iterable value

            #\ result
            returnList = pool.map_async(func, list(range(expecting_page + 1)))

            #\ Accumulate the counter by lock
            DataCNT_lock = Lock()
            with DataCNT_lock:
                TotalCount += DataCNT.value
                DataCNT.value = 0

            #\ GUI display
            self.ICurrentNumLabel_text(TotalCount)
            print("[current total crawl]: {} data".format(TotalCount))

            #\ check if the total counts over the limit
            #\ to prevent over crawling which will cause heavy load to the web owner
            #\ set the limit yourself in Index.limit_cnt
            if TotalCount <= Index.limit_cnt:
                if not (len(returnList.get()) == 0) :
                    #\ The function tools "reduce(add, list_args)" will add all the element in the list_args and output the final sum
                    DataTmpList = reduce(add, returnList.get())
                else:
                    print("No Data need to update\n")
                    return False
            else:
                self.IStateLabel_text("!!!Meet the limit for data counts!!!!")
                print("[warning] !!!Meet the limit for data counts!!!!\n")
                pool.terminate()
                return True  #\End the program

        #\ without multiprocessing
        #\ singal thread and singal process
        else:
            DataTmpList = crawl_all_data(Input_species_famliy, Input_species, Total_num, Index.limit_cnt, oldID)

        #\ reformat the data
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

        #\ check if there is data need to update
        if len(Data) == 0:
            self.IStateLabel_text("No Data need to update")
            print("[warning] No Data need to update")
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

        #\ GUI display
        self.IStateLabel_text(f"Finished crawling data ~  spend: {int(derivation/60)}min {round(derivation%60)}s") #\print('Finished crawling data ~  spend: {} min {} s'.format(int(derivation/60), round(derivation%60), 1))



#\ parse all species
def parse_all(self):
    program_stop_check = False

    #\ login
    [Session_S2F, _, _] = Login_Web(Index.myaccount, Index.mypassword)

    #\ find the total number of the species_input (expect for executing one time)
    Species_total_num_Dict = Find_species_total_data()

    #\ store the items that need to update in this variable
    Update = checkUpdateSpecies(Species_total_num_Dict, Index.TotalNumberOfSpecies_filepath)

    #\ write the total number to json file
    writeTotalNum2Json(Species_total_num_Dict, Index.TotalNumberOfSpecies_filepath)

    #\ GUI display
    self.ICurrentNumLabel_text(0)

    #\ if there is no json file, which means parsing at the first time
    if len(Update) == 0:
        for species_family_loop in Index.Species_Family_Name:
            for species_loop in Index.Species_Name_Group[Index.Species_Family_Name.index(species_family_loop)]:
                folder = 'Crawl_Data\\' + Index.Species_class_key[species_family_loop]
                File_name = folder + "\\" + Index.Species_class_key[species_family_loop] + Index.Species_key[species_loop] + '.csv'
                Save2File(self, species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                self.progressbar.step(100 / TotalSpeciesNumber)
                self.pbLabel_text()
                if program_stop_check:
                    return

            #\ GUI display
            self.IFinishStateLabel_text("---Finishing crawling {} --- ".format(species_family_loop))

    #\ pasring for the second times, after the json file been created
    else:
        for species_family_loop in Index.Species_Family_Name:
            for species_loop in Index.Species_Name_Group[Index.Species_Family_Name.index(species_family_loop)]:

                #\ file to write to
                folder = 'Crawl_Data\\' + Index.Species_class_key[species_family_loop]
                File_name = folder + "\\" + Index.Species_class_key[species_family_loop] + Index.Species_key[species_loop] + '.csv'

                #\ check the file exist or not
                file_check = path.exists(Index.current_path + "\\" + File_name)

                #\ GUI display - progress bar
                self.progressbar.step(100 / TotalSpeciesNumber)
                self.pbLabel_text()

                #\ if the species is in the update list or the file doesn't exist
                if (species_loop in Update) or (not file_check):
                    Save2File(self, species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                    if program_stop_check:
                        return

            #\ GUI display
            self.IFinishStateLabel_text("---Finishing crawling {} --- ".format(species_family_loop))

    #\ update the file to the clean file which all of the data needs to have LAT and LNG information
    CleanDataTF()




#\ read the file from csv database
def ReadFromFile(file:str)->List[DetailedTableInfo]:
    ReadFileList = []
    if (os.path.exists(file) == True):
        with open(file, 'r', newline="", errors='ignore') as r:
            ReadFile = csv.reader(r)
            for line in ReadFile:
                ReadFileList.append(
                    DetailedTableInfo(line[2], line[3], line[4], line[6], line[7], line[8], line[9],
                                        line[5], line[10], line[11], line[0], line[1], line[12])
                )
            del ReadFileList[0:1]
            if len(ReadFileList) == 0:
                messagebox.showinfo("info", "No record")
    return ReadFileList



#########################################################################
#\ select the parsing type : all family or one
def savefile(self, parsetype:str, Update_enable:List[bool]):
    # --main--
    if __name__ == 'Save2File':
        #\ start timer
        Start = time.time()

        _, _, UpdateNewdata = Update_enable
        if UpdateNewdata:
            if parsetype == 'parse_all':
                parse_all(self)
            else:
                print("[warning] !!!! No parse type define !!!!!")
        else:
            print("[warning] Not going to Update new data from web !!!!!")


        #\ Build the MySQL connection
        print("start writing to the MySQL database")
        connection_SF = create_connection(Index.hostaddress, Index.username, Index.password, Index.DB_name)


        #\ also insert to the data base
        Update_database(self, connection_SF, Update_enable)


        #\ End timer
        End = time.time()


        #\ GUI display
        self.pbLabel_text()
        Time_interval = End - Start
        self.set_all_to_empty()
        self.IUpdateNumLabel_text(f"--- Finished crawling all the data ---  Totally spend: {int(Time_interval / 60)}m {round(Time_interval % 60)}s")
        print(f"\n--- Finished crawling all the data ---  Totally spend: {int(Time_interval / 60)}m {round(Time_interval % 60)}s" )


