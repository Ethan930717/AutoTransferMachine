from loguru import logger
import time
import os
from AutoTransferMachine.utils.uploader.upload_tools import *
import re
import cloudscraper

def icc_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://www.icc2022.com/takeupload.php"
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
        select_type='408'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='409'
        logger.info('已成功填写类型为其它')          
        


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
    elif 'CD' in file1.pathinfo.medium.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD')       
    else:
        medium_sel='7'
        logger.info('未识别到媒介信息，选择other')

    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'VC1' in file1.pathinfo.video_format:
        codec_sel='2'
        logger.info('已成功选择编码为VC1')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='7'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')                       
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，选择other')  



    #选择分辨率
    if '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='6'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '8K' in file1.standard_sel:
        standard_sel='7'
    elif '2K' in file1.standard_sel:
        standard_sel='5'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率')

        #选择制作组
    if 'HDS' in file1.sub.upper():
        team_sel='1'
    elif 'CHD' in file1.sub.upper():
        team_sel='2'
    elif 'MYSILU' in file1.sub.upper():
        team_sel='3'
    elif 'WIKI' in file1.sub.upper():
        team_sel='4'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)

    #选择标签

    if 'HDR' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR10标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY标签')          
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语标签')
    if '粤' in file1.language:
        tags.append(11)
        logger.info('已选择粤语标签')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan) and '英' in file1.sublan:
        tags.append(10)
        logger.info('已选择中英字幕')
    elif not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字标签')
     

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
            "pt_gen": file1.doubanurl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "medium_sel[4]": medium_sel,
            "standard_sel[4]": standard_sel,
            "codec_sel[4]": codec_sel,
            "team_sel[4]": team_sel,
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