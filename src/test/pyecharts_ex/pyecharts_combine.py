# import pyecharts.options as opts
# from pyecharts.globals import ThemeType
# from pyecharts.commons.utils import JsCode
# from pyecharts.charts import Timeline, Grid, Bar, Map, Pie
# import os
# """
# Gallery 使用 pyecharts 1.0.0
# 参考地址: https://gallery.echartsjs.com/editor.html?c=xSkGI6zLmb

# 目前无法实现的功能:

# 1、
# """

# data = [
#     {
#         "time": 1980,
#         "data": [
#             {"name": "台湾", "value": [633.76, 12.28, "台湾"]},
#             {"name": "香港", "value": [432.47, 8.38, "香港"]},
#             {"name": "江苏", "value": [319.8, 6.2, "江苏"]},
#             {"name": "上海", "value": [311.89, 6.05, "上海"]},
#             {"name": "山东", "value": [292.13, 5.66, "山东"]},
#             {"name": "辽宁", "value": [281, 5.45, "辽宁"]},
#             {"name": "广东", "value": [249.65, 4.84, "广东"]},
#             {"name": "四川", "value": [229.31, 4.44, "四川"]},
#             {"name": "河南", "value": [229.16, 4.44, "河南"]},
#             {"name": "黑龙江", "value": [221, 4.28, "黑龙江"]},
#         ],
#     },
#     {
#         "time": 2000,
#         "data": [
#             {"name": "台湾", "value": [27435.15, 19.47, "台湾"]},
#             {"name": "香港", "value": [14201.59, 10.08, "香港"]},
#             {"name": "广东", "value": [10741.25, 7.62, "广东"]},
#             {"name": "江苏", "value": [8553.69, 6.07, "江苏"]},
#             {"name": "山东", "value": [8337.47, 5.92, "山东"]},
#             {"name": "浙江", "value": [6141.03, 4.36, "浙江"]},
#             {"name": "河南", "value": [5052.99, 3.59, "河南"]},
#             {"name": "河北", "value": [5043.96, 3.58, "河北"]},
#             {"name": "上海", "value": [4771.17, 3.39, "上海"]},
#             {"name": "辽宁", "value": [4669.1, 3.31, "辽宁"]},
#         ],
#     },
#     {
#         "time": 2005,
#         "data": [
#             {"name": "台湾", "value": [30792.89, 12.52, "台湾"]},
#             {"name": "广东", "value": [22527.37, 9.16, "广东"]},
#             {"name": "江苏", "value": [18598.69, 7.56, "江苏"]},
#             {"name": "山东", "value": [18366.87, 7.47, "山东"]},
#             {"name": "香港", "value": [14869.68, 6.05, "香港"]},
#             {"name": "浙江", "value": [13417.68, 5.46, "浙江"]},
#             {"name": "河南", "value": [10587.42, 4.3, "河南"]},
#             {"name": "河北", "value": [10043.42, 4.08, "河北"]},
#             {"name": "上海", "value": [9247.66, 3.76, "上海"]},
#             {"name": "辽宁", "value": [8047.3, 3.27, "辽宁"]},
#         ],
#     },
#     {
#         "time": 2010,
#         "data": [
#             {"name": "广东", "value": [46036.25, 9.49, "广东"]},
#             {"name": "江苏", "value": [41425.48, 8.54, "江苏"]},
#             {"name": "山东", "value": [39169.92, 8.08, "山东"]},
#             {"name": "台湾", "value": [30205.64, 6.23, "台湾"]},
#             {"name": "浙江", "value": [27747.65, 5.72, "浙江"]},
#             {"name": "河南", "value": [23092.36, 4.76, "河南"]},
#             {"name": "河北", "value": [20394.26, 4.21, "河北"]},
#             {"name": "辽宁", "value": [18457.3, 3.81, "辽宁"]},
#             {"name": "四川", "value": [17185.48, 3.54, "四川"]},
#             {"name": "上海", "value": [17165.98, 3.54, "上海"]},
#         ],
#     },
#     {
#         "time": 2015,
#         "data": [
#             {"name": "广东", "value": [72812.55, 9.35, "广东"]},
#             {"name": "江苏", "value": [70116.38, 9, "江苏"]},
#             {"name": "山东", "value": [63002.3, 8.09, "山东"]},
#             {"name": "浙江", "value": [42886, 5.51, "浙江"]},
#             {"name": "河南", "value": [37010.25, 4.75, "河南"]},
#             {"name": "台湾", "value": [32604.52, 4.19, "台湾"]},
#             {"name": "四川", "value": [30103.1, 3.87, "四川"]},
#             {"name": "河北", "value": [29806.1, 3.83, "河北"]},
#             {"name": "湖北", "value": [29550.19, 3.8, "湖北"]},
#             {"name": "湖南", "value": [29047.2, 3.73, "湖南"]},
#         ],
#     },
# ]


# def get_year_chart(year: int):
#     map_data = [
#         [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == year
#     ][0]
#     min_data, max_data = (
#         min([d[1][0] for d in map_data]),
#         max([d[1][0] for d in map_data]),
#     )
#     map_chart = (
#         Map()
#         .add(
#             series_name="",
#             data_pair=map_data,
#             label_opts=opts.LabelOpts(is_show=False),
#             is_map_symbol_show=False,
#             itemstyle_opts={
#                 "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
#                 "emphasis": {
#                     "label": {"show": Timeline},
#                     "areaColor": "rgba(255,255,255, 0.5)",
#                 },
#             },
#         )
#         .set_global_opts(
#             title_opts=opts.TitleOpts(
#                 title="1980年以来中国各省GDP排名变化情况",
#                 subtitle="GDP单位:亿元",
#                 pos_left="center",
#                 pos_top="top",
#                 title_textstyle_opts=opts.TextStyleOpts(
#                     font_size=25, color="rgba(255,255,255, 0.9)"
#                 ),
#             ),
#             tooltip_opts=opts.TooltipOpts(
#                 is_show=True,
#                 formatter=JsCode(
#                     """function(params) {
#                     if ('value' in params.data) {
#                         return params.data.value[2] + ': ' + params.data.value[0];
#                     }
#                 }"""
#                 ),
#             ),
#             visualmap_opts=opts.VisualMapOpts(
#                 is_calculable=True,
#                 dimension=0,
#                 pos_left="10",
#                 pos_top="center",
#                 range_text=["High", "Low"],
#                 range_color=["lightskyblue", "yellow", "orangered"],
#                 textstyle_opts=opts.TextStyleOpts(color="#ddd"),
#                 min_=min_data,
#                 max_=max_data,
#             ),
#         )
#     )

#     bar_x_data = [x[0] for x in map_data]

#     # 这里注释的部分会导致 label 和 value 与 饼图不一致
#     # 使用下面的 List[Dict] 就可以解决这个问题了。
#     # bar_y_data = [x[1][0] for x in map_data]
#     bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
#     bar = (
#         Bar()
#         .add_xaxis(xaxis_data=bar_x_data)
#         .add_yaxis(
#             series_name="",
#             yaxis_index=1,
#             y_axis=bar_y_data,
#             label_opts=opts.LabelOpts(
#                 is_show=True, position="right", formatter="{b}: {c}"
#             ),
#         )
#         .reversal_axis()
#         .set_global_opts(
#             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
#             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
#             tooltip_opts=opts.TooltipOpts(is_show=False),
#             visualmap_opts=opts.VisualMapOpts(
#                 is_calculable=True,
#                 dimension=0,
#                 pos_left="10",
#                 pos_top="center",
#                 range_text=["High", "Low"],
#                 range_color=["lightskyblue", "yellow", "orangered"],
#                 textstyle_opts=opts.TextStyleOpts(color="#ddd"),
#                 min_=min_data,
#                 max_=max_data,
#             ),
#             graphic_opts=[
#                 opts.GraphicGroup(
#                     graphic_item=opts.GraphicItem(
#                         rotation=JsCode("Math.PI / 4"),
#                         bounding="raw",
#                         right=110,
#                         bottom=110,
#                         z=100,
#                     ),
#                     children=[
#                         opts.GraphicRect(
#                             graphic_item=opts.GraphicItem(left="center", top="center", z=100),
#                             graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
#                             graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
#                                 fill="rgba(0,0,0,0.3)"
#                             ),
#                         ),
#                         opts.GraphicText(
#                             graphic_item=opts.GraphicItem(left="center", top="center", z=100),
#                             graphic_textstyle_opts=opts.GraphicTextStyleOpts(
#                                 text=f"{str(year)} 年",
#                                 font="bold 26px Microsoft YaHei",
#                                 graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="#fff"),
#                             ),
#                         ),
#                     ],
#                 )
#             ],
#         )
#     )

#     pie_data = [[x[0], x[1][0]] for x in map_data]
#     percent_sum = sum([x[1][1] for x in map_data])
#     rest_value = 0
#     for d in map_data:
#         rest_percent = 100.0
#         rest_percent = rest_percent - percent_sum
#         rest_value = d[1][0] * (rest_percent / d[1][1])
#     pie_data.append(["其他省份", rest_value])
#     pie = (
#         Pie()
#         .add(
#             series_name="",
#             data_pair=pie_data,
#             radius=["12%", "20%"],
#             center=["75%", "85%"],
#             itemstyle_opts=opts.ItemStyleOpts(
#                 border_width=1, border_color="rgba(0,0,0,0.3)"
#             ),
#         )
#         .set_global_opts(
#             tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
#             legend_opts=opts.LegendOpts(is_show=False),
#         )
#     )

#     grid_chart = (
#         Grid()
#         .add(
#             bar,
#             grid_opts=opts.GridOpts(
#                 pos_left="10", pos_right="45%", pos_top="70%", pos_bottom="5"
#             ),
#         )
#         .add(pie, grid_opts=opts.GridOpts())
#         .add(map_chart, grid_opts=opts.GridOpts())
#     )

#     return grid_chart


# # Draw Timeline
# time_list = [1980, 2000, 2005, 2010, 2015]
# timeline = Timeline(
#     init_opts=opts.InitOpts(width="1200px", height="800px", theme=ThemeType.DARK)
# )
# for y in time_list:
#     g = get_year_chart(year=y)
#     timeline.add(g, time_point=str(y))

# timeline.add_schema(
#     orient="vertical",
#     is_auto_play=True,
#     is_inverse=True,
#     play_interval=5000,
#     pos_left="null",
#     pos_right="5",
#     pos_top="20",
#     pos_bottom="20",
#     width="50",
#     label_opts=opts.LabelOpts(is_show=True, color="#fff"),
# )

# timeline.render("china_gdp_from_1980.html")
# os.system("china_gdp_from_1980.html")


import pyecharts.options as opts
from pyecharts.charts import WordCloud, Timeline
import os

data = [
    ("生活资源", "999"),
    ("供热管理", "888"),
    ("供气质量", "777"),
    ("生活用水管理", "688"),
    ("一次供水问题", "588"),
    ("交通运输", "516"),
    ("城市交通", "515"),
    ("环境保护", "483"),
    ("房地产管理", "462"),
    ("城乡建设", "449"),
    ("社会保障与福利", "429"),
    ("社会保障", "407"),
    ("文体与教育管理", "406"),
    ("公共安全", "406"),
    ("公交运输管理", "386"),
    ("出租车运营管理", "385"),
    ("供热管理", "375"),
    ("市容环卫", "355"),
    ("自然资源管理", "355"),
    ("粉尘污染", "335"),
    ("噪声污染", "324"),
    ("土地资源管理", "304"),
    ("物业服务与管理", "304"),
    ("医疗卫生", "284"),
    ("粉煤灰污染", "284"),
    ("占道", "284"),
    ("供热发展", "254"),
    ("农村土地规划管理", "254"),
    ("生活噪音", "253"),
    ("供热单位影响", "253"),
    ("城市供电", "223"),
    ("房屋质量与安全", "223"),
    ("大气污染", "223"),
    ("房屋安全", "223"),
    ("文化活动", "223"),
    ("拆迁管理", "223"),
    ("公共设施", "223"),
    ("供气质量", "223"),
    ("供电管理", "223"),
    ("燃气管理", "152"),
    ("教育管理", "152"),
    ("医疗纠纷", "152"),
    ("执法监督", "152"),
    ("设备安全", "152"),
    ("政务建设", "152"),
    ("县区、开发区", "152"),
    ("宏观经济", "152"),
    ("教育管理", "112"),
    ("社会保障", "112"),
    ("生活用水管理", "112"),
    ("物业服务与管理", "112"),
    ("分类列表", "112"),
    ("农业生产", "112"),
    ("二次供水问题", "112"),
    ("城市公共设施", "92"),
    ("拆迁政策咨询", "92"),
    ("物业服务", "92"),
    ("物业管理", "92"),
    ("社会保障保险管理", "92"),
    ("低保管理", "92"),
    ("文娱市场管理", "72"),
    ("城市交通秩序管理", "72"),
    ("执法争议", "72"),
    ("商业烟尘污染", "72"),
    ("占道堆放", "71"),
    ("地上设施", "71"),
    ("水质", "71"),
    ("无水", "71"),
    ("供热单位影响", "71"),
    ("人行道管理", "71"),
    ("主网原因", "71"),
    ("集中供热", "71"),
    ("客运管理", "71"),
    ("国有公交（大巴）管理", "71"),
    ("工业粉尘污染", "71"),
    ("治安案件", "71"),
    ("压力容器安全", "71"),
    ("身份证管理", "71"),
    ("群众健身", "41"),
    ("工业排放污染", "41"),
    ("破坏森林资源", "41"),
    ("市场收费", "41"),
    ("生产资金", "41"),
    ("生产噪声", "41"),
    ("农村低保", "41"),
    ("劳动争议", "41"),
    ("劳动合同争议", "41"),
    ("劳动报酬与福利", "41"),
    ("医疗事故", "21"),
    ("停供", "21"),
    ("基础教育", "21"),
    ("职业教育", "21"),
    ("物业资质管理", "21"),
    ("拆迁补偿", "21"),
    ("设施维护", "21"),
    ("市场外溢", "11"),
    ("占道经营", "11"),
    ("树木管理", "11"),
    ("农村基础设施", "11"),
    ("无水", "11"),
    ("供气质量", "11"),
    ("停气", "11"),
    ("市政府工作部门（含部门管理机构、直属单位）", "11"),
    ("燃气管理", "11"),
    ("市容环卫", "11"),
    ("新闻传媒", "11"),
    ("人才招聘", "11"),
    ("市场环境", "11"),
    ("行政事业收费", "11"),
    ("食品安全与卫生", "11"),
    ("城市交通", "11"),
    ("房地产开发", "11"),
    ("房屋配套问题", "11"),
    ("物业服务", "11"),
    ("物业管理", "11"),
    ("占道", "11"),
    ("园林绿化", "11"),
    ("户籍管理及身份证", "11"),
    ("公交运输管理", "11"),
    ("公路（水路）交通", "11"),
    ("房屋与图纸不符", "11"),
    ("有线电视", "11"),
    ("社会治安", "11"),
]
data2 = [
    ("林业资源", "11"),
    ("其他行政事业收费", "11"),
    ("经营性收费", "11"),
    ("食品安全与卫生", "11"),
    ("体育活动", "11"),
    ("有线电视安装及调试维护", "11"),
    ("低保管理", "11"),
    ("劳动争议", "11"),
    ("社会福利及事务", "11"),
    ("一次供水问题", "11"),]

tl =Timeline()
D= [data,data2]
for i in range(2):
    WC=(
            WordCloud()
            .add(series_name="热点分析", data_pair=D[i], word_size_range=[6, 66])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
        )
    tl.add(WC, "{}年".format(i))
tl.render("basic_wordcloud.html")
os.system("basic_wordcloud.html")