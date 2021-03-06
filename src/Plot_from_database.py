import plot_matplotlib
import mysql.connector
import Index
import plot_pyecharts


#\ The function to be call for plotting the chart from database
def PlotChart(PlotType:str, DB_species:str, time:list):

    connection = mysql.connector.connect(
        host=Index.hostaddress,
        user=Index.username,
        passwd=Index.password,
        database=Index.DB_name)

    #\ read
    # readquery = "SELECT * FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2020-01-01' AND '2020-07-19'"
    # result = read_data(connection, readquery)

    #\ the input data
    DB_species = "dragonfly_db." + DB_species

    if PlotType == "Matplotlib":
        #\ plot from matplotlib
        #\ plot the species appearance among the years
        plot_matplotlib.plot_species_time_bar(connection, DB_species, time)
    elif PlotType == "Pyecharts":
        #\ plot from pyecharts
        #\ plot the distribution of the dragonfly in Taiwan
        plot_pyecharts.plot_species_city(connection, DB_species, time)
    else :
        print("No plot type specified")




##### test #####
def test():
    connection = mysql.connector.connect(
        host=Index.hostaddress,
        user=Index.username,
        passwd=Index.password,
        database=Index.DB_name)

    #\ read
    '''readquery = "SELECT * FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2020-01-01' AND '2020-07-19'"
    result = read_data(connection, readquery)'''

    #\ the input data
    DB_species = "dragonfly_db.Calopterygidae01"

    time = ["2011-01-01", "2020-07-19"]

    #\ plot from matplotlib
    #\ plot the species appearance among the years
    #plot_species_time_bar(connection, DB_species, time)

    #\ plot from pyecharts
    #\ plot the distribution of the dragonfly in Taiwan
    plot_pyecharts.plot_species_city(connection, DB_species, time)




#\ run
# test()