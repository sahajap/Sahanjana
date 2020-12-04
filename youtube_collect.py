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
conn = sqlite3.connect('data.db')
cur = conn.cursor()

#collects the top (insert number) of videos, given a keyword and the number of results wanted
def topVideos(keyword):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + keyword + "&publishedAfter=2020-03-01T00:00:00Z&maxResults=100&key=" + API_KEY
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    # try:
    #     data = data['items'][00]['id']['videoId']
    # except:
    #     data = None

    youtlist = []
    for i in range(0, len(data['items'])):
        etag = (data['items'][i]['etag'])
        video_id = data['items'][i]['id']['videoId']
        channel_id = data['items'][i]['snippet']['channelId']
        channel_title = data['items'][i]['snippet']['channelTitle']
        publishTime = (data['items'][i]['snippet']['publishTime'])[:-11]

        youtuple = (etag, video_id, channel_id, channel_title, publishTime)
        youtlist.append(youtuple)
    
    return youtlist
    

def video_stats(video_id):
    url = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=' + video_id + '&key=' + API_KEY
    json_url = requests.get(url)
    data = json.loads(json_url.text)

    try:
        data = data['items'][0]['statistics']
    except:
        data = None
    
    video_tuple = (video_id, data['viewCount'], data['likeCount'])
    
    return video_tuple

def channel_stats(channel_id):
    channel_url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + API_KEY
    json_url = requests.get(channel_url)
    data = json.loads(json_url.text)
    try:
        data = data['items'][0]['statistics']
    except:
        data = None
    
    channel_tuple = (channel_id, data['viewCount'], data['subscriberCount'], data['videoCount'])
    
    return channel_tuple

def create_workout_table():
    cur.execute('''CREATE TABLE if not exists WorkoutTop 
    (etag text PRIMARY_KEY, videoId text, channelId text, channelTitle text, publishDate text)''')
    # counter = 0
    topVidList = topVideos('workout')

    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            conn.execute('INSERT INTO WorkoutTop VALUES(?,?,?,?,?)', topVidList[j])
            conn.commit()
            

    # for value in topVidList:
    #     if counter > 24:
    #         print("Retrieved 25 tuples, run again to load more data")
    #         break

    #     # if cur.execute == None:
    #     conn.execute('INSERT INTO topWorkout VALUES(?,?,?,?,?)', value)
    #     conn.commit()

    #     counter = counter + 1

def create_video_table():
    topVidList = topVideos('workout')
    cur.execute('''CREATE TABLE if not exists video_data
    (videoId text, viewCount number, likeCount number)''')

    # counter = 0
    # for i in range(0, len(topVidList)):
    #     videoId = topVidList[i][1]
    #     vidTup = video_stats(videoId)
    #     if counter > 24:
    #         print("Retrieved 25 tuples, run again to load more data")
    #         break

    #     # if cur.execute == None:
    #     conn.execute('INSERT INTO ideo_data VALUES(?,?,?)', vidTup)
    #     conn.commit()
    #     counter = counter + 1
    
    avoid_duplicates_video_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            videoId = topVidList[j][1]
            if videoId not in avoid_duplicates_video_list:
                avoid_duplicates_video_list.append(videoId)
                vidTup = video_stats(videoId)
                conn.execute('INSERT INTO video_data VALUES(?,?,?)', vidTup)
                conn.commit()

def create_channel_workout_table():
    topVidList = topVideos('workout')
    cur.execute('''CREATE TABLE if not exists channel_data
    (channelId text PRIMARY KEY, viewCount number, subscriberCount number, videoCount number)''')
    # counter = 0
    # for i in range(0, len(topVidList)):
    #     videoId = topVidList[i][1]
    #     vidTup = video_stats(videoId)
    #     if counter > 24:
    #         print("Retrieved 25 tuples, run again to load more data")
    #         break

    #     # if cur.execute == None:
    #     conn.execute('INSERT INTO ideo_data VALUES(?,?,?)', vidTup)
    #     conn.commit()
    #     counter = counter + 1
    
    avoid_duplicates_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            channelId = topVidList[j][2]
            if channelId not in avoid_duplicates_list:
                avoid_duplicates_list.append(channelId)
                channelTup = channel_stats(channelId)
                conn.execute('INSERT INTO channel_data VALUES(?,?,?,?)', channelTup)
                conn.commit()
 

#create_workout_table()
create_video_table()
#create_channel_workout_table()

# new = topVideos('workout')

#channel_stats('UCCgLoMYIyP0U56dEhEL1wXQ')
# video_stats(new[0][1])






