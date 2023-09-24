from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper

def pter_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://pterclub.com/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='405'        
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'music' in file1.pathinfo.type.lower() and 'video' in file1.pathinfo.type.lower():
        select_type='418'        
    elif 'music' in file1.pathinfo.type.lower():
        select_type='406'                
    else:
        select_type='412'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择来源 
    if 'WEB' in file1.pathinfo.medium.upper():
        source_sel='5'
        logger.info('已成功选择来源为WEB-DL')         
    elif 'UHD' in file1.pathinfo.medium.upper():
        source_sel='1'
        logger.info('已成功选择来源为UHD-BLURAY')        
    elif 'BLU' in file1.pathinfo.medium.upper():
        source_sel='2'
        logger.info('已成功选择来源为BLURAY')         
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        source_sel='6'
        logger.info('已成功选择来源为ENCODE')         
    elif 'HDTV' in file1.pathinfo.medium.upper():
        source_sel='4'
        logger.info('已成功选择来源为HDTV')         
    elif 'REMUX' in file1.pathinfo.medium.upper():
        source_sel='3'
        logger.info('已成功选择来源为REMUX')
    elif 'DVD' in file1.pathinfo.medium.upper():
        source_sel='7'
        logger.info('已成功选择来源为DVD')
    elif 'FLAC' in file1.pathinfo.audio_format.upper():
        source_sel='8'
        logger.info('已成功选择来源为FLAC')                             
    else:
        source_sel='15'
        logger.info('已成功选择来源为其它') 

    
    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            team_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            team_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            team_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '俄' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '瑞' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)                 
        elif '韩国' in file1.country:
            team_sel='5'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            team_sel='6'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            team_sel='7'
            logger.info('国家信息已选择'+file1.country)
        else:
            team_sel='4'
            logger.info('未找到资源国家信息，选择欧美')
    else:
        team_sel='4'
        logger.info('未找到资源国家信息，选择欧美')


    jinzhuan = 'no'
    guoyu    = 'no'
    zhongzi  = 'no'
    pr       = 'no'
    guanfang = 'no'
    uplver   = 'no'
    if 'audience' in file1.pathinfo.exclusive :
        jinzhuan = 'yes'
    if '国' in file1.language or '中' in file1.language or '国' in file1.pathinfo.tags:
        guoyu    = 'yes'
    if '粤' in file1.language or '粤' in file1.pathinfo.tags:
        yueyu    = 'yes'        
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan) or '中' in file1.pathinfo.tags:
        zhongzi  = 'yes'
    if '英' in file1.sublan:
        ensub  = 'yes'        
    if 'PTER' in file1.sub.upper():
        guanfang = 'yes'
    
    tags=list(set(tags))
    tags.sort()
    
    if siteinfo.uplver==1:
        uplver='yes'

        

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            
    
    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url": file1.imdburl,
            "douban": file1.doubanurl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info+'\n'+"[hide=Mediainfo]"+file1.mediainfo+"[/hide]"+'\n'+file1.screenshoturl+'\n'+file1.pathinfo.contenttail,
            "type": select_type,
            "source_sel": source_sel,
            "team_sel": team_sel,
            }
    buttomlist=["uplver","jinzhuan","guoyu","zhongzi","pr","guanfang"]
    for item in buttomlist:
        if eval(item+"=='yes'"):
            exec('other_data["'+item+'"]="yes"')
            

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