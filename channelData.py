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

API_KEY = 'AIzaSyDcg05zH6fsV5z4dqeLs6Pb3tNsx6K9GtM'
conn = sqlite3.connect('final.db')
cur = conn.cursor()

def channel_stats(channel_id, keyword):
    channel_url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + API_KEY
    json_url = requests.get(channel_url)
    data = json.loads(json_url.text)
    try:
        data = data['items'][0]['statistics']
    except:
        data = None
    try:
        subscriberCount = data['subscriberCount']
    except:
        subscriberCount = 0
    channel_tuple = (channel_id, keyword, data['viewCount'], subscriberCount, data['videoCount'])

    return channel_tuple

def create_channel_stats_table(keyword):
    cur.execute('SELECT channelId FROM top50videos')
    channel_rows = cur.fetchall()
    channel_id_list = []
    for channel in channel_rows:
        channel_id_list.append(channel[0])

    cur.execute('''CREATE TABLE if not exists channelData
    (channelId text PRIMARY KEY, category text, viewCount number, subscriberCount number, videoCount number)''')

    cur.execute('SELECT channelID FROM channelData')
    rows = cur.fetchall()
    avoid_duplicates_list = []
    for row in rows:
        avoid_duplicates_list.append(row[0])
    
    counter = 0
    break_sign = 0
    for i in range(0, 5):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                channelId = channel_id_list[j]
                if channelId not in avoid_duplicates_list:
                    avoid_duplicates_list.append(channelId)
                    channelTup = channel_stats(channelId, keyword)
                    conn.execute('INSERT INTO channelData VALUES(?,?,?,?,?)', channelTup)
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

#run workout 2 times
#run cooking 3 times
channel_type = input("Input channel type: ")
create_channel_stats_table(channel_type)

