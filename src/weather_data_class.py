import threading
import queue

# Worker 類別，負責處理資料
class WeatherDataWorker(threading.Thread):
  def __init__(self, queue, num):
    threading.Thread.__init__(self)
    self.queue = queue
    self.num = num

  def run(self, function_input):
      #\ execute the function
      function_input()

