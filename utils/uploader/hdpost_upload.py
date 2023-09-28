from loguru import logger
import time
import os
from AutoTransferMachine.utils.uploader.upload_tools import *
import re
import cloudscraper
from bs4 import BeautifulSoup

def get_token(cookie):
    headers = {
            'host': 'pt.hdpost.top',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': cookie,
            'origin': 'https://pt.hdpost.top',
            'referer': 'https://pt.hdpost.top/upload/2',
            'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0',
    }
    scraper=cloudscraper.create_scraper()
    r = scraper.get('https://pt.hdpost.top',headers=headers)
    soup = BeautifulSoup (r.text, "lxml")
    res=soup.find_all('meta',{'name':'_token'})
    if len(res)<=0:
        return ''
    if not 'content' in res[0].attrs:
        return ''
    return res[0].attrs['content']
    
def hdpost_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename
    #选择类别
    if 'anime' in file1.pathinfo.type.lower() and file1.pathinfo.complete==1:
        select_type='2'
        imdb_id=file1.pathinfo.imdb_id
    elif 'anime' in file1.pathinfo.type.lower():
        select_type='1'
        imdb_id=file1.pathinfo.imdb_id
    elif 'doc' in file1.pathinfo.type.lower() and file1.pathinfo.complete==1:
        select_type='2'
        imdb_id=file1.pathinfo.imdb_id
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='1'
        imdb_id=file1.pathinfo.imdb_id
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='2'
        imdb_id=file1.pathinfo.imdb_id
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='1'       
    elif 'mv' in file1.pathinfo.type.lower() or 'music' in file1.pathinfo.type.lower():
        select_type='3'
        imdb_id=file1.pathinfo.imdb_id    
    else:
        select_type='1'
        imdb_id=""
    url = siteinfo.url
    post_url = f"{url}post/{select_type}"

    #选择规格
    if 'WEBRIP' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为WEBRIP')  
    elif 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为WEB-DL')            
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为UHD')
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为HDTV')        
    elif 'FLAC' in file1.pathinfo.medium.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为FLAC')      
    else:
        medium_sel='3'
        logger.info('未识别到媒介信息，已选择Others')


    #选择分辨率
    if '2160' in file1.standard_sel:
        standard_sel='2'
    elif '4320' in file1.standard_sel:
        standard_sel='1'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='3'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='4'
    elif '720' in file1.standard_sel:
        standard_sel='5'
    elif 'SD' in file1.standard_sel:
        standard_sel='8'
    else:
        standard_sel='10'
    logger.info('已成功选择分辨率为'+file1.standard_sel)

    
    if siteinfo.uplver==1:
        uplver='1'
    else:
        uplver='0'

    torrent_file = file1.torrentpath
    file_tup = ("torrent", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
    token=get_token(siteinfo.cookie)
    other_data = {
            "_token": token,
            "nfo": "",
            "torrent-cover": "",
            "torrent-banner": "",
            "name": file1.pathinfo.tmdb_name+file1.uploadname,
            "mediainfo": file1.mediainfo,
            "season_number" : file1.pathinfo.seasonnum,
            "episode_number": "0",
            "tmdb": file1.pathinfo.tmdb_id,
            "imdb": imdb_id,
            "tvdb": "0",
            "mal": "0",
            "igdb": "0",
            "keywords": "",
            "isPreviewEnabled": "0",
            "category_id": select_type,
            "type_id": medium_sel,
            "resolution_id": standard_sel,
            "description": file1.screenshoturl,
            "anonymous": uplver,
            "bdinfo": "",
            "stream": "0",
            "sd": "0",
            "internal": "0",
            "personal_release": "0",
            "mod_queue_opt_in": "0",
            "free": "1",
            "post": "true",
            }
    scraper=cloudscraper.create_scraper()
    headers = {
        'authority': 'pt.hdpost.top',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #'content-length': '6820',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryEVG6BHsXWq0Ddoi',
        'cookie': siteinfo.cookie,
        'origin': 'https://pt.hdpost.top',
        'referer': 'https://pt.hdpost.top/upload/2',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0',
        'x-csrf-token': content,        
    } 
    
    success_upload=0
    try_upload=0
    while success_upload==0:
        try_upload+=1
        if try_upload>5:
            return False,fileinfo+' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            r = scraper.post(post_url, headers=headers,cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)