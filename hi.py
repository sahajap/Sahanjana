
import requests as req
from bs4 import BeautifulSoup as bs
import re
def sub_scraper(url, var):
    r = req.get(url)
    print(r.status_code)
    soup = bs(r.text, 'lxml')
    script_divs = soup.find_all('script', {'type': 'text/javascript'})
    res = 0
    for i in range(len(script_divs)):
#         print(i)
#         print(script_divs[i])
        if "CSV" in str(script_divs[i]):
            if var == 'count':
                res = script_divs[i]
            elif var == 'total':
                res = script_divs[i + 1]
            elif var == 'views':
                res = script_divs[i + 2]
            elif var == 'views_tot':
                res = script_divs[i + 3]
            break
#     print(res)
    lst = str(res).split('+')
    lst = [test.strip() for test in lst]
    lst = [test.replace('\\n"', '').replace('"', '') for test in lst]
    return lst

leafy = 'https://web.archive.org/web/20161218062757/https://socialblade.com/youtube/user/leafyishere/monthly'
sub_scraper(leafy, 'count')