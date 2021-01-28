import threading
import queue
import Index
import requests
from Database_function import *


# Worker 類別，負責處理資料
class WeatherDataWorker(threading.Thread):
  def __init__(self, controller, queue, num, response):
    threading.Thread.__init__(self)
    self.response = response
    self.queue = queue
    self.num = num
    self.controller = controller



  def run(self):
    #\ shared variable
    global request_cnt, key_cnt

    #\ The indicator for how many portion of the update will be, this var is to let the progressbar adjest by how many check button been selected.
    progressbar_portion = self.controller.progressbar_portion_calc()

    #\ check the weather request data is vaild or not
    if check_weather_data(self.controller, self.response):

      #\ request data format
      data = {"key": Index.weather_key[key_cnt],
              "q" : f'{self.response["Latitude"]}, {self.response["Longitude"]}',
              "format" : "json",
              "date" : self.response["Dates"],
              "enddate" : self.response["Dates"]
          }


          # limit the request times
          if request_cnt <= Index.weather_request_limit:

              #\ this is the API
              ######################################################################
              weather_r = requests.post(url=Index.OnlineWeatherURL, data=data).json()
              #######################################################################

              #\ count the request time
              request_cnt += 1
              print("request counts: ", str(request_cnt))

              #\ GUI display
              self.controller.Info_FileName_label['text']  = Index.Species_key_fullname_E2C[DB_species]
              self.controller.IStateLabel_text("request counts: "+ str(request_cnt))
              self.controller.progressbar.step((100*progressbar_portion["weather_portion"]) / (len(Index.weather_key) * Index.weather_request_limit))
              self.controller.pbLabel_text()

          else:
              changekey_Info(self)
              request_cnt = 0
              continue

          #\--- problem : if the noraml data will cause error here since there will be no such column or class or object
          #\ check if the error occurred
          # if weather_r["data"]["error"][0]["msg"] == Index.WRE_No_data_available:
          #     continue
          # else:


      #\ Extract the data, extract by hour
      for data_seperate_time in weather_r["data"]["weather"][0]["hourly"]:
          #\ select the corresponding hour
          #\ remove the minutes. i.e. "1800" --> "18", get it from counting back
          respponse_hour = int(data_seperate_time["time"][:-2]) if data_seperate_time["time"] != "0" else 0
          if int(self.response["HOUR(Times)"]) in range(respponse_hour, respponse_hour+3): #\ the response is in three hours interval
              update_weather_data(self,
                                  connection,
                                  DB_species,
                                  data_seperate_time,
                                  self.response["species_info_id"])

