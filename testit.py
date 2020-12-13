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
from topVideos import topVideos

API_KEY = 'AIzaSyDcg05zH6fsV5z4dqeLs6Pb3tNsx6K9GtM'
conn = sqlite3.connect('test.db')
cur = conn.cursor()

def video_stats(video_id, keyword):
    url = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=' + video_id + '&key=' + API_KEY
    json_url = requests.get(url)
    data = json.loads(json_url.text)

    try:
        data = data['items'][0]['statistics']
    except:
        data = None

    try:
        likeCount = data['likeCount']
    except:
        likeCount = 0

    video_tuple = (video_id, keyword, data['viewCount'], likeCount)

    return video_tuple

def create_video_stats_table(keyword):
    topVidList = topVideos(keyword)
    cur.execute('''CREATE TABLE if not exists VIDEO2
    (videoId text PRIMARY_KEY, category text, viewCount number, likeCount number)''')

    cur.execute('SELECT * FROM VIDEO2')
    rows = cur.fetchall()
    avoid_duplicates_video_list = []
    for row in rows:
        avoid_duplicates_video_list.append(row[0])

    for i in range(0, 2):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                videoId = topVidList[j][2]
                if videoId not in avoid_duplicates_video_list:
                    avoid_duplicates_video_list.append(videoId)
                    vidTup = video_stats(videoId, keyword)
                    conn.execute('INSERT INTO VIDEO1 VALUES(?,?,?,?)', vidTup)
                    conn.commit()
            except:
                break
        if ((j+1) % 25 == 0):
            break
        continue

create_video_stats_table('workout')
