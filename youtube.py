import requests
import json
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import operator


class Stats:
    def __init__ (self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None

    def get_channel_statistics(self):
        url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + self.channel_id + "&key=" + self.api_key
        print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        print(data)

#https://socialblade.com/youtube/channel/UCpQ34afVgk8cRQBjSJ1xuJQ/monthly 
#the channel id is the same for the youtube api and the social blade url 
#extract current number of subscribers from youtube
#extract annual growth rate from 
#2019 capture: https://web.archive.org/web/20190524113349/https://socialblade.com/youtube/user/chloesaddiction/monthly
#2020 capture: https://web.archive.org/web/20200610170746/https://socialblade.com/youtube/user/chloesaddiction/monthly
#Current capture: https://socialblade.com/youtube/user/chloesaddiction/monthly


url = 'https://web.archive.org/web/20200610170746/https://socialblade.com/youtube/user/chloesaddiction/monthly'

def create_lists(url):
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'html.parser')

    table_tag = soup.find('body')

    date_tags = table_tag.find_all('div', style="float: left; width: 95px;")
    sub_tags = table_tag.find_all('div', style="width: 140px; float: left;")

    date_tag_list = []
    for tag in date_tags:
        item = (tag.text).strip()
        date_tag_list.append(item)

    sub_tag_list = []
    count = 0
    for tag in sub_tags:
        if count % 2 == 0:
            item = (tag.text).strip()
            sub_tag_list.append(item)
        count = count + 1

    sub_tag_list[-1] = sub_tag_list[-1][:-6]

    print(sub_tag_list)
    print(date_tag_list)

#CHLOE TING
# test_url = 'https://web.archive.org/web/20200610170746/https://socialblade.com/youtube/user/chloesaddiction/monthly'
# create_lists(test_url)
# print("hi                       okay")
# test2_url = 'https://web.archive.org/web/20190524113349/https://socialblade.com/youtube/user/chloesaddiction/monthly'
# create_lists(test2_url)

#BABISH
# test_url = 'https://web.archive.org/web/20190524071535/https://socialblade.com/youtube/user/bgfilms/monthly'
# test2_url = 'https://web.archive.org/web/20200928231806/https://socialblade.com/youtube/user/bgfilms/monthly'
create_lists(test2_url)





