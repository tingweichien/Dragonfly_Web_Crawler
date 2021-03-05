# SQL
import mysql.connector
from mysql.connector import Error
import Index
import csv
import requests
from typing import List
from datetime import datetime
import queue
import weather_data_class
from tkinter import messagebox

#\ global
weather_cursor = None
weather_connection = None




# establish the connection
def create_connection(host_name, user_name, user_password, DB_name) -> mysql.connector :
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=DB_name)
        print("connect to MySQL DB successful")
    except Error as e:
        print(f"[warning] The error'{e}' occurred")

    return connection

# create the database
def create_database(connection:mysql.connector, query:str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"[warning] The error '{e}' occurred")


# create Table
def create_table(connection:mysql.connector, query:str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"[warning] The error '{e}' occurred")


# insert
def insert_data(connection:mysql.connector, query:str, values):
    cursor = connection.cursor()
    cursor.executemany(query, values)
    connection.commit()

# insert
def insert_single_data(connection:mysql.connector, query:str, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()


# read data
def read_data(connection:mysql.connector, query:str)->List[dict]:
    result = []
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        # for row in result:
        #     print(row)
    except:
        print("[warning] The species might not have any recorder")
    return result



#\ create new column in the exit table
def ALTER_TABLE(connection: mysql.connector, column_name:str, column_type:str ,Table:str):
    cursor = connection.cursor()
    try :
        create_query = f"""
        ALTER TABLE {Table}
        ADD COLUMN {column_name} {column_type};
        """

        cursor.execute(create_query)
        connection.commit()
        print(f"Create the {column_name} column ")

    except:
        print(f"The {column_name} column has been created")





#\ Insert the data that's not exit after the table been build
# -- ALTER TABLE mytags
# -- ADD COLUMN vendor int AFTER tags;
# -- UPDATE mytags SET vendor = 333 WHERE id=1;
def update_weather_data(self, Table:str, data_seperate_time:dict, species_info_id:int, weather_connection:mysql.connector):
    # global weather_cursor, weather_connection

    #\ create if there is no such column

    value = f"""'{{"tempC" : { data_seperate_time["tempC"].replace(" ", "") }, \
"FeelsLikeC" : { data_seperate_time["FeelsLikeC"].replace(" ", "") }, \
"windspeedKmph" : { data_seperate_time["windspeedKmph"].replace(" ", "") }, \
"winddirDegree" : { data_seperate_time["winddirDegree"].replace(" ", "") }, \
"winddir16Point" : "{ data_seperate_time["winddir16Point"].replace(" ", "") }", \
"humidity" : { data_seperate_time["humidity"].replace(" ", "") }}}'"""

    #\ Insert the data
    Insert_query =f"UPDATE {Index.DB_name}.{Table} SET weather = {value} WHERE species_info_id = {species_info_id};"
    print("Insert_query: ", Insert_query)

    #\print on the GUI
    self.IUpdateNumLabel_text(f"Insert_query: UPDATE {Index.DB_name}.{Table} \n{value} \nWHERE species_info_id = {species_info_id}")
    self.Info_UpdateNum_label["justify"] = "left"

    #\ MYSQL
    try:
        weather_connection.cursor().execute(Insert_query)
        weather_connection.commit()
        print("--- Update weather data to database successfully ---")
    except Error as e:
        print(f"[warning] The error '{e}' occurred")



#\ Thread for the get-weather-data
#\ (G)et (W)eather (D)ata
def GetWeatherDataThread(self, dataList, DB_species, weather_connection):

    #\ create the queue
    GWD_queue = queue.Queue()

    #\ create the workers
    worker_list = []
    for num in range(len(dataList)):
        worker_list.append(weather_data_class.WeatherDataWorker(self, GWD_queue, num, dataList[num], DB_species, weather_connection))

    #\ start the thread
    WorkerLength = len(worker_list)
    for number in range(WorkerLength):
        worker_list[number].start()


    #\ wait for the thread to join to show the result
    for number in range(WorkerLength):
        worker_list[number].join()


    #\ check if running success
    for number in range(WorkerLength):
        if worker_list[number].KeyChange:
            return False
    return True



#\ Send the request to get the weather data
#\ link : https://www.worldweatheronline.com/developer/#
#\ Loop through the different table (DB_species)
#\ Check each row of the input table in this function
def get_weather_data(self, connection:mysql.connector, DB_species:str)->bool:
    #\ global
    global weather_cursor, weather_connection
    weather_connection = connection
    weather_cursor = connection.cursor()

    #\ init
    current_parsing_date = 0 #\ this is the datetime buffer for check if the date change to avoid re-request the same day again on the online weather api
    current_LATLNG =()
    weather_r = {}
    currentCNT = 0
    currentCNT_END = 0

    #\ show the crawling species information
    self.Info_FileName_label['text']  = f'Current crawling --- {Index.Species_key_fullname_E2C[DB_species]} --- weather data'
    print(f'Current crawling --- {Index.Species_key_fullname_E2C[DB_species]} --- weather data')

    #\ The indicator for how many portion of the update will be, this var is to let the progressbar adjest by how many check button been selected.
    progressbar_portion = self.progressbar_portion_calc()

    #\ create the new column
    ALTER_TABLE(weather_connection, "weather", "JSON", DB_species)

    #\ if the key is not available or request meets the limit then change the key
    if Index.key_cnt < len(Index.weather_key) :
        try:
            #\ read query
            readqurery = f"SELECT species_info_id, Dates, HOUR(Times), Latitude, Longitude FROM {Index.DB_name}.{DB_species} WHERE weather is null;"

            #\ get all the row that do not have weather data
            response_List = read_data(weather_connection, readqurery)

            endFlag = False

            #\ weather multithread
            if Index.weather_multithread:

                while not endFlag:

                    #\ if the end overflow the length of the response list, then set the end to the length of the response list
                    currentCNT_END = currentCNT + Index.MaxQueueNum
                    if currentCNT_END > len(response_List):
                        currentCNT_END = len(response_List)
                        endFlag = True

                    #\ get the weather data thread.
                    dataList = response_List[currentCNT : currentCNT_END]
                    GWD_return_status = GetWeatherDataThread(self, dataList, DB_species, weather_connection)

                    #\ if false this might means APO key is out of date or reach calls per day.
                    if  GWD_return_status == False:
                        return False

                    #\ break the while loop since the rest of the data have been overdated
                    if Index.WeatherTimeOverLimitStatus == Index.overtimelimit:
                        Index.WeatherTimeOverLimitStatus = False
                        endFlag = True
                    else:
                        currentCNT = currentCNT_END


            #\ weather single thread
            else:
                #\ fill the weather data for each row
                for response in response_List:
                    #\ check the weather request data is vaild or not
                    if check_weather_data(self, response):

                        #\ request data format
                        data = {"key": Index.weather_key[Index.key_cnt],
                                "q" : f'{response["Latitude"]}, {response["Longitude"]}',
                                "format" : "json",
                                "date" : response["Dates"],
                                "enddate" : response["Dates"]
                            }

                        #\ API and check the parsing date is the same day and position is same or not
                        #\ since the API only accept to seond in decimal, so we do the round()
                        if (response["Dates"] != current_parsing_date) or ((round(response["Latitude"], 2), round(response["Longitude"], 2)) != current_LATLNG):

                            #\ this is the API
                            ######################################################################
                            weather_r = requests.post(url=Index.OnlineWeatherURL, data=data).json()
                            #######################################################################

                            #\ count the request time
                            Index.request_cnt += 1
                            print("request counts: ", str(Index.request_cnt))

                            #\ GUI display
                            self.Info_FileName_label['text']  = Index.Species_key_fullname_E2C[DB_species]
                            self.IStateLabel_text("request counts: "+ str(Index.request_cnt))
                            self.progressbar.step((100*progressbar_portion["weather_portion"]) / (len(Index.weather_key) * Index.weather_request_limit))
                            self.pbLabel_text()


                            #\--- problem : if the noraml data will cause error here since there will be no such column or class or object
                            #\ check if the error occurred
                            # if weather_r["data"]["error"][0]["msg"] == Index.WRE_No_data_available:
                            #     continue
                            # else:

                            #\ update the current data
                            current_parsing_date = response["Dates"]
                            current_LATLNG = ( round(response["Latitude"], 2), round(response["Longitude"], 2) )


                        #\ Extract the data, extract by hour
                        for data_seperate_time in weather_r["data"]["weather"][0]["hourly"]:
                            #\ select the corresponding hour
                            #\ remove the minutes. i.e. "1800" --> "18", get it from counting back
                            respponse_hour = int(data_seperate_time["time"][:-2]) if data_seperate_time["time"] != "0" else 0
                            if int(response["HOUR(Times)"]) in range(respponse_hour, respponse_hour+3): #\ the response is in three hours interval
                                update_weather_data(self,
                                                    DB_species,
                                                    data_seperate_time,
                                                    response["species_info_id"],
                                                    weather_connection)

        except:
            changekey_Info(self)

    #\ key had been run out
    else :
        print("[warning] key counts overflow, no weather key is available")
        return False



#\ change key infomation
def changekey_Info(self):
    Index.key_cnt += 1  #\ move to the next key
    print("\n--Change Key--\n")
    self.IUpdateNumLabel_text("--Change Key--")
    if Index.key_cnt < len(Index.weather_key):
        print(f"current key : {Index.weather_key[Index.key_cnt-1]} to New key {Index.weather_key[Index.key_cnt]}")
        self.IUpdateNumLabel_text(f"current key : {Index.weather_key[Index.key_cnt-1]} to New key {Index.weather_key[Index.key_cnt]}")



#\ check the data is vaild or not
def check_weather_data(self, response)->bool:

    #\ somehow in multithread the key count will overflow
    if Index.key_cnt >= len(Index.weather_key):
        return False

    #\ check if the key is out of date
    if datetime.now().date() <= Index.weather_Key_expire_date[Index.key_cnt]:

        #\ check if the request date is not over the earliest date
        if response["Dates"] > Index.Weather_earliest_date:

            #\ if the LAT and LNG is NULL then skip
            if response["Latitude"] and response["Longitude"] is not None:

                #\ limit the request times
                if Index.request_cnt <= Index.weather_request_limit:
                    return True

                #\ over the limit
                else:
                    changekey_Info(self)
                    Index.request_cnt = 0

            #\ if the LAT and LNG is NULL
            else:
                # print("[warning] Latitude and Longitutde is Null\n")
                return  False

        #\ if the the date time over the earliest date
        else:
            print(f'[warning] The date({response["Dates"]}) is over the limit date {Index.Weather_earliest_date}!!!!\n')
            self.IUpdateNumLabel_text(f'[warning] The date({response["Dates"]}) is over the limit date {Index.Weather_earliest_date}!!!!')
            Index.WeatherTimeOverLimitStatus = True
            return  False

    #\ Key is out of date
    else :
        print(f"[warning] Key {Index.key_cnt} : {Index.weather_Key_expire_date[Index.key_cnt]} is out of date!!!!!!")
        return False



#\ read the json format
# SELECT JSON_EXTRACT(name, "$.id") AS name
# FROM table
# WHERE JSON_EXTRACT(name, "$.id") > 3




#\ change the table name to new name
def update_header(connection:mysql.connector, Species_table_name:str):
    Update_header_query = f"ALTER TABLE {Species_table_name} CHANGE Longitutde Longitude DOUBLE;"
    read_data(connection, Update_header_query)



###################################################################

create_species_family_table ="""
CREATE TABLE IF NOT EXISTS Species_Family_table (
    species_family_id INT AUTO_INCREMENT,
    species_family_name TEXT NOT NULL,
    PRIMARY KEY (species_family_id)
)ENGINE=InnoDB
"""

create_species_table = """
CREATE TABLE IF NOT EXISTS Species_table(
    species_id INT AUTO_INCREMENT,
    species_family_id INT NOT NULL,
    species_name TEXT NOT NULL,
    FOREIGN KEY (species_family_id) REFERENCES Species_Family_table(species_family_id),
    PRIMARY KEY (species_id)
)ENGINE=InnoDB
"""

create_species_info_table_first = """CREATE TABLE IF NOT EXISTS """
create_species_info_table_end = """(species_info_id INT AUTO_INCREMENT,
    species_family_id INT NOT NULL,
    species_id INT NOT NULL,
    Species_Name TEXT NOT NULL,
    ID INT NOT NULL,
    recorder TEXT NOT NULL,
    Dates DATE NOT NULL,
    Times TIME NOT NULL,
    City TEXT NOT NULL,
    District TEXT NOT NULL,
    Altitude INT,
    Place TEXT NOT NULL,
    Latitude DOUBLE,
    Longitude DOUBLE,
    FOREIGN KEY (species_id) REFERENCES Species_table(species_id),
    FOREIGN KEY (species_family_id) REFERENCES Species_Family_table(species_family_id),
    PRIMARY KEY (species_info_id)
)ENGINE=InnoDB
"""
#\ build species table
insertquery_S = "INSERT INTO Species_table (species_name, species_family_id) VALUES(%s, %s)"
insertquery_SI_first = "INSERT INTO "
insertquery_SI_end = """ (species_family_id, species_id, Species_Name, ID, recorder, Dates, Times, City, District, Altitude, Place, Latitude, Longitude) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
insertquery_SI_0_end = """ (species_family_id, species_id, Species_Name, ID, recorder, Dates, Times, City, District, Place) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


#\ create database
# connection = create_connection(Index.hostaddress, Index.username, Index.password)
# create_database_query = "CREATE DATABASE " + Index.DB_name
# create_database(connection, create_database_query)



'''2021/1/28 move to Update_database.py
#\ auto update the data in csv into DATABASE
#\ maybe the next sep will be update by the save2File
#\ contain update weather data
def Update_database(self, connection:mysql.connector, Update_enable:List[bool]):

    #\ INIT the key
    global request_cnt, key_cnt
    request_cnt = 0
    key_cnt = 0

    #\ create connection
    create_table(connection, create_species_family_table)
    create_table(connection, create_species_table)

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
            update_header(connection, Species_table_name)

            #\ inseert the data to the MySQL database from excel file
            if Update_MySQL:
                try:
                    #\ query
                    create_species_info_table = create_species_info_table_first + Species_table_name + create_species_info_table_end
                    create_table(connection, create_species_info_table)
                    filepath = ".\\Crawl_Data\\" + Index.Species_class_key[S] + "\\" + Index.Species_class_key[S] + Index.Species_key[Sp] + ".csv"
                    with open(filepath, 'r', newline='', errors='ignore') as r:
                        CSVData_org = csv.DictReader(r)
                        CSVData = [line for line in CSVData_org]
                        currentData_Num = read_data(connection, "SELECT COUNT(*) FROM " + Index.Species_class_key[S] + Index.Species_key[Sp])
                        insertdata_SI = []
                        #\ read the database to check the current data number and insert the data from csv file start from it.
                        for SI in CSVData[currentData_Num: ]:
                            # insert data
                            if SI['Latitude'] == '' and SI['Longitude'] == '':
                                insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['District'], SI['Place'])
                                insertquery_SI = insertquery_SI_first + Species_table_name + insertquery_SI_0_end
                            else:
                                insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['District'], SI['Altitude'], SI['Place'], SI['Latitude'], SI['Longitude'])
                                insertquery_SI = insertquery_SI_first + Species_table_name + insertquery_SI_end

                            #\ insert the data into database
                            insert_single_data(connection, insertquery_SI, insertdata_SI)
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
                get_weather_data(self, connection, Species_table_name)
                print('\nUpdate the {} weather data\n'.format(Species_table_name))

'''


