from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def pttime_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='431'
        logger.info('已成功填写类型为动漫') 
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'
        logger.info('已成功填写类型为综艺')                
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
        logger.info('已成功填写类型为剧集')          
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
        logger.info('已成功填写类型为电影')                   
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
        logger.info('已成功填写类型为纪录片')          
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='408'
        logger.info('已成功填写类型为MV')          
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='405'
        logger.info('已成功填写类型为体育')          
    elif 'music' in file1.pathinfo.type.lower():
        select_type='408'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='490'
        logger.info('已成功填写类型为其它')          
        

    #选择标签

    if '国' in file1.language or '中' in file1.language:
        tags.append('gy')
        logger.info('已选择国语')
    if '粤' in file1.language:
        tags.append('yue')
        logger.info('已选择粤语')
    if '韩' in file1.language:
        tags.append('hy')
        logger.info('已选择韩语')
    if '日' in file1.language:
        tags.append('yue')
        logger.info('已选择日语')
    if '英' in file1.language:
        tags.append('yy')
        logger.info('已选择英语')
    if '印' in file1.language:
        tags.append('ydy')
        logger.info('已选择印语')
    if not file1.sublan=='' and not '国' in file1.language and not '中' in file1.language and not '粤' in file1.language and not '韩' in file1.language and not '日' in file1.language and not '英' in file1.language and not '印' in file1.language:
        tags.append('wy')
        logger.info('已选择其他语种')


    if '英' in file1.sublan and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append('zy')
        logger.info('已选择中英双字')
    elif '简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan:
        tags.append('zz')
        logger.info('已选择中字')
    elif '英' in file1.sublan:
        tags.append('yz')
        logger.info('已选择中字')
    elif not file1.sublan=='':
        tags.append('qt')
        logger.info('已选择其他字幕')

    elif 'HDR10' in file1.pathinfo.tags:
        tags.append('hdr')
        logger.info('已选择HDR10标签')
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append('dbsj')
        logger.info('已选择杜比视界标签')
    if 'blu' in file1.type.lower():
        tags.append('dwj')
        logger.info('已选择原盘标签') 
    if '2160' in file1.standard_sel or '4k' in file1.standard_sel.lower():
        tags.append('sk')
        logger.info('已选择4K标签')     

    
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
            "url" : file1.imdburl,
            "dburl": file1.doubanurl, 
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "anonymous": uplver,
            "tags[]": tags,
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