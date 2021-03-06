import Index
import Database_function
from typing import List
import mysql.connector
from tkinter import messagebox
import csv
import weather_data_class


#\ auto update the data in csv into DATABASE
#\ maybe the next sep will be update by the save2File
#\ contain update weather data
def Update_database(self, connection:mysql.connector, Update_enable:List[bool]):

    #\ INIT the key
    Index.request_cnt = 0
    Index.key_cnt = 0

    #\ create connection
    Database_function.create_table(connection, Database_function.create_species_family_table)
    Database_function.create_table(connection, Database_function.create_species_table)

    #\ buld species family table
    # insertquery_SF = "INSERT INTO Species_Family_table (species_family_name) VALUES (%s)"
    # insertdatas_SF = [tuple([SFN]) for SFN in Index.Species_Family_Name]
    # insert_data(connection, insertquery_SF, insertdatas_SF)


    #\ assign the enable bits
    Update_MySQL, Update_weather, _ = Update_enable

    for S in Index.Species_Family_Name:
        #\ insert species name data into species table
        #\ Counts
        Id = Index.Species_Family_Name.index(S)
        # length_S = len(Index.Species_Name_Group[Id])
        # insertdata_S = list(zip(Index.Species_Name_Group[Id], [Id+1]*length_S))
        # insert_data(connection, insertquery_S, insertdata_S)

    #\ build species info table
        for Sp in Index.Species_Name_Group[Id]:

            #\ This is to update the infomation from dragonfly recording web
            ##########################################################################
            Species_table_name = Index.Species_class_key[S] + Index.Species_key[Sp]
            ##########################################################################

            #\ change the table name to new name
            Database_function.update_header(connection, Species_table_name)

            #\ inseert the data to the MySQL database from excel file
            if Update_MySQL:
                try:
                    #\ query
                    create_species_info_table = Database_function.create_species_info_table_first + Species_table_name + Database_function.create_species_info_table_end
                    Database_function.create_table(connection, create_species_info_table)
                    filepath = ".\\Crawl_Data\\" + Index.Species_class_key[S] + "\\" + Index.Species_class_key[S] + Index.Species_key[Sp] + ".csv"
                    with open(filepath, 'r', newline='', errors='ignore') as r:
                        CSVData_org = csv.DictReader(r)
                        CSVData = [line for line in CSVData_org]
                        currentData_Num = Database_function.read_data(connection, "SELECT COUNT(*) FROM " + Index.Species_class_key[S] + Index.Species_key[Sp])
                        insertdata_SI = []
                        #\ read the database to check the current data number and insert the data from csv file start from it.
                        for SI in CSVData[currentData_Num: ]:
                            # insert data
                            if SI['Latitude'] == '' and SI['Longitude'] == '':
                                insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['District'], SI['Place'])
                                insertquery_SI = Database_function.insertquery_SI_first + Species_table_name + Database_function.insertquery_SI_0_end
                            else:
                                insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['District'], SI['Altitude'], SI['Place'], SI['Latitude'], SI['Longitude'])
                                insertquery_SI = Database_function.insertquery_SI_first + Species_table_name + Database_function.insertquery_SI_end

                            #\ insert the data into database
                            Database_function.insert_single_data(connection, insertquery_SI, insertdata_SI)
                    print('create the {} table'.format(Species_table_name))

                except:
                    print('create the table, but no such csv file or no such data')


            #\ This is to update the weather information from World weather online
            if Update_weather:

                #\ clear the update infomation block and reset the information
                self.Update_Block_set_all_to_empty()

                #\ set the progress in this update section
                self.progressbar_partial["mode"] = "indeterminate"
                self.progressbar_partial.start(50)

                #\ The weather data update main function
                state = Database_function.get_weather_data(self, connection, Species_table_name)
                print('\nUpdate the {} weather data\n'.format(Species_table_name))

                #\ Stop update the weather data due to key problem or calling limit per day.
                if state == False:
                    messagebox.showwarning("Weather Crawling warning", f"Weather data crawling warning\n{weather_data_class.ErrorLog}")
                    return