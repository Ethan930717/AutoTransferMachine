from loguru import logger
import time
import os
from atm.utils.uploader.upload_tools import *
import re
import cloudscraper
from bs4 import BeautifulSoup
def get_token(cookie):
    headers = {
            'authority': 'zhuque.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': cookie,
            'origin': 'https://zhuque.in',
            'referer': 'https://zhuque.in/torrent/upload',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    }
    scraper=cloudscraper.create_scraper()
    r = scraper.get('https://zhuque.in/index',headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    res=soup.find_all('meta',{'name':'x-csrf-token'})
    if len(res)<=0:
        return ''
    if not 'content' in res[0].attrs:
        return ''
    return res[0].attrs['content']
def zhuque_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://zhuque.in/api/torrent/upload"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower() and "完结" in file1.pathinfo.tags:
        select_type='503'
        tmdbtype= "1"
    elif 'anime' in file1.pathinfo.type.lower():
        select_type='503'
        tmdbtype= "0"  
    elif 'doc' in file1.pathinfo.type.lower() and "完结" in file1.pathinfo.tags:
        select_type='503'
        tmdbtype= "1"    
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='503'
        tmdbtype= "0"          
    elif 'show' in file1.pathinfo.type.lower():
        select_type='504'
        tmdbtype= "1"          
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='502'
        tmdbtype= "1"        
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='501'  
        tmdbtype= "0"        
    else:
        select_type='599'
        tmdbtype= "0"         
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #填写TMDB评分
    tmdbid = file1.pathinfo.tmdb_id
    logger.info('TMDBID为'+file1.pathinfo.tmdb_id)


    #选择媒介
    if 'WEB' in file1.pathinfo.medium.upper():
        medium_sel='309'
    elif 'UHD' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='302'
    elif 'UHD' in file1.pathinfo.medium.upper():
        medium_sel='301'
    elif 'BLU' in file1.pathinfo.medium.upper() and 'DIY' in file1.pathinfo.medium.upper():
        medium_sel='303'
    elif 'BLU' in file1.pathinfo.medium.upper():
        medium_sel='304'
    elif 'REMUX' in file1.pathinfo.medium.upper():
        medium_sel='305'
    elif 'HDTV' in file1.pathinfo.medium.upper() and '2160' in file1.standard_sel:
        medium_sel='307'
    elif 'HDTV' in file1.type.upper():
        medium_sel='308'
    elif 'ENCODE' in file1.type.upper():
        medium_sel='306'
    else:
        medium_sel='399'
    logger.info('已成功选择媒介为'+file1.type)


    #选择编码
    if 'H' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='101'
    elif 'X' in file1.pathinfo.video_format.upper() and '264' in file1.pathinfo.video_format:
        codec_sel='103'
    elif 'X' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='104'
    elif 'H' in file1.pathinfo.video_format.upper() and '265' in file1.pathinfo.video_format:
        codec_sel='102'
    else:
        codec_sel='105'
    logger.info('已成功选择编码为'+file1.Video_Format)


    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='499'
    elif '2160' in file1.standard_sel:
        standard_sel='404'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='403'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='402'
    elif '720' in file1.standard_sel:
        standard_sel='401'
    elif '480' in file1.standard_sel:
        standard_sel='499'
    else:
        standard_sel='499'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

 
    

    if 'ZHUQUE' in file1.sub.upper():
        tags.append(601)
        logger.info('已选择官方')
    if 'zhuque' in file1.pathinfo.exclusive :
        tags.append(602)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(603)
        logger.info('已选择国语') 
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(604)
        logger.info('已选择中字')
    if '杜比' in file1.pathinfo.tags or 'DV' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags :
        tags.append(611)
        logger.info('已选择Dovi') 
    if 'HDR' in file1.pathinfo.tags:
        tags.append(613)
        logger.info('已选择HDR')           

    
    tags=list(set(tags))
    tags.sort()
    tags=[str(titem) for titem in tags]
    if siteinfo.uplver==1:
        uplver='true'
    else:
        uplver='false'
        
        

    torrent_file = file1.torrentpath
    file_tup = ("torrent", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
    token=get_token(siteinfo.cookie)
    if token=='' and siteinfo.token=='':
        return False,fileinfo+' 发布种子发生错误,错误信息:朱雀缺少站点token信息，请联系站点/莫与解决'
    elif token=='':
        token=siteinfo.token
    headers = {
            'authority': 'zhuque.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': siteinfo.cookie,
            'origin': 'https://zhuque.in',
            'referer': 'https://zhuque.in/torrent/upload',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
            'x-csrf-token': token,
    }
    other_data = {
            "title": file1.uploadname,
            "subtitle": file1.small_descr+file1.pathinfo.exinfo,
            "screenshot": file1.screenshoturl.replace('[img]','').replace('[/img]',''),
            "mediainfo": file1.mediainfo,
            "category": select_type,
            "medium": medium_sel,
            "videoCoding": codec_sel,
            "resolution": standard_sel,
            "anonymous": uplver,
            "tags": ','.join(tags),
            "tmdbtype": tmdbtype,
            "tmdbid": tmdbid,
            "note": '转自'+file1.pathinfo.sub+',感谢原作者发布',
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
            r = scraper.post(post_url, headers=headers,data=other_data, files=file_tup,timeout=time_out)
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0
        
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)