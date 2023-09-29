from loguru import logger
import time
import os
from AutoTransferMachine.utils.uploader.upload_tools import *
import re
import cloudscraper

def wuerpt_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
    elif 'opera' in file1.pathinfo.type.lower():
        select_type='410'
        logger.info('已成功填写类型为戏曲')        
    elif 'audio' in file1.pathinfo.type.lower():
        select_type='408'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='401'
        logger.info('已成功填写类型为电影')          
        


    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为WEB-DL')        
    elif 'UHD' in file1.pathinfo.medium.upper() and "中字" not in file1.pathinfo.tags:
        medium_sel='15'
        logger.info('已成功选择媒介为4K原盘中字')         
    elif 'UHD' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='12'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')
    elif 'UHD' in file1.pathinfo.medium.upper() and 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为UHD无中文')
    elif 'BLU' in file1.pathinfo.medium.upper() and "中字" not in file1.pathinfo.tags:
        medium_sel='14'
        logger.info('已成功选择媒介为2K原盘中字')          
    elif 'BLU' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='12'
        logger.info('已成功选择媒介为BLURAY DIY')
    elif 'BLU' in file1.pathinfo.medium.upper() and 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为BLURAY DIY') 
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='11'
        logger.info('已成功选择媒介为BLURAY无中文')         
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为HDTV')        
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为DVD/DVDR')   
    elif 'CD' in file1.pathinfo.medium.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD/HDCD')
    elif '8K' in file1.pathinfo.medium.upper():
        medium_sel='13'
        logger.info('已成功选择媒介为8K')       
    else:
        medium_sel='9'
        logger.info('未识别到媒介信息，已选择Others')


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='13'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='11'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='13'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='14'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='12'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='1'
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
        audiocodec_sel='4'
        logger.info('已选择音频编码为DTS.HDMA')  
    elif 'AutoTransferMachineOS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='10'
        logger.info('已选择音频编码为TrueHD AutoTransferMachineos')  
    elif 'TRUE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='12'
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
        audiocodec_sel='4'
        logger.info('已选择音频编码为MP3')  
    elif 'EAC3' in file1.pathinfo.audio_format.upper() or 'EAC-3' in file1.pathinfo.audio_format.upper() or 'DDP' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='6'
        logger.info('已选择音频编码为DD')  
    elif 'AC3' in file1.pathinfo.audio_format.upper() or 'AC-3' in file1.pathinfo.audio_format.upper() or 'DD' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='6'
        logger.info('已选择音频编码为DD')  
    elif 'DTS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='3'
        logger.info('已选择音频编码为DTS')  
    elif 'WAV' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='11'
        logger.info('已选择音频编码为WAV')  
    elif 'AAC' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='13'
        logger.info('已选择音频编码为AAC')  
    elif 'LPCM' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='14'
        logger.info('已选择音频编码为LPCM') 
    else:
        audiocodec_sel='7'
        logger.info('未查询到音频编码，已选择音频编码为Others')  
    #选择分辨率
    if '8K' in file1.standard_sel :
        standard_sel='7'
    elif '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    else:
        standard_sel='6'
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
            "tags[]": tags,
            }
    scraper=cloudscraper.create_scraper()
    headers = {
        'authority': '52pt.site',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #'content-length': '6820',
        'cookie': siteinfo.cookie,
        'origin': 'https://52pt.site',
        'referer': 'https://52pt.site/upload.php',
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