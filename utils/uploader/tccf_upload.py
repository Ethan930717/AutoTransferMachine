from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def tccf_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'doc' in file1.pathinfo.type.lower():
        select_type='624'
        logger.info('已成功填写类型为纪录片')   
    else:
        select_type='0'
        logger.info('已成功填写类型为纪录片')        
        
    #选择次类型
    source_sel='14'   

    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='9'      
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='10'
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='1'
    elif 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为REMUX')           
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        medium_sel='11'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为HDTV')        
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为DVD/DVDR')     
    else:
        medium_sel='8'
        logger.info('未识别到媒介信息，已选择Others')


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='7'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='8'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='8'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG')          
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')          
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')          
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，已选择others')  


    #选择音频编码
    if file1.pathinfo.audio_format=='AAC':
        audiocodec_sel='6'
        logger.info('已选择音频编码为AAC')  
    elif 'DTS-HDMA' in file1.pathinfo.audio_format.upper() or 'DTS-HD MA' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='8'
        logger.info('已选择音频编码为DTS.HDMA')  
    elif 'AutoTransferMachineOS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='9'
        logger.info('已选择音频编码为TrueHD AutoTransferMachineos')  
    elif 'TRUE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='9'
        logger.info('已选择音频编码为TrueHD')  
    elif 'DTS:X' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='3'
        logger.info('已选择音频编码为DTS:X')  
    elif 'FLAC' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='1'
        logger.info('已选择音频编码为FLAC')  
    elif 'APE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='2'
        logger.info('已选择音频编码为APE')  
    elif 'MP3' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='5'
        logger.info('已选择音频编码为MP3')  
    elif 'EAC3' in file1.pathinfo.audio_format.upper() or 'EAC-3' in file1.pathinfo.audio_format.upper() or 'DDP' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='4'
        logger.info('已选择音频编码为DD')  
    elif 'AC3' in file1.pathinfo.audio_format.upper() or 'AC-3' in file1.pathinfo.audio_format.upper() or 'DD' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='4'
        logger.info('已选择音频编码为DD')  
    elif 'DTS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='3'
        logger.info('已选择音频编码为DTS')  
    elif 'WAV' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='11'
        logger.info('已选择音频编码为WAV')  
    elif 'AAC' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='6'
        logger.info('已选择音频编码为AAC')  
    elif 'LPCM' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='10'
        logger.info('已选择音频编码为LPCM') 
    else:
        audiocodec_sel='7'
        logger.info('未查询到音频编码，已选择音频编码为Others')  
    #选择分辨率
    if '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率')

   #选择制作组
    if 'TLF' in file1.sub.upper():
        team_sel='2'
    elif 'BMDRU' in file1.sub.upper():
        team_sel='3'
    elif 'CATEDU' in file1.sub.upper():
        team_sel='4'
    elif 'MADFOX' in file1.sub.upper():
        team_sel='5'
    else:
        team_sel='7'
    
    
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
            "source_sel": source_sel,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "tags[]": tags,
            }
    scraper=cloudscraper.create_scraper()
    headers = {
        'authority': 'et8.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #'content-length': '6820',
        'cookie': 'c_secure_uid=NzM1MDE%3D; c_secure_pass=05e0bd3a6d27c02a24fc4b012d355334; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=eWVhaA%3D%3D; c_secure_login=bm9wZQ%3D%3D',
        'origin': 'https://et8.org',
        'referer': 'https://et8.org/upload.php',
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