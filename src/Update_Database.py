import Index
import Database_function
from typing import List
import mysql.connector
from tkinter import messagebox
import csv
import weather_data_class
import Save2File


#\ (1) Auto update the data in csv into DATABASE
#\ (2) contain update weather data
def Update_database(self, connection:mysql.connector, Update_enable:List[bool]):

    #\ INIT the key
    Index.request_cnt = 0
    Index.key_cnt = 0

    #\ create index for this database which list all the species and species family if not exist
    Database_function.create_table(connection, Database_function.create_species_family_table)
    Database_function.create_table(connection, Database_function.create_species_table)

    #\ buld species family table
    # insertquery_SF = "INSERT INTO Species_Family_table (species_family_name) VALUES (%s)"
    # insertdatas_SF = [tuple([SFN]) for SFN in Index.Species_Family_Name]
    # insert_data(connection, insertquery_SF, insertdatas_SF)

    #\ Assign the enable bits
    Update_MySQL, Update_weather, _ = Update_enable

    #\ Start the progress bar and return if non of them been enabled
    if Update_MySQL or Update_weather is True:
        Update_data_updating_GUI(self, Update_enable, "start")
    else:
        return

    #\ Print the Upating info
    update_string = ["updating to MySQL", "updating weather data"]
    for idx, update_state in enumerate(Update_enable[0:2]):
        if update_state:
            print("-------------------------------------------")
            print(f"\n[Update] --Start{update_string[idx]}--\n")


    #\ Loop through the whole dragonflt species
    for S in Index.Species_Family_Name:
        #\ insert species name data into species table
        #\ Counts
        Id = Index.Species_Family_Name.index(S)
        # length_S = len(Index.Species_Name_Group[Id])
        # insertdata_S = list(zip(Index.Species_Name_Group[Id], [Id+1]*length_S))
        # insert_data(connection, insertquery_S, insertdata_S)

        #\ build species info table
        for Sp in Index.Species_Name_Group[Id]:

            #\ This is to update the infomation from dragonfly recording web ex: libellulidae58
            ##########################################################################
            Species_table_name = Index.Species_class_key[S] + Index.Species_key[Sp]
            ##########################################################################

            #\ [Temp fix] Change the table name to new name
            #Database_function.update_header(connection, Species_table_name)

            #\ (1)Insert the data to the MySQL database from excel file
            if Update_MySQL:
                try:
                  UpdateCsv2MySql(connection, S, Sp, Id, Species_table_name)

                except:
                    print('create the table, but no such csv file or no such data')

            #\ (2)This is to update the weather information from World weather online
            if Update_weather:

                #\ [Temp fix] Add a new weather column in csv
                file_path = f'{Index.folder_all_crawl_data}{Index.Species_class_key[S]}\\{Species_table_name}.csv'
                CsvOldData, _, _, _, _ = Save2File.Read_check_File(file_path)
                if len(CsvOldData) != 0:
                    if len(CsvOldData[0]) < Index.WeatherCsvIndex+1:
                        Save2File.Update2File(file_path,
                                                CsvOldData,
                                                "add header",
                                                _,
                                                Index.WeatherCsvIndex,
                                                "weather")
                #\ [Temp fix] end


                #\ The weather data update main function
                state = Database_function.get_weather_data(self, connection, Species_table_name, CsvOldData, file_path)
                print('\nUpdate the {} weather data\n'.format(Species_table_name))

                #\ Stop update the weather data due to key problem or calling limit per day.
                if state == False:
                    messagebox.showwarning("Weather Crawling warning", f"Weather data crawling warning\n{weather_data_class.ErrorLog}")
                    return


        #\ Finishing update per species
        try:
            #\ re-arrange the primary key after inserting
            print("[Info] re-arrange primary key")
            Database_function.ReArrangePrimaryKey(connection, Species_table_name, Database_function.Primary_Key)
            print("[Info] Finished re-arranging primary key")

            #\ [Temp fix] Delete duplicate column in MySQL if exist
            # print("[Fixing] Delete duplicate")
            # Database_function.Delete_duplicate(connection, Species_table_name)
            # print("[Fixing] Finishing Delete duplicate")
            #\ [Temp fix] end

        except:
            raise Exception


    #\ End of the updating
    for idx, update_state in enumerate(Update_enable[:2]):
        if update_state:
            print(f"\n[Update] --Finished{update_string[idx]}--\n")
            print("----------------------------------------------")

    #\ Updating the GUI
    Update_data_updating_GUI(self, Update_enable, "finish")



#\  Update GUI
#\  state: "start" or "finish"
def Update_data_updating_GUI(self, update_enable:List[bool], state:str):
    if state == "start":
        #\ clear the update infomation block and reset the information
        self.Update_Block_set_all_to_empty()

        #\ set the progress in this update section
        self.update_section = "Save2File"
        self.progressbar_partial["mode"] = "indeterminate"
        self.progressbar_partial.start(50)

        #\ selector color for weather-data, checkbox_MySQL
        if update_enable[0]:
            self.checkbox_MySQL["fg"] = self.updating_fg_color
            self.checkbox_MySQL["bg"] = self.updating_bg_color
        if update_enable[1]:
            self.checkbox_weather["fg"] = self.updating_fg_color
            self.checkbox_weather["bg"] = self.updating_bg_color

    elif state == "finish":
        #\ selector color for weather-data, checkbox_MySQL
        if update_enable[0]:
            self.checkbox_MySQL["bg"] = self.finished_bg_color
        if update_enable[1]:
            self.checkbox_weather["bg"] = self.finished_bg_color

    else:
        print("please specify the state args")




#\ Update data from CSV to MySQL
def UpdateCsv2MySql(connection:mysql.connector, S:str, Sp:str, Id:int ,Species_table_name:str):
    #\ Insert query
    # create_species_info_table = Database_function.create_species_info_table_first + Species_table_name + Database_function.create_species_info_table_end
    # Database_function.create_table(connection, create_species_info_table)

    filepath = ".\\Crawl_Data\\" + Index.Species_class_key[S] + "\\" + Index.Species_class_key[S] + Index.Species_key[Sp] + ".csv"

    #\ patch to update the CSV header
    Save2File.UpdateCsvHeader(filepath)

    with open(filepath, 'r', newline='', errors='ignore') as r:
        CSVData_org = csv.DictReader(r)
        CSVData = [line for line in CSVData_org]
        currentData_Num = Database_function.read_data(connection, "SELECT COUNT(*) FROM " + Index.Species_class_key[S] + Index.Species_key[Sp])
        Data_update_Num = len(CSVData) - currentData_Num[0]['COUNT(*)']
        print(f"\nstart from 0 ~ {Data_update_Num}")
        if Data_update_Num > 0 :
            insertdata_SI = []
            #\ read the database to check the current data number and insert the data from csv file start from it.
            for Cnt, SI in enumerate(CSVData[0:Data_update_Num]):
                # insert data
                insertquery_SI = Database_function.insertquery_SI_first + Species_table_name
                if SI['Latitude'] == '' and SI['Longitude'] == '':
                    insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['District'], SI['Place'])
                    insertquery_SI += Database_function.insertquery_SI_0_end
                else:
                    insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['District'], SI['Altitude'], SI['Place'], SI['Latitude'], SI['Longitude'])
                    insertquery_SI +=  Database_function.insertquery_SI_end

                #\ insert the data into database
                Database_function.insert_single_data(connection, insertquery_SI, insertdata_SI)
                print(f"Updating ~ {Cnt}/{Data_update_Num}", end="\r")
        else:
            print("[info] All been updated, no need to update from CSV to MySQL")

    #\ rearrange the primary key
    if Data_update_Num > 0 :
        print("Rearrange primary key")
        Database_function.ReArrangePrimaryKey(connection, f"{Index.DB_name}.{Species_table_name}", "species_info_id")
    print("Create the {} table from CSV to MySQL".format(Species_table_name))