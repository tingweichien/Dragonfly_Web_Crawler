from pyecharts._version import __version__

#########################################################################################################################################################
#\ new version v1.
if int(__version__.split(".")[0]) >= 1:
    print(__version__)

    '''from pyecharts import options as opts
    from pyecharts.charts import Geo
    from pyecharts.faker import Faker
    from pyecharts.globals import ChartType
    import os

    c = (
        Geo(init_opts=opts.InitOpts(page_title="Taiwan"))
        .add_schema(maptype="台湾")
        .add(
            "geo",
            [list(z) for z in zip(Faker.provinces, Faker.values())],
            type_=ChartType.EFFECT_SCATTER,
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False, font_family='Arial'))
        .set_global_opts(title_opts=opts.TitleOpts(title="Geo-EffectScatter"))
        .render("geo_effectscatter.html")
    )
    os.system("geo_effectscatter.html")'''


    ###################################################
    import os

    from pyecharts import options as opts
    from pyecharts.charts import Map
    from pyecharts.commons.utils import JsCode

    #\ simplified to tradition Dict
    s2t = {'新北市':'新北市', '基隆市':'基隆市','台北市':'台北市','桃园市':'桃園市','新竹市':'新竹市','台中市':'台中市','台南市':'台南市','高雄市':'高雄市','彰化县':'彰化縣','嘉义市':'嘉義市','屏东县':'屏東縣','云林县':'雲林縣','苗栗县':'苗栗縣','新竹县':'新竹縣','嘉义县':'嘉義縣','宜兰县':'宜蘭縣','花莲县':'花蓮縣','台东县':'台東縣','南投县':'南投縣','金门县':'金門縣','连江县':'連江縣','中国属钓鱼岛':'釣魚島','澎湖县':'澎湖縣'};
    t2s = {v : k for k, v in s2t.items()}

    #\ simplified to tradition function
    s2tFunc = lambda x : [t2s[i] for i in x]

    # labelformatter = JsCode("""function(x){
    #                                 console.log(x.name + ', '+ x.value + ', ' + x.dataIndex);
    #                                 if (x.name == '桃园市'){
    #                                     return '桃園市';
    #                                 }
    #                                 else if (x.name == '彰化县'){
    #                                     return '彰化縣';
    #                                 }
    #                                 else if (x.name == '嘉义市'){
    #                                     return '嘉義市';
    #                                 }
    #                                 else if (x.name == '屏东县'){
    #                                     return '屏東縣';
    #                                 }
    #                                 else if (x.name == '云林县'){
    #                                     return '雲林縣';
    #                                 }
    #                                 else if (x.name == '苗栗县'){
    #                                     return '苗栗縣';
    #                                 }
    #                                 else if (x.name == '新竹县'){
    #                                     return '新竹縣';
    #                                 }
    #                                 else if (x.name == '嘉义县'){
    #                                     return '嘉義縣';
    #                                 }
    #                                 else if (x.name == '宜兰县'){
    #                                     return '宜蘭縣';
    #                                 }
    #                                 else if (x.name == '宜兰县'){
    #                                     return '宜蘭縣';
    #                                 }
    #                                 else if (x.name == '花莲县'){
    #                                     return '花蓮縣';
    #                                 }
    #                                 else if (x.name == '台东县'){
    #                                     return '台東縣';
    #                                 }
    #                                 else if (x.name == '南投县'){
    #                                     return '南投縣';
    #                                 }
    #                                 else if (x.name == '金门县'){
    #                                     return '金門縣';
    #                                 }
    #                                 else if (x.name == '连江县'){
    #                                     return '連江縣';
    #                                 }
    #                                 else if (x.name == '中国属钓鱼岛'){
    #                                     return '釣魚島';
    #                                 }
    #                                 else if (x.name == '澎湖县'){
    #                                     return '澎湖縣';
    #                                 }
    #                                 else{
    #                                     return x.name;
    #                                 }
    #                             }""")

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

    #\ the imput data
    value=[3986291,2785159,2776846,2184655,1886465,1282669,830303,690662,554267,551816,511520,501474]
    attr = s2tFunc(["新北市", "台中市", "高雄市", "台北市", "台南市", "彰化縣", "屏東縣", "雲林縣", "苗栗縣", "新竹縣", "嘉義縣", "南投縣"])

    #\ createmap
    c = (
        Map(init_opts=opts.InitOpts(page_title="Taiwan" ,width="1600px", height="700px"))
        .add("", list(zip(attr, value)), maptype='台湾')
        .set_global_opts(title_opts=opts.TitleOpts(title="台灣"), visualmap_opts=opts.VisualMapOpts(max_=max(value)))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter='{b} : 123'))
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter=labelformatter),
            tooltip_opts=opts.TooltipOpts(formatter=tooltipformatter)
            )
        .render("map_base.html")
    )
    os.system("map_base.html")

    ###
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-显示 ToolBox"),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .render("bar_toolbox.html")
    )
    os.system("bar_toolbox.html")

#########################################################################################################################################################
#\ old version v0.5.11
if __version__ == "0.5.11":
    import os
    from pyecharts import Map

    def tooltipformatter(params):
        return "name: " + params.name + "<br>" + "value: " + params.value

    value = [10,255]
    attr = ["台中市","嘉義縣"]
    map = Map("台灣", width=1500, height=700)
    map.add(
            "",
            attr,
            value,
            maptype='台湾',
            is_label_show=True,
            label_formatter='{b},{c}',
            is_visualmap=True,
            is_map_symbol_show=False,
            visual_text_color="#000",
            visual_range_text=["0", "255"],
            visual_range=[0, 255],
            #tooltip_formatter = '{b}, {c}'
            tooltip_formatter = tooltipformatter
            )
    map.render("map_base.html")
    os.system("map_base.html")


    ########################################################################
    # from pyecharts import WordCloud
    # import os
    # name = [
    #     'Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World', 'Charter Communications',
    #     'Chick Fil A', 'Planet Fitness', 'Pitch Perfect', 'Express', 'Home', 'Johnny Depp',
    #     'Lena Dunham', 'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
    #     'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']
    # value = [
    #     10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112,
    #     965, 847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    # wordcloud = WordCloud(width=1300, height=620)
    # wordcloud.add("", name, value, word_size_range=[20, 100])
    # wordcloud.render("map_base.html")
    # os.system("map_base.html")