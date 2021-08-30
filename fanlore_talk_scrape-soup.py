# fanlore talk pages scraping - BeautifulSoup version
# ------------------------------------
# this method ignores the API and looks directly at the HTML code of the "recent changes" page.



import requests
from bs4 import BeautifulSoup
import pandas
import datetime #not sure if I'll need this...
import plotly.express

r = requests.get('https://fanlore.org/w/index.php?namespace=1&tagfilter=&days=90&limit=500&title=Special%3ARecentChanges')
soup = BeautifulSoup(r.content, 'html.parser')

print("Edits to talk pages on www.fanlore.org - past 90 days")
print()
print("Paging fanlore - reponse is: ", r.status_code)
print()


# .find gives
# the tag and what's inside it... <b>blahblahblah</b>
entryTest = soup.find('h4')
# .contents takes just the thing between the tags? 
entryFull = entryTest.contents
print(entryFull)
print(entryTest)



#dates are in <h4> tags; 
getDates = soup.findAll('h4')
talkdates_List =[]
for entry in getDates:
    talkdates_List.append(entry.text)

# getTitle = soup.findall('mw-changeslist-title')
# titles_List = []
# for entry in getTitle:
#     titles_list.append(entry.text)

# print(titles_List)

for child in getDates.children:
    print(child)


finalFrame = pandas.DataFrame()

