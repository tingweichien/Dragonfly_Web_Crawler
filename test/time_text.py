from datetime import datetime, timedelta
import datetime as dt
from dateutil import relativedelta
# today = dt.datetime.today()
# print(today.strftime("%Y-%m-%d"))
# print(today.year)
# print(today-dt.timedelta(days=2))
# prevuious_year = today-relativedelta.relativedelta(years=3)
# print(prevuious_year.strftime("%Y-%m-%d"))

# current date and time
now = datetime.now()
print(now)
timestamp = datetime.timestamp(now)
print("timestamp =", timestamp)
datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
print(datetime_object)
timestamp = datetime.timestamp(datetime_object)
print("timestamp =", timestamp)