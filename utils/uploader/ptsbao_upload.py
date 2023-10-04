from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper
import requests

def ptsbao_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        select_type='414'
        logger.info('已成功填写类型为MV')                 
    elif 'music' in file1.pathinfo.type.lower():
        select_type='414'
        logger.info('已成功填写类型为音乐')          
    else:
        select_type='409'
        logger.info('已成功填写类型为其它')          
        




    #子类型
    if 'movie' in file1.pathinfo.type.lower() and 'DIY' in file1.pathinfo.tags:
        select_source='93'
        logger.info('已成功填写类型为Movie DIY') 
    elif 'movie' in file1.pathinfo.type.lower() and 'WEB' in file1.pathinfo.medium.upper():
        select_source='4'
        logger.info('已成功填写类型为Movie WEBDL') 
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.pathinfo.medium.upper():
        select_source='55'
        logger.info('已成功填写类型为Movie BLURAY')  
    elif 'movie' in file1.pathinfo.type.lower() and 'DVD' in file1.pathinfo.medium.upper():
        select_source='79'
        logger.info('已成功填写类型为Movie DVD')         
    elif 'movie' in file1.pathinfo.type.lower() and 'HDTV' in file1.pathinfo.medium.upper():
        select_source='94'
        logger.info('已成功填写类型为Movie HDTV')
    elif 'movie' in file1.pathinfo.type.lower() and 'REMUX' in file1.pathinfo.medium.upper():
        select_source='88'
        logger.info('已成功填写类型为Movie REMUX')
    elif 'movie' in file1.pathinfo.type.lower() and '2160p' in file1.standard_sel.lower():
        select_source='92'
        logger.info('已成功填写类型为Movie 2160p')
    elif 'movie' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_source='3'
        logger.info('已成功填写类型为Movie 1080p')
    elif 'movie' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_source='91'
        logger.info('已成功填写类型为Movie 720p')               

    elif 'show' in file1.pathinfo.type.lower():
        select_source='15'
        logger.info('已成功填写类型为综艺综合')   

    elif 'tv' in file1.pathinfo.type.lower() and '大陆' in file1.country:
        select_source='23'
        logger.info('已成功填写类型为中国大陆')
    elif 'tv' in file1.pathinfo.type.lower() and '香港' in file1.country:
        select_source='24'
        logger.info('已成功填写类型为中国香港')  
    elif 'tv' in file1.pathinfo.type.lower() and '台湾' in file1.country:
        select_source='24'
        logger.info('已成功填写类型为中国台湾')
    elif 'tv' in file1.pathinfo.type.lower() and '泰国' in file1.country:
        select_source='70'
        logger.info('已成功填写类型为泰国')
    elif 'tv' in file1.pathinfo.type.lower() and '日本' in file1.country:
        select_source='26'
        logger.info('已成功填写类型为日本')
    elif 'tv' in file1.pathinfo.type.lower() and '韩国' in file1.country:
        select_source='27'
        logger.info('已成功填写类型为韩国')  
    elif 'tv' in file1.pathinfo.type.lower() and '美国' in file1.country:
        select_source='25'
        logger.info('已成功填写类型为美国') 
    elif 'tv' in file1.pathinfo.type.lower() and '英国' in file1.country:
        select_source='90'
        logger.info('已成功填写类型为美国')    
    elif 'tv' in file1.pathinfo.type.lower():
        select_source='70'
        logger.info('已成功填写类型为其他剧集')   


    elif 'anime' in file1.pathinfo.type.lower() and '完结' in file1.pathinfo.tags:
        select_source='66'
        logger.info('已成功填写类型为动漫完结')
    elif 'anime' in file1.pathinfo.type.lower():
        select_source='67'
        logger.info('已成功填写类型为动漫剧场版')

    elif 'doc' in file1.pathinfo.type.lower() and '国家地理' in file1.pathinfo.small_descr:
        select_source='34'
        logger.info('已成功填写类型为纪录片国家地理')
    elif 'doc' in file1.pathinfo.type.lower() and '探索' in file1.pathinfo.small_descr:
        select_source='35'
        logger.info('已成功填写类型为纪录片探索')
    elif 'doc' in file1.pathinfo.type.lower() and '历史' in file1.pathinfo.small_descr:
        select_source='40'
        logger.info('已成功填写类型为纪录片历史')
    elif 'doc' in file1.pathinfo.type.lower() and 'CCTV' in file1.pathinfo.small_descr:
        select_source='37'
        logger.info('已成功填写类型为纪录片CCTV')
    elif 'doc' in file1.pathinfo.type.lower() and 'NHK' in file1.pathinfo.small_descr:
        select_source='77'
        logger.info('已成功填写类型为纪录片NHK')
    elif 'doc' in file1.pathinfo.type.lower() and 'BBC' in file1.pathinfo.small_descr:
        select_source='39'
        logger.info('已成功填写类型为纪录片BBC')
    elif 'doc' in file1.pathinfo.type.lower() and 'Netflix' in file1.pathinfo.small_descr:
        select_source='95'
        logger.info('已成功填写类型为网飞')
    elif 'doc' in file1.pathinfo.type.lower():
        select_source='41'
        logger.info('已成功填写类型为纪录片其他')

        
    elif 'mv' in file1.pathinfo.type.lower():
        select_source='49'
        logger.info('已成功填写类型为MV')                   
    else:
        select_source='68'
        logger.info('已成功填写类型为其它')         

    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='2'
        logger.info('已成功选择媒介为WEB-DL')              
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为UHD-BLURAY')         
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='1'
        logger.info('已成功选择媒介为BLURAY DIY')          
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为HDTV')        
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='3'
        logger.info('已成功选择媒介为DVD')
    elif 'CD' in file1.pathinfo.medium.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD')         
    else:
        medium_sel='9'
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
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')            
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')  
    elif 'VP' in file1.pathinfo.video_format.upper():
        codec_sel='7'
        logger.info('已成功选择编码为VP9')
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')                  
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，不选择')  

#选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'MP2' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'OPUS' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel.upper() or '4320' in file1.standard_sel:
        standard_sel='6'
    if '2K' in file1.standard_sel.upper():
        standard_sel='7'
    elif '2160' in file1.standard_sel or '4K' in file1.standard_sel.upper():
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='1'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='6'
    logger.info('已成功选择分辨率为'+file1.standard_sel)


    #选择处理
    if 'ENCODE' in file1.pathinfo.medium.upper():
        processing_sel='2'
    elif 'REMUX' in file1.pathinfo.medium.upper():
        processing_sel='1'
    elif 'BLU' in file1.pathinfo.medium.upper():
        processing_sel='5'
    else:
        processing_sel='3'
    

    #选择制作组
    if 'FFANSBD' in file1.sub.upper():
        team_sel='8'
    elif 'OPS' in file1.sub.upper():
        team_sel='11'
    elif 'FFANSWEB' in file1.sub.upper():
        team_sel='12'
    elif 'FFANSTV' in file1.sub.upper():
        team_sel='13'
    elif 'HQC' in file1.sub.upper():
        team_sel='10'
    elif 'TTG' in file1.sub.upper():
        team_sel='3'
    elif 'HDC' in file1.sub.upper():
        team_sel='6'
    elif 'HDS' in file1.sub.upper():
        team_sel='9'
    elif 'CMCT' in file1.sub.upper():
        team_sel='4'
    elif 'FRDS' in file1.sub.upper():
        team_sel='5'
    elif 'FFANSDVD' in file1.sub.upper():
        team_sel='14'
    elif 'FHDMV' in file1.sub.upper():
        team_sel='15'
    elif '19977' in file1.sub.upper():
        team_sel='17'
    elif 'QHSTUIDIO' in file1.sub.upper():
        team_sel='18'
    elif 'FFANSAIENCE' in file1.sub.upper():
        team_sel='19'
    elif 'SGXT' in file1.sub.upper():
        team_sel='20'
    else:
        team_sel='7'    
    logger.info('制作组已成功选择为Other')
    
    k4  = 'no'
    zz  = 'no'
    hdr = 'no'
    yp  = 'no'
    diy = 'no'
    uplver   = 'no'    
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        zz = 'yes'
    if 'HDR10' in file1.pathinfo.tags:
        hdr = 'yes'
    if '2160' in file1.standard_sel or '4K' in file1.standard_sel.upper():
        k4 = 'yes'
    if 'BLU' in file1.pathinfo.medium.upper():
        yp = 'yes'
    if 'DIY' in file1.pathinfo.tags:
        diy = 'yes'
    if siteinfo.uplver==1:
        uplver='yes'


    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "upload": "8381589",
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "imdburl": file1.imdburl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "source_sel": select_source,
            "team_sel": team_sel,
            "medium_sel": medium_sel,
            "standard_sel": standard_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "cite_torrent": "",
            "chinese_name": "",
            "english_name": "",
            "releasedate": "",
            "release_time": "",             
            "processing_sel": processing_sel,
            "uplver": uplver,
            }
    buttomlist=["uplver","k4","zz","hdr","yp","diy"]
    for item in buttomlist:
        if eval(item+"=='yes'"):
            exec('other_data["'+item+'"]="yes"')            


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