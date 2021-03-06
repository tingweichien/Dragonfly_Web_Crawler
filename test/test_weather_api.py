'''
World weather online
https://www.worldweatheronline.com/developer/premium-api-explorer.aspx
'''

import requests
import json
#\api keys
# key = ["190ec7d0ebfe4c7992f161552201012",  "4a28a928fa024ac6aa1174831201212"]
# LatLon = "25.33, 121.228"
# startdate = "2020-9-10"
# enddate = "2020-9-10"

# data = {"key": key[0],
#         "q" : LatLon,
#         "format" : "json",
#         "date" : startdate,
#         "enddate" : enddate,
#         }
# r = requests.post(url="http://api.worldweatheronline.com/premium/v1/past-weather.ashx",data=data).json()

# for data_seperate_time in r["data"]["weather"][0]["hourly"]:
#         print(json.dumps(data_seperate_time, indent=2))
#         print("///////////////////////////////////////////////")

#\ data I want
#\ "tempC": "29", "FeelsLikeC": "33", "windspeedKmph" : "5", "winddirDegree": "180", "winddir16Point": "S", "humidity": "76",
# "weatherDesc": [
#     {
#       "value": "Patchy rain possible"
#     }
#   ],



###########################ｗｉｎｄｙ


# result = requests.get(url = "https://api.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid=ef759779eb91210f0c0207e5439fa748").json()
para = {"lat":35,"lon":139, "units":"metric", "dt":1609444310, "appid":"ef759779eb91210f0c0207e5439fa748"}
result = requests.get(url = "http://api.openweathermap.org/data/2.5/onecall/timemachine", params=para).json()
print(json.dumps(result, indent=2))