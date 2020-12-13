import requests
import json
import requests
import re
import os
import csv
import unittest
import operator
import sqlite3


conn = sqlite3.connect('final.db')
cur = conn.cursor()

def covidCalculations(csvfile):
    cur.execute('SELECT * FROM covidData')
    rows = cur.fetchall()
    cases_list = []
    date_list = []
    for row in rows:
        date_list.append(row[0])
        cases_list.append(row[1])
    
    covid_daily_growth = []
    for i in range(1, len(cases_list)):
        percentincrease = (cases_list[i] + cases_list[i-1])/cases_list[i-1]
        covid_daily_growth.append(percentincrease)
    
    with open(csvfile, mode='w') as csv_file:
        fieldnames = ['date', 'cases', 'growth_rate']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    
        for i in range(0, len(date_list)):
            date = date_list[i]
            num_cases = cases_list[i]
            try:
                growth = covid_daily_growth[i+1]
            except:
                break
            writer.writerow({'date': date, 'cases': num_cases, 'growth_rate': growth})

def socialBladeCalculations(csvfile, keyword):
    cur.execute('SELECT * FROM SOCIALBLADE WHERE user="{}"'.format(keyword))
    rows = cur.fetchall()
    sub_list = []
    date_list = []
    for row in rows:
        date_list.append(row[1])
        sub_list.append(float(row[2]))
    
    subs_growth = []
    for i in range(1, len(date_list)):
        percentincrease = (sub_list[i] + sub_list[i-1])/sub_list[i-1]
        if percentincrease < 3:
            subs_growth.append(percentincrease)
        else:
            subs_growth.append(2.0)
    
    with open(csvfile, mode='w') as csv_file:
        fieldnames = ['channel_name', 'date', 'growth_rate']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0, len(date_list)):
            date = date_list[i]
            try:
                growth = subs_growth[i+1]
            except:
                break
            writer.writerow({'channel_name': keyword, 'date': date, 'growth_rate': growth})

def socialBladeAverageCalculations(csvfile, keyword):
    cur.execute('SELECT * FROM SOCIALBLADE WHERE user="{}"'.format(keyword))
    rows = cur.fetchall()
    sub_list = []
    date_list = []
    for row in rows:
        date_list.append(row[1])
        sub_list.append(float(row[2]))
    
    subs_growth = []
    for i in range(1, len(date_list)):
        percentincrease = (sub_list[i] + sub_list[i-1])/sub_list[i-1]
        if percentincrease < 3:
            subs_growth.append(percentincrease)
        else:
            subs_growth.append(2.0)
    
    with open(csvfile, mode='w') as csv_file:
        fieldnames = ['channel_name', '2019average', '2020average']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        total2019 = 0
        count2019 = 0
        total2020 = 0
        count2020 = 0
        for i in range(0, len(date_list)):
            year = date_list[i].split("-")[0]
            if year == "2019":
                try:
                    total2019 = total2019 + subs_growth[i]
                    count2019 = count2019 + 1
                except:
                    continue
            if year == "2020":
                try:
                    total2020 = total2020 + subs_growth[i]
                    count2020 = count2020+1
                except:
                    continue
            
        average2019 = total2019/count2019
        average2020 = total2020/count2020

            
        writer.writerow({'channel_name': keyword, '2019average': average2019, '2020average':average2020})
    
    

# covidCalculations('covid.csv')
socialBladeCalculations('chloesaddictiongrowth.csv', 'chloesaddiction')
socialBladeAverageCalculations('chloesaddictionaveragegrowth.csv', 'chloesaddiction')
socialBladeCalculations('fitnessblendergrowth.csv', 'fitnessblender')
socialBladeAverageCalculations('fitnessblenderaveragegrowth.csv', 'fitnessblender')
socialBladeCalculations('bgfilmsgrowth.csv', 'bgfilms')
socialBladeAverageCalculations('bgfilmsaveragegrowth.csv', 'bgfilms')
socialBladeCalculations('bonappetitdotcomgrowth.csv', 'bonappetitdotcom')
socialBladeAverageCalculations('bonappetitdotcomaveragegrowth.csv', 'bonappetitdotcom')