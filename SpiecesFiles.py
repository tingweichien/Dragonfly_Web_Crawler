# https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/
# 透過selenium 操作下拉式選單
# 1.可以用selenium中的select 功能
# 2.因為我可以看到各種蜓種的代碼，而我要requests的URL就是網址+kind_key=代碼

# Reference :
# https://blog.csdn.net/u014519194/article/details/53927149
# https://www.zhihu.com/question/26921730
# https://stackoverflow.com/questions/2241348/what-is-unicode-utf-8-utf-16

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
from DataClass import *
from Index import *

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

# get the latitude and longitude of sprcified species
#"http://dragonfly.idv.tw/dragonfly/tokei.php?kind_key=Megapodagrionidae01"
'''
general_url = "http://dragonfly.idv.tw/dragonfly/"
map_info_url = "tokei.php?kind_key="
'''

family_input = '珈蟌科'
species_input = '白痣珈蟌'

target_url = general_url + map_info_url + Species_class_key[family_input] + Species_key[species_input]
print(target_url)
map_response = session.post(target_url, headers=headers)



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
