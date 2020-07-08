import requests
from bs4 import BeautifulSoup
import DataClass
from DataClass import *
import re
from Index import *


########################
ErrorID = {
    "Login_error": -1,
    "ID_overflow": -2
}

session = requests.Session()


##################################################################
def Login_Web(Input_account, Input_password):
    #\ Login account and password
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }
    Login_state = True

    #\ 執行登入
    Login_Response = session.post(Login_url, headers=headers, data=data)

    #\確認是否成功登入
    soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
    script = soup_login_ckeck.find("script").extract() # find the alert
    alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text) #\r\n    alert("登入失敗，請重新登入");\r\n  
    if (len(alert) > 0):
       Login_state = False # to show the error that the password or account might be wrong

    return [Login_Response, Login_state]
      


###################################################################
def DataCrawler(Login_Response, Input_ID):
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    '''
    
    #\ Login account and password
    '''
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }
    '''

    
    
    #\ 執行登入
    '''
    session = requests.Session()
    Login_Response = session.post(Login_url, headers=headers, data=data)
    '''


    #\ 執行進入"蜓種觀察資料查詢作業"
    All_Observation_Data_response = session.post(All_Observation_Data_url, headers=headers)

    
    #\ 下一頁
    '''
    page = 1
    response_next_page = session.post(All_Observation_Data_url + Next_page_url + str(page), headers=headers)
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
    '''
    id = 64774
    response_Detailed_discriptions = session.post(general_url + Detailed_discriptions_url + str(id), headers=headers)
    soup = BeautifulSoup(response_Detailed_discriptions.text, 'html.parser')
    Longitude = soup.find(id = 'R_LNG').get('value')
    print('經度 : ' + Longitude)
    Lateral = soup.find(id = 'R_LAT').get('value')
    print('緯度 : ' + Lateral)
    '''

    
    #\ 嘗試非自己可以看的詳細內容
    '''
    id = 65430
    response_Detailed_discriptions2 = session.post(general_url + Detailed_discriptions_url + str(id), headers=headers)
    soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
    Longitude = soup2.find(id = 'R_LNG').get('value')
    print('經度 : ' + Longitude)
    Lateral = soup2.find(id = 'R_LAT').get('value')
    print('緯度 : ' + Lateral)
    '''


    '''
    target_url = 'http://dragonfly.idv.tw/dragonfly/member_center.php'
    response = session.get(target_url, headers=headers)
    print(response.text);
    '''



    #\ 解析資料
    '''
    Data_List = []
    tmp_List = []
    soup = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    for All_Observation_Data_response_Data_Set in soup.find_all(id='theRow'):
        for All_Observation_Data_response_Data in All_Observation_Data_response_Data_Set.find_all('td'):
            # check if the wanted data crawl to the last and avoid the unwanted data
            if All_Observation_Data_response_Data.text == '簡述':
                Data_List.append(simplifyTableInfo(tmp_List[0], tmp_List[1], tmp_List[2], tmp_List[3], tmp_List[4], tmp_List[5], tmp_List[6], tmp_Listp[7]))
                tmp_List.clear()
                break
            tmp_List.append(All_Observation_Data_response_Data.text)
            
    for obj in Data_List:
        print(obj, sep =' ')
    '''

    '''
    #\ 執行GUI input
    #\確認是否成功登入
    soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
    script = soup_login_ckeck.find("script").extract() # find the alert
    alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text) #\r\n    alert("登入失敗，請重新登入");\r\n  
    if (len(alert) > 0):
        return [ErrorID["Login_error"], ErrorID["Login_error"]] # to show the error that the password or account might be wrong
    '''

    #\先確ID認是否超處範圍
    id = Input_ID
    soup_ID_check = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    All_Observation_Data_response_Data_Set = soup_ID_check.find(id='theRow')
    Max_All_Observation_Data_response_Data = All_Observation_Data_response_Data_Set.find_all('td')
    #print('Max = ' + Max_All_Observation_Data_response_Data[0].text)
    if (int(id) > int(Max_All_Observation_Data_response_Data[0].text) or int(id) < 0):
        return [ErrorID["ID_overflow"], ErrorID["ID_overflow"]] # to show the error that the ID number is out of range

    #\ 執行 
    response_Detailed_discriptions2 = session.post(general_url + Detailed_discriptions_url + id, headers=headers)
    soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
    Longitude = soup2.find(id = 'R_LNG').get('value')
    print('經度 : ' + Longitude)
    Lateral = soup2.find(id = 'R_LAT').get('value')
    print('緯度 : ' + Lateral)

    return [Longitude, Lateral]



###############################################################################################
def SpeiciesCrawler(Login_Response, family_input, species_input):
    '''
    family_input = '珈蟌科'
    species_input = '白痣珈蟌'
    '''

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

    return map_result_List

