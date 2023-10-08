from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def wintersakura_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower() and '完结' in file1.pathinfo.tags:
        select_type='423'
    elif 'anime' in file1.pathinfo.type.lower():
        select_type='422'             
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'        
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection>=1:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='414'
        else:
            select_type='414'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='414'
        else:
            select_type='414'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='410'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    else:
        select_type='409'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择媒介
    if 'WEBRIP' in file1.type.upper():
        medium_sel='25'
        logger.info('已成功选择媒介为WEB-DL')
    elif 'WEB' in file1.type.upper():
        medium_sel='21'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')                
    elif 'UHD' in file1.type.upper() and 'DIY' in file1.type.upper():
        medium_sel='11'
        logger.info('已成功选择媒介为UHD-BLURAY DIY')
    elif 'UHD' in file1.type.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为UHD-BLURAY')
        tags.append(22)
        logger.info('已选择原盘')                 
    elif 'BLU' in file1.type.upper() and 'DIY' in file1.type.upper():
        medium_sel='13'
        logger.info('已成功选择媒介为BLURAY-DIY')
    elif 'BLU' in file1.type.upper() and():
        medium_sel='12'
        logger.info('已成功选择媒介为BLURAY') 
        tags.append(22)
        logger.info('已选择原盘')                           
    elif 'ENCODE' in file1.type.upper():
        medium_sel='15'
        logger.info('已成功选择媒介为ENCODE')        
    elif 'HDTV' in file1.type.upper():
        medium_sel='16'
        logger.info('已成功选择媒介为HDTV')        
    elif 'REMUX' in file1.type.upper():
        medium_sel='14'
        logger.info('已成功选择媒介为REMUX')
    elif 'DVDR' in file1.type.upper():
        medium_sel='17'
        logger.info('已成功选择媒介为DVD')      
    else:
        medium_sel='0'
        logger.info('未识别到媒介信息，不选择媒介')



    #选择编码
    if 'H' in file1.Video_Format.upper() and '264' in file1.Video_Format:
        codec_sel='6'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.Video_Format.lower() and '264' in file1.Video_Format:
        codec_sel='8'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.Video_Format:
        codec_sel='6'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.Video_Format.upper() and '265' in file1.Video_Format:
        codec_sel='9'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.Video_Format.lower() and '265' in file1.Video_Format:
        codec_sel='7'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.Video_Format.upper():
        codec_sel='9'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-2' in file1.Video_Format.upper():
        codec_sel='11'
        logger.info('已成功选择编码为MPEG-2')          
    elif 'VC' in file1.Video_Format.upper():
        codec_sel='10'
        logger.info('已成功选择编码为VC1')          
    elif 'AV' in file1.Video_Format.upper():
        codec_sel='16'
        logger.info('已成功选择编码为AV1')       
    else:
        codec_sel='13'
        logger.info('未识别到视频编码信息，已选择Others')  

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='19'
    elif 'DTS' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper():
        audiocodec_sel='9'        
    elif 'DTS' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'DTS' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='22'
    elif 'DDP' in file1.Audio_Format.upper() and 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='26'                             
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='11'        
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='25'        
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='20'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='23'
    elif 'DSD' in file1.Audio_Format.upper():
        audiocodec_sel='24'
    elif 'AAC' in file1.Audio_Format.upper():
        audiocodec_sel='19'        
    else:
        audiocodec_sel='0'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='6'
    elif '2160' in file1.standard_sel:
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)

         #选择制作组
    if 'PTER' in file1.sub.upper():
        team_sel='8'
    elif 'TJUPT' in file1.sub.upper():
        team_sel='17'        
    elif 'CMCT' in file1.sub.upper():
        team_sel='6'         
    elif 'TTG' in file1.sub.upper():
        team_sel='15'       
    elif 'FRDS' in file1.sub.upper():
        team_sel='7'
    elif 'MTEAM' in file1.sub.upper():
        team_sel='13'
    elif 'HDC' in file1.sub.upper():
        team_sel='14'   
    elif 'HDS' in file1.sub.upper():
        team_sel='1'   
    elif 'CHD' in file1.sub.upper():
        team_sel='2'   
    elif 'BHD' in file1.sub.upper():
        team_sel='9'                                                                  
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)      
    
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY') 
    if '杜比' in file1.pathinfo.tags or 'DV' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags :
        tags.append(11)
        logger.info('已选择Dovi') 
    if 'HDR10+' in file1.pathinfo.tags:
        tags.append(10)
        logger.info('已选择HDR10+')       
    elif 'HDR' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR10+')
    elif '特效' in file1.pathinfo.tags:
        tags.append(9)
        logger.info('已选择HDR10+')              
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')
    if '粤' in file1.language:
        tags.append(12)
        logger.info('已选择粤语')    

    
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
            "standard_sel[4]": standard_sel,
            "codec_sel[4]": codec_sel,
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