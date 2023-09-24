from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper

def hdtime_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://hdtime.org/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='405'
        tags.append(18)
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'        
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.pathinfo.medium.upper():
        select_type='424'    
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='409'
    elif 'cartoon' in file1.pathinfo.type.lower():
        select_type='412'
        tags.append(18)
    else:
        select_type='401'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择来源
    if 'movie' in file1.pathinfo.type.lower() and 'REMUX' in file1.pathinfo.medium.upper():
        source_sel='81'
        logger.info('已成功选择来源为电影-REMUX')  
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        source_sel='80'
        logger.info('已成功选择来源为电影-DIY原盘')        
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.pathinfo.medium.upper():
        source_sel='79'
        logger.info('已成功选择来源为电影-BLURAY原盘')        
    elif 'movie' in file1.pathinfo.type.lower() and '10bit' in file1.pathinfo.video_format.lower():
        source_sel='3'
        logger.info('已成功选择来源为电影-10bit')
    elif 'movie' in file1.pathinfo.type.lower() and '1080' in file1.standard_sel:
        source_sel='6'
        logger.info('已成功选择来源为电影-1080')       
    elif 'movie' in file1.pathinfo.type.lower() and '720' in file1.standard_sel:
        source_sel='5'
        logger.info('已成功选择来源为电影-720')          
    elif 'anime' in file1.pathinfo.type.lower() and '10bit' in file1.pathinfo.video_format.lower():
        source_sel='83'
        logger.info('已成功选择来源为动漫-10bit')
    elif 'anime' in file1.pathinfo.type.lower() and "完结" in file1.pathinfo.tags:
        source_sel='66'
        logger.info('已成功选择来源为动漫完结')    
    elif 'anime' in file1.pathinfo.type.lower():
        source_sel='67'
        logger.info('已成功选择来源为动漫剧场版')                       
    elif 'tv' in file1.pathinfo.type.lower() and '大陆' in file1.country:
        source_sel='23'
        logger.info('已成功选择来源为大陆剧集')
    elif 'tv' in file1.pathinfo.type.lower() and ('香港' in file1.country or '台湾' in file1.country):
        source_sel='24'
        logger.info('已成功选择来源为港台剧集')           
    elif 'tv' in file1.pathinfo.type.lower() and '美国' in file1.country:
        source_sel='25'
        logger.info('已成功选择来源为美剧') 
    elif 'tv' in file1.pathinfo.type.lower() and '日本' in file1.country:
        source_sel='26'
        logger.info('已成功选择来源为日剧')  
    elif 'tv' in file1.pathinfo.type.lower() and '韩国' in file1.country:
        source_sel='27'
        logger.info('已成功选择来源为韩剧') 
    elif 'tv' in file1.pathinfo.type.lower():
        source_sel='70'
        logger.info('已成功选择来源为其他剧集')    
    elif 'show' in file1.pathinfo.type.lower():
        source_sel='15'
        logger.info('已成功选择来源为综艺综合')        
    else:
        source_sel='49'
        logger.info('已成功选择来源为其它') 



    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='0'
        logger.info('已成功选择媒介为WEB-DL')  
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='1'
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
        logger.info('已成功选择媒介为DVDR') 
    elif 'DVD' in file1.pathinfo.medium.upper():
        medium_sel='5'
        logger.info('已成功选择媒介为DVD') 
    elif 'BD' in file1.pathinfo.medium.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为MiniBD') 
    elif 'CD' in file1.pathinfo.medium.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD')       
    else:
        medium_sel='7'
        logger.info('未识别到媒介信息，选择other')
   


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format and '10bit' in file1.pathinfo.video_format.lower():
        codec_sel='12'
        logger.info('已成功选择编码为x264-10bit')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='10'
        logger.info('已成功选择编码为x264')        
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='12'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='12'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='12'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')         
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为VC1')          
    elif 'AV1' in file1.pathinfo.video_format.upper():
        codec_sel='5'
        logger.info('已成功选择编码为AV1')    
    elif 'VP9' in file1.pathinfo.video_format.upper():
        codec_sel='5'
        logger.info('已成功选择编码为VP9')  
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')       
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，选择other')  



    #选择制作组
    if 'CHD' in file1.sub.upper():
        team_sel='2'
    elif 'beAst' in file1.sub.upper():
        team_sel='3'
    elif 'WIKI' in file1.sub.upper():
        team_sel='4'
    elif 'HDTime' in file1.sub.upper():
        team_sel='6'
    elif 'PADTime' in file1.sub.upper():
        team_sel='7'
    elif 'CMCT' in file1.sub.upper():
        team_sel='8'
    elif 'CHDBITS' in file1.sub.upper():
        team_sel='2'
    elif 'CMCT' in file1.sub.upper():
        team_sel='4'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)
    

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
            "url" : file1.imdburl,
            "pt_gen": file1.doubanurl,            
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info.replace(''.join(re.findall('\[img\]https://img9\.douban.*p\d*.jpg\[/img\]',file1.douban_info)),'')+'\n'+file1.pathinfo.contenttail,
            "technical_info" : file1.mediainfo,
            "type": select_type,
            "medium_sel[4]": medium_sel,
            "codec_sel[4]": codec_sel,
            "source_sel[4]": source_sel,
            "team_sel[4]": team_sel,
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