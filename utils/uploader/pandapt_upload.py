from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper

def pandapt_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://pandapt.net/takeupload.php"
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
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='408'
    else:
        select_type='401'
    logger.info('已成功填写类型为'+file1.pathinfo.type)



    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为WEB-DL')        
    elif 'UHD' in file1.pathinfo.medium.upper() and 'TV' in file1.pathinfo.type.upper():
        medium_sel='12'
        logger.info('已成功选择媒介为UHD-BLURAY REMUX')           
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='11'
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
        logger.info('已成功选择媒介为DVD') 
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='2'
        logger.info('已成功选择媒介为HDDVD')            
    elif 'CD' in file1.pathinfo.medium.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD')
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
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='6'
        logger.info('已成功选择编码为MPEG-2')   
    elif 'MPEG-4' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-4')        
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')          
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')
    elif 'VP' in file1.pathinfo.video_format.upper():
        codec_sel='7'
        logger.info('已成功选择编码为VP9')             
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，不选择')  


#选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='7'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='18'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'MP2' in file1.Audio_Format.upper():
        audiocodec_sel='17'        
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'OPUS' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    else:
        audiocodec_sel='16'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel :
        standard_sel='6'
    elif '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif 'SD' in file1.standard_sel:
        standard_sel='7'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率')
    


    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            source_sel='7'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            source_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            source_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '新加坡' in file1.country:
            source_sel='8'
            logger.info('国家信息已选择'+file1.country)
        elif '马来西亚' in file1.country:
            source_sel='8'
            logger.info('国家信息已选择'+file1.country)
        elif '泰国' in file1.country:
            source_sel='8'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            source_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            source_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            source_sel='9'
            logger.info('国家信息已选择'+file1.country)
        else:
            source_sel='1'
            logger.info('未找到资源国家信息，已选择其他')
    else:
        source_sel='6'
        logger.info('未找到资源国家信息，选择其他')

    #选择制作组

    if 'BEITAI' in file1.sub.upper():
        team_sel='11'
    elif 'DGB' in file1.sub.upper():
        team_sel='12'
    elif 'GBWEB' in file1.sub.upper():
        team_sel='13'
    elif 'CATEDU' in file1.sub.upper():
        team_sel='15'
    elif 'LEAGUEWEB' in file1.sub.upper():
        team_sel='16'
    elif 'LEAGUENF' in file1.sub.upper():
        team_sel='17'
    elif 'LHD' in file1.sub.upper():
        team_sel='18'      
    else:
        team_sel='5'    
    logger.info('制作组已成功选择为Other')            
    
    if 'pandapt' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language or '国' in file1.pathinfo.tags:
        tags.append(5)
        logger.info('已选择国语')
    if '粤' in file1.language or '粤' in file1.pathinfo.tags:
        tags.append(13)
        logger.info('已选择粤语')
    if '简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan or '中' in file1.pathinfo.tags:
        tags.append(6)
        logger.info('已选择中字')
    if file1.pathinfo.complete==1:
        tags.append(10)
        logger.info('已选择完结')
    if 'HDR10+' in file1.pathinfo.tags:
        tags.append(9)
        logger.info('已选择HDR10+标签')
    elif 'HDR10' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR10标签')        
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append(8)
        logger.info('已选择杜比视界标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
        logger.info('已选择DIY标签')          

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
            "nfo": "0",            
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info+'\n'+file1.screenshoturl+'\n'+file1.pathinfo.contenttail,
            "technical_info": file1.mediainfo,
            "type": select_type,
            "medium_sel[4]": medium_sel,
            "standard_sel[4]": standard_sel,
            "codec_sel[4]": codec_sel,
            "audiocodec_sel[4]": audiocodec_sel,
            "source_sel[4]": source_sel,
            "team_sel[4]": team_sel,            
            "uplver": uplver,
            "tags[4][]": tags,
            }

    scraper=cloudscraper.create_scraper()
    headers = {
        'authority': 'pandapt.net',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #'content-length': '6820',
        'cookie': siteinfo.cookie,
        'origin': 'https://pandapt.net',
        'referer': 'https://pandapt.net/upload.php',
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