from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def yiptba_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
    elif 'music' in file1.pathinfo.type.lower():
        select_type='411'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='405'
        logger.info('已成功填写类型为其它')          
        




    #选择来源
    if 'WEB' in file1.pathinfo.source.upper():
        source_sel='23'
        logger.info('已成功选择来源为WEB-DL')  
    elif 'UHD' in file1.pathinfo.source.upper() and 'DIY' in file1.pathinfo.source.upper():
        source_sel='17'
        logger.info('已成功选择来源为UHD-BLURAY DIY')         
    elif 'UHD' in file1.pathinfo.source.upper():
        source_sel='16'
        logger.info('已成功选择来源为UHD-BLURAY')        
    elif 'BLU' in file1.pathinfo.source.upper() and 'DIY' in file1.pathinfo.source.upper():
        source_sel='19'
        logger.info('已成功选择来源为BLURAY DIY') 
    elif 'BLU' in file1.pathinfo.source.upper():
        source_sel='1'
        logger.info('已成功选择来源为BLURAY')         
    elif 'ENCODE' in file1.pathinfo.source.upper():
        source_sel='22'
        logger.info('已成功选择来源为ENCODE')         
    elif 'HDTV' in file1.pathinfo.source.upper():
        source_sel='4'
        logger.info('已成功选择来源为HDTV')         
    elif 'REMUX' in file1.pathinfo.source.upper():
        source_sel='20'
        logger.info('已成功选择来源为REMUX')         
    else:
        source_sel='6'
        logger.info('已成功选择来源为其它') 

    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='0'
        logger.info('已成功选择媒介为WEB-DL')        
    elif 'UHD' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='17'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')         
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='16'
        logger.info('已成功选择媒介为UHD-BLURAY')        
    elif 'BLU' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='19'
        logger.info('已成功选择媒介为BLURAY DIY') 
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
    else:
        medium_sel='0'
        logger.info('未识别到媒介信息，不选择媒介')


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='18'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='18'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='18'
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
        codec_sel='0'
        logger.info('未识别到视频编码信息，不选择')  


    #选择音频编码
    if file1.pathinfo.audio_format=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.pathinfo.audio_format.upper() or 'DTS-HD MA' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='3'
    elif 'AutoTransferMachineOS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'TRUE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'FLAC' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='4'
    elif 'EAC3' in file1.pathinfo.audio_format.upper() or 'EAC-3' in file1.pathinfo.audio_format.upper() or 'DDP' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'AC3' in file1.pathinfo.audio_format.upper() or 'AC-3' in file1.pathinfo.audio_format.upper() or 'DD' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'DTS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'OGG' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='5'
    elif 'OPUS' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='7'
    elif 'AAC' in file1.pathinfo.audio_format.upper():
        audiocodec_sel='6'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码')

    #选择分辨率
    if '8K' in file1.standard_sel :
        standard_sel='17'
    elif '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='16'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif 'SD' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率')
    
    #选择处理
    if 'ENCODE' in file1.pathinfo.medium.upper():
        processing_sel='2'
    else:
        processing_sel='1'

    #选择标签
    if 'HDR10+' in file1.pathinfo.tags:
        tags.append(22)
        logger.info('已选择HDR10+标签')
    elif 'HDR10' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR10标签')
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append(21)
        logger.info('已选择杜比视界标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY标签')            
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语标签')
    if '粤' in file1.language:
        tags.append(19)
        logger.info('已选择粤语标签')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
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
            "url": file1.imdburl,
            "pt_gen": file1.doubanurl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info+'\n'+file1.screenshoturl+'\n'+file1.pathinfo.contenttail,
            "technical_info": file1.mediainfo,
            "type": select_type,
            "medium_sel[4]": medium_sel,
            "source_sel[4]": source_sel,
            "standard_sel[4]": standard_sel,
            "codec_sel[4]": codec_sel,
            "audiocodec_sel[4]": audiocodec_sel,
            "processing_sel[4]": processing_sel,
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