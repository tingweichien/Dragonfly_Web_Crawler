import threading
import queue
import Index
import requests
import Database_function

#\ global lock for the MySQL
MySQL_Lock = threading.Lock()
Check_Lock = threading.Lock()

#\ error log to be reported
ErrorLog =  ""



# Worker 類別，負責處理資料
class WeatherDataWorker(threading.Thread):
  def __init__(self, controller, queue, num, response, DB_species, weather_connection):
    threading.Thread.__init__(self)
    self.response = response
    self.queue = queue
    self.num = num
    self.controller = controller
    self.DB_species = DB_species
    self.weather_connection = weather_connection
    self.KeyChange = False


  #\ the callback function triggered by the thread start
  def run(self):
    global ErrorLog

    #\ The indicator for how many portion of the update will be, this var is to let the progressbar adjest by how many check button been selected.
    progressbar_portion = self.controller.progressbar_portion_calc()

    #\ Get the check status
    Check_Lock.acquire()
    Check_status = Database_function.check_weather_data(self.controller, self.response)
    Check_Lock.release()

    #\ check the weather request data is vaild or not
    if not Check_status:

      #\ request data format
      data = {"key": Index.weather_key[Index.key_cnt],
              "q" : f'{self.response["Latitude"]}, {self.response["Longitude"]}',
              "format" : "json",
              "date" : self.response["Dates"],
              "enddate" : self.response["Dates"]
          }

      try:
        #\ this is the API
        ######################################################################
        weather_r = requests.post(url=Index.OnlineWeatherURL, data=data).json()
        #######################################################################

        #\ @ lock it to let only one get the authorization
        MySQL_Lock.acquire()

        #\ count the request time
        Index.request_cnt += 1
        print("request counts: ", str(Index.request_cnt))

        #\ GUI display
        self.controller.Info_FileName_label['text']  = Index.Species_key_fullname_E2C[self.DB_species]
        self.controller.IStateLabel_text("request counts: "+ str(Index.request_cnt))
        self.controller.progressbar.step((100*progressbar_portion["weather_portion"]) / (len(Index.weather_key) * Index.weather_request_limit))
        self.controller.pbLabel_text()
        self.controller.IFinishStateLabel_text(f"current key {Index.key_cnt} : {Index.weather_key[Index.key_cnt]}")


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
                Database_function.update_weather_data(self.controller,
                                                      self.DB_species,
                                                      data_seperate_time,
                                                      self.response["species_info_id"],
                                                      self.weather_connection)

      #\ something wrong with the weather api
      except:
        ErrorLog = f"[warning] API warning : {weather_r}"
        print(ErrorLog)
        self.KeyChange = True


      #\ @ release the lock
      MySQL_Lock.release()