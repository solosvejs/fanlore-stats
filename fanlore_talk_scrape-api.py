## Web scraping stats - fanlore.org

import requests
import json
from collections import Counter
import plotly.express as px


tsList = [] #Empty list to store the timestamps we will get later


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

#ask the Fanlore server for the data and load it with JSON
r = requests.get("https://fanlore.org/w/api.php", params = parameters)
scrape = json.loads(r.content)

print("Edits to talk pages on www.fanlore.org - past 90 days")
print()
print("Paging fanlore - reponse is: ", r.status_code)

for change in scrape['query']['recentchanges']:
    tsList.append(change['timestamp'])

print(f"Retrieved {len(tsList)} edits from the server. (Maximum is 500)")
print(f"The latest date is {tsList[0]}. The earliest date is {tsList[(len(tsList)-1)]}")

# This list will hold just the date part of the timestamp.
tsListTrimmed = []

for item in tsList:
    tsListTrimmed.append(item.split('T')[0])

tsCounter = Counter(tsListTrimmed) #This one seems to be ordered from highest to lowest count...
graphData = dict(tsCounter) #While this one is chronological

### Graph ####

x_val = list(graphData.keys()) #dates
y_val = list(graphData.values()) #freq

print("Making the graph... Check your browser!")

graph = px.line(
    x=x_val,
    y=y_val,
    title="Frequency of Talk Page edits on Fanlore.org",
    labels={"x" : "Date","y" : "# of Edits"})

graph.update_xaxes(rangeslider_visible=True)


graph.show()
