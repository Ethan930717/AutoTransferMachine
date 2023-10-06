from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def rousi_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
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
        select_type='415'
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
        select_type='406'
    else:
        select_type='405'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    source_sel='24'
    #选择来源
    if 'WEB' in file1.source.upper():
        source_sel='24'
    elif 'UHD' in file1.source.upper():
        source_sel='23'
    elif 'BLU' in file1.source.upper():
        source_sel='22'
    elif 'ENCODE' in file1.source.upper():
        source_sel='24'
    elif 'dvd' in file1.type.lower():
        source_sel='25'
    elif 'ENCODE' in file1.source.upper():
        source_sel='22'
    elif 'HDTV' in file1.source.upper():
        source_sel='26'
    elif 'REMUX' in file1.source.upper():
        source_sel='22'
    else:
        source_sel='28'


    #选择媒介
    if 'web' in file1.type.lower() and 'dl' in file1.type.lower():
        medium_sel='10'
    elif (file1.type=='bluray') and '2160' in file1.standard_sel:
        medium_sel='1'
    elif file1.type=='bluray':
        medium_sel='1'
    elif 'rip' in file1.type.lower() and  'dvd' in file1.type.lower():
        medium_sel='6'
    elif 'rip' in file1.type.lower()  :
        medium_sel='7'
    elif 'HDTV' in file1.type.upper() and '2160' in file1.standard_sel:
        medium_sel='5'
    elif 'HDTV' in file1.type.upper():
        medium_sel='5'
    elif 'remux' in file1.type.lower():
        medium_sel='3'
    elif 'dvd' in file1.type.lower():
        medium_sel='2'
    else:
        medium_sel='10'
    logger.info('已成功填写来源为'+file1.type)



    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='1'
    elif file1.Video_Format=='H265':
        codec_sel='6'
    elif file1.Video_Format=='x265':
        codec_sel='6'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'TRUEHD AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='7'
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
        tags.append(18)
        logger.info('已选择4K')
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        standard_sel='7'
    else:
        standard_sel='8'
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
    

    if 'rousi' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if 'ROUSI' in file1.sub.upper():
        tags.append(3)
        logger.info('已选择官方')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')
    if not file1.sublan=='' and '英' in file1.sublan:
        tags.append(14)
        logger.info('已选择英字')
    if '粤' in file1.language:
        tags.append(15)
        logger.info('已选择粤语')
    if 'ROUSIWEB' in file1.sub.upper():
        tags.append(13)
        logger.info('已选择RousiWeb')
    if 'ROUSIWEB' in file1.sub.upper():
        tags.append(13)
        logger.info('已选择RousiWeb')
    if 'HDR' in file1.pathinfo.tags:
        tags.append(7)
        logger.info('已选择HDR标签')
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append(11)
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
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info+'\n'+file1.screenshoturl+'\n'+file1.pathinfo.contenttail,
            "technical_info": file1.mediainfo,
            "type": select_type,
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