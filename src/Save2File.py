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
import os
import os.path
import Index
import Dragonfly
import DataClass
from functools import reduce
from operator import add
import multiprocessing
import time
import json
import Update_Database
from functools import partial
from typing import List
import Database_function
import chardet
import codecs


TotalSpeciesNumber = 0

#\ Read data from csv file
def Read_check_File(File_name:str):
    oldData = []
    oldData_len = 0
    oldID = 0
    file_size = -1 #means no such file

    #\ check the file exist or not
    file_check = os.path.exists(Index.current_path + "\\" + File_name)

    #\ get the Old ID
    if file_check:
        file_size = os.stat(Index.current_path + "\\" + File_name).st_size
        if not file_size == 0:
            with open(File_name, newline='', errors = "ignore", encoding=DetectFileEncoding(File_name, False)) as F:
                R = csv.reader(F, dialect='excel', skipinitialspace=True)
                oldData = [line for line in R]
                oldID = oldData[0][0]
                oldData_len = len(oldData) - 1
    return [oldData, oldData_len, oldID, file_check, file_size]


#\ Detect the file encoding type
def DetectFileEncoding(File_path:str, return_or_not:bool) -> str:
    """[summary]

    Args:
        File_path (str): file to detect
        return_or_not (bool): (True) to return the detected encoding or (False) to return the default encoding

    Returns:
        str: encoding
    """
    with open(File_path, "rb") as r:
        result = chardet.detect(r.read(10000))
        print(f"[Info] {File_path} is encoding in {result['encoding']} type")
        if return_or_not:
            return result['encoding']
        else:
            return Index.DefaultEncoding


#\ transform the file encoding to certain type
def Encode2SpecificType(File_path:str, target_path:str, Type:str):
    #\ read
    with open(File_path, "r", encoding="cp950") as In_File:
        # R = csv.reader(F, skipinitialspace=True)
        # oldData = [line for line in R]

        #\ write
        with open(target_path, "w", encoding=Type) as Save_File:
            # File_writer = csv.writer(Save_File, delimiter=',')
            # File_writer.writerows(oldData)
            Save_File.write(In_File.read())




#\ write data to csv file
def Write2File(File_path:str, folder:str, file_check:bool, file_size:int, CSV_Header:List[str], Data:list, oldData:list):
    #\ auto make the directories
    newDir = Index.current_path + "\\" + folder
    if (not os.path.isdir(newDir)):
        os.mkdir(newDir)

    #\ 'a' stands for append, which can append the new data to old one
    with open(File_path, mode='w', newline='', errors = "ignore", encoding=DetectFileEncoding(File_path, False)) as Save_File:
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


#\ Update data to CSV database for fixing or adding to current database
#\ if update header then the row_index do not need to specify
#\ @params
#\      File_path   : File path to update
#\      Data        : Data to update
#\      Task        : Task to do
#\      Row_index   : Modify row
#\      Col_index   : Modify column
#\      Content     : Content to update or modify
def Update2File(File_path:str, Data:list, task:str, Row_index:int=None, Col_index:int=None, Content:str=None) -> bool:
    if File_path is None or len(Data) == 0:
        print("[Warning] File_path or Data is None")
        return False

    Update2FileTaskList = ["modify header", "add header", "update content"]
    Flag = False
    if task in Update2FileTaskList:
        with open(File_path, mode='w', newline='', errors = "ignore", encoding=DetectFileEncoding(File_path, False)) as Save_File:
            File_writer = csv.writer(Save_File, skipinitialspace=True)

            #\ switch task
            #\ modify header
            if task == Update2FileTaskList[0]:
                if Col_index != None and Content != None:
                    Data[0][Col_index] = Content
                    File_writer.writerows(Data)
                    print(f"\n[info] Update the header [{Content}] to become new header --> {Data[0]}")
                    Flag = True
            #\ add header and initial the column
            elif task == Update2FileTaskList[1]:
                if Col_index != None and Content != None:
                    #\ add the header
                    Data[0].insert(Col_index, Content)
                    #\ initial this columm
                    for i in range(1,len(Data)):
                        Data[i].insert(Col_index, "")
                    File_writer.writerows(Data)
                    print(f"\n[info] Insert the header [{Content}] to become new header --> {Data[0]}")
                    Flag = True
            #\ update Content
            elif task == Update2FileTaskList[2]:
                if Col_index != None and Row_index != None and Content != None:
                    if (ListIndexValid(Data, Row_index, Col_index)):
                        Data[Row_index][Col_index] = Content
                        File_writer.writerows(Data)
                        print(f"\n[info] Update the data [{Content}] -->  Data[{Row_index}][{Col_index}]")
                        Flag = True
    else :
        print("[warning] No avaliable Update2File task been assign")

    return Flag



#\ Check if the list index is vaild or not
def ListIndexValid(LIST:list, row:int, col:int):
    if row <= len(LIST) :
        if col <= len(LIST[row]) :
            print("list vaild")
            return True
        else :
            print(f"col {col} of list invalid should be less than {len(LIST)}")
            return False
    else :
        print(f"row {row} of list invalid should be less than {len(LIST[row])}")
        return False

#\ write species number to json file
def writeTotalNum2Json(inputDict:dict, filepath:str):
    with open(filepath, 'w', encoding=DetectFileEncoding(filepath, False)) as outputfile:
        json.dump(inputDict, outputfile, ensure_ascii=False, indent = 4) #ident =4 use for pretty print, write inputDict to the outputfile


#\ read json file
def ReadTotalNum2Json(filepath:str):
    global TotalSpeciesNumber
    try:
        with open(filepath, 'r', errors='ignore', encoding=DetectFileEncoding(filepath, False)) as readfile:
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
                    with open("Crawl_Data\\Record_Num_each_species.txt", "r", newline='', errors="ignore", encoding=Index.DefaultEncoding) as js:
                        totalNum = json.load(js)
                    R = list(csv.reader(r))
                    print("Total: " + str(totalNum[spec]))
                    print("lens: " + str(len(R)))
                    with open(Save_File+ ".csv", "w", newline='', errors="ignore", encoding=Index.DefaultEncoding) as w:
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
            with open(filepath, 'w', newline='', errors="ignore", encoding=Index.DefaultEncoding) as w:
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
            self.expecting_CNT = expecting_CNT

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
            pool = multiprocessing.Pool(Index.cpus,
                        initializer=Dragonfly.init,
                        initargs=(Dragonfly.DataCNT,))
            func = partial( Dragonfly.crawl_all_data_mp2,
                            session_S2F,
                            Input_species_famliy,
                            Input_species,
                            expecting_CNT,
                            expecting_page,
                            renmaind_data_Last_page) # combine the not iterable value

            #\ result
            returnList = pool.map_async(func, list(range(expecting_page + 1)))

            #\ Accumulate the counter by lock
            DataCNT_lock = multiprocessing.Lock()
            with DataCNT_lock:
                Dragonfly.TotalCount += Dragonfly.DataCNT.value
                Dragonfly.DataCNT.value = 0

            #\ GUI display
            self.ICurrentNumLabel_text(Dragonfly.TotalCount)
            print("[current total crawl]: {} data".format(Dragonfly.TotalCount))

            #\ check if the total counts over the limit
            #\ to prevent over crawling which will cause heavy load to the web owner
            #\ set the limit yourself in Index.limit_cnt
            if Dragonfly.TotalCount <= Index.limit_cnt:
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
            DataTmpList = Dragonfly.crawl_all_data(Input_species_famliy, Input_species, Total_num, Index.limit_cnt, oldID)


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
    [Session_S2F, _, _] = Dragonfly.Login_Web(Index.myaccount, Index.mypassword)

    #\ find the total number of the species_input (expect for executing one time)
    Species_total_num_Dict = Dragonfly.Find_species_total_data()

    #\ store the items that need to update in this variable
    Update = checkUpdateSpecies(Species_total_num_Dict, Index.TotalNumberOfSpecies_filepath)

    #\ write the total number to json file
    writeTotalNum2Json(Species_total_num_Dict, Index.TotalNumberOfSpecies_filepath)

    #\ GUI display
    self.ICurrentNumLabel_text(0)

    #\ The indicator for how many portion of the update will be, this var is to let the progressbar adjest by how many check button been selected.
    progressbar_portion = self.progressbar_portion_calc()

    #\ if there is no json file, which means parsing at the first time
    if len(Update) == 0:
        for species_family_loop in Index.Species_Family_Name:
            for species_loop in Index.Species_Name_Group[Index.Species_Family_Name.index(species_family_loop)]:
                folder = Index.folder_all_crawl_data + Index.Species_class_key[species_family_loop]
                File_name = folder + "\\" + Index.Species_class_key[species_family_loop] + Index.Species_key[species_loop] + '.csv'
                Save2File(self, species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                self.progressbar.step((100*progressbar_portion["UpdatefWeb_portion"]) / TotalSpeciesNumber)
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
                folder = Index.folder_all_crawl_data + Index.Species_class_key[species_family_loop]
                File_name = folder + "\\" + Index.Species_class_key[species_family_loop] + Index.Species_key[species_loop] + '.csv'

                #\ check the file exist or not
                file_check = os.path.exists(Index.current_path + "\\" + File_name)

                #\ GUI display - progress bar
                self.progressbar.step((100*progressbar_portion["UpdatefWeb_portion"]) / TotalSpeciesNumber)
                self.pbLabel_text()

                #\ if the species is in the update list or the file doesn't exist
                if (species_loop in Update) or (not file_check):
                    ##########################################################################################################
                    Save2File(self, species_family_loop, species_loop, Session_S2F, Species_total_num_Dict, File_name, folder)
                    ##########################################################################################################
                    if program_stop_check:
                        return

            #\ GUI display
            self.IFinishStateLabel_text("---Finishing crawling {} --- ".format(species_family_loop))

    #\ update the file to the clean file which all of the data needs to have LAT and LNG information
    CleanDataTF()


#\ the parsing all function with the GUI effect
def parse_all_dragonfly_data(self):
    print("------------------------------------------------------")
    print("\n[Update] --Start Crawling dragonfly daTa from web--\n")
    self.checkbox_UpdatefWeb["fg"] = self.updating_fg_color
    self.checkbox_UpdatefWeb["bg"] = self.updating_bg_color
    parse_all(self)
    self.checkbox_UpdatefWeb["bg"] = self.finished_bg_color
    print("\n[Update] --Finished Crawling dragonfly daTa from web--\n")
    print("------------------------------------------------------")



#\ read the file from csv database
def ReadFromFile(file:str)->List[DataClass.DetailedTableInfo]:
    ReadFileList = []
    if (os.path.exists(file) == True):
        with open(file, 'r', newline="", errors='ignore', encoding=Index.DefaultEncoding) as r:
            ReadFile = csv.reader(r)
            for line in ReadFile:
                ReadFileList.append(
                    DataClass.DetailedTableInfo(line[2], line[3], line[4], line[6], line[7], line[8], line[9],
                                        line[5], line[10], line[11], line[0], line[1], line[12])
                )
            del ReadFileList[0:1]
            if len(ReadFileList) == 0:
                messagebox.showinfo("info", "No record")
    return ReadFileList







#########################################################################
#\ The main function for updating
#\  1. Update from web and save the dragonfly info to the csv file
#\  2. Update the csv file result to the MySQL database
#\      (1) Update to MySQL database
#\      (2) Update the weather data to MySQL
#\  Some parameters
#\      - Var_MySQL_enable : Update the crawling data from csv to MySQL
#\      - Var_weather_enable :　Update the weather data
#\      - Var_UpdatefWeb_enable : Update the data from web and save to the csv
def savefile(self, parsetype:str, Update_enable:List[bool]):
    # --main--
    if __name__ == 'Save2File':
        #\ start timer
        Start = time.time()

        #\ -- 1. Update the data from web to csv file--
        #\ Checking which of the update option been selected
        _, _, UpdateNewdata = Update_enable
        if UpdateNewdata:
            if parsetype == 'parse_all':
                parse_all_dragonfly_data(self)
            else:
                print("[warning] !!!! No parse type define !!!!!")
        else:
            print("[warning] Not going to Update new data from web !!!!!")


        #\ Build the MySQL connection
        connection_SF = Database_function.create_connection(Index.hostaddress, Index.username, Index.password, Index.DB_name)


        #\ -- 2. Insert to the data base--
        #\      - (1) Update to MySQL database
        # \     - (2) Update the weather data to MySQL
        Update_Database.Update_database(self, connection_SF, Update_enable)


        #\ End timer
        End = time.time()


        #\ GUI display
        self.pbLabel_text()
        Time_interval = End - Start
        self.Update_Block_set_all_to_empty()
        self.progressbar_partial.stop()
        self.IUpdateNumLabel_text(f"--- Finished crawling all the data ---  Totally spend: {int(Time_interval / 60)}m {round(Time_interval % 60)}s")
        print(f"\n--- Finished crawling all the data ---  Totally spend: {int(Time_interval / 60)}m {round(Time_interval % 60)}s" )

        #\ After finishing, force the bar number to 100%
        self.pbVar.set(100)
        self.progressbar_label['text'] = '100%'
        self.progressbar.stop()
        self.button_popup['text'] = 'Finish'

        #\ End info message box
        messagebox_Flag = messagebox.showinfo("Finished updating~", "Finished updating the data~")
        if messagebox_Flag:
            self.Save2File_popup_closeWindow()





