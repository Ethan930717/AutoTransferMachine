from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def carpt_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        select_type='403'
        logger.info('已成功填写类型为动漫')       
    elif 'show' in file1.pathinfo.type.lower():
        select_type='405'
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
    elif 'music' in file1.pathinfo.type.lower():
        select_type='406'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='407'
        logger.info('已成功填写类型为其他')          

    #选择媒介
    if 'WEB' in file1.type.upper():
        medium_sel='2'
        logger.info('已成功选择媒介为WEB-DL')              
    elif 'UHD' in file1.type.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为UHD')
    elif 'BLU' in file1.type.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为BLURAY无中文')         
    elif 'ENCODE' in file1.type.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.type.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为HDTV')        
    elif 'DVD' in file1.type.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为DVD/DVDR')   
    elif 'CD' in file1.type.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为CD/HDCD')
    elif 'REMUX' in file1.type.upper():
        medium_sel='9'
        logger.info('已成功选择媒介为REMUX')       
    else:
        medium_sel='6'
        logger.info('未识别到媒介信息，已选择Others')


    #选择编码
    if 'H' in file1.Video_Format.upper() and '264' in file1.Video_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.Video_Format.lower() and '264' in file1.Video_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.Video_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.Video_Format.upper() and '265' in file1.Video_Format:
        codec_sel='2'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.Video_Format.lower() and '265' in file1.Video_Format:
        codec_sel='2'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.Video_Format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG' in file1.Video_Format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为MPEG')          
    elif 'VC' in file1.Video_Format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为VC1')          
    elif 'XVID' in file1.Video_Format.upper():
        codec_sel='5'
        logger.info('已成功选择编码为XVID')          
    else:
        codec_sel='6'
        logger.info('未识别到视频编码信息，已选择others')  
    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='7'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    else:
        audiocodec_sel='9'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '2160' in file1.standard_sel:
        standard_sel='1'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='2'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='3'
    elif 'SD' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='5'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    #选择制作组
    if 'CARPT' in file1.sub.upper():
        team_sel='1'
    elif 'WIKI' in file1.sub.upper():
        team_sel='2'
    elif 'CMCT' in file1.sub.upper():
        team_sel='3'
    elif 'M-TEAM' in file1.sub.upper() or 'MTEAM' in file1.sub.upper():
        team_sel='4'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'carpt' in file1.sub.lower():
        tags.append(3)
        logger.info('已选择官方')
    if 'carpt' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')
    if 'HDR' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR标签')

    
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
            "codec_sel[4]": codec_sel,
            "audiocodec_sel[4]": audiocodec_sel,
            "standard_sel[4]": standard_sel,
            "team_sel[4]": team_sel,
            "uplver": uplver,
            "tags[4][]": tags,
            }
    scraper=cloudscraper.create_scraper()
    headers = {
        'authority': 'carpt.net',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #'content-length': '6820',
        'cookie': siteinfo.cookie,
        'origin': 'https://carpt.net',
        'referer': 'https://carpt.net/upload.php',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62',
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