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

def top5channels(keyword):
    cur.execute('SELECT etag FROM top50videos')
    rows = cur.fetchall()
    avoid_duplicates_list = []
    for row in rows:
        avoid_duplicates_list.append(row[0])
