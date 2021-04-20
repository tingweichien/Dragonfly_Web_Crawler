import threading
import Save2File
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
  def __init__(self, controller, queue, num, DataList, DB_species, weather_connection, CsvOldData, file_path):
    threading.Thread.__init__(self)
    self.DataList = DataList #\ [species_info_id, Dates, HOUR(Times), Latitude, Longitude]
    self.queue = queue
    self.Workernumber = num #\ number of the worker
    self.controller = controller
    self.DB_species = DB_species
    self.weather_connection = weather_connection
    self.KeyChange = False
    self.weather_r = None
    self.CsvOldData = CsvOldData
    self.CsvFilePath = file_path


  #\ the callback function triggered by the thread start
  def run(self):
    global ErrorLog

    #\ The indicator for how many portion of the update will be, this var is to let the progressbar adjest by how many check button been selected.
    progressbar_portion = self.controller.progressbar_portion_calc()

    #\ Get the check status
    Check_Lock.acquire()
    Check_status = Database_function.check_weather_data(self.controller, self.DataList)
    Check_Lock.release()

    #\ check the weather request data is vaild or not
    if Check_status:

      #\ request data format
      data = {"key": Index.weather_key[Index.key_cnt],
              "q" : f'{self.DataList["Latitude"]}, {self.DataList["Longitude"]}',
              "format" : "json",
              "date" : self.DataList["Dates"],
              "enddate" : self.DataList["Dates"]
          }
      print(data)

      try:
        #\ this is the API
        ######################################################################
        self.weather_r = requests.post(url=Index.OnlineWeatherURL, headers=Index.headers, data=data).json()
        #######################################################################

        if self.weather_r == "None":
          print("[warning] weather response none")
          return

        #\ @ lock it to let only one get the authorization
        MySQL_Lock.acquire()

        #\ overlimit
        if self.weather_r != Index.WRE_API_over_limit:

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
          for data_seperate_time in self.weather_r["data"]["weather"][0]["hourly"]:
              #\ select the corresponding hour
              #\ remove the minutes. i.e. "1800" --> "18", get it from counting back
              respponse_hour = int(data_seperate_time["time"][:-2]) if data_seperate_time["time"] != "0" else 0
              if int(self.DataList["HOUR(Times)"]) in range(respponse_hour, respponse_hour+3): #\ the DataList is in three hours interval

                  #\ value to update
                  value = f"""'{{"tempC" : { data_seperate_time["tempC"].replace(" ", "") }, \
"FeelsLikeC" : { data_seperate_time["FeelsLikeC"].replace(" ", "") }, \
"windspeedKmph" : { data_seperate_time["windspeedKmph"].replace(" ", "") }, \
"winddirDegree" : { data_seperate_time["winddirDegree"].replace(" ", "") }, \
"winddir16Point" : "{ data_seperate_time["winddir16Point"].replace(" ", "") }", \
"humidity" : { data_seperate_time["humidity"].replace(" ", "") }}}'"""

                  #\ Update to MySQL
                  Database_function.update_weather_data(self.controller,
                                                        self.DB_species,
                                                        value,
                                                        self.DataList["species_info_id"],
                                                        self.weather_connection)
                  #\ Update to CSV
                  status = Save2File.Update2File(self.CsvFilePath,
                                                 self.CsvOldData,
                                                "update content",
                                                self.DataList["species_info_id"],
                                                Index.WeatherCsvIndex,
                                                value)
                  if status == False:
                    print("[Warning] Weather update to csv failed")
                    break

        #\ overlimit
        else:
          self.errorLog()

      #\ something wrong with the weather api
      except:
        self.errorLog()


      #\ @ release the lock
      try:
        MySQL_Lock.release()
      except:
        # workaround for some error that not able to relesase the lock since it might not have request the lock before
        print("[Warning] Release MySQL_Lock wrong")


  #\ error log
  def errorLog(self):
    ErrorLog = f"[Warning] API warning : \n {self.weather_r}"
    print(ErrorLog)
    self.KeyChange = True
    # raise Exception