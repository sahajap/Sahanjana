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
    cur.execute('SELECT videoId FROM top50videos')
    video_rows = cur.fetchall()
    video_id_list = []
    for videoid in video_rows:
        video_id_list.append(videoid[0])
    cur.execute('''CREATE TABLE if not exists videoData
    (videoId text PRIMARY_KEY, category text, viewCount number, likeCount number)''')

    cur.execute('SELECT * FROM videoData')
    rows = cur.fetchall()
    avoid_duplicates_video_list = []
    for row in rows:
        avoid_duplicates_video_list.append(row[0])

    counter = 0
    break_sign = 0
    for i in range(0, 4):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                videoId = video_id_list[j]
                if videoId not in avoid_duplicates_video_list:
                    avoid_duplicates_video_list.append(videoId)
                    vidTup = video_stats(videoId, keyword)
                    conn.execute('INSERT INTO videoData VALUES(?,?,?,?)', vidTup)
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

channel_type = input("Input channel type: ")
create_video_stats_table(channel_type)