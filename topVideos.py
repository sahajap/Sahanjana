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

def topVideos(keyword):
    # Utilizes YoutubeAPI 
    # Collects the top 50 videos for a specific channel_type(keyword) and outputs a list of tuples in format of  
    # (unique tag, channel_type, videoid, channelid, title of channel, and publishTime)
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + keyword + "&publishedAfter=2020-03-01T00:00:00Z&maxResults=50&key=" + API_KEY
    json_url = requests.get(url)
    data = json.loads(json_url.text)

    youtlist = []
    for i in range(0, (len(data['items']))):
        etag = (data['items'][i]['etag'])
        try:
            video_id = data['items'][i]['id']['videoId']
        except:
            video_id = data['items'][i]['id']['playlistId']
        channel_id = data['items'][i]['snippet']['channelId']
        channel_title = data['items'][i]['snippet']['channelTitle']
        publishTime = (data['items'][i]['snippet']['publishTime'])[:-11]

        youtuple = (etag, keyword, video_id, channel_id, channel_title, publishTime)
        youtlist.append(youtuple)

    return youtlist

def create_topVideos_table(keyword):
    # Takes in the channel_type and creates a table in the database with the tuple of 
    # (unique tag, channel_type, videoid, channelid, title of channel, and publishTime) 
    # for the top 50 channels of the specific keyword
    cur.execute('''CREATE TABLE if not exists TESTtop50videos
    (etag text PRIMARY_KEY, category text, videoId text, channelId text, channelTitle text, publishDate text)''')
    topVidList = topVideos(keyword)

    cur.execute('SELECT etag FROM TESTtop50videos')
    rows = cur.fetchall()
    avoid_duplicates_list = []
    for row in rows:
        avoid_duplicates_list.append(row[0])
    
    if len(avoid_duplicates_list) == 50 and (keyword == 'workout'):
        return
    counter = 0
    break_sign = 0
    for i in range(0, 2):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                etag = topVidList[j][0]
                if etag not in avoid_duplicates_list:
                    conn.execute('INSERT INTO TESTtop50videos VALUES(?,?,?,?,?,?)', topVidList[j])
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

#create_topVideos_table('workout')
channel_type = input("Input channel type (choose workout or cooking): ")
create_topVideos_table(channel_type)
