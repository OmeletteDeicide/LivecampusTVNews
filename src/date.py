import datetime
import pandas as pd
start = datetime.datetime.strptime("01-12-2021", "%d-%m-%Y")
end = datetime.datetime.strptime("07-12-2021", "%d-%m-%Y")
date_generated = pd.date_range(start, end)
print(date_generated.strftime("%d-%m-%Y"))