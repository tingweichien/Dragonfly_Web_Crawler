import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
#\ Login account and password
data = {
    'account' : '簡庭威',
    'password' : 'tim960622',
}

###################################################
#\ request url
# general ur 
general_url = 'http://dragonfly.idv.tw/dragonfly/'

# 登入
#Login_url = 'http://dragonfly.idv.tw/dragonfly/login.php'
Login_url = general_url + 'login.php'

# 蜓種觀察資料查詢作業
#All_observation_Data_url = 'http://dragonfly.idv.tw/dragonfly/rec_list_view.php'
All_observation_Data_url = general_url + 'rec_list_view.php'

# Next page url
Next_page_url = general_url + '?pageNum_rs_dragonfly_record='

# 執行簡述 url
Brief_discriptions_url = 'view_data.php?id='

# 執行詳述 url
# http://dragonfly.idv.tw/dragonfly/read_data.php?id=64774
Detailed_discriptions_url = 'read_data.php?id='

###################################################
#\ 執行登入
session = requests.Session()
session.post(Login_url, headers=headers, data=data)

#\ 執行進入"蜓種觀察資料查詢作業"
response = session.post(All_observation_Data_url, headers=headers)
#print(response.text);

#\ 下一頁
'''
page = 1
response_next_page = session.post(All_observation_Data_url + Next_page_url + str(page), headers=headers)
#print(response_next_page.text)
'''

#\ 執行點入簡述
# request url = http://dragonfly.idv.tw/dragonfly/view_data.php?id=65431
'''
id = 65431
response_Brief_discriptions = session.post(general_url + Brief_discriptions_url + str(id), headers=headers)
print(response_Brief_discriptions.text)
'''

#\ 執行詳述
# request url = http://dragonfly.idv.tw/dragonfly/read_data.php?id=65431
id = 64774
response_Detailed_discriptions = session.post(general_url + Detailed_discriptions_url + str(id), headers=headers)
soup = BeautifulSoup(response_Detailed_discriptions.text, 'html.parser')
Longitude = soup.find(id = 'R_LNG').get('value')
print('經度 : ' + Longitude)
Lateral = soup.find(id = 'R_LAT').get('value')
print('緯度 : ' + Lateral)


#\ 嘗試非自己可以看的詳細內容
# id = 65430
print('Enter the id: ')
id = input()
response_Detailed_discriptions2 = session.post(general_url + Detailed_discriptions_url + str(id), headers=headers)
soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
Longitude = soup2.find(id = 'R_LNG').get('value')
print('經度 : ' + Longitude)
Lateral = soup2.find(id = 'R_LAT').get('value')
print('緯度 : ' + Lateral)

"""
target_url = 'http://dragonfly.idv.tw/dragonfly/member_center.php'
response = session.get(target_url, headers=headers)
print(response.text);
"""