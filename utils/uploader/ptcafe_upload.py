from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def ptcafe_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        select_type='408'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='409'
        logger.info('已成功填写类型为其它')          
        




    #选择来源
    if '大陆' in file1.country:
        source_sel='1'
    elif '香港' in file1.country or '台湾' in file1.country:
        source_sel='2'
    elif '日本' in file1.country:
        source_sel='4'
    elif '韩国' in file1.country:
        source_sel='5'
    elif '印度' in file1.country:
        source_sel='6'
    elif '新加坡' in file1.country or '马来西亚' in file1.country or '泰国' in file1.country:
        source_sel='7'
    else:
        source_sel='3'

    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为WEB-DL')        
    elif 'UHD' in file1.pathinfo.medium.upper() and 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为UHD-BLURAY REMUX')   
    elif 'UHD' in file1.pathinfo.medium.upper() and 'TV' in file1.pathinfo.type.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为UHD-BLURAY REMUX')           
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='7'
        logger.info('已成功选择媒介为UHD-BLURAY')        
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='2'
        logger.info('已成功选择媒介为BLURAY')         
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为REMUX')  
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='11'
        logger.info('已成功选择媒介为DVD')   
    elif 'CD' in file1.pathinfo.medium.upper():
        medium_sel='12'
        logger.info('已成功选择媒介为CD')         
    else:
        medium_sel='13'
        logger.info('未识别到媒介信息，不选择媒介')


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='2'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='4'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='2'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='3'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='1'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='6'
        logger.info('已成功选择编码为MPEG-2')   
    elif 'MPEG-4' in file1.pathinfo.video_format.upper():
        codec_sel='7'
        logger.info('已成功选择编码为MPEG-4')        
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='5'
        logger.info('已成功选择编码为VC1')          
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='8'
        logger.info('已成功选择编码为XVID')
    elif 'VP' in file1.pathinfo.video_format.upper():
        codec_sel='9'
        logger.info('已成功选择编码为VP9')    
    elif 'DIVX' in file1.pathinfo.video_format.upper():
        codec_sel='10'
        logger.info('已成功选择编码为DIVX')              
    else:
        codec_sel='11'
        logger.info('未识别到视频编码信息，不选择')  


#选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='8'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'TAA' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    else:
        audiocodec_sel='16'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel :
        standard_sel='1'
    elif '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='2'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='3'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='3'
    elif '720' in file1.standard_sel:
        standard_sel='4'
    elif 'SD' in file1.standard_sel:
        standard_sel='5'
    else:
        standard_sel='6'
    logger.info('已成功选择分辨率')
    

    #选择制作组
    if 'ADE' in file1.sub.upper():
        team_sel='1'
    elif 'ADWEB' in file1.sub.upper():
        team_sel='2'
    elif 'AUDIES' in file1.sub.upper():
        team_sel='3'
    elif 'BEITAI' in file1.sub.upper():
        team_sel='4'
        tags.append(10)
        logger.info('已选择备胎标签')   
    elif 'CAFETV' in file1.sub.upper():
        team_sel='5'
    elif 'CAFEWEB' in file1.sub.upper():
        team_sel='6'
    elif 'CHDBITS' in file1.sub.upper():
        team_sel='8'
    elif 'CHD' in file1.sub.upper():
        team_sel='7'
    elif 'CMCT' in file1.sub.upper():
        team_sel='9'
    elif 'DREAM' in file1.sub.upper():
        team_sel='10'
    elif 'FRDS' in file1.sub.upper():
        team_sel='11'
    elif 'HARES' in file1.sub.upper():
        team_sel='12'
    elif 'HARESTV' in file1.sub.upper():
        team_sel='13'
    elif 'HARESWEB' in file1.sub.upper():
        team_sel='14'
    elif 'HDCTV' in file1.sub.upper():
        team_sel='15'
    elif 'HDHOME' in file1.sub.upper():
        team_sel='17'
    elif 'HDHTV' in file1.sub.upper():
        team_sel='18'
    elif 'HDH' in file1.sub.upper():
        team_sel='16'
    elif 'HDSKY' in file1.sub.upper():
        team_sel='20'
    elif 'HDS' in file1.sub.upper():
        team_sel='19'
    elif 'HHWEB' in file1.sub.upper():
        team_sel='21'
    elif 'LEAGUEWEB' in file1.sub.upper():
        team_sel='22'
    elif 'MTEAM' in file1.sub.upper() or 'M-TEAM' in file1.sub.upper():
        team_sel='23'
    elif 'NTB' in file1.sub.upper():
        team_sel='24'
    elif 'OURBITS' in file1.sub.upper():
        team_sel='25'
    elif 'PTCAFE' in file1.sub.upper():
        team_sel='26'
    elif 'QHSTUDIO' in file1.sub.upper():
        team_sel='27'
    elif 'SAKURAWEB' in file1.sub.upper():
        team_sel='28'
    elif 'WIKI' in file1.sub.upper():
        team_sel='29'
    else:
        team_sel='30'    
    logger.info('制作组已成功选择为Other')

    #选择标签
    if 'HDR10' in file1.pathinfo.tags:
        tags.append(12)
        logger.info('已选择HDR10标签')
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append(11)
        logger.info('已选择杜比视界标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(13)
        logger.info('已选择DIY标签')            
    if '国' in file1.language or '中' in file1.language:
        tags.append(7)
        logger.info('已选择国语标签')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(9)
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
            "nfo": "",
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