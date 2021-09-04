## Web scraping stats - fanlore.org

import requests
import json

from collections import Counter, OrderedDict
import pandas
import plotly.express as px
from datetime import datetime

#convert 90 days into seconds - for rcend parameter below
rangeEnd = 60*60*24*90

#dictionary w/ parameters for the API request
parameters = {
    "format": "json",
    "action" : "query",
    "list" : "recentchanges",
    "rcnamespace" : 1,
    "rcprop" : "timestamp|title|ids|user",
    "rcstart" : "now",
    "rcend" : f"{rangeEnd}",
    "rclimit" : 500,
}

tsList = []  # Empty list to store the timestamps we will get later

#ask the Fanlore server for the data and load it with JSON - feat. Continue loop by Fox
done = False


#not loop version:
r = requests.get("https://fanlore.org/w/api.php", params=parameters)
print("Sending query to fanlore... - reponse is: ", r.status_code)
scrape = json.loads(r.content)


# loop version
# while not done:
#     r = requests.get("https://fanlore.org/w/api.php", params = parameters)
#     print("Sending query to fanlore... - reponse is: ", r.status_code)
#     scrape = json.loads(r.content)
#     # Check if the continue key is in the data
#     if 'continue' in scrape:
#         # Set the rccontinue parameter for the next loop.
#         parameters['rccontinue'] = scrape['continue']['rccontinue']
#         print(f"Set new continue timestamp of {parameters['rccontinue']}")
#     # If it isn't, set done True so the loop stops after finishing this cycle.
#     else:
#         done = True


for change in scrape['query']['recentchanges']:
    tsList.append(change['timestamp'])


# This list will hold just the date part of the timestamp.
tsListTrim = []

for item in tsList:
    tsListTrim.append(item.split('T')[0])
    
print(f"Retrieved {len(tsListTrim)} edits from the server. (Maximum is 500)")
print(f"The latest date is {tsListTrim[0]}. The earliest date is {tsListTrim[(len(tsListTrim)-1)]}")
print()

tsCounter = Counter(tsListTrim) #This one seems to be ordered from highest to lowest count...

print(f'The dates with the top 5 most edits are:{(tsCounter.most_common(3))}')
print()
print(f'The average number of edits per day is {sum(tsCounter.values())/len(tsListTrim)}')



# #trying to see if the days of the week matter at all...
# tsListTrim_days = []
# for each in tsListTrim:
#     tsListTrim_days.append(datetime.strptime(each,"%Y-%m-%d"))

# days_List = []
# for each in tsListTrim_days:
#     # days_List.append(datetime.strftime(each,"%A"))
#     days_List.append(datetime.strftime(each, "%u-%A"))
    

# days_Listcount = Counter(days_List)
# days_count_sorted = OrderedDict(sorted(days_Listcount.items(), key=lambda t: t[0]))

# days_df = pandas.DataFrame(list(days_count_sorted.items()), columns=['Day', 'Edits'])


# # # ### Bar Graph ####

# daysGraph = px.bar(
#     days_df,
#     title="Days with highest Talk page activity",
#     x='Day',
#     y='Edits',
#     labels={"x":"Day","y":"Edits"},
#     color='Day',
#     color_discrete_sequence=px.colors.qualitative.Plotly,
#     template="plotly",
#     )

# daysGraph.show()


# # ### Line Graph ####

# freqData = dict(tsCounter)


# ts_x = list(freqData.keys()) #dates
# ts_y = list(freqData.values()) #freq

# freqGraph = px.line(
#     x=ts_x,
#     y=ts_y,
#     title="Frequency of Talk Page edits on Fanlore.org, last 90 days",
#     labels={"x" : "Date","y" : "# of Edits"})

# freqGraph.update_xaxes(rangeslider_visible=True)

# freqGraph.show()
