# https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/
# 透過selenium 操作下拉式選單
# 1.可以用selenium中的select 功能
# 2.因為我可以看到各種蜓種的代碼，而我要requests的URL就是網址+kind_key=代碼

# Reference :
# https://blog.csdn.net/u014519194/article/details/53927149
# https://www.zhihu.com/question/26921730

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
from DataClass import DetailedTableInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
data = {
    'account' : "簡庭威",
    'password' : "tim960622",
}

target_url = "http://dragonfly.idv.tw/dragonfly/tokei.php?kind_key=Megapodagrionidae01"
Login_url = "http://dragonfly.idv.tw/dragonfly/login.php"

session = requests.Session()
Login_response = session.post(Login_url, headers=headers, data=data)


#########################################################
# Method 1



#########################################################
#\ Method2

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
    "纖腰蜻蜓": "58",
}

# get the latitude and longitude of sprcified species
#"http://dragonfly.idv.tw/dragonfly/tokei.php?kind_key=Megapodagrionidae01"
general_url = "http://dragonfly.idv.tw/dragonfly/"
map_info_url = "tokei.php?kind_key="
print("enter the family: ")
family_input = '珈蟌科'
print("enter the species: ")
species_input = '白痣珈蟌'

target_url = general_url + map_info_url + Species_class_key[family_input] + Species_key[species_input]
print(target_url)
map_response = session.post(target_url, headers=headers)

#print(map_response.text)

soup_map = BeautifulSoup(map_response.text, 'html.parser')
# what you'll get
#{
# "latitude":25.136123329501,
# "longitude":121.59439712763,
# "title":"\u5167\u96d9\u6eaa(mhtsou)",                     #地點
# "content":"<div style='font-size: 11px;'>
#           \u8713\u3000\u7a2e \u82bd\u75e3\u8e63\u87cc<br> #蜓種
#           \u65e5\u3000\u671f 2003-04-20\u300017:00:00<br> #日期
#           \u6d77\u3000\u62d4 445 m<br>                    #海拔
#           \u7d00\u9304\u8005 mhtsou                       #紀錄者
#           <\/div>"
# }
map_result = []
map_result_List = []
for map_script in re.split(r'},', soup_map.text):
    #!!!! the return of the re.findall or re.split is a list type, so access the member in the list
    map_result.append(re.findall(r'(?<=latitude\":).+(?=,\"longitude\")', map_script)[0])    # latitude     
    map_result.append(re.findall(r'(?<=longitude\":).+(?=,\"title\")', map_script)[0])    # longitude
    map_result.append(re.findall(r'(?<=title\":\").+(?=\()', map_script)[0].encode('utf-8').decode('unicode_escape'))  # title ,actually is place
    content = re.findall(r'(?<=content\":\").+(?=<)',map_script)[0]
    Date_Time = re.findall(r'(?<=\\u65e5\\u3000\\u671f ).+(?=\\u6d77\\u3000\\u62d4)', content)[0]
    map_result.append(Date_Time.split('\\u3000')[0])  # Date
    map_result.append(Date_Time.split('\\u3000')[1])  # Time
    map_result.append(re.findall(r'(?<=\\u6d77\\u3000\\u62d4 ).+(?=\\u7d00)', map_script)[0]) # Altitude
    map_result.append(re.findall(r'(?<=\\u7d00\\u9304\\u8005 ).+(?=<)', map_script)[0])  #Recorder
    print(map_result)
    map_result_List.append(DetailedTableInfo('-', map_result[3], map_result[4], '-', '-', map_result[2], map_result[5], map_result[6], map_result[0], map_result[1], species_input, '-'))
    map_result.clear()
print('END')
