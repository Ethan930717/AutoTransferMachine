import os
from loguru import logger
import time
import requests
import re
import json
import sys
from atm.utils.mediafile.douban_book import *
from atm.utils.mediafile.douban_movie import *

def getdoubaninfo(url:str='',cookie:str=''):
    if 'movie.douban.com' in url:
        if cookie.strip()=='':
            page_parse=MoviePageParse(movie_url=url)
        else:
            page_parse=MoviePageParse(movie_url=url,cookie=cookie)
    elif 'book.douban.com' in url:
        if cookie.strip()=='':
            page_parse=BookPageParse(book_url=url)
        else:
            page_parse=BookPageParse(book_url=url,cookie=cookie)
    else:
        raise Exception('豆瓣链接填写错误')
    print('\n'+page_parse.info())


def ptgen_douban_info(doubanurl):
    url='https://api.iyuu.cn/App.Movie.Ptgen?url='+doubanurl
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {
            'user-agent': user_agent,
            'referer': url,
        }
    logger.info('正在获取豆瓣信息')
    try:
        r = requests.get(url,headers=headers,timeout=20)
    except Exception as r:
        logger.error('获取豆瓣信息失败，原因: %s' %(r))
        return 

    logger.info('获取豆瓣信息完毕，正在处理信息，请稍等...')
    
    try:
        info_json=r.json()
        logger.trace(info_json)
    except Exception as r:
        logger.warning('获取豆瓣信息转换json格式失败，原因: %s' %(r))
        return
    
    if not r.ok:
        logger.trace(r.content)
        logger.warning(
            f"获取豆瓣信息失败: HTTP {r.status_code}, reason: {r.reason} ")
        return 

    if 'data' not in info_json or 'format' not in info_json['data']:
        logger.warning(f"豆瓣信息获取失败")
        return 
    
    info=info_json['data']['format']
    info=info[0:info.find('<a')]
    
    imgurl=re.findall('img[0-9]\.doubanio\.com',info)
    if len(imgurl)>0:
        info=info.replace(imgurl[0],'img9.doubanio.com')
    return info

def doubaninfo(doubanurl):
    res=None
    trynum=0
    while res==None:
        trynum=trynum+1
        if trynum>10:
            print('获取失败')
            return 
        res=ptgen_douban_info(doubanurl)
        if res==None:
            time.sleep(3)
    print('\n'+res)
    return 




