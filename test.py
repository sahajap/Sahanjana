import requests
import json
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import sqlite3


url = 'https://api.covid19api.com/total/country/united-states/status/confirmed?from=2020-03-01T00:00:00Z&to=2020-10-15T00:00:00Z'
json_url = requests.get(url)
data = json.loads(json_url.text)

print(len(data))



data_length = len(data)
covid_cases = []
for i in range(0, data_length):
    cases_count = data[i]['Cases']
    date = (data[i]['Date'])[:-11]
    covid_tuple = (date, cases_count)
    covid_cases.append(covid_tuple)


conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists covid (date text, cases number)''')
# conn.executemany('INSERT INTO covid VALUES (?,?)', covid_cases)
# for row in conn.execute('SELECT * FROM covid'):
#     print(row)

counter = 0
for value in covid_cases:
    if counter > 24:
        print("Retrieved 25 tuples, run again to load more data")
        break

    # if cur.execute == None:
    conn.execute('INSERT INTO covid VALUES(?,?)', value)
    conn.commit()

    counter = counter + 1

# for row in conn.execute('SELECT * FROM covid'):
#     print(row)
conn.close()