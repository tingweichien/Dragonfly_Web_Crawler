#\ use the plot of matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.colors as mcolors
import numpy as np
import re
import Index
import calendar
from operator import add
from scipy.stats import norm
import scipy.stats as st
import Database_function

piecolors = list(mcolors.TABLEAU_COLORS.values())+list(mcolors.BASE_COLORS.values())

#\ read data
# def read_data(connection, query):
#     result = []
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#     except:
#         print("the species might not have any recorder")
#     return result

#\ normalize
#\ but this seems to be no use for such less data
def NormalizeFun(xlist, mu, sigma):
    P_D_F = []
    for x in xlist:
        P_D_F.append(1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2)))
    return P_D_F


#\ plot pie
def plot_species_time_pie(InputData: list, title:str, title_fontP:dict):
    piefont = {'size': '8'}
    # piecolors = cm.coolwarm(np.linspace(0, 1, 12))
    cmap = cm.get_cmap("coolwarm")
    piecolors = cmap(np.linspace(0, 1, 12))
    plt.figure(num = 'pie plot')
    data = []
    label = []
    for count, d in enumerate(InputData):
        if d > 0:
            data.append(d)
            label.append(calendar.month_abbr[count + 1])
    plt.pie(data, labels=label, textprops=piefont ,autopct="%.1f%%", colors=piecolors[0: len(data)], labeldistance=1.1, radius = 1, pctdistance=0.6, counterclock= False)
    plt.title(title, fontproperties=title_fontP)


#\ plot the pie with notation
def plot_species_time_pie_notation(InputData: list, title: str, title_font: dict):
    plt.figure(num="pie chart with notation")
    data = []
    label = []
    TextList = ["{} ({})".format(MON, SUM) for MON, SUM in zip(calendar.month_abbr, InputData) if SUM > 0]
    Rpie = 0.8
    startangle =-90

    #\ specify the hollow pie
    for count, d in enumerate(InputData):
        if d > 0:
            data.append(d)
            label.append(calendar.month_abbr[count + 1])
    wedge, _ = plt.pie( data,
                            wedgeprops=dict(width=0.5),
                            startangle=startangle,
                            radius=Rpie,
                            colors=piecolors)

    #\ specify the annotation
    widen = 0
    for count, p in enumerate(wedge):
        angle = p.theta1 + ((p.theta2 - p.theta1) / 2)
        x = Rpie * np.cos(np.deg2rad(angle))
        y = Rpie * np.sin(np.deg2rad(angle))
        if p.theta2 - p.theta1 < 25:
            widen += 1 # if the too many text in same range together than make it sperate
            sign = -1 if angle < 180 else 1
            Yend = 1.65 * (1 + sign * 0.1 * widen) * y
            Xend = 1.3 * np.sign(x)
        else:
            widen = 0
            Yend = 1.4 * y
            Xend = 1.3 * np.sign(x)
        horizontalalignment = {-1: 'right', 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle, angleA=0, angleB={}".format(angle)
        arrowprops= {"connectionstyle": connectionstyle, "arrowstyle": '->'}
        plt.annotate(   TextList[count],
                        xy=(x, y),
                        xytext=(Xend, Yend),
                        arrowprops=arrowprops,
                        horizontalalignment=horizontalalignment,
                        va="center",
                        bbox={"boxstyle": "Square, pad=0.3", "fc": "w"},
                        size = 8)
    plt.title(title, pad = 1, fontproperties=title_font)


# \ main loop
#\ this is the function fot plotting from the database
#\ DB_species should be in English
#\ time should be in list[] ex:["2018-06-01", "2020-05-01"]
def plot_species_time_bar(connection, DB_species:str, time:list):

    #\ QUERY
    readqurery = "SELECT YEAR(Dates), MONTH(Dates), COUNT(*) FROM " + DB_species + " WHERE Dates BETWEEN \'" + time[0] + "\' AND \'" + time[1]\
                   + "\' GROUP BY YEAR(Dates), MONTH(Dates)" + " ORDER BY YEAR(Dates), MONTH(Dates);"
    result = Database_function.read_data(connection, readqurery)

    #\ To avoid that that the spoecies might not have any record
    if result == []:
        print("No records found")
        return

    #\ args
    month_in_year = 12
    ShiftAxis = 0.5
    bottom = None
    start_year = int(time[0].split("-")[0])
    check_year = start_year
    end_year = int(time[1].split("-")[0])
    interval = end_year - start_year + 1

    #\
    monthList = np.arange(1,month_in_year+1) + ShiftAxis
    init_countlist = list([0]*month_in_year)
    countList = init_countlist.copy() #\ be careful that the assignment from a list to another list should be by calling .copy() method, using l1 = l2 will be pointer

    #\ legend
    legend_year = []
    tableData = []
    cellColors = []
    cellColors_tmp = ['w'] * month_in_year
    C_counter = 0
    color = plt.rcParams['axes.prop_cycle'].by_key()['color'] * 2  #\ this might have some problem if the data over 10

    #\ text size and font
    title_text_size = 10
    table_text_size = 8
    legend_font = {'size': '8'}


    while check_year <= end_year:
        #\ get the group of the data in same year
        SameYearData = list(filter(lambda res: res["YEAR(Dates)"] == check_year, result))

        #\do the assignment if there is the data
        for r in SameYearData:
            countList[r["MONTH(Dates)"] - 1] = r["COUNT(*)"]
            cellColors_tmp[r["MONTH(Dates)"] - 1] = color[C_counter]

        #\ combine the cellColors_tmp together
        cellColors.append(cellColors_tmp.copy())
        cellColors_tmp = ['w'] * month_in_year

        #\ plot bar
        plt.bar(monthList, countList, bottom=bottom)

        #\ modify the next bottom
        if bottom == None:
            bottom = countList.copy()
        else:
            #\ use copy to do assignment not pointer
            bottom = list(map(add, bottom, countList.copy()))

        #\ build the table
        tableData.append(countList)
        countList = init_countlist.copy()
        legend_year.append(str(check_year))
        check_year += 1
        C_counter += 1



    #\ specify the title
    EngTitle = re.findall(r'(\w+?)(\d+)', DB_species.split('.')[1])[0]
    KEY = list(Index.Species_class_key.values())
    title_species = Index.Species_Name_Group[KEY.index(EngTitle[0])][int(EngTitle[1]) - 1]

    #\ add the sum column
    #\ at the end bottom will be the sum
    sumText = bottom.copy()
    for count, ind in enumerate(bottom):
        if ind > 0:
            sumText[count] = '$\\bf{' + str(bottom[count]) + '}$'
    tableData.append(sumText)

    #\ add the sum cell color
    cellColors.append(cellColors_tmp.copy())

    #\ add the table at the bottom of the axes
    legend_year.append('Total')
    rowColors = color[0:interval] + ['w']
    the_table = plt.table(  cellText = tableData,
                            rowLabels = legend_year,
                            rowColours = rowColors,
                            cellColours = cellColors,
                            colLabels = calendar.month_abbr[1:13],
                            cellLoc = 'center',
                            loc='bottom')

    #\ to align thr table with plot
    plt.xlim([1,13])
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(table_text_size)
    the_table.scale(1, 2)

    #\ plot normal distribution
    #\ bottom will be the sum of all the data
    #normalY = NormalizeFun(bottom, np.mean(bottom), np.std(bottom, ddof=1))
    NData = []
    # shift = 0 #\ this is due to the prevoius shifting to align the table

    #\ specify the data
    for count, i in enumerate(bottom):
        NData.extend([(count + 1 + ShiftAxis)] * i)

    mn, mx = plt.xlim()
    kde_x = np.linspace(mn + ShiftAxis, mx - ShiftAxis, 12)  #\ set it in the range of 1.5 ~ 12.5
    #kde_x = np.linspace(mn, mx, 100)
    kde = st.gaussian_kde(NData)
    kde_y = kde.pdf(kde_x)

    #\ specify the markers
    kde_x_1f = [round(x, 1) for x in kde_x]
    markx = np.arange(1.5, 13, 1)
    markers_on = [kde_x_1f.index(m) for m in markx]  #\specify the marker place
    for X, Y in zip(markx, kde.pdf(markx)*max(bottom)/max(kde_y)):
        plt.text(X, Y, str(round(100 * kde.pdf(X)[0], 1)) + '%')

    #\ plot the distribution curve
    plt.plot(kde_x, kde_y*max(bottom)/max(kde_y), markevery=markers_on, marker='.', linestyle='-', color='k', linewidth=1)
    plt.xlim(mn, mx)

    #\ Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.1, bottom=0.05*(interval))

    #\ title Font
    title_fontP = font_manager.FontProperties()
    title_fontP.set_family('MingLiU')
    title_fontP.set_size(title_text_size)

    #\ plot
    #\ modify the legend
    legend_year.insert(0, 'Distribution')
    legend_year.remove('Total')
    plt.legend(tuple(legend_year), prop = legend_font)

    TITLE = title_species + " record from " + time[0] + " to " + time[1]
    plt.title(TITLE, fontproperties=title_fontP)
    plt.ylabel("Counts")
    plt.ylim([0, max(bottom)*1.1])# toi give some space on the top of the plot
    plt.xticks([])
    #plt.xlabel("Month")
    #plt.xticks(monthList)

    #\ plot the pie
    plot_species_time_pie(bottom, TITLE, title_fontP)

    #\ plot the pie with annotations
    plot_species_time_pie_notation(bottom, TITLE, title_fontP)

    plt.show()




