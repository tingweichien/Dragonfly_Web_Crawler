#\ Put the info and parameter in here

# import
from fake_useragent import UserAgent
import os
from multiprocessing import Process
import multiprocessing

##################################################
# my account and password
myaccount =  None
mypassword = None


# auto save account and password file
Login_path = os.getenv('temp')
Login_Filename = os.path.join(Login_path, 'Password_Account_info.txt')


###################################################
# Gui setting
Login_geometry = "300x330" # Width x Height
MainPageGeometry = "380x520"
updateWinGeometry = "500x350"

# PY GUI setting
Table_scroll_num = 10

# map setting
mapfilename = "map.html"
map_plot_max_data_num = 100
info_box_template = """
    <dl>
    <dt><b>[User]</b></dt><dt>{User}</dt>
    <dt><b>[Dates]</b></dt><dt>{Dates}</dt>
    <dt><b>[Times]</b></dt><dt>{Times}</dt>
    <dt><b>[Place]</b></dt><dt>{Place}</dt>
    <dt><b>[Altitude]</b></dt><dt>{Altitude}</dt>
    <dt><b>[Latitude]</b></dt><dt>{Latitude}</dt>
    <dt><b>[Longitude]</b></dt><dt>{Longitude}</dt>
    </dl>
    """


# ico image path
ico_image_path = 'image\\dragonfly_ico.ico'

# statement in the login page
copyright_text = "Developed by Ting Wei Chien\n 2020/7/26"



###################################################
#\ request url
# general ur
general_url = 'http://dragonfly.idv.tw/dragonfly/'

# 登入
#Login_url = 'http://dragonfly.idv.tw/dragonfly/login.php'
Login_url = general_url + 'login.php'

#Login_url for webdriver
webdriver_Login_url = general_url + 'index.php'

# 蜓種觀察資料查詢作業
#All_Observation_Data_url = 'http://dragonfly.idv.tw/dragonfly/rec_list_view.php'
All_Observation_Data_url = general_url + 'rec_list_view.php'

# Next page url
Next_page_url = general_url + '?pageNum_rs_dragonfly_record='

# 執行簡述 url
Brief_discriptions_url = 'view_data.php?id='

# 執行詳述 url
# http://dragonfly.idv.tw/dragonfly/read_data.php?id=64774
Detailed_discriptions_url = 'read_data.php?id='

# 地圖 url
map_info_url = 'tokei.php?kind_key='

# 蜓轉相關資料一覽 url
# http://dragonfly.idv.tw/dragonfly/rec_list_view_for_key.php?pageNum_rs_dragonfly_record=0&type=total_kind&kind=Chlorocyphidae01
species_all_record_data_first_url = 'rec_list_view_for_key.php'
species_all_record_data_page_url = '?pageNum_rs_dragonfly_record='
species_all_record_data_species_url = '&type=total_kind&kind='

# total number of the species url
# "http://dragonfly.idv.tw/dragonfly/kind_total_records.php"
total_num_species_url = "kind_total_records.php"


# Header
'''
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
'''
#--->Now use random fake user agent
# https://ithelp.ithome.com.tw/articles/10209356
UA = UserAgent()
headers = {
        'User-Agent' : UA.random,
}


# file path
current_path = os.getcwd()

# image path
Image_path = current_path + "\image"

# webdriver to crawl the total number of the record
popup_chrome_web = False


##----crawl dtat to csv----

# chrome driver path
ChromeDriverPath = r".\\chromedriver.exe"

# csv title
CSV_Head = ["Species Family", "Species", "ID", "Date", "Time", "User", "City", "District", "Place", "Altitude", "Latitude", "Longitude", "Description"]


# mutiprocessing cpu number
extra_cpu = 0
maxcpus = extra_cpu + multiprocessing.cpu_count()
cpus = maxcpus

# do multiprocessing or not
do_multiprocessing = True

# state how many row data in one page
data_per_page = 10

# determine how you want to parse the data
# 'parse_a_family' 'parse_all' 'parse_one'
parse_type = 'parse_all'
parse_one_family_name = "幽蟌科"
parse_one_species_name = "短腹幽蟌"


# limit the count for each time looping
limit_cnt = 5000

# first folder for crawling data
folder_all_crawl_data = 'Crawl_Data\\'

# json file path to record the total number of each species
TotalNumberOfSpecies_filepath = folder_all_crawl_data + 'Record_Num_each_species.txt'

# progress window
# state the max frame for the LOAD gif
GIFMAXFRAME = 80




#####################################################################
# Species name
Calopterygidae_Species = [
                # 珈蟌科
                "白痣珈蟌",
                "細胸珈蟌",
                "綠翅珈蟌",
                "中華珈蟌南臺亞種",
                "中華珈蟌指名亞種"]
Chlorocyphidae_Species = [
                # 鼓蟌科
                "脊紋鼓蟌",
                "簾格鼓蟌",
                "棋紋鼓蟌",
                "朱環鼓蟌"]
Coenagrionidae_Species = [
                # 細蟌科
                "針尾細蟌",
                "白粉細蟌",
                "橙尾細蟌",
                "紅腹細蟌",
                "昧影細蟌",
                "黃腹細蟌",
                "朱紅細蟌",
                "亞東細蟌",
                "朝雲細蟌",
                "青紋細蟌",
                "四斑細蟌",
                "月斑細蟌",
                "藍彩細蟌",
                "葦笛細蟌",
                "蔚藍細蟌",
                "錢博細蟌",
                "瘦面細蟌",
                "弓背細蟌",
                "丹頂細蟌"]
Euphaeidae_Species = [
                # 幽蟌科
                "短尾幽蟌",
                "短腹幽蟌"]
Lestidae_Species = [
                # 絲蟌科
                "青紋絲蟌",
                "鑲紋絲蟌",
                "隱紋絲蟌",
                "長痣絲蟌"]
Megapodagrionidae_Species = [
                # 蹣蟌科
                "芽痣蹣蟌"]
Platycnemididae_Species =[
                # 琵蟌科
                "美姿琵蟌",
                "青黑琵蟌",
                "黃尾琵蟌",
                "環紋琵蟌",
                "脛蹼琵蟌"]
Protoneuridae_Species = [
                # 樸蟌科
                "朱背樸蟌",
                "烏齒樸蟌"]
Synlestidae_Species = [
                # 洵蟌科
                "黃腹洵蟌",
                "黃肩洵蟌"]
Aeshnidae_Species = [
                # 晏蜓科
                "泰雅晏蜓",
                "碧翠晏蜓",
                "烏基晏蜓",
                "烏點晏蜓",
                "烏帶晏蜓",
                "麻斑晏蜓",
                "綠胸晏蜓",
                "微刺晏蜓",
                "浡鋏晏蜓",
                "長鋏晏蜓",
                "倭鋏晏蜓",
                "琉球晏蜓",
                "舞鋏晏蜓",
                "柱鋏晏蜓",
                "石垣晏蜓",
                "李斯晏蜓",
                "陽明晏蜓",
                "朱黛晏蜓",
                "描金晏蜓",
                "喙鋏晏蜓",
                "日清晏蜓",
                "源埡晏蜓",
                "刃鋏晏蜓",
                "鉤鋏晏蜓",
                "短鋏晏蜓"]
Cordulegastridae_Species =[
                # 勾蜓科
                "無霸勾蜓",
                "短痣勾蜓",
                "褐翼勾蜓",
                "闊翼勾蜓",
                "斑翼勾蜓"]
Corduliidae_Species = [
                # 弓蜓科
                "慧眼弓蜓",
                "岷峨弓蜓",
                "褐面弓蜓",
                "海神弓蜓",
                "耀沂弓蜓",
                "天王弓蜓",
                "黃尾弓蜓",
                "臺灣弓蜓"]
Gomphidae_Species = [
                # 春蜓科
                "國姓春蜓",
                "長唇春蜓",
                "海南春蜓",
                "雙角春蜓",
                "圓痣春蜓",
                "鉤紋春蜓",
                "蟲莖春蜓",
                "火神春蜓",
                "聯紋春蜓",
                "異紋春蜓",
                "曲尾春蜓",
                "粗鉤春蜓",
                "鉤尾春蜓",
                "紹德春蜓指名亞種",
                "紹德春蜓嘉義亞種",
                "窄胸春蜓",
                "闊腹春蜓",
                "細鉤春蜓",
                "鉸剪春蜓",
                "球角春蜓",
                "錘角春蜓",
                "南山春蜓"]
Libellulidae_Species = [
                # 蜻蜓科
                "粗腰蜻蜓",
                "八仙蜻蜓",
                "橙斑蜻蜓",
                "褐斑蜻蜓",
                "線紋蜻蜓",
                "猩紅蜻蜓",
                "短痣蜻蜓",
                "侏儒蜻蜓",
                "硃紅蜻蜓",
                "海神蜻蜓",
                "廣腹蜻蜓",
                "樹穴蜻蜓",
                "高翔蜻蜓",
                "小紅蜻蜓",
                "漆黑蜻蜓",
                "淺褐蜻蜓",
                "善變蜻蜓",
                "雙截蜻蜓",
                "琥珀蜻蜓",
                "白刃蜻蜓",
                "金黃蜻蜓",
                "扶桑蜻蜓",
                "呂宋蜻蜓",
                "灰黑蜻蜓",
                "霜白蜻蜓西里亞種",
                "霜白蜻蜓中印亞種",
                "杜松蜻蜓",
                "赭黃蜻蜓",
                "鼎脈蜻蜓",
                "薄翅蜻蜓",
                "溪神蜻蜓",
                "黃紉蜻蜓",
                "黑翅蜻蜓",
                "藍黑蜻蜓",
                "賽琳蜻蜓",
                "三角蜻蜓",
                "彩裳蜻蜓",
                "赤衣蜻蜓",
                "長尾蜻蜓",
                "仲夏蜻蜓",
                "秋紅蜻蜓",
                "焰紅蜻蜓",
                "紅脈蜻蜓",
                "褐頂蜻蜓",
                "孔凱蜻蜓",
                "纖紅蜻蜓",
                "黃基蜻蜓",
                "夜遊蜻蜓",
                "海霸蜻蜓微斑亞種",
                "海霸蜻蜓粗斑亞種",
                "大華蜻蜓",
                "紫紅蜻蜓",
                "樂仙蜻蜓",
                "灰脈蜻蜓",
                "褐基蜻蜓",
                "高砂蜻蜓",
                "灰影蜻蜓",
                "纖腰蜻蜓"]


# these are shown for the dropdown list
Species_Family_Name = ["珈蟌科", "鼓蟌科", "細蟌科", "幽蟌科", "絲蟌科", "蹣蟌科", "琵蟌科",
                "樸蟌科", "洵蟌科", "晏蜓科", "勾蜓科", "弓蜓科", "春蜓科", "蜻蜓科"]

Species_Name_Group = [Calopterygidae_Species, Chlorocyphidae_Species, Coenagrionidae_Species,
                    Euphaeidae_Species, Lestidae_Species, Megapodagrionidae_Species, Platycnemididae_Species,
                    Protoneuridae_Species, Synlestidae_Species, Aeshnidae_Species, Cordulegastridae_Species,
                    Corduliidae_Species, Gomphidae_Species, Libellulidae_Species]


# state the family(科) dictionary
Species_class_key = {
    "珈蟌科": "Calopterygidae",
    "鼓蟌科": "Chlorocyphidae",
    "細蟌科": "Coenagrionidae",
    "幽蟌科": "Euphaeidae",
    "絲蟌科": "Lestidae",
    "蹣蟌科": "Megapodagrionidae",
    "琵蟌科": "Platycnemididae",
    "樸蟌科": "Protoneuridae",
    "洵蟌科": "Synlestidae",
    "晏蜓科": "Aeshnidae",
    "勾蜓科": "Cordulegastridae",
    "弓蜓科": "Corduliidae",
    "春蜓科": "Gomphidae",
    "蜻蜓科": "Libellulidae"
}

# state the Species(科) dictionary
Species_key = {
    # 珈蟌科
    "白痣珈蟌": "01",
    "細胸珈蟌": "02",
    "綠翅珈蟌": "03",
    "中華珈蟌南臺亞種": "04",
    "中華珈蟌指名亞種": "05",
    # 鼓蟌科
    "脊紋鼓蟌": "01",
    "簾格鼓蟌": "02",
    "棋紋鼓蟌": "03",
    "朱環鼓蟌": "04",
    # 細蟌科
    "針尾細蟌": "01",
    "白粉細蟌": "02",
    "橙尾細蟌": "03",
    "紅腹細蟌": "04",
    "昧影細蟌": "05",
    "黃腹細蟌": "06",
    "朱紅細蟌": "07",
    "亞東細蟌": "08",
    "朝雲細蟌": "09",
    "青紋細蟌": "10",
    "四斑細蟌": "11",
    "月斑細蟌": "12",
    "藍彩細蟌": "13",
    "葦笛細蟌": "14",
    "蔚藍細蟌": "15",
    "錢博細蟌": "16",
    "瘦面細蟌": "17",
    "弓背細蟌": "18",
    "丹頂細蟌": "19",
    # 幽蟌科
    "短尾幽蟌": "01",
    "短腹幽蟌": "02",
    # 絲蟌科
    "青紋絲蟌": "01",
    "鑲紋絲蟌": "02",
    "隱紋絲蟌": "03",
    "長痣絲蟌": "04",
    # 蹣蟌科
    "芽痣蹣蟌": "01",
    # 琵蟌科
    "美姿琵蟌": "01",
    "青黑琵蟌": "02",
    "黃尾琵蟌": "03",
    "環紋琵蟌": "04",
    "脛蹼琵蟌": "05",
    # 樸蟌科
    "朱背樸蟌": "01",
    "烏齒樸蟌": "02",
    # 洵蟌科
    "黃腹洵蟌": "01",
    "黃肩洵蟌": "02",
    # 晏蜓科
    "泰雅晏蜓": "01",
    "碧翠晏蜓": "02",
    "烏基晏蜓": "03",
    "烏點晏蜓": "04",
    "烏帶晏蜓": "05",
    "麻斑晏蜓": "06",
    "綠胸晏蜓": "07",
    "微刺晏蜓": "08",
    "浡鋏晏蜓": "09",
    "長鋏晏蜓": "10",
    "倭鋏晏蜓": "11",
    "琉球晏蜓": "12",
    "舞鋏晏蜓": "13",
    "柱鋏晏蜓": "14",
    "石垣晏蜓": "15",
    "李斯晏蜓": "16",
    "陽明晏蜓": "17",
    "朱黛晏蜓": "18",
    "描金晏蜓": "19",
    "喙鋏晏蜓": "20",
    "日清晏蜓": "21",
    "源埡晏蜓": "22",
    "刃鋏晏蜓": "23",
    "鉤鋏晏蜓": "24",
    "短鋏晏蜓": "25",
    # 勾蜓科
    "無霸勾蜓": "01",
    "短痣勾蜓": "02",
    "褐翼勾蜓": "03",
    "闊翼勾蜓": "04",
    "斑翼勾蜓": "05",
    # 弓蜓科
    "慧眼弓蜓": "01",
    "岷峨弓蜓": "02",
    "褐面弓蜓": "03",
    "海神弓蜓": "04",
    "耀沂弓蜓": "05",
    "天王弓蜓": "06",
    "黃尾弓蜓": "07",
    "臺灣弓蜓": "08",
    # 春蜓科
    "國姓春蜓": "01",
    "長唇春蜓": "02",
    "海南春蜓": "03",
    "雙角春蜓": "04",
    "圓痣春蜓": "05",
    "鉤紋春蜓": "06",
    "蟲莖春蜓": "07",
    "火神春蜓": "08",
    "聯紋春蜓": "09",
    "異紋春蜓": "10",
    "曲尾春蜓": "11",
    "粗鉤春蜓": "12",
    "鉤尾春蜓": "13",
    "紹德春蜓指名亞種": "14",
    "紹德春蜓嘉義亞種": "15",
    "窄胸春蜓": "16",
    "闊腹春蜓": "17",
    "細鉤春蜓": "18",
    "鉸剪春蜓": "19",
    "球角春蜓": "20",
    "錘角春蜓": "21",
    "南山春蜓": "22",
    # 蜻蜓科
    "粗腰蜻蜓": "01",
    "八仙蜻蜓": "02",
    "橙斑蜻蜓": "03",
    "褐斑蜻蜓": "04",
    "線紋蜻蜓": "05",
    "猩紅蜻蜓": "06",
    "短痣蜻蜓": "07",
    "侏儒蜻蜓": "08",
    "硃紅蜻蜓": "09",
    "海神蜻蜓": "10",
    "廣腹蜻蜓": "11",
    "樹穴蜻蜓": "12",
    "高翔蜻蜓": "13",
    "小紅蜻蜓": "14",
    "漆黑蜻蜓": "15",
    "淺褐蜻蜓": "16",
    "善變蜻蜓": "17",
    "雙截蜻蜓": "18",
    "琥珀蜻蜓": "19",
    "白刃蜻蜓": "20",
    "金黃蜻蜓": "21",
    "扶桑蜻蜓": "22",
    "呂宋蜻蜓": "23",
    "灰黑蜻蜓": "24",
    "霜白蜻蜓西里亞種": "25",
    "霜白蜻蜓中印亞種": "26",
    "杜松蜻蜓": "27",
    "赭黃蜻蜓": "28",
    "鼎脈蜻蜓": "29",
    "薄翅蜻蜓": "30",
    "溪神蜻蜓": "31",
    "黃紉蜻蜓": "32",
    "黑翅蜻蜓": "33",
    "藍黑蜻蜓": "34",
    "賽琳蜻蜓": "35",
    "三角蜻蜓": "36",
    "彩裳蜻蜓": "37",
    "赤衣蜻蜓": "38",
    "長尾蜻蜓": "39",
    "仲夏蜻蜓": "40",
    "秋紅蜻蜓": "41",
    "焰紅蜻蜓": "42",
    "紅脈蜻蜓": "43",
    "褐頂蜻蜓": "44",
    "孔凱蜻蜓": "45",
    "纖紅蜻蜓": "46",
    "黃基蜻蜓": "47",
    "夜遊蜻蜓": "48",
    "海霸蜻蜓微斑亞種": "49",
    "海霸蜻蜓粗斑亞種": "50",
    "大華蜻蜓": "51",
    "紫紅蜻蜓": "52",
    "樂仙蜻蜓": "53",
    "灰脈蜻蜓": "54",
    "褐基蜻蜓": "55",
    "高砂蜻蜓": "56",
    "灰影蜻蜓": "57",
    "纖腰蜻蜓": "58"
}

#\ Species_key keys to list
#\ This will be an ordered list of species name that can be used to count for index
#\ will be used in database
Species_key_keys_list = Species_key.keys()

#\ Species_key value to list
Species_key_values_list = Species_key.values()
