from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import requests
from requests.adapters import HTTPAdapter
import socket
import certifi
import ssl
from ssl import create_default_context
import cloudscraper


def hudbt_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'movie' in file1.pathinfo.type.lower():
        if '大陆' in file1.country:
            select_type='401'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            select_type='413'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            select_type='413'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            select_type='415'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            select_type='415'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            select_type='415'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            select_type='414'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            select_type='414'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            select_type='414'
            logger.info('国家信息已选择'+file1.country)
        elif '马来西亚' in file1.country:
            select_type='414'
            logger.info('国家信息已选择'+file1.country)
        elif '泰国' in file1.country:
            select_type='414'
            logger.info('国家信息已选择'+file1.country)
        elif '新加坡' in file1.country:
            select_type='414'
            logger.info('国家信息已选择'+file1.country)
        else:
            select_type='415'
            logger.info('未找到资源国家信息，已选择欧美')
    if 'show' in file1.pathinfo.type.lower():
        if '大陆' in file1.country:
            select_type='403'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            select_type='419'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            select_type='419'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            select_type='421'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            select_type='421'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            select_type='421'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            select_type='420'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            select_type='420'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            select_type='420'
            logger.info('国家信息已选择'+file1.country)
        elif '马来西亚' in file1.country:
            select_type='420'
            logger.info('国家信息已选择'+file1.country)
        elif '泰国' in file1.country:
            select_type='420'
            logger.info('国家信息已选择'+file1.country)
        elif '新加坡' in file1.country:
            select_type='420'
            logger.info('国家信息已选择'+file1.country)
        else:
            select_type='421'
            logger.info('未找到资源国家信息，已选择欧美')
    elif 'tv' in file1.pathinfo.type.lower():
        if '大陆' in file1.country:
            select_type='402'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            select_type='417'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            select_type='417'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            select_type='418'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            select_type='418'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            select_type='418'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            select_type='416'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            select_type='416'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            select_type='416'
            logger.info('国家信息已选择'+file1.country)
        elif '马来西亚' in file1.country:
            select_type='416'
            logger.info('国家信息已选择'+file1.country)
        elif '泰国' in file1.country:
            select_type='416'
            logger.info('国家信息已选择'+file1.country)
        elif '新加坡' in file1.country:
            select_type='416'
            logger.info('国家信息已选择'+file1.country)
        else:
            select_type='418'
            logger.info('未找到资源国家信息，已选择欧美')
    elif 'anime' in file1.pathinfo.type.lower() and '完结' in file1.pathinfo.tags:
        select_type='405'
    elif 'anime' in file1.pathinfo.type.lower():
        select_type='428'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='406'
    else:
        select_type='433'
    logger.info('已成功填写类型为'+file1.pathinfo.type)



    #选择分辨率
    if '2160' in file1.standard_sel:
        standard_sel='7'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif 'SD' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath

    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url" : file1.imdburl,
            "nfo": "",
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "standard_sel": standard_sel,
            "uplver": uplver,
            }

    scraper=cloudscraper.create_scraper()
    headers = {
        'host': 'hudbt.hust.edu.cn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'aache-control': 'max-age=0',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
         #'content-length': '499686',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryfhTMBNBVOA7pufqF',
        'cookie': siteinfo.cookie,
        'origin': 'https://hudbt.hust.edu.cn',
        'referer': 'https://hudbt.hust.edu.cn/upload.php',
        'Sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-ch-ua-mobile': '?0',
        'Sec-ch-ua-platform': '"Windows"',
        'Sec-fetch-dest': 'document',
        'Sec-fetch-mode': 'navigate',
        'Sec-fetch-site': 'same-origin',
        'Sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0',
    } 
    
    success_upload=0
    try_upload=0
    ctx = ssl.create_default_context(cafile="/usr/local/share/ca-certificates/_.hust.edu.cn.crt")
    while success_upload==0:
        try_upload+=1
        if try_upload>5:
            return False,fileinfo+' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            ctx = create_default_context()
            r = scraper.post(post_url, headers=headers,cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out, cert="/usr/local/share/ca-certificates/_.hust.edu.cn.crt")
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)