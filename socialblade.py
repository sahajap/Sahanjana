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


#https://socialblade.com/youtube/channel/UCpQ34afVgk8cRQBjSJ1xuJQ/monthly 
#the channel id is the same for the youtube api and the social blade url 
#extract current number of subscribers from youtube
#extract annual growth rate from 
#2019 capture: https://web.archive.org/web/20190524113349/https://socialblade.com/youtube/user/chloesaddiction/monthly
#2020 capture: https://web.archive.org/web/20200610170746/https://socialblade.com/youtube/user/chloesaddiction/monthly
#Current capture: https://socialblade.com/youtube/user/chloesaddiction/monthly


url = 'https://web.archive.org/web/20200610170746/https://socialblade.com/youtube/user/chloesaddiction/monthly'

def create_date_list(year, user):
    url = 'https://web.archive.org/web/' + str(year) + '0610170746/https://socialblade.com/youtube/user/' + user + '/monthly'
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'html.parser')

    table_tag = soup.find('body')

    date_tags = table_tag.find_all('div', style="float: left; width: 95px;")

    date_tag_list = []
    for tag in date_tags:
        item = (tag.text).strip()
        date_tag_list.append(item)
    
    sub_tags = table_tag.find_all('div', style="width: 140px; float: left;")

    sub_tag_list = []
    count = 0
    for tag in sub_tags:
        if count % 2 == 0:
            if year == 2020:
                item = (tag.text).strip()
                sub_tag_list.append(item[:-1])
            else:
                item = (tag.text).strip()   
                answer = (float(item.replace(',','')))/1000000
                new_item = str(round(answer, 2))
                sub_tag_list.append(new_item)
        count = count + 1
    
    if year == 2020:
        sub_tag_list[-1] = sub_tag_list[-1][:-5]

    final_list = []
    for i in range(0, len(date_tag_list)):
        tups = (user, date_tag_list[i], sub_tag_list[i])
        final_list.append(tups)
    
    return final_list


def create_subscriber_list(year, user):
    url = 'https://web.archive.org/web/' + str(year) + '0610170746/https://socialblade.com/youtube/user/' + user + '/monthly'
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'html.parser')

    table_tag = soup.find('body')

    sub_tags = table_tag.find_all('div', style="width: 140px; float: left;")

    sub_tag_list = []
    count = 0
    for tag in sub_tags:
        if count % 2 == 0:
            if year == 2020:
                item = (tag.text).strip()
                sub_tag_list.append(item[:-1])
            else:
                item = (tag.text).strip()   
                answer = (float(item.replace(',','')))/1000000
                new_item = str(round(answer, 2))
                sub_tag_list.append(new_item)
        count = count + 1
    
    if year == 2020:
        sub_tag_list[-1] = sub_tag_list[-1][:-5]
    
    subs_list = []
    for sub in sub_tag_list:
        sub_tup = (user, sub)
        subs_list.append(sub_tup)
    
    return subs_list


def create_table(year, user):
    cur.execute('''CREATE TABLE if not exists SOCIALBLADE (user text, date text, subscribers text)''')

    date_list = create_date_list(year, user)

    cur.execute('SELECT * FROM SOCIALBLADE')
    rows = cur.fetchall()
    avoid_duplicates_list = []
    for row in rows:
        avoid_duplicates_list.append(row)

    counter = 0
    break_sign = 0
    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            try:
                value = date_list[j] 
                if value in avoid_duplicates_list:
                    break
                conn.execute('INSERT INTO SOCIALBLADE VALUES(?,?,?)', value)
                counter = counter + 1
                conn.commit()
            except:
                break
            if counter == 25:
                break_sign = 1
                break
        if break_sign == 1:
            break
        continue


# user_id_list = ['chloesaddiction', 'fitnessblender', 'bgfilms', 'bonappetitdotcom']
# for user in user_id_list:
#     create_table(2019, user)
#     create_table(2020, user)

user_name = input("Type username: ")
if user_name != "":
    input_year = input("Type year: ")

if input_year == "2020":
    create_table(float(input_year), user_name)
else:
    create_table((input_year), user_name)