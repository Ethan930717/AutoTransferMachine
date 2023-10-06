from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def hdu_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        logger.info('已成功填写类型为Movie')                     
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
        select_type='411'
        logger.info('已成功填写类型为其它')          
        


    #选择媒介
    if 'DVD' in file1.type.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为DVD')  
    elif 'tv' in file1.pathinfo.type.lower() and 'WEB' in file1.type.upper():
        medium_sel='13'
        logger.info('已成功选择媒介为WEB-DL TV')
    elif 'WEB' in file1.type.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为WEB-DL')   
    elif 'tv' in file1.pathinfo.type.lower() and 'UHD' in file1.type.upper() and 'REMUX' in file1.type.upper():
        medium_sel='16'
        logger.info('已成功选择媒介为TV UHD-REMUX')
    elif 'UHD' in file1.type.upper() and 'REMUX' in file1.type.upper():
        medium_sel='15'
        logger.info('已成功选择媒介为UHD-REMUX')
    elif 'tv' in file1.pathinfo.type.lower() and 'REMUX' in file1.type.upper():
        medium_sel='12'
        logger.info('已成功选择媒介为REMUX TV')
    elif 'REMUX' in file1.type.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为REMUX')
    elif 'UHD' in file1.type.upper():
        medium_sel='11'
        logger.info('已成功选择媒介为UHDBLURAY')           
    elif 'BLU' in file1.type.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'tv' in file1.pathinfo.type.lower() and 'ENCODE' in file1.type.upper():
        medium_sel='14'
        logger.info('已成功选择媒介为ENCODETV')
    elif 'ENCODE' in file1.type.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为ENCODE')           
    elif 'HDTV' in file1.type.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.type.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为REMUX')
    elif 'BD' in file1.type.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为MiniBD') 
    elif 'CD' in file1.type.upper():
        medium_sel='9'
        logger.info('已成功选择媒介为CD')       
    else:
        medium_sel='7'
        logger.info('未识别到媒介信息，选择other')

    #选择编码
    if 'H' in file1.Videio_Format.upper() and '264' in file1.Videio_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.Videio_Format.lower() and '264' in file1.Videio_Format:
        codec_sel='16'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.Videio_Format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.Videio_Format.upper() and '265' in file1.Videio_Format:
        codec_sel='14'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.Videio_Format.lower() and '265' in file1.Videio_Format:
        codec_sel='14'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.Videio_Format.upper():
        codec_sel='14'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG' in file1.Videio_Format.upper():
        codec_sel='18'
        logger.info('已成功选择编码为MPEG-2')         
    elif 'VC' in file1.Videio_Format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')          
    elif 'AV1' in file1.Videio_Format.upper():
        codec_sel='5'
        logger.info('已成功选择编码为AV1')    
    elif 'XVID' in file1.Videio_Format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')        
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，选择other')  


    #选择音频编码
    if file1.Audio_Format=='AAC':
        audiocodec_sel='6'
    elif 'DTS' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    elif 'DTS' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'MPEG' in file1.Audio_Format.upper():
        audiocodec_sel='18'
    else:
        audiocodec_sel='13'
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
        standard_sel='1'
    logger.info('已成功选择分辨率')

    #选择处理
    if '大陆' in file1.country:
        processing_sel='1'
    elif '香港' in file1.country or '台湾' in file1.country:
        processing_sel='2'
    elif '日本' in file1.country:
        processing_sel='4'
    elif '韩国' in file1.country:
        processing_sel='5'
    elif '印度' in file1.country:
        processing_sel='6'
    elif '泰国' in file1.country or '越南' in file1.country or '柬埔寨' in file1.country or '缅甸' in file1.country or '马来西亚' in file1.country or '新加坡' in file1.country or '印度尼西亚' in file1.country or '菲律宾' in file1.country or '文莱' in file1.country or '东帝汶' in file1.country or '印尼' in file1.country :
        processing_sel='4'
    else:
        processing_sel='2'

    #选择制作组
    if 'HDU' in file1.sub.upper():
        team_sel='2'
    else:
        team_sel='5'
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
            "processing_sel": processing_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "tags[]": tags,
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