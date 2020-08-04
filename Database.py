# SQL
import mysql.connector
from mysql.connector import Error


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
        

#insert
def insert_data(connection, query, values):
    cursor = connection.cursor()
    cursor.executemany(query, values)
    connection.commit()


# read data
def read_data(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)

create_users_table ="""
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  age INT, 
  gender TEXT, 
  nationality TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

create_posts_table = """
CREATE TABLE IF NOT EXISTS posts (
  id INT AUTO_INCREMENT, 
  title TEXT NOT NULL, 
  description TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  FOREIGN KEY fk_user_id (user_id) REFERENCES users(id), 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

username = "timweiwei"
hostaddress = "127.0.0.1"
password = "tim960622"
DB_name =  'Dragonfly_DB'

connection = create_connection(hostaddress, username, password)


'''
Connection_cursor = connection.cursor()
DB_list = Connection_cursor.execute("SHOW DATABASES")

if not DB_list == None:
    if (DB_name in DB_list):
        connection = mysql.connector.connect(
            host=hostaddress,
            user=username,
            passwd=password,
            database=DB_name)
else:
    create_database_query = "CREATE DATABASE " + DB_name
    create_database(connection, create_database_query)
'''

create_database_query = "CREATE DATABASE " + DB_name
create_database(connection, create_database_query)


connection = mysql.connector.connect(
    host=hostaddress,
    user=username,
    passwd=password,
    database=DB_name)


create_table(connection, create_users_table)
create_table(connection, create_posts_table)

insertquery = "INSERT INTO users (name, age) values(%s, %s)"
insertdatas = [("Steve", 24),
                ("Max", 25),
                ("Chang" ,26),]
insert_data(connection, insertquery, insertdatas)

readquery = "SELECT name, age FROM users"
read_data(connection, readquery)