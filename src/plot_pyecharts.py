#\ this is the plotting function from pyecharts
#] this is using pyecharts v1
import os
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Grid, Bar, Tab, WordCloud, Pie, Line
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
import Database_function
import Index
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



#\ simplified to tradition Dict
s2t = {'新北市':'新北市', '基隆市':'基隆市','台北市':'台北市','桃园市':'桃園市','新竹市':'新竹市','台中市':'台中市','台南市':'台南市','高雄市':'高雄市','彰化县':'彰化縣','嘉义市':'嘉義市','屏东县':'屏東縣','云林县':'雲林縣','苗栗县':'苗栗縣','新竹县':'新竹縣','嘉义县':'嘉義縣','宜兰县':'宜蘭縣','花莲县':'花蓮縣','台东县':'台東縣','南投县':'南投縣','金门县':'金門縣','连江县':'連江縣','中国属钓鱼岛':'釣魚島','澎湖县':'澎湖縣'}
t2s = {v : k for k, v in s2t.items()}


labelformatter = JsCode("""function(x){
                                var s2t = { '新北市':'新北市',
                                            '基隆市':'基隆市',
                                            '台北市':'台北市',
                                            '桃园市':'桃園市',
                                            '新竹市':'新竹市',
                                            '台中市':'台中市',
                                            '台南市':'台南市',
                                            '高雄市':'高雄市',
                                            '彰化县':'彰化縣',
                                            '嘉义市':'嘉義市',
                                            '屏东县':'屏東縣',
                                            '云林县':'雲林縣',
                                            '苗栗县':'苗栗縣',
                                            '新竹县':'新竹縣',
                                            '嘉义县':'嘉義縣',
                                            '宜兰县':'宜蘭縣',
                                            '花莲县':'花蓮縣',
                                            '台东县':'台東縣',
                                            '南投县':'南投縣',
                                            '金门县':'金門縣',
                                            '连江县':'連江縣',
                                            '中国属钓鱼岛':'釣魚島',
                                            '澎湖县':'澎湖縣'};
                                return s2t[x.name]
                            }""")

#\ tooltip format
tooltipformatter=JsCode("""function(params){
                                var s2t = { '新北市':'新北市',
                                            '基隆市':'基隆市',
                                            '台北市':'台北市',
                                            '桃园市':'桃園市',
                                            '新竹市':'新竹市',
                                            '台中市':'台中市',
                                            '台南市':'台南市',
                                            '高雄市':'高雄市',
                                            '彰化县':'彰化縣',
                                            '嘉义市':'嘉義市',
                                            '屏东县':'屏東縣',
                                            '云林县':'雲林縣',
                                            '苗栗县':'苗栗縣',
                                            '新竹县':'新竹縣',
                                            '嘉义县':'嘉義縣',
                                            '宜兰县':'宜蘭縣',
                                            '花莲县':'花蓮縣',
                                            '台东县':'台東縣',
                                            '南投县':'南投縣',
                                            '金门县':'金門縣',
                                            '连江县':'連江縣',
                                            '中国属钓鱼岛':'釣魚島',
                                            '澎湖县':'澎湖縣'};
                                return 'name: '+ s2t[params.name] + '<br>' + 'value: ' + params.value
                            }""")




#######################################################################################################################################
#\ Input data
def plot_species_city(connection, DB_species:str, time:list):
    #\ query 1
    #\ SELECT YEAR(Dates), City, COUNT(*) FROM dragonfly_db.aeshnidae01 WHERE Dates BETWEEN '2010-01-01' AND '2020-07-19' GROUP BY YEAR(Dates), City
    query = "SELECT YEAR(Dates), City, COUNT(*) FROM " +  DB_species + " WHERE Dates BETWEEN \'" + time[0]+ "\' AND \'" + time[1] + "\' GROUP BY YEAR(Dates), City"

    #\ return the vlaue from database , the return will be list of dictionary
    result = Database_function.read_data(connection, query)


    #\ query 2
    #\ new request
    query_multi = "SELECT YEAR(Dates), MONTH(Dates), COUNT(*) FROM " +  DB_species + " WHERE Dates BETWEEN \'" + time[0]+ "\' AND \'" + time[1] + "\' GROUP BY YEAR(Dates), MONTH(Dates) ORDER BY YEAR(Dates), MONTH(Dates)"

    #\ return from MySQL
    result_multi = Database_function.read_data(connection, query_multi)

    #\ To avoid that that the spoecies might not have any record
    if result == [] or result_multi == []:
        print("No records found")
        return


    #\ createmap
    start_year = int(time[0].split("-")[0])
    end_year = int(time[1].split("-")[0])
    value = []
    attrS = []
    attrT = []
    value_multi = []

    #\ time line
    x_mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    #\ title
    Title = Index.Species_key_fullname_E2C[DB_species.split(".")[1]]


    #\ time line create
    timeline = Timeline(init_opts=opts.InitOpts(page_title="Taiwan",
                                            width="1500px",
                                            height="650px"))
    timeline.add_schema(is_auto_play=True, play_interval=4000)
    timeline2 = Timeline(init_opts=opts.InitOpts(page_title="Taiwan",
                                            width="1400px",
                                            height="650px"))
    timeline2.add_schema(is_auto_play=True, play_interval=4000)
    timeline3 = Timeline(init_opts=opts.InitOpts(page_title="Taiwan",
                                            width="1400px",
                                            height="650px"))
    timeline3.add_schema(is_auto_play=True, play_interval=4000)


    #\ Multi Y Bar
    bar_multiY = Bar(init_opts=opts.InitOpts(page_title="Taiwan", width="1400px", height="650px"))
    bar_multiY.add_xaxis(x_mon)
    value_multi_accumulate = [0]*12


    #\ iterating through the years
    for year in range(start_year, end_year+1):

        #\ group the data in same year
        DataSameYear = list(filter(lambda x: x['YEAR(Dates)'] == year, result))
        DataSameYear_multi = list(filter(lambda x: x['YEAR(Dates)'] == year, result_multi))

        #\ value inputs to pyecharts
        attrS.clear()
        attrT.clear()
        value.clear()
        value_multi = [0]*12
        for data,data2 in zip(DataSameYear, DataSameYear_multi):
            value.append(data['COUNT(*)'])
            attrS.append(t2s[data['City']])
            attrT.append(data['City'])
            value_multi[data2['MONTH(Dates)']-1] = data2['COUNT(*)']

        #\ make sure that the emoty data can keep on
        if value == [] or attrS == []:
            continue

        #\ specify the title
        TITLE = "{}-{}".format(Title, year)

        #\ Map object
        map0 = (
            Map()
            .add("",
                list(zip(attrS, value)),
                maptype='台湾',
                )
            .set_global_opts(title_opts=opts.TitleOpts(title=TITLE),
                            toolbox_opts=opts.ToolboxOpts(),
                            visualmap_opts=opts.VisualMapOpts(  max_= max(value),
                                                                min_= 0,
                                                                is_calculable=True,
                                                                dimension=0,        # ** remember to add for color shown
                                                                pos_left="10",
                                                                pos_top="middle",
                                                                range_text=["High", "Low"],
                                                                range_color=["lightskyblue", "yellow", "orangered"],
                                                                textstyle_opts=opts.TextStyleOpts(color="#000"),
                                                                )
                            )
            .set_series_opts(
                label_opts=opts.LabelOpts(formatter=labelformatter),
                tooltip_opts=opts.TooltipOpts(formatter=tooltipformatter)
                )
        )

        #\ Bar
        bar0 = (
                Bar()
                .add_xaxis(attrT)
                .add_yaxis("",y_axis=value)
                .reversal_axis()
                .set_series_opts(label_opts=opts.LabelOpts(position="right"))
                .set_global_opts(title_opts=opts.TitleOpts(title=""),
                                 visualmap_opts=opts.VisualMapOpts(
                                    is_calculable=True,
                                    dimension=0,        # ** remember to add for color shown
                                    pos_left="10",
                                    pos_top="middle",
                                    range_text=["High", "Low"],
                                    range_color=["lightskyblue", "yellow", "orangered"],
                                    min_=0,
                                    max_=max(value),
                                 )
                )
        )


        #\ Bar with multi y axis
        value_multi_zero_compensate = value_multi + [0] * (12 - len(value_multi))
        bar_multiY.add_yaxis(str(year), value_multi_zero_compensate, stack="stack1")

        #\ Accumulate the counts for each month during the year duration
        value_multi_accumulate = [sum(val) for val in zip(value_multi_accumulate, value_multi_zero_compensate)]




        #\ Pie
        pie0 = (
            Pie()
            .add(series_name="",
                data_pair=list(zip(attrT, value)),
                radius = ["0%", "20%"],
                center = ["11%", "85%"], # this will specify the position of the pie
            )
            .set_global_opts(title_opts=opts.TitleOpts(title=""),
                             visualmap_opts=opts.VisualMapOpts(
                                dimension=0,        # ** remember to add for color shown
                                range_text=["High", "Low"],
                                range_color=["lightskyblue", "yellow", "orangered"],
                                min_=0,
                                max_=max(value),
                            ),
                            legend_opts=opts.LegendOpts(is_show=True)
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", color="black"),
            )
        )


        #\ Grid with bar pie map
        bar_map_pie_grid = (
            Grid()
            .add(bar0, grid_opts=opts.GridOpts(pos_left="80%"))
            .add(map0, grid_opts=opts.GridOpts(pos_left="50%"))
            .add(pie0, grid_opts=opts.GridOpts())
        )


        #\ World Cloud
        words = list(zip(attrT, value))
        worldcloud0 = (
            WordCloud()
            .add(series_name="",
                data_pair=words,
                word_size_range=[20, 150],
                textstyle_opts=opts.TextStyleOpts(font_family="cursive")
            )
            .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                title_opts=opts.TitleOpts(
                    title=TITLE + "熱點分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
        )
        words.clear()


        #\ this bar and line are for the plot to demonstrate the species number in different month
        bar_multiA = (
                Bar()
                .add_xaxis(x_mon)
                .add_yaxis("總數", y_axis=value_multi)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=TITLE),
                    toolbox_opts=opts.ToolboxOpts(),
                    visualmap_opts=opts.VisualMapOpts(
                                    is_calculable=True,
                                    dimension=1,        # ** remember to add for color shown
                                    pos_left="10",
                                    pos_top="middle",
                                    range_text=["High", "Low"],
                                    range_color=["lightskyblue", "yellow", "orangered"],
                                    min_=0,
                                    max_=max(value_multi),
                    )
                )
        )
        line_multiA = (
                Line()
                .add_xaxis(x_mon)
                .add_yaxis("", value_multi, yaxis_index=1)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True, color="black"))
                .set_global_opts(
                    visualmap_opts=opts.VisualMapOpts(
                                    is_calculable=True,
                                    dimension=0,        # ** remember to add for color shown
                                    range_color=["black"],
                                    min_=0,
                                    max_=0,
                    )
                )


        )

        #\ combine the line and bar
        bar_multiA.overlap(line_multiA)

        #\ make a grid
        grid_multi = Grid()
        grid_multi.add(bar_multiA, opts.GridOpts())

        #\ Add the plot to timeline module
        timeline.add(bar_map_pie_grid, "{}年".format(year))
        timeline2.add(worldcloud0, "{}年".format(year))
        timeline3.add(grid_multi, "{}年".format(year))

    ## --end of for loop--


    #\ Multi Y Bar with counts
    bar_multiY.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar_multiY.set_global_opts( title_opts=opts.TitleOpts(title=Title + str(start_year) + " to " + str(end_year+1)))

    #\ line in the Multi Y Bar with counts
    line_multiY = (
            Line()
            .add_xaxis(x_mon)
            .add_yaxis("", value_multi_accumulate, yaxis_index=1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, color="black"))
    )

    line_multiY.overlap(bar_multiY)
    #\ make a grid
    bar_multiY_grid = Grid(init_opts=opts.InitOpts(page_title="Taiwan",
                                            width="1500px",
                                            height="650px"))
    bar_multiY_grid.add(line_multiY, opts.GridOpts())




    #\ Table data
    THeader = ["Year","City","Numbers"]
    Trows = []
    for d in result:
        Trows.append([d['YEAR(Dates)'],d['City'],d['COUNT(*)']])


    #\ Build table
    table0 = Table()
    table0.add(THeader, Trows)
    table0.set_global_opts(
        title_opts=ComponentTitleOpts(title="Data Table")
    )


    #\ Add the Tab to show different frame
    tab = (
        Tab(page_title="Taiwan")
        .add(timeline, "TimeLine")
        .add(timeline2, "WorldCloud")
        .add(timeline3, "Species total count")
        .add(bar_multiY_grid, "Counts stack")
        .add(table0, "Table")
    )

    #\ Save and render to the following file
    tab.render(Index.pyecharts_psc_html)

    #\ open  in the browser
    webbrowser.open(Index.pyecharts_psc_html, new = 2, autoraise=False)


    # browser = webdriver.Chrome()
    # browser.get('file:///' + os.getcwd() + pyecharts_psc_html)
    # browser.refresh()
