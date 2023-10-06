from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def hdatmos_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        tags.append(12)
        logger.info('已选择动画标签')
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='408'

    else:
        select_type='401'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择来源
    if 'WEB' in file1.type.upper():
        source_sel='2'
        logger.info('已成功选择媒介为WEB-DL')        
    elif 'UHD' in file1.type.upper():
        source_sel='6'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')
    elif 'BLU' in file1.type.upper():
        source_sel='6'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'ENCODE' in file1.type.upper():
        source_sel='1'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.type.upper():
        source_sel='3'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.type.upper():
        source_sel='5'
        logger.info('已成功选择媒介为REMUX')
    elif 'DVD' in file1.type.upper() and 'HD' in file1.type.upper():
        source_sel='7'
        logger.info('已成功选择媒介为DVD')  
    elif 'DVD' in file1.type.upper():
        source_sel='8'
        logger.info('已成功选择媒介为DVD')
    elif 'CD' in file1.type.upper():
        source_sel='8'
        logger.info('已成功选择媒介为CD')
    elif 'MINI' in file1.type.upper():
        source_sel='4'
        logger.info('已成功选择媒介为MINIBD')   
    elif 'CD' in file1.type.upper():
        source_sel='9'
        logger.info('已成功选择媒介为TRACK')       
    else:
        source_sel='12'
        logger.info('未识别到媒介信息，不选择媒介')



    #选择媒介
    if 'WEB' in file1.type.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为WEB-DL')        
    elif 'UHD' in file1.type.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')
    elif 'BLU' in file1.type.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'ENCODE' in file1.type.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.type.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.type.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为REMUX')
    elif 'DVD' in file1.type.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为DVD') 
    elif 'CD' in file1.type.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD')
    elif 'MINI' in file1.type.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为MINIBD')   
    elif 'DVD' in file1.type.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为TRACK')       
    else:
        medium_sel='13'
        logger.info('未识别到媒介信息，不选择媒介')



    #选择编码
    if 'H' in file1.Videio_Format.upper() and '264' in file1.Videio_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.Videio_Format.lower() and '264' in file1.Videio_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.Videio_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.Videio_Format.upper() and '265' in file1.Videio_Format:
        codec_sel='10'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.Videio_Format.lower() and '265' in file1.Videio_Format:
        codec_sel='10'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.Videio_Format.upper():
        codec_sel='10'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-4' in file1.Videio_Format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-4') 
    elif 'MPEG-2' in file1.Videio_Format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')          
    elif 'VC' in file1.Videio_Format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')          
    elif 'XVID' in file1.Videio_Format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')      
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，已选择Others')  

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='20'
    elif 'DTS-HD' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'DTS' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper() :
        audiocodec_sel='12'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='18'
    elif 'DD' in file1.Audio_Format.upper() and '5.1' in file1.Audio_Format.upper():
        audiocodec_sel='23'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='22'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='22'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='19'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'DSD' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    else:
        audiocodec_sel='21'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='15'
    elif '2160' in file1.standard_sel:
        standard_sel='10'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='11'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='12'
    elif '720' in file1.standard_sel:
        standard_sel='13'
    elif 'SD' in file1.standard_sel:
        standard_sel='14'
    else:
        standard_sel='16'
    logger.info('已成功选择分辨率为'+file1.standard_sel)

    #选择处理
    if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
        processing_sel='3'
    elif '美国' in file1.country:
        processing_sel='4'
    elif '日本' in file1.country:
        processing_sel='5'
    elif '韩国' in file1.country:
        processing_sel='6'
    elif '德国' in file1.country:
        processing_sel='8'
    elif not '新加坡' in file1.country and not '马来西亚' in file1.country and not '泰国' in file1.country:
        processing_sel='9'
    else:
        processing_sel='9'

    team_sel='22'
    
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
            "source_sel[8]": medium_sel,
            "team_sel[8]": team_sel,
            "medium_sel[8]": medium_sel,
            "standard_sel[8]": standard_sel,
            "codec_sel[8]": codec_sel,
            "audiocodec_sel[8]": audiocodec_sel,
            "processing_sel[8]": processing_sel,
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