# SQL
import mysql.connector
from mysql.connector import Error
import Index
import csv


# establish the connection
def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password)
        print("connect to MySQL DB successful")
    except Error as e:
        print(f"The error'{e}' occurred")

    return connection

# create the database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error'{e}' occurred")


# create Table
def create_table(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# insert
def insert_data(connection, query, values):
    cursor = connection.cursor()
    cursor.executemany(query, values)
    connection.commit()

# insert
def insert_single_data(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()


# read data
def read_data(connection, query):
    result = []
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
    except:
        print("the species might not have any recorder")
    return result



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
    Longitutde DOUBLE,
    FOREIGN KEY (species_id) REFERENCES Species_table(species_id),
    FOREIGN KEY (species_family_id) REFERENCES Species_Family_table(species_family_id),
    PRIMARY KEY (species_info_id)
)ENGINE=InnoDB
"""
#\ build species table
insertquery_S = "INSERT INTO Species_table (species_name, species_family_id) VALUES(%s, %s)"
insertquery_SI_first = "INSERT INTO "
insertquery_SI_end = """ (species_family_id, species_id, Species_Name, ID, recorder, Dates, Times, City, District, Altitude, Place, Latitude, Longitutde) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
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
        Id = Index.Species_Family_Name.index(S)
        # length_S = len(Index.Species_Name_Group[Id])
        # insertdata_S = list(zip(Index.Species_Name_Group[Id], [Id+1]*length_S))
        # insert_data(connection, insertquery_S, insertdata_S)

    #\ build species info table
        for Sp in Index.Species_Name_Group[Id]:
            try:
                Species_table_name = Index.Species_class_key[S] + Index.Species_key[Sp]
                create_species_info_table = create_species_info_table_first + Species_table_name + create_species_info_table_end
                create_table(connection, create_species_info_table)
                filepath = ".\Crawl_Data\\" + Index.Species_class_key[S] + "\\" + Index.Species_class_key[S] + Index.Species_key[Sp] + ".csv"
                with open(filepath, 'r', newline='', errors='ignore') as r:
                    CSVData_org = csv.DictReader(r)
                    CSVData = [line for line in CSVData_org]
                    insertdata_SI = []
                    for SI in CSVData:
                        # insert data
                        if SI['Latitude'] == '' and SI['Longitude'] == '':
                            insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['Dictrict'], SI['Place'])
                            insertquery_SI = insertquery_SI_first + Species_table_name + insertquery_SI_0_end
                        else:
                            insertdata_SI = (Id + 1, Index.Species_key[Sp], Sp, SI['ID'], SI['User'], SI['Date'], SI['Time'], SI['City'], SI['Dictrict'], SI['Altitude'], SI['Place'], SI['Latitude'], SI['Longitude'])
                            insertquery_SI = insertquery_SI_first + Species_table_name + insertquery_SI_end
                        insert_single_data(connection, insertquery_SI, insertdata_SI)
                print('create the {} table'.format(Species_table_name))
            except:
                print('create the table, but no such csv file or no such data')






