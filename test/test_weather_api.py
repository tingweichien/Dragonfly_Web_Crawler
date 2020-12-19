'''
World weather online
https://www.worldweatheronline.com/developer/premium-api-explorer.aspx
'''

import requests
import json
#\api keys
key = ["190ec7d0ebfe4c7992f161552201012",  "4a28a928fa024ac6aa1174831201212"]
LatLon = "25.33, 121.228"
startdate = "2020-9-10"
enddate = "2020-9-10"

data = {"key": key[0],
        "q" : LatLon,
        "format" : "json",
        "date" : startdate,
        "enddate" : enddate,
        }
r = requests.post(url="http://api.worldweatheronline.com/premium/v1/past-weather.ashx",data=data).json()

for data_seperate_time in r["data"]["weather"][0]["hourly"]:
        print(json.dumps(data_seperate_time, indent=2))
        print("///////////////////////////////////////////////")

#\ data I want
#\ "tempC": "29", "FeelsLikeC": "33", "windspeedKmph" : "5", "winddirDegree": "180", "winddir16Point": "S", "humidity": "76",
# "weatherDesc": [
#     {
#       "value": "Patchy rain possible"
#     }
#   ],

