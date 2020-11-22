# from datetime import datetime, timedelta
import datetime as dt
from dateutil import relativedelta
today = dt.datetime.today()
print(today.strftime("%Y-%m-%d"))
print(today.year)
print(today-dt.timedelta(days=2))
prevuious_year = today-relativedelta.relativedelta(years=3)
print(prevuious_year.strftime("%Y-%m-%d"))