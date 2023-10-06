from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def itzmx_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        select_type='405'
        logger.info('已成功填写类型为动漫')        
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
        logger.info('已成功填写类型为剧集')          
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.type.upper():
        select_type='401'
        logger.info('已成功填写类型为电影')                      
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='402'
        logger.info('已成功填写类型为纪录片')          
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='408'
        logger.info('已成功填写类型为MV')                    
    elif 'music' in file1.pathinfo.type.lower():
        select_type='408'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='401'
        logger.info('已成功填写类型为其它')          
        




    #选择分辨率
    if '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='3'
    elif '1080' in file1.standard_sel.lower():
        standard_sel='1'
    elif '720' in file1.standard_sel:
        standard_sel='2'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率')

        #选择制作组
    team_sel='1'
    logger.info('制作组已成功选择为other')

    

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "standard_sel": standard_sel,
            "team_sel": team_sel,
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