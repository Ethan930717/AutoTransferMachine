from loguru import logger
import requests
import time
import os
from AutoTransferMachine.utils.uploader.upload_tools import *
import re
import cloudscraper


def zmpt_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    time_out=40
    tags=[]
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        if not file1.country=='':
            if '大陆' in file1.country:
                select_type='417'
                logger.info('国家信息已选择'+file1.country)
            elif '香港' in file1.country:
                select_type='417'
                logger.info('国家信息已选择'+file1.country)
            elif '台湾' in file1.country:
                select_type='417'
                logger.info('国家信息已选择'+file1.country)
            elif '美国' in file1.country:
                select_type='420'
                logger.info('国家信息已选择'+file1.country)
            elif '英国' in file1.country:
                select_type='420'
                logger.info('国家信息已选择'+file1.country)
            elif '法国' in file1.country:
                select_type='420'
                logger.info('国家信息已选择'+file1.country)
            elif '韩国' in file1.country:
                select_type='419'
                logger.info('国家信息已选择'+file1.country)
            elif '日本' in file1.country:
                select_type='418'
                logger.info('国家信息已选择'+file1.country)
            elif '印度' in file1.country:
                select_type='421'
                logger.info('国家信息已选择'+file1.country)
            else:
                select_type='421'
                logger.info('未找到资源国家信息，已选择其他')
        else:
            select_type='418'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'            

    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='422'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='423'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='423'
    else:
        select_type='401'
    logger.info('已成功填写类型为'+file1.pathinfo.type)



    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为WEB-DL')               
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为UHD-BLURAY')        
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为REMUX')
    elif 'DVDR' in file1.pathinfo.medium.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为DVDR')   
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='2'
        logger.info('已成功选择媒介为DVD')
    elif 'BD' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为MiniBD')           
    else:
        medium_sel='7'
        logger.info('未识别到媒介信息，不选择媒介')    

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='9'
    elif '2160' in file1.standard_sel:
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='1'
    elif '720' in file1.standard_sel:
        standard_sel='8'
    elif '480' in file1.standard_sel:
        standard_sel='7'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    #选择制作组
    if 'ZmPT' in file1.sub.upper():
        team_sel='6'
    elif 'ZmWeb' in file1.sub.upper():
        team_sel='7'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)

    if 'zmpt' in file1.pathinfo.exclusive :
        tags.append(1)
    if 'ZMPT' in file1.sub.upper() or 'ZMWEB' in file1.sub.upper():
        tags.append(3)
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
    if 'HDR' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR10标签')
    if '完结' in file1.pathinfo.tags:
        tags.append(12)
        logger.info('已选择完结标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY标签')   
    
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url": file1.imdburl,            
            "pt_gen": file1.doubanurl,
            "price": "",
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "medium_sel[4]": medium_sel,
            "standard_sel[4]": standard_sel,
            "team_sel[4]": team_sel,
            "uplver": uplver,
            "tags[4][]": tags,
            }
    scraper=cloudscraper.create_scraper()
    headers = {
        'host': 'zmpt.cc',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': siteinfo.cookie,
        'origin': 'https://zmpt.cc',
        'referer': 'https://zmpt.cc/upload.php',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
    } 
    
    success_upload=0
    try_upload=0
    while success_upload==0:
        try_upload+=1
        if try_upload>5:
            return False,fileinfo+' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            r = requests.post(post_url, headers=headers,cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0

    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)