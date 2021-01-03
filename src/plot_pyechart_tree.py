#\ pls use pyecharts v1
#\ this is the plot by using pyechart

import json
from pyecharts import options as opts
from pyecharts.charts import Tree, Bar
from Index import *
from pyecharts.commons.utils import JsCode
import webview

#\ specify the tree data
# reference:
# (1) https://pyecharts.org/#/zh-cn/series_options?id=labelopts%ef%bc%9a%e6%a0%87%e7%ad%be%e9%85%8d%e7%bd%ae%e9%a1%b9
# (2) https://pyecharts.readthedocs.io/zh/latest/en-us/charts_base/#tree
#
# {
#     Tchildren: [],
#     Tname:"",
# }
#

Tchildren = "children"
Tname = "name"
Tvalue = "value"

Family_group = []
Family_group_all = []
family_count = 0
for suborder_count, sb in enumerate([Species_Name_Group_Damselfly, Species_Name_Group_Dragonfly]):
    for species_names in sb:
        family = {Tchildren: [{Tvalue: Species_Family_Name_E[family_count] + str(number+1), Tname: value} for number,value in enumerate(species_names)],
                Tname: Species_Family_Name[family_count],
                Tvalue: Species_Family_Name_E[family_count]}
        family_count += 1

        #\ combine 科別(infraorder)
        Family_group.append(family)

    #\ combine 亞目類別(order)
    Family_group_all.append({Tchildren:Family_group.copy(), Tname:species_SubOrder[suborder_count], Tvalue:species_SubOrder_E[suborder_count]})
    Family_group.clear()

#\ combine all the children together
TData = [{Tchildren:Family_group_all, Tname:species_Order}]

#\ selecting the type of the tree plot
tree_layout = "orthogonal"  #"radial"
tree_leaves_position = "right" #"top"


#\ tooltip formatter
# reference : https://blog.csdn.net/hula1108/article/details/93211095
tooltip_F = JsCode("""function (params){
                        return params.value;
                    }""")

#\ specify the tree plot
tree = Tree(init_opts=opts.InitOpts(width="1800px", height="900px"))
tree.add(series_name = "",
        data = TData,
        initial_tree_depth = 2,
        edge_fork_position = '70%',
        collapse_interval = 0,
        pos_top = "2%", pos_bottom = "5%",
        layout = tree_layout,
        label_opts = opts.LabelOpts(position = "top"),
        leaves_label_opts = opts.LabelOpts(position = tree_leaves_position, distance = 4),
        tooltip_opts=opts.TooltipOpts(formatter=tooltip_F),
        )
tree.get_options()
tree.render("pyechart_results\Dragonfly_tree_plot.html")

webview.create_window("HTML window", "pyechart_results\Dragonfly_tree_plot.html")
webview.start(http_server=True, gui='qt')
