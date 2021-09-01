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

#ask the Fanlore server for the data and load it with JSON
r = requests.get("https://fanlore.org/w/api.php", params = parameters)
scrape = json.loads(r.content)

print("Edits to talk pages on www.fanlore.org - past 90 days")
print()
print("Paging fanlore - reponse is: ", r.status_code)

for change in scrape['query']['recentchanges']:
    tsList.append(change['timestamp'])


# This list will hold just the date part of the timestamp.
tsListTrimmed = []

for item in tsList:
    tsListTrimmed.append(item.split('T')[0])
    
print(f"Retrieved {len(tsListTrimmed)} edits from the server. (Maximum is 500)")
print(f"The latest date is {tsListTrimmed[0]}. The earliest date is {tsListTrimmed[(len(tsListTrimmed)-1)]}")

tsCounter = Counter(tsListTrimmed) #This one seems to be ordered from highest to lowest count...
graphData = dict(tsCounter) #While this one is chronological

#trying to see if the days of the week matter at all...
tsListTrimmed_days = []
for each in tsListTrimmed:
    tsListTrimmed_days.append(datetime.strptime(each,"%Y-%m-%d"))

days_List = []
for each in tsListTrimmed_days:
    # days_List.append(datetime.strftime(each,"%A"))
    days_List.append(datetime.strftime(each, "%u-%A"))
    

days_Listcount = Counter(days_List)
days_count_sorted = OrderedDict(sorted(days_Listcount.items(), key=lambda t: t[0]))

days_df = pandas.DataFrame(list(days_count_sorted.items()), columns=['Day', 'Edits'])


# # ### Bar Graph ####
x_days = list(days_count_sorted.keys())
y_days = list(days_count_sorted.values())

graph2 = px.bar(
    days_df,
    title="Days with highest Talk page activity",
    x='Day',
    y='Edits',
    labels={"x":"Day","y":"Edits"},
    color='Day',
    color_discrete_sequence=px.colors.qualitative.Plotly,
    template="plotly",
    )

graph2.show()


# ### Line Graph ####

x_val = list(graphData.keys()) #dates
y_val = list(graphData.values()) #freq

print("Making the graph... Check your browser!")

graph = px.line(
    x=x_val,
    y=y_val,
    title="Frequency of Talk Page edits on Fanlore.org, last 90 days",
    labels={"x" : "Date","y" : "# of Edits"})

graph.update_xaxes(rangeslider_visible=True)

graph.show()
