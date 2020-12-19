# SQL
import mysql.connector
from mysql.connector import Error
import Index
import csv
import requests
from typing import List
from datetime import datetime



#\ weather api key count
key_cnt = 0

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
        print(f"The error'{e}' occurred")

    return connection

# create the database
def create_database(connection:mysql.connector, query:str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# create Table
def create_table(connection:mysql.connector, query:str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


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
        print("the species might not have any recorder")
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
        print("Create the weather column ")

    except:
        print("The weather column has been created")





#\ Insert the data that's not exit after the table been build
# -- ALTER TABLE mytags
# -- ADD COLUMN vendor int AFTER tags;
# -- UPDATE mytags SET vendor = 333 WHERE id=1;
def update_weather_data(connection:mysql.connector, Table:str, data_seperate_time:dict, species_info_id:int):
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
    #\ MYSQL
    cursor = connection.cursor()
    try:
        cursor.execute(Insert_query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")




#\ Send the request to get the weather data
#\ link : https://www.worldweatheronline.com/developer/#
#\ Loop through the different table (DB_species)
#\ Check each row of the input table in this function
def get_weather_data(connection:mysql.connector, DB_species:str):
    global key_cnt
    current_parsing_date = 0 #\ this is the datetime buffer for check if the date change to avoid re-request the same day again on the online weather api
    weather_r = {}

    #\ create the new column
    ALTER_TABLE(connection, "weather", "JSON", DB_species)

    #\ if the key is not available or request meets the limit then change the key
    if key_cnt < len(Index.weather_key) :
        try:
            #\ read query
            readqurery = f"SELECT species_info_id, Dates, HOUR(Times), Latitude, Longitude FROM {Index.DB_name}.{DB_species} WHERE weather is null;"

            #\ get all the row that do not have weather data
            response_List = read_data(connection, readqurery)

            #\ fill the weather data for each row
            for response in response_List:

                #\ if the LAT and LNG is NULL then skip
                if response["Latitude"] and response["Longitude"] is not None:

                    data = {"key": Index.weather_key[key_cnt],
                            "q" : f'{response["Latitude"]}, {response["Longitude"]}',
                            "format" : "json",
                            "date" : response["Dates"],
                            "enddate" : response["Dates"]
                        }

                    #\ api
                    #\ and check the parsing date is the same day or not
                    if response["Dates"] != current_parsing_date:
                        weather_r = requests.post(url="http://api.worldweatheronline.com/premium/v1/past-weather.ashx",data=data).json()
                        current_parsing_date = response["Dates"] #\ update teh current data


                    #\ Extract the data
                    #\ extract by hour
                    for data_seperate_time in weather_r["data"]["weather"][0]["hourly"]:
                        #\ select the corresponding hour
                        #\ remove the minutes. i.e. "1800" --> "18", get it from counting back
                        respponse_hour = int(data_seperate_time["time"][:-2]) if data_seperate_time["time"] != "0" else 0
                        if int(response["HOUR(Times)"]) in range(respponse_hour, respponse_hour+3): #\ the response is in three hours interval
                            update_weather_data(connection,
                                                DB_species,
                                                data_seperate_time,
                                                response["species_info_id"]
                                                )
                            # print(json.dumps(data_seperate_time, indent=2))

        except:
            key_cnt += 1  #\ move to the next key
            print("\n\nChange Key\n")
    else :
        print("key counts overflow, no weather key is available")





#\ read the json format
# SELECT JSON_EXTRACT(name, "$.id") AS name
# FROM table
# WHERE JSON_EXTRACT(name, "$.id") > 3



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


#\ auto update the data in csv into DATABASE
#\ maybe the next sep will be update by the save2File
def Update_database(connection):
    create_table(connection, create_species_family_table)
    create_table(connection, create_species_table)

    #\ buld species family table
    # insertquery_SF = "INSERT INTO Species_Family_table (species_family_name) VALUES (%s)"
    # insertdatas_SF = [tuple([SFN]) for SFN in Index.Species_Family_Name]
    # insert_data(connection, insertquery_SF, insertdatas_SF)


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
            Species_table_name = Index.Species_class_key[S] + Index.Species_key[Sp]

            #\ change the table name to new name
            Update_header_query = f"ALTER TABLE {Species_table_name} CHANGE Longitutde Longitude DOUBLE;"
            read_data(connection, Update_header_query)

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
            get_weather_data(connection, Species_table_name)
            print('\nUpdate the {} weather data\n'.format(Species_table_name))





