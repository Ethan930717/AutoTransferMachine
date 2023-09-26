from loguru import logger
import time
import os
from AutoTransferMachine.utils.uploader.upload_tools import *
import re
import cloudscraper

def hares_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://club.hares.top/takeupload.php"
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
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='415'
    else:
        select_type='415'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='5'
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='1'
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='2'
    elif 'ENCODE' in file1.pathinfo.medium.upper():
        medium_sel='4'
    elif 'tv' in file1.pathinfo.type.lower() and 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='6'
    elif 'HDTV' in file1.pathinfo.medium.upper():
        medium_sel='8'
    elif 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='3'
    else:
        medium_sel='4'
    logger.info('已成功填写来源为'+file1.type)


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '264' in file1.pathinfo.video_format:
        codec_sel='8'
        logger.info('已成功选择编码为H264/AVC')     
    elif 'AVC' in file1.pathinfo.video_format:
        codec_sel='1'
        logger.info('已成功选择编码为H264/AVC')                
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.pathinfo.video_format.lower() and '265' in file1.pathinfo.video_format:
        codec_sel='7'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.pathinfo.video_format.upper():
        codec_sel='6'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-2' in file1.pathinfo.video_format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')  
    elif 'MPEG-4' in file1.pathinfo.video_format.upper():
        codec_sel='9'
        logger.info('已成功选择编码为MPEG-4')          
    elif 'VC' in file1.pathinfo.video_format.upper():
        codec_sel='5'
        logger.info('已成功选择编码为VC1')          
    elif 'AV1' in file1.pathinfo.video_format.upper():
        codec_sel='10'
        logger.info('已成功选择编码为AV1')    
    elif 'XVID' in file1.pathinfo.video_format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为XVID')        
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，选择other')  

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'DTS' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='5'
    elif '2160' in file1.standard_sel:
        standard_sel='6'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '1440' in file1.standard_sel:
        standard_sel='7'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            processing_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            processing_sel='7'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            processing_sel='7'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            processing_sel='9'
            logger.info('国家信息已选择'+file1.country)
        else:
            processing_sel='10'
            logger.info('未找到资源国家信息，已选择其他')
    else:
        processing_sel='10'
        logger.info('未找到资源国家信息，已默认其他')

    #选择制作组
    if 'HARESWEB' in file1.sub.upper():
        team_sel='2'
    elif 'HARESTV' in file1.sub.upper():
        team_sel='3'
    elif 'HARES' in file1.sub.upper():
        team_sel='1'
    elif 'CHD' in file1.sub.upper():
        team_sel='4'
    elif 'HDS' in file1.sub.upper():
        team_sel='5'
    elif 'WIKI' in file1.sub.upper():
        team_sel='6'
    elif 'CMCT' in file1.sub.upper():
        team_sel='8'
    elif 'BEAST' in file1.sub.upper():
        team_sel='9'
    elif 'HDC' in file1.sub.upper():
        team_sel='10'
    elif 'FRDS' in file1.sub.upper():
        team_sel='11'
    elif 'PTER' in file1.sub.upper():
        team_sel='12'
    elif 'BHD' in file1.sub.upper():
        team_sel='13'
    elif 'PTH' in file1.sub.upper():
        team_sel='14'
    else:
        team_sel='15'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'hare' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if 'HARES' in file1.sub.upper():
        tags.append(3)
        logger.info('已选择官方')
    if file1.pathinfo.transfer==0:
        tags.append(4)
        logger.info('已选择原创')
    if '国' in file1.language or '中' in file1.language:
        tags.append(6)
        logger.info('已选择国语')
    if '粤' in file1.language:
        tags.append(7)
        logger.info('已选择粤语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(9)
        logger.info('已选择中字')
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.complete==0:
        tags.append(16)
        logger.info('已选择追更')
    if 'HDR10+' in file1.pathinfo.tags:
        tags.append(14)
        logger.info('已选择HDR10+标签')
    elif 'HDR10' in file1.pathinfo.tags:
        tags.append(13)
        logger.info('已选择HDR10标签')
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append(15)
        logger.info('已选择杜比视界标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append(11)
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
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info.replace(''.join(re.findall('\[img\]https://img9\.douban.*p\d*.jpg\[/img\]',file1.douban_info)),'')+'\n'+file1.pathinfo.contenttail,
            "technical_info" : file1.mediainfo,
            "type": select_type,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "tags[]": tags,
            }
    if len(re.findall(r'\[img\](.*)\[/img\]',file1.douban_info))>0:
        other_data["url_poster"] = re.findall(r'\[img\](.*)\[/img\]',file1.douban_info)[0]
    else:
        return False,fileinfo+'未找到豆瓣简介中的海报图链接,无法填写海报信息'
    shots=file1.screenshoturl.replace('[img]','').replace('[/img]','').strip()
    if shots!='':
        other_data["screenshots"] = shots
    else:
        return False,fileinfo+'检测到用户设置为不截图，但是白兔强制要求资源截图'
    if file1.doubanurl!=None and file1.doubanurl!='':
        other_data["pt_gen[douban][link]"]= file1.doubanurl
    if file1.imdburl!=None and file1.imdburl!='':
        other_data["pt_gen[imdb][link]"] = file1.imdburl
    if file1.bgmurl!=None and file1.bgmurl!='':
        other_data["pt_gen[bangumi][link]"] = file1.bgmurl
    
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