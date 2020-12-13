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
        if percentincrease < 4:
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
    
def top5(keyword):
    cur.execute('SELECT channelId FROM top50videos WHERE category="{}"'.format(keyword))
    rows = cur.fetchall()
    channel_list = []
    for row in rows:
        channel_list.append(row[0])
    
    channel_count = {}
    for channel in channel_list:
        if channel not in channel_count:
            channel_count[channel] = 1
        else:
            channel_count[channel] = channel_count[channel] + 1
    
    sorted_dict = sorted(channel_count.items(), key=lambda x: x[1], reverse=True)


    top = []
    for value in sorted_dict[:5]:
        new_value = value[0]
        top.append(new_value)
    return top

def JOINfunc(keyword, csvfile):
    #selectTrack.title, Genre.namefromTrackjoinGenreonTrack.genre_id= Genre.id
    top5_list = top5(keyword)

    
    with open(csvfile, mode='w') as csv_file:
        fieldnames = ['Channel Title', 'Number of Videos','Total Views', 'Total Likes', 'Proportion of Likes', 'Subscriber Count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        listt = []
        for channel in top5_list:
            cur.execute('SELECT channelData.subscriberCount, top50videos.channelTitle FROM top50videos JOIN channelData ON top50videos.channelId = channelData.channelId WHERE channelData.channelId ="{}"'.format(channel))
            subCount = cur.fetchone()
            channel_tuple = (channel, subCount)
            listt.append(channel_tuple)
            cur.execute('SELECT videoData.viewCount, videoData.likeCount FROM top50videos JOIN channelData JOIN videoData ON top50videos.videoId = videoData.videoId and top50videos.channelId = channelData.channelId WHERE channelData.channelId ="{}"'.format(channel))
            videodataa = cur.fetchall()
            likecounttotal = 0
            viewcounttotal = 0
            for value in videodataa:
                viewcounttotal = viewcounttotal + value[0]
                likecounttotal = likecounttotal + value[1]
            ratio = likecounttotal/viewcounttotal
            writer.writerow({'Channel Title': channel_tuple[0], 'Number of Videos': len(videodataa),'Total Views': viewcounttotal, 'Total Likes':likecounttotal, 'Proportion of Likes': ratio, 'Subscriber Count': channel_tuple[1]})

        
    return listt

    



# covidCalculations('covid.csv')
# socialBladeCalculations('chloesaddictiongrowth.csv', 'chloesaddiction')
# socialBladeAverageCalculations('chloesaddictionaveragegrowth.csv', 'chloesaddiction')
# socialBladeCalculations('fitnessblendergrowth.csv', 'fitnessblender')
# socialBladeAverageCalculations('fitnessblenderaveragegrowth.csv', 'fitnessblender')
# socialBladeCalculations('bgfilmsgrowth.csv', 'bgfilms')
# socialBladeAverageCalculations('bgfilmsaveragegrowth.csv', 'bgfilms')
# socialBladeCalculations('bonappetitdotcomgrowth.csv', 'bonappetitdotcom')
# socialBladeAverageCalculations('bonappetitdotcomaveragegrowth.csv', 'bonappetitdotcom')

JOINfunc('workout', 'top5workout.csv')
JOINfunc('cooking', 'top5cooking.csv')


