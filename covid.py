import requests
import json
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import operator
import sqlite3

conn = sqlite3.connect('final.db')
cur = conn.cursor()

def collect_covid_data():
    url = 'https://api.covid19api.com/total/country/united-states/status/confirmed?from=2020-03-01T00:00:00Z&to=2020-11-10T00:00:00Z'
    json_url = requests.get(url)
    data = json.loads(json_url.text)

    data_length = len(data)
    covid_cases = []
    for i in range(0, data_length):
        cases_count = data[i]['Cases']
        date = (data[i]['Date'])[:-10]
        covid_tuple = (date, cases_count)
        covid_cases.append(covid_tuple)
    
    return covid_cases

# def create_covid_table(covid_data):
#     cur.execute('''CREATE TABLE if not exists covidData (date text, cases number)''')

#     for i in range(0, 10):
#         for j in range(0, 25):
#             j = j + (25 * i)
#             value = covid_data[j]
#             conn.execute('INSERT INTO covidData VALUES(?,?)', value)
#             conn.commit()


#will need to run this code 10 times!
def test_create_covid_table(covid_data):
    cur.execute('''CREATE TABLE if not exists covidData (date text PRIMARY KEY, cases number)''')

    for i in range(0, 10):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                value = covid_data[j]
                conn.execute('INSERT INTO covidData VALUES(?,?)', value)
                conn.commit()
            except:
                break
        if ((j+1) % 25 == 0):
            break
        continue


covid_data = collect_covid_data()
test_create_covid_table(covid_data)
