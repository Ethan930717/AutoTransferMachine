from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper

def joyhd_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://www.joyhd.net/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='405'
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
        select_type='406'
        logger.info('已成功填写类型为MV')          
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
        logger.info('已成功填写类型为体育')          
    elif 'music' in file1.pathinfo.type.lower():
        select_type='414'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='409'
        logger.info('已成功填写类型为其它')          
        




    #子类型
    if 'movie' in file1.pathinfo.type.lower() and '10bit' in file1.pathinfo.video_format:
        select_source='5'
        logger.info('已成功填写类型为Movie 10bit') 
    elif 'movie' in file1.pathinfo.type.lower() and 'WEB' in file1.pathinfo.medium.upper():
        select_source='4'
        logger.info('已成功填写类型为Movie WEBDL') 
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.pathinfo.medium.upper():
        select_source='55'
        logger.info('已成功填写类型为Movie BLURAY')  
    elif 'movie' in file1.pathinfo.type.lower() and 'DVD' in file1.pathinfo.medium.upper():
        select_source='79'
        logger.info('已成功填写类型为Movie DVD')         
    elif 'movie' in file1.pathinfo.type.lower() and 'HDTV' in file1.pathinfo.medium.upper():
        select_source='80'
        logger.info('已成功填写类型为Movie HDTV')
    elif 'movie' in file1.pathinfo.type.lower() and 'ENCODE' in file1.pathinfo.medium.upper():
        select_source='81'
        logger.info('已成功填写类型为Movie BDRIP')
    elif 'movie' in file1.pathinfo.type.lower() and 'REMUX' in file1.pathinfo.medium.upper():
        select_source='57'
        logger.info('已成功填写类型为Movie REMUX')
    elif 'movie' in file1.pathinfo.type.lower() and '2160p' in file1.standard_sel.lower():
        select_source='82'
        logger.info('已成功填写类型为Movie 2160p')
    elif 'movie' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_source='6'
        logger.info('已成功填写类型为Movie 1080p')
    elif 'movie' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_source='7'
        logger.info('已成功填写类型为Movie 720p')               

    elif 'show' in file1.pathinfo.type.lower():
        select_source='15'
        logger.info('已成功填写类型为综艺综合')   

    elif 'tv' in file1.pathinfo.type.lower() and '大陆' in file1.country:
        select_source='23'
        logger.info('已成功填写类型为中国大陆')
    elif 'tv' in file1.pathinfo.type.lower() and '香港' in file1.country:
        select_source='24'
        logger.info('已成功填写类型为中国香港')  
    elif 'tv' in file1.pathinfo.type.lower() and '台湾' in file1.country:
        select_source='24'
        logger.info('已成功填写类型为中国台湾')
    elif 'tv' in file1.pathinfo.type.lower() and '泰国' in file1.country:
        select_source='70'
        logger.info('已成功填写类型为泰国')
    elif 'tv' in file1.pathinfo.type.lower() and '日本' in file1.country:
        select_source='26'
        logger.info('已成功填写类型为日本')
    elif 'tv' in file1.pathinfo.type.lower() and '韩国' in file1.country:
        select_source='27'
        logger.info('已成功填写类型为韩国')  
    elif 'tv' in file1.pathinfo.type.lower() and '美国' in file1.country:
        select_source='25'
        logger.info('已成功填写类型为美国')    
    elif 'tv' in file1.pathinfo.type.lower():
        select_source='70'
        logger.info('已成功填写类型为其他剧集')   


    elif 'anime' in file1.pathinfo.type.lower() and '完结' in file1.pathinfo.tags:
        select_source='66'
        logger.info('已成功填写类型为动漫完结')
    elif 'anime' in file1.pathinfo.type.lower():
        select_source='67'
        logger.info('已成功填写类型为动漫剧场版')

    elif 'doc' in file1.pathinfo.type.lower() and '国家地理' in file1.pathinfo.small_descr:
        select_source='34'
        logger.info('已成功填写类型为纪录片国家地理')
    elif 'doc' in file1.pathinfo.type.lower() and '探索' in file1.pathinfo.small_descr:
        select_source='35'
        logger.info('已成功填写类型为纪录片探索')
    elif 'doc' in file1.pathinfo.type.lower() and '历史' in file1.pathinfo.small_descr:
        select_source='40'
        logger.info('已成功填写类型为纪录片历史')
    elif 'doc' in file1.pathinfo.type.lower() and 'CCTV' in file1.pathinfo.small_descr:
        select_source='37'
        logger.info('已成功填写类型为纪录片CCTV')
    elif 'doc' in file1.pathinfo.type.lower() and 'NHK' in file1.pathinfo.small_descr:
        select_source='77'
        logger.info('已成功填写类型为纪录片国NHK')
    elif 'doc' in file1.pathinfo.type.lower() and 'BBC' in file1.pathinfo.small_descr:
        select_source='39'
        logger.info('已成功填写类型为纪录片BBC')
    elif 'doc' in file1.pathinfo.type.lower():
        select_source='41'
        logger.info('已成功填写类型为纪录片其他')

        
    elif 'mv' in file1.pathinfo.type.lower():
        select_source='60'
        logger.info('已成功填写类型为MV')           
    elif 'sport' in file1.pathinfo.type.lower():
        select_source='22'
        logger.info('已成功填写类型为体育')        
    elif 'music' in file1.pathinfo.type.lower():
        select_source='60'
        logger.info('已成功填写类型为体育720')          
    else:
        select_source='45'
        logger.info('已成功填写类型为其它')         



    #选择制作组
    if 'JOYHD' in file1.sub.upper():
        team_sel='1'
    elif 'IFT' in file1.sub.upper():
        team_sel='2'
    elif 'HDWING' in file1.sub.upper():
        team_sel='6'
    elif 'WIKI' in file1.sub.upper():
        team_sel='4'
    elif 'CMCT' in file1.sub.upper():
        team_sel='10'
    elif 'CHD' in file1.sub.upper():
        team_sel='8'
    elif 'BEAST' in file1.sub.upper():
        team_sel='7'
    elif 'MTEAM' in file1.sub.upper():
        team_sel='9'
    elif 'HDTIME' in file1.sub.upper():
        team_sel='11'
    elif 'SPARK' in file1.sub.upper():
        team_sel='12'
    elif 'IHQ' in file1.sub.upper():
        team_sel='15'
    else:
        team_sel='13'
    logger.info('制作组已成功选择为'+file1.sub)

    
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "imdburl": file1.imdburl,
            "dburl": file1.doubanurl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "source_sel": select_source,
            "team_sel": team_sel,
            "uplver": uplver,
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