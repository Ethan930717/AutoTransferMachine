from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper

def hdarea_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://hdarea.club/takeupload.php"
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
    elif 'movie' in file1.pathinfo.type.lower() and 'UHD' in file1.pathinfo.medium.upper():
        select_type='300'
        logger.info('已成功填写类型为Movie UHD-4K')
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.pathinfo.medium.upper():
        select_type='401'
        logger.info('已成功填写类型为Movie Blu-Ray')
    elif 'movie' in file1.pathinfo.type.lower() and 'REMUX' in file1.pathinfo.medium.upper():
        select_type='415'
        logger.info('已成功填写类型为Movie REMUX')
    elif 'movie' in file1.pathinfo.type.lower() and 'WEB' in file1.pathinfo.medium.upper():
        select_type='412'
        logger.info('已成功填写类型为Movie WEB-DL')
    elif 'movie' in file1.pathinfo.type.lower() and 'DVD' in file1.pathinfo.medium.upper():
        select_type='414'
        logger.info('已成功填写类型为Movie DVD') 
    elif 'movie' in file1.pathinfo.type.lower() and 'HDTV' in file1.pathinfo.medium.upper():
        select_type='413'
        logger.info('已成功填写类型为Movie HDTV')  
    elif 'movie' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='410'
        logger.info('已成功填写类型为Movie 1080p')
    elif 'movie' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_type='411'
        logger.info('已成功填写类型为Movie 720p')                       
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
        select_type='410'
        logger.info('已成功填写类型为其它')          
        


    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='9'
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
        medium_sel='0'
        logger.info('未识别到媒介信息，不选择媒介')

    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='7'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='7'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='7'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-4' in file1.pathinfo.video_format.upper():
        codec_sel='1'
        logger.info('已成功选择编码为MPEG-4')  
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')         
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')          
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')          
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，不选择')  


    #选择音频编码
    if file1.pathinfo.audio_format=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.pathinfo.audio_format.upper() or 'DTS-HD MA' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='4'
    elif 'ATMOS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='10'
    elif 'TRUE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'FLAC' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='4'
    elif 'EAC3' in file1.pathinfo.audio_format.upper() or 'EAC-3' in file1.pathinfo.audio_format.upper() or 'DDP' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='11'
    elif 'AC3' in file1.pathinfo.audio_format.upper() or 'AC-3' in file1.pathinfo.audio_format.upper() or 'DD' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='5'
    elif 'DTS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='9'
    elif 'LPCM' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='8'
    else:
        audiocodec_sel='0'
    logger.info('已成功选择音频编码')

    #选择分辨率
    if '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif 'SD' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='0'
    logger.info('已成功选择分辨率')
    


    
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
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "uplver": uplver,
            }
    scraper=cloudscraper.create_scraper()
    headers = {
        'authority': 'hdarea.club',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #'content-length': '6820',
        'cookie': siteinfo.cookie,
        'origin': 'https://hdarea.club',
        'referer': 'https://hdarea.club/upload.php',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0',
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