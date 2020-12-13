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
conn = sqlite3.connect('test.db')
cur = conn.cursor()

#collects the top (insert number) of videos, given a keyword and the number of results wanted
def topVideos(keyword):
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

def create_topVideos_table(keyword):
    cur.execute('''CREATE TABLE if not exists totalTopVideos
    (etag text PRIMARY_KEY, category text, videoId text, channelId text, channelTitle text, publishDate text)''')
    topVidList = topVideos(keyword)

    # avoid_dups_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            conn.execute('INSERT INTO totalTopVideos VALUES(?,?,?,?,?,?)', topVidList[j])
            conn.commit()

def create_video_stats_table(keyword):
    topVidList = topVideos(keyword)
    cur.execute('''CREATE TABLE if not exists totalvideoData
    (videoId text PRIMARY_KEY, category text, viewCount number, likeCount number)''')

    avoid_duplicates_video_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            videoId = topVidList[j][2]
            if videoId not in avoid_duplicates_video_list:
                avoid_duplicates_video_list.append(videoId)
                vidTup = video_stats(videoId, keyword)
                conn.execute('INSERT INTO totalvideoData VALUES(?,?,?,?)', vidTup)
                conn.commit()

def create_channel_stats_table(keyword):
    topVidList = topVideos(keyword)
    cur.execute('''CREATE TABLE if not exists totalchannel
    (channelId text PRIMARY KEY, category text, viewCount number, subscriberCount number, videoCount number)''')

    avoid_duplicates_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            j = j + (25 * i)
            channelId = topVidList[j][3]
            if channelId not in avoid_duplicates_list:
                avoid_duplicates_list.append(channelId)
                channelTup = channel_stats(channelId, keyword)
                conn.execute('INSERT INTO totalchannel VALUES(?,?,?,?,?)', channelTup)
                conn.commit()

def TEST_create_topVideos_table(keyword):
    cur.execute('''CREATE TABLE if not exists FINALTopVideos
    (etag text PRIMARY_KEY, category text, videoId text, channelId text, channelTitle text, publishDate text)''')
    topVidList = topVideos(keyword)

    # avoid_dups_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                conn.execute('INSERT INTO FINALTopVideos VALUES(?,?,?,?,?,?)', topVidList[j])
                conn.commit()
            except:
                break
        if ((j+1) % 25 == 0):
            break
        continue
def TEST_create_video_stats_table(keyword):
    topVidList = topVideos(keyword)
    cur.execute('''CREATE TABLE if not exists totalvideoData1
    (videoId text PRIMARY_KEY, category text, viewCount number, likeCount number)''')

    avoid_duplicates_video_list = []
    for i in range(0, 2):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                videoId = topVidList[j][2]
                if videoId not in avoid_duplicates_video_list:
                    avoid_duplicates_video_list.append(videoId)
                    vidTup = video_stats(videoId, keyword)
                    conn.execute('INSERT INTO totalvideoData1 VALUES(?,?,?,?)', vidTup)
                    conn.commit()
            except:
                break
        if ((j+1) % 25 == 0):
            break
        continue

def TEST_create_channel_stats_table(keyword):
    topVidList = topVideos(keyword)
    cur.execute('''CREATE TABLE if not exists totalChannel8
    (channelId text PRIMARY KEY, category text, viewCount number, subscriberCount number, videoCount number)''')

    cur.execute('SELECT channelID FROM totalChannel8')
    rows = cur.fetchall()
    avoid_duplicates_list = []
    for row in rows:
        avoid_duplicates_list.append(row[0])
    
    counter = 0
    break_sign = 0
    for i in range(0, 2):
        for j in range(0, 25):
            try:
                j = j + (25 * i)
                channelId = topVidList[j][3]
                if channelId not in avoid_duplicates_list:
                    avoid_duplicates_list.append(channelId)
                    channelTup = channel_stats(channelId, keyword)
                    conn.execute('INSERT INTO totalChannel8 VALUES(?,?,?,?,?)', channelTup)
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





