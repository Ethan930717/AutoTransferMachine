from loguru import logger
import time
import os
from AutoTransferMachine.utils.uploader.upload_tools import *
import re
import cloudscraper

def discfan_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://discfan.net/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='419'
        logger.info('已成功填写类型为动漫')
    elif 'show' in file1.pathinfo.type.lower():
        select_type='416'
        logger.info('已成功填写类型为综艺')                  
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='411'
        logger.info('已成功填写类型为剧集')          
    elif 'movie' in file1.pathinfo.type.lower() and '大陆' in file1.country:
        select_type='401'
        logger.info('已成功填写类型为中国大陆')
    elif 'movie' in file1.pathinfo.type.lower() and '香港' in file1.country:
        select_type='404'
        logger.info('已成功填写类型为中国香港')  
    elif 'movie' in file1.pathinfo.type.lower() and '台湾' in file1.country:
        select_type='405'
        logger.info('已成功填写类型为中国台湾')
    elif 'movie' in file1.pathinfo.type.lower() and '泰国' in file1.country:
        select_type='402'
        logger.info('已成功填写类型为泰国')
    elif 'movie' in file1.pathinfo.type.lower() and '日本' in file1.country:
        select_type='403'
        logger.info('已成功填写类型为日本')
    elif 'movie' in file1.pathinfo.type.lower() and '韩国' in file1.country:
        select_type='406'
        logger.info('已成功填写类型为韩国')                          
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='413'
        logger.info('已成功填写类型为纪录片')          
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='414'
        logger.info('已成功填写类型为MV')          
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='417'
        logger.info('已成功填写类型为体育')          
    elif 'music' in file1.pathinfo.type.lower():
        select_type='414'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='410'
        logger.info('已成功填写类型为其它')          
        


    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        source_sel='9'
        logger.info('已成功选择媒介为WEB-DL')  
    elif 'UHD' in file1.pathinfo.medium.upper():
        source_sel='2'
        logger.info('已成功选择媒介为UHD-BLURAY')        
    elif 'BLU' in file1.pathinfo.medium.upper():
        source_sel='3'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        source_sel='10'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.pathinfo.medium.upper():
        source_sel='5'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.pathinfo.medium.upper():
        source_sel='131'
        logger.info('已成功选择媒介为REMUX')
    elif 'DVD' in file1.pathinfo.medium.upper():
        source_sel='4'
        logger.info('已成功选择媒介为DVD')      
    else:
        source_sel='0'
        logger.info('未识别到媒介信息，不选择媒介')



    #选择标签
    if 'HDR' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY标签')            
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语标签')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字标签')
    if '粤' in file1.language:
        tags.append(8)
        logger.info('已选择粤语')
    
    tags=list(set(tags))
    tags.sort()
    
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
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "source_sel[4]": source_sel,
            "uplver": uplver,
            "tags[4][]": tags,
            }

    scraper=cloudscraper.create_scraper()
    success_upload=0
    try_upload=0
    while success_upload==0:
        try_upload+=1
        if try_upload>5:
            return False,fileinfo+' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)