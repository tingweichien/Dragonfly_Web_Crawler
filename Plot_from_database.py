from plot_matplotlib import plot_species_time_bar
from Database_function import *
from Index import *
from plot_pyecharts import plot_species_city

##### main #####
connection = mysql.connector.connect(
    host=hostaddress,
    user=username,
    passwd=password,
    database=DB_name)

#\ read
'''readquery = "SELECT * FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2020-01-01' AND '2020-07-19'"
result = read_data(connection, readquery)'''

#\ the input data
DB_species = "dragonfly_db.Calopterygidae01"

time = ["2011-01-01", "2020-07-19"]

#\ plot from matplotlib
#\ plot the species appearance among the years
plot_species_time_bar(connection, DB_species, time)

#\ plot from pyecharts
#\ plot the distribution of the dragonfly in Taiwan
plot_species_city(connection, DB_species, time)