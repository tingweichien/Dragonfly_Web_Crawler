# reference
# https://www.itread01.com/content/1546805191.html


import requests
from bs4 import BeautifulSoup
import DataClass
import re
import Index
from multiprocessing import Process, Pool, Value, Lock
from typing import List
import proxyscrape
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# global
session = requests.session()
session.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))

stop_crawl_all_data_mp = False

DataCNT = Value('i', 0)
BoolClearDataCntAccuForProgressbar = Value('i', False)

TotalCount = 0

DataCNT_lock = Lock()

##################################################################

#\ Proxy auto crawling
#\ by proxyscrape 0.3.0
#\ https://pypi.org/project/proxyscrape/
def get_proxy()->list:
    collector = proxyscrape.create_collector('default', 'https')  # Create a collector for http resources
    proxy = collector.get_proxy({'country': 'united states'})  # Retrieve a united states proxy
    print(f"proxy: {proxy}")
    return proxy



#\ Login
"""
params:
    account
    password
return:
    session
    Login_Response
    Login_state
"""
def Login_Web(Input_account:str, Input_password:str):
    #\ Login account and password
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }

    Login_state = True
    re_try = 0
    #\ retry for certain times if failed
    while re_try < Index.re_try_limit:
        try:
            #\ auto get the proxy
            #get_proxy()
            try:
                list_len = len(Index.proxy_list)
                loginStatus = requests.get(Index.Login_url, proxies=Index.proxy_list[re_try % list_len])
                Login_type = "proxy"
            except:
                loginStatus = requests.get(Index.Login_url)
                Login_type = "No proxy"

            print(f"[INFO]  login type: {Login_type}, login status: {loginStatus}")


        except:
            #\ print the retry
            re_try += 1
            print(f"[INFO]  retry: {re_try}")


        else:
            #\ 執行登入
            Login_Response = session.post(Index.Login_url, headers=Index.headers, data=data)

            #\ 確認是否成功登入
            # print(f"[INFO] Login response text : \n {Login_Response.text}")
            soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
            script = soup_login_ckeck.find("script") # find the alert
            try :
                alert = re.findall(r'(?<=alert\(\").+(?=\")', script.contents[0]) #\r\n    alert("登入失敗，請重新登入");\r\n

            except :
                alert = ""

            if (len(alert) > 0):
                Login_state = False # to show the error that the password or account might be wrong
            else:
                Login_state = True
            return [session, Login_Response, Login_state]

    #\ retry failed
    print("[waning] Login failed")
    return [None, None, None]


###################################################################
def DataCrawler(Login_Response, Input_ID:str)->list:
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
    All_Observation_Data_response = session.post(Index.All_Observation_Data_url, headers=Index.headers)


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
    """
    Data_List = []
    tmp_List = []
    soup = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    for All_Observation_Data_response_Data_Set in soup.find_all(id='theRow'):
        for All_Observation_Data_response_Data in All_Observation_Data_response_Data_Set.find_all('td'):
            # check if the wanted data crawl to the last and avoid the unwanted data
            if All_Observation_Data_response_Data.text == '簡述':
                Data_List.append(simplifyTableInfo(tmp_List[0], tmp_List[1], tmp_List[2], tmp_List[3], tmp_List[4], tmp_List[5], tmp_List[6], tmp_List[7]))
                tmp_List.clear()
                break
            tmp_List.append(All_Observation_Data_response_Data.text)

    for obj in Data_List:
        print(obj, sep =' ')


    #\ 執行GUI input
    #\確認是否成功登入
    soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
    script = soup_login_ckeck.find("script").extract() # find the alert
    alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text) #\r\n    alert("登入失敗，請重新登入");\r\n
    if (len(alert) > 0):
        return [ErrorID["Login_error"], ErrorID["Login_error"]] # to show the error that the password or account might be wrong
    """

    #\先確ID認是否超處範圍
    overflow = False
    soup_ID_check = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    All_Observation_Data_response_Data_Set = soup_ID_check.find(id='theRow')
    Max_All_Observation_Data_response_Data = All_Observation_Data_response_Data_Set.find_all('td')
    Max_ID_Num = Max_All_Observation_Data_response_Data[0].text
    #\check if the ID is out of the range
    if (int(Input_ID) > int(Max_All_Observation_Data_response_Data[0].text) or int(Input_ID) < 0):
        overflow = True
        ID_find_result = []
    else:
        #\ 執行
        response_Detailed_discriptions2 = session.post(Index.general_url + Index.Detailed_discriptions_url + Input_ID, headers=Index.headers)
        soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
        Longitude = soup2.find(id = 'R_LNG').get('value')
        print('經度 : ' + Longitude)
        Lateral = soup2.find(id = 'R_LAT').get('value')
        print('緯度 : ' + Lateral)
        ID_find_result = DataClass.DetailedTableInfo(Input_ID,
                                            soup2.find(id='日期').get('value'),
                                            soup2.find(id='時間').get('value'),
                                            "",
                                            "",
                                            soup2.find(id='地點').get('value'),
                                            soup2.find(id='R_ELEVATION').get('value'),
                                            soup2.find(id='紀錄者').get('value'),
                                            soup2.find(id='R_LAT').get('value'),
                                            soup2.find(id='R_LNG').get('value'),
                                            "",
                                            "",
                                            soup2.find(id='R_MEMO').get('value'))

    return [ID_find_result, overflow, int(Max_ID_Num)]



###############################################################################################
#\ get the data from map
# https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/
# 透過selenium 操作下拉式選單
# 1.可以用selenium中的select 功能
# 2.因為我可以看到各種蜓種的代碼，而我要requests的URL就是網址+kind_key=代碼

# Reference :
# https://blog.csdn.net/u014519194/article/details/53927149
# https://www.zhihu.com/question/26921730
# https://stackoverflow.com/questions/2241348/what-is-unicode-utf-8-utf-16

def SpeiciesCrawler(family_input:str, species_input:str)->list:
    '''
    family_input = '珈蟌科'
    species_input = '白痣珈蟌'
    '''

    target_url = Index.general_url + Index.map_info_url + Index.Species_class_key[family_input] + Index.Species_key[species_input]
    #print(target_url)
    map_response = session.post(target_url, headers=Index.headers)



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
    split_all_to_one_DetailedInfo = re.split(r'},', soup_map.text)
    if (len(split_all_to_one_DetailedInfo) > 1):    #'{"markers":[]}@@@@@@@@' --> this is what zero result will be
        for map_script in split_all_to_one_DetailedInfo:
            #!!!! the return of the re.findall or re.split is a list type, so access the member in the list, add XXXX[0]
            map_result.append(re.findall(r'(?<=latitude\":).+(?=,\"longitude\")', map_script)[0])    # latitude
            map_result.append(re.findall(r'(?<=longitude\":).+(?=,\"title\")', map_script)[0])    # longitude
            map_result.append(re.findall(r'(?<=title\":\").+(?=\()', map_script)[0].encode('utf-8').decode('unicode_escape'))  # title ,actually is place
            content = re.findall(r'(?<=content\":\").+(?=<)',map_script)[0]
            Date_Time = re.findall(r'(?<=\\u65e5\\u3000\\u671f ).+(?=\\u6d77\\u3000\\u62d4)', content)[0]
            map_result.append(Date_Time.split('\\u3000')[0])  # Date
            map_result.append(Date_Time.split('\\u3000')[1])  # Time
            map_result.append(re.findall(r'(?<=\\u6d77\\u3000\\u62d4 ).+(?=\\u7d00)', map_script)[0]) # Altitude
            map_result.append(re.findall(r'(?<=\\u7d00\\u9304\\u8005 ).+(?=<)', map_script)[0].encode('utf-8').decode('unicode_escape'))  #Recorder
            map_result_List.append(DataClass.DetailedTableInfo('-', map_result[3], map_result[4], '-', '-', map_result[2], map_result[5], map_result[6], map_result[0], map_result[1], family_input, species_input, '-'))
            map_result.clear()

    return map_result_List



##########################################
#\ --- not using (use multithread crawl_all_data_mp2 instead) ---
#\ crawl the detailed info to the database
# from <23.各蜓種紀錄總筆數查詢>
# crawl to the next is empty, the next page id show empty data in the table
# multithread : https://www.maxlist.xyz/2020/03/20/multi-processing-pool/
def crawl_all_data(Web_rawl_Species_family_name:str, Web_rawl_Species_name:str, Total_num:int, Limit_CNT:int, oldID:int)->List[DataClass.DetailedTableInfo]:
    #\ 執行進入"蜓種觀察資料查詢作業"
    page = 0
    DataCNT = 0
    id = 0
    Data_List = []
    tmp_List = []

    while True:
        Species_all_record_data = session.post( Index.general_url +
                                                Index.species_all_record_data_first_url +
                                                Index.species_all_record_data_page_url + str(page) +
                                                Index.species_all_record_data_species_url +
                                                Index.Species_class_key[Web_rawl_Species_family_name] +
                                                Index.Species_key[Web_rawl_Species_name],
                                                headers=Index.headers)

        soup = BeautifulSoup(Species_all_record_data.text, 'html.parser')
        for Species_all_record_data_Data_Set in soup.find_all(id='theRow'):
            tmp_List = Species_all_record_data_Data_Set.find_all('td')

            # End condition
            # 1.no data in next page
            # 2.for update to find unti the old data by inspecting its ID
            # 3.if it count over the the limit count
            id = tmp_List[0].text
            if (len(id) == 0) or (int(id) == oldID) or (DataCNT == Limit_CNT):
                #print(' --Finish crawl--' + ' crawl to page: '+ str(page) + ", ID: " + id + ", count: " + str(DataCNT))
                return Data_List

            response_DetailedInfo = session.post(Index.general_url + Index.Detailed_discriptions_url + id, headers=Index.headers)
            soup2 = BeautifulSoup(response_DetailedInfo.text, 'html.parser')
            Data_List.append(DataClass.DetailedTableInfo(tmp_List[0].text,
                                                tmp_List[1].text,
                                                tmp_List[2].text,
                                                tmp_List[3].text,
                                                tmp_List[4].text,
                                                tmp_List[5].text,
                                                tmp_List[7].text,
                                                tmp_List[6].text,
                                                soup2.find(id='R_LAT').get('value'),  # type: ignore
                                                soup2.find(id='R_LNG').get('value'),  # type: ignore
                                                Web_rawl_Species_family_name,
                                                Web_rawl_Species_name,
                                                soup2.find(id='R_MEMO').get('value')))  # type: ignore
            DataCNT += 1
            print("Current finished datas >> " +
                    str(DataCNT) + " /" + str(Total_num) +
                    " (" + str(int(DataCNT * 100 / Total_num)) + "%)", end='\r')

        page += 1


###########################################################
#\ multiprocessing ver
#\ init pool
def init(*args):
    global DataCNT
    DataCNT = args[0]



#\ multiprocessing
def crawl_all_data_mp2(session, Web_rawl_Species_family_name:str,
                       Web_rawl_Species_name:str,
                       expecting_CNT:int,
                       expecting_page:int,
                       remain_data_Last_page:int,
                       page:int)->List[DataClass.DetailedTableInfo]:
    #\ 執行進入"蜓種觀察資料查詢作業"
    global DataCNT, DataCNT_lock
    tmp_List = []
    Data_List = []
    Species_all_record_data = session.get( Index.general_url +
                                            Index.species_all_record_data_first_url +
                                            Index.species_all_record_data_page_url + str(page) +
                                            Index.species_all_record_data_species_url +
                                            Index.Species_class_key[Web_rawl_Species_family_name] +
                                            Index.Species_key[Web_rawl_Species_name],
                                            headers=Index.headers,
                                            timeout=Index.requestTimeOut)

    soup = BeautifulSoup(Species_all_record_data.text, 'html.parser')
    Row_Data = soup.find_all(id='theRow')
    if page == expecting_page:
        del Row_Data[remain_data_Last_page:]

    for Species_all_record_data_Data_Set in Row_Data:
        tmp_List = Species_all_record_data_Data_Set.find_all('td')
        id = tmp_List[0].text
        # response_DetailedInfo = session.get(Index.general_url + Index.Detailed_discriptions_url + id, headers=Index.headers, timeout=Index.requests_timeout)
        response_DetailedInfo = session.get(Index.general_url + Index.Detailed_discriptions_url + id, headers=Index.headers)
        soup2 = BeautifulSoup(response_DetailedInfo.text, 'html.parser')
        Data_List.append(DataClass.DetailedTableInfo(tmp_List[0].text, tmp_List[1].text, tmp_List[2].text, tmp_List[3].text, tmp_List[4].text, tmp_List[5].text, tmp_List[7].text, tmp_List[6].text,
                                            soup2.find(id='R_LAT').get('value'),  # type: ignore
                                            soup2.find(id='R_LNG').get('value'),  # type: ignore
                                            Web_rawl_Species_family_name,
                                            Web_rawl_Species_name,
                                            soup2.find(id='R_MEMO').get('value')))  # type: ignore


        #\ counts for the crawling times
        # DataCNT_lock = Lock()
        with DataCNT_lock:
            DataCNT.value += 1
            print("\r[Multi-process] Current Progress >> " +
                    str(DataCNT.value) + " / " + str(expecting_CNT) +
                    " (" + str(int((DataCNT.value) * 100 / expecting_CNT)) + "%)", end='\r')

    return Data_List



### <<< unsolve

#\ update weather data on web2 while crawling the dragonfly data
#\ crawl the dragonfly and weathe data and write both of them to the MySQL database onces.
#\ Open weahter api at https://openweathermap.org/api
# def weatherData(self, connection, date, time, LAT, LNG):
#     dt_datetime = datetime.strptime(date+time, "%Y-%m-%d %H:%M:%S")
#     dt = datetime.timestamp(dt_datetime)
#     para = {"lat":LAT,
#             "lon":LNG,
#             "dt":dt,
#             "units":"metric",
#             "appid":Index.OpenWeatherKey}

#     #\ api request
#     response = requests.get(url = Index.OpenWeahterURL, params=para).json()
#     weather = f"""'{{"tempC" : { response["tempC"].replace(" ", "") }, \
# "FeelsLikeC" : { response["FeelsLikeC"].replace(" ", "") }, \
# "windspeedKmph" : { response["windspeedKmph"].replace(" ", "") }, \
# "winddirDegree" : { response["winddirDegree"].replace(" ", "") }, \
# "winddir16Point" : "{ response["winddir16Point"].replace(" ", "") }", \
# "humidity" : { response["humidity"].replace(" ", "") }}}'"""
#     return weather

### >>>unsolve



 ################################################################
#\ find the total data of the species
#\ using the webdriver in this method, actually you can use webdriver in login also
#\ input  : None
#\ output : {"白痣珈蟌": "10000", "舞鋏晏蜓": "95", ....}

def Find_species_total_data():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options



    options = Options()
    # 關閉瀏覽器跳出訊息
    # 不開啟實體瀏覽器背景執行
    if not Index.popup_chrome_web:
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')


    driver = webdriver.Chrome(executable_path = Index.chromedriver_path, chrome_options = options)
    driver.get(Index.webdriver_Login_url)
    driver.find_element_by_name("account").send_keys(Index.myaccount)
    driver.find_element_by_name("password").send_keys(Index.mypassword)
    driver.find_element_by_name("login").click()
    driver.get(Index.general_url + Index.total_num_species_url) #\ "http://dragonfly.idv.tw/dragonfly/kind_total_records.php"
    label_list = driver.find_elements_by_tag_name("label")
    label_list_text = [label_tmp.text for label_tmp in label_list]
    td_list = driver.find_elements_by_tag_name("td")
    td_list_text = [td_tmp.text for td_tmp in td_list]

    Dictionary = dict()

    for td_list_text_tmp in td_list_text:
        if td_list_text_tmp in label_list_text:
            number = td_list_text[(td_list_text.index(td_list_text_tmp)) + 1]
            if number == ' ' :
                number = '0'
            Dictionary[td_list_text_tmp.split('.')[1].strip()] = number
    driver.quit()

    #\ Temp WA for 黑翅蜻蜓, Since this has been removed on the remote website
    #\ Keep the current data and let it go
    #\ need to modify the all content again
    Dictionary["黑翅蜻蜓"] = 0

    return Dictionary

