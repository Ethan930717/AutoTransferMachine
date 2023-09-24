from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper

def dajiao_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://dajiao.cyou/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='405'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'        
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection>=1:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='402'
        else:
            select_type='402'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='402'
        else:
            select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='415'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='417'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='409'
    else:
        select_type='405'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为WEB-DL')            
    elif 'BLU' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='11'
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
    elif 'DVDR' in file1.pathinfo.medium.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为DVDR')
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='2'
        logger.info('已成功选择媒介为HD DVD')  
    elif 'BD' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为MiniBD')                                    
    else:
        medium_sel='7'
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
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='6'
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
        logger.info('未识别到视频编码信息，选择other')  

#选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())
        


    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='6'
    elif '2160' in file1.standard_sel:
        standard_sel='6'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif 'SD' in file1.standard_sel:
        standard_sel='4'        
    elif '480' in file1.standard_sel:
        standard_sel='7'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
    #选择制作组
    if 'DJWEB' in file1.sub.upper():
        team_sel='1'
    elif 'DJTV' in file1.sub.upper():
        team_sel='2'
    elif 'DJZB' in file1.sub.upper():
        team_sel='3'
    elif 'CatEDU' in file1.sub.upper():
        team_sel='6'
    elif 'Zaxyzit' in file1.sub.upper():
        team_sel='8'
    else:
        team_sel='7'
    logger.info('制作组已成功选择为'+file1.sub)
    

    if 'dajiao' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')
    if 'HDR10' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR10标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY标签')
    if 'doc' in file1.pathinfo.type.lower() and '国家地理' in file1.pathinfo.small_descr:
        tags.append(18)
    if 'doc' in file1.pathinfo.type.lower() and '探索' in file1.pathinfo.small_descr:
        tags.append(20)
    if 'doc' in file1.pathinfo.type.lower() and '历史' in file1.pathinfo.small_descr:
        tags.append(21)
    if 'doc' in file1.pathinfo.type.lower() and 'CCTV' in file1.pathinfo.small_descr:
        tags.append(8)
    if 'doc' in file1.pathinfo.type.lower() and 'NHK' in file1.pathinfo.small_descr:
        tags.append(19)
    if 'doc' in file1.pathinfo.type.lower() and 'BBC' in file1.pathinfo.small_descr:
        tags.append(17)
    if 'doc' in file1.pathinfo.type.lower() and '美食' in file1.pathinfo.small_descr:
        tags.append(12)
    if 'doc' in file1.pathinfo.type.lower() and ('人文' in file1.pathinfo.small_descr or '社会' in file1.pathinfo.small_descr):
        tags.append(11)
    if 'doc' in file1.pathinfo.type.lower() and ('动物' in file1.pathinfo.small_descr or '自然' in file1.pathinfo.small_descr):
        tags.append(23)
    if 'doc' in file1.pathinfo.type.lower() and '医' in file1.pathinfo.small_descr:
        tags.append(10) 
    if 'doc' in file1.pathinfo.type.lower() and ('人物' in file1.pathinfo.small_descr or '传记' in file1.pathinfo.small_descr):
        tags.append(16)
    if 'doc' in file1.pathinfo.type.lower() and ('军事' in file1.pathinfo.small_descr or '太空' in file1.pathinfo.small_descr or '宇宙' in file1.pathinfo.small_descr):
        tags.append(22) 
    if 'doc' in file1.pathinfo.type.lower() and ('运动' in file1.pathinfo.small_descr or '探险' in file1.pathinfo.small_descr):
        tags.append(14)                                                                     


    
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
            "codec_sel[4]": codec_sel,
            "standard_sel[4]": standard_sel,
            "team_sel[4]": team_sel,
            "audiocodec_sel[4]": audiocodec_sel,
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