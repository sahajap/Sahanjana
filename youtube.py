from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import operator

url = "https://api.covid19api.com/total/country/united-states/status/confirmed?from=2020-03-01T00:00:00Z&to=2020-06-01T00:00:00Z"
resp = requests.get(url).text
soup = BeautifulSoup(resp, 'html.parser')

print(soup)