import calendar
from datetime import datetime

# Get the current date
current_date = datetime.now()

# Get the last day of the current month
last_day = calendar.monthrange(current_date.year, current_date.month)[1]

# Create a new date with the last day of the current month
last_day_of_month = datetime(current_date.year, current_date.month, last_day)

print("Last day of the current month:", last_day_of_month.strftime("%d.%m.%Y"))
