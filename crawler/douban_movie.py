# coding: utf-8

######
## from https://blog.csdn.net/qq_40693171/article/details/98644495
######

import requests
import urllib.parse
from http import cookiejar
from bs4 import BeautifulSoup

url = 'https://accounts.douban.com/j/mobile/login/basic'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
    'Origin': 'https://accounts.douban.com',
    'content-Type': 'application/x-www-form-urlencoded',
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'connection': 'keep-alive',
    'Host': 'accounts.douban.com'
}
data = {
    'ck': '',
    'name': '',
    'password': '',
    'remember': 'false',
    'ticket': ''
}


def login(username, password):
    global data
    data['name'] = username
    data['password'] = password
    data = urllib.parse.urlencode(data)
    req = requests.post(url, headers=header, data=data, verify=False)
    cookies = requests.utils.dict_from_cookiejar(req.cookies)
    return cookies


def getcomment(cookies):
    start = 0
    f_out = open('output.tsv', 'w')
    while True:
        try:
            page_url = 'https://movie.douban.com/subject/26794435/comments?start=' + str(
                start) + '&limit=20&sort=new_score&status=P&comments_only=1'
            start += 20
            req = requests.get(page_url, cookies=cookies)
            res = req.json()
            res = res['html']
            soup = BeautifulSoup(res)
            node = soup.select('.comment-item')
            for va in node:
                name = va.a.get('title')
                star = va.select_one('.comment-info').select('span')[1].get('class')[0][-2]
                comment = va.select_one('.short').text
                print(name, star, comment)
                f_out.write('\t'.join([name, star, comment]) + '\n')
        except Exception as e:
            print(e)
            break
        f_out.close()


getcomment(login('*', '*'))

