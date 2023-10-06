from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper

def hdhome_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower() and 'UHD' in file1.type.upper():
        select_type='501'
        logger.info('已成功填写类型为anime Blu-Ray')
    elif 'anime' in file1.pathinfo.type.lower() and 'BLU' in file1.type.upper():
        select_type='454'
        logger.info('已成功填写类型为anime Blu-Ray')
    elif 'anime' in file1.pathinfo.type.lower() and 'REMUX' in file1.type.upper():
        select_type='448'
        logger.info('已成功填写类型为anime REMUX')
    elif 'anime' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='447'
        logger.info('已成功填写类型为anime 1080p')
    elif 'anime' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_type='446'
        logger.info('已成功填写类型为anime 720p')  
    elif 'anime' in file1.pathinfo.type.lower() and '2160' in file1.standard_sel.lower():
        select_type='449'
        logger.info('已成功填写类型为anime 2160p')        
    elif 'tv' in file1.pathinfo.type.lower() and 'UHD' in file1.type.upper():
        select_type='502'
        logger.info('已成功填写类型为tv Blu-Ray')
    elif 'tv' in file1.pathinfo.type.lower() and 'BLU' in file1.type.upper():
        select_type='453'
        logger.info('已成功填写类型为tv Blu-Ray')
    elif 'tv' in file1.pathinfo.type.lower() and 'REMUX' in file1.type.upper():
        select_type='437'
        logger.info('已成功填写类型为tv REMUX')
    elif 'tv' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='436'
        logger.info('已成功填写类型为tv 1080p')
    elif 'tv' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='435'
        logger.info('已成功填写类型为tv 1080i')
    elif 'tv' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_type='434'
        logger.info('已成功填写类型为tv 720p')  
    elif 'tv' in file1.pathinfo.type.lower() and '2160' in file1.standard_sel.lower():
        select_type='438'
        logger.info('已成功填写类型为tv 2160p')  
    elif 'show' in file1.pathinfo.type.lower() and 'BLU' in file1.type.upper():
        select_type='452'
        logger.info('已成功填写类型为show Blu-Ray')
    elif 'show' in file1.pathinfo.type.lower() and 'REMUX' in file1.type.upper():
        select_type='430'
        logger.info('已成功填写类型为show REMUX')
    elif 'show' in file1.pathinfo.type.lower() and '1080i' in file1.standard_sel.lower():
        select_type='428'
        logger.info('已成功填写类型为show 1080i')
    elif 'show' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='429'
        logger.info('已成功填写类型为show 1080p')
    elif 'show' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_type='427'
        logger.info('已成功填写类型为show 720p')  
    elif 'show' in file1.pathinfo.type.lower() and '2160' in file1.standard_sel.lower():
        select_type='431'
        logger.info('已成功填写类型为show 2160p')                   
    elif 'movie' in file1.pathinfo.type.lower() and 'UHD' in file1.type.upper():
        select_type='499'
        logger.info('已成功填写类型为Movie UHD-4K')
    elif 'movie' in file1.pathinfo.type.lower() and 'BLU' in file1.type.upper():
        select_type='450'
        logger.info('已成功填写类型为Movie Blu-Ray')
    elif 'movie' in file1.pathinfo.type.lower() and 'REMUX' in file1.type.upper():
        select_type='415'
        logger.info('已成功填写类型为Movie REMUX')
    elif 'movie' in file1.pathinfo.type.lower() and '2160p' in file1.standard_sel.lower():
        select_type='416'
        logger.info('已成功填写类型为Movie 2160p')
    elif 'movie' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='414'
        logger.info('已成功填写类型为Movie 1080p')
    elif 'movie' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_type='413'
        logger.info('已成功填写类型为Movie 720p')                     
    elif 'doc' in file1.pathinfo.type.lower() and 'UHD' in file1.type.upper():
        select_type='500'
        logger.info('已成功填写类型为doc Blu-Ray')
    elif 'doc' in file1.pathinfo.type.lower() and 'BLU' in file1.type.upper():
        select_type='451'
        logger.info('已成功填写类型为doc Blu-Ray')
    elif 'doc' in file1.pathinfo.type.lower() and 'REMUX' in file1.type.upper():
        select_type='421'
        logger.info('已成功填写类型为doc REMUX')
    elif 'doc' in file1.pathinfo.type.lower() and '1080p' in file1.standard_sel.lower():
        select_type='420'
        logger.info('已成功填写类型为doc 1080p')
    elif 'doc' in file1.pathinfo.type.lower() and '720' in file1.standard_sel.lower():
        select_type='419'
        logger.info('已成功填写类型为doc 720p')  
    elif 'doc' in file1.pathinfo.type.lower() and '2160' in file1.standard_sel.lower():
        select_type='422'
        logger.info('已成功填写类型为doc 2160p')         
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='441'
        logger.info('已成功填写类型为MV')           
    elif 'sport' in file1.pathinfo.type.lower() and '1080' in file1.standard_sel:
        select_type='443'
        logger.info('已成功填写类型为体育1080')
    elif 'sport' in file1.pathinfo.type.lower() and '720' in file1.standard_sel:
        select_type='443'
        logger.info('已成功填写类型为体育1080')    
    elif 'sport' in file1.pathinfo.type.lower() and '2160' in file1.standard_sel:
        select_type='504'
        logger.info('已成功填写类型为体育2160')           
    elif 'music' in file1.pathinfo.type.lower():
        select_type='442'
        logger.info('已成功填写类型为体育720')          
    else:
        select_type='450'
        logger.info('已成功填写类型为其它')          
        


    #选择来源
    if 'WEB' in file1.source.upper():
        source_sel='7'
        logger.info('已成功选择来源为WEB-DL')  
    elif 'UHD' in file1.source.upper():
        source_sel='9'
        logger.info('已成功选择来源为UHD-BLURAY')        
    elif 'BLU' in file1.source.upper():
        source_sel='1'
        logger.info('已成功选择来源为BLURAY')               
    elif 'HDTV' in file1.source.upper():
        source_sel='4'
        logger.info('已成功选择来源为HDTV')        
    elif 'DVD' in file1.source.upper():
        source_sel='3'
        logger.info('已成功选择来源为DVD')     
    else:
        source_sel='8'
        logger.info('未识别到来源信息，选择other')


    #选择媒介
    if 'WEB' in file1.type.upper():
        medium_sel='11'
        logger.info('已成功选择媒介为WEB-DL')  
    elif 'UHD' in file1.type.upper():
        medium_sel='10'
        logger.info('已成功选择媒介为UHD-BLURAY')        
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
    elif 'DVDR' in file1.type.upper():
        medium_sel='6'
        logger.info('已成功选择媒介为DVDR') 
    elif 'BD' in file1.type.upper():
        medium_sel='4'
        logger.info('已成功选择媒介为MiniBD')
    elif 'CD' in file1.type.upper():
        medium_sel='8'
        logger.info('已成功选择媒介为CD')       
    else:
        medium_sel='0'
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
        codec_sel='2'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'x' in file1.Videio_Format.lower() and '265' in file1.Videio_Format:
        codec_sel='2'
        logger.info('已成功选择编码为H265/HEVC')    
    elif 'HEVC' in file1.Videio_Format.upper():
        codec_sel='2'
        logger.info('已成功选择编码为H265/HEVC')                
    elif 'MPEG-2' in file1.Videio_Format.upper():
        codec_sel='4'
        logger.info('已成功选择编码为MPEG-2')         
    elif 'VC' in file1.Videio_Format.upper():
        codec_sel='3'
        logger.info('已成功选择编码为VC1')            
    else:
        codec_sel='5'
        logger.info('未识别到视频编码信息，选other')  


    #选择音频编码
    if file1.Audio_Format=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HD' in file1.Audio_Format.upper() and '7.1' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'MA' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'DTS-HD' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel='18'
    elif 'AutoTransferMachineOS' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'EAC3' in file1.Audio_Format.upper() or 'EAC-3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    else:
        audiocodec_sel='0'
    logger.info('已成功选择音频编码')

    #选择分辨率
    if '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel='1'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='2'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='3'
    elif '720' in file1.standard_sel:
        standard_sel='4'
    elif 'SD' in file1.standard_sel:
        standard_sel='5'
    elif '4320' in file1.standard_sel or '8K' in file1.standard_sel:
        standard_sel='10'
    else:
        standard_sel='0'
    logger.info('已成功选择分辨率')
    
    #选择处理
    if 'ENCODE' in file1.type.upper():
        processing_sel='2'
    else:
        processing_sel='1'

    #选择标签
    if 'HDR10+' in file1.pathinfo.tags:
        tags.append('hdrm')
        logger.info('已选择HDR10+标签')
    elif 'HDR10' in file1.pathinfo.tags:
        tags.append('hdr10')
        logger.info('已选择HDR10标签')
    if '杜比' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags:
        tags.append('db')
        logger.info('已选择杜比视界标签')
    if 'DIY' in file1.pathinfo.tags:
        tags.append('diy')
        logger.info('已选择DIY标签')            
    if '国' in file1.language or '中' in file1.language:
        tags.append('gy')
        logger.info('已选择国语标签')
    if '粤' in file1.language:
        tags.append('yy')
        logger.info('已选择粤语标签')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append('zz')
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
            "url": file1.imdburl,
            "pt_gen": file1.doubanurl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "medium_sel": medium_sel,
            "source_sel": source_sel,
            "standard_sel": standard_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "processing_sel": processing_sel,
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