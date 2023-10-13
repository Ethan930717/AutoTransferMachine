import time
from loguru import logger
import sys
import shutil
import yaml
import urllib
import requests
import os
import logging
from qbittorrentapi import Client
from utils.getinfo.shadowflow_download import *

def get_torrent(yamlinfo):
    start_time = time.time()
    choosesite = input(f"请选择你要获取信息的网站\n1.影 \n请输入序号:")
    if choosesite == "1":
        sitename = "shadowflow"
        logger.info('即将从影站获取种子信息')
    else:
        logger.info('未能识别当前选择的站点，退出脚本')
        sys.exit(0)
    siteurl = yamlinfo['site info'][sitename]['url']
    sitecookie = yamlinfo['site info'][sitename]['cookie']
    sitepasskey = yamlinfo['site info'][sitename]['passkey']
    return shadowflow_down(sitename,siteurl,sitecookie,yamlinfo,start_time)

def download_torrent(ws,yamlinfo):
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s",filename=f"{yamlinfo['basic']['record_path']}/torrent_download.log")
    row = ws.max_row
    file_path = f"{yamlinfo['basic']['torrent_path']}/"
    old_count = len([name for name in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, name))])
    logger.info(f'开始下载种子，当前种子文件夹中文件数量为{old_count}个')
    url_list = []
    counter = 1
    try:
        client = Client(host=yamlinfo['qbinfo']['qburl'], username=yamlinfo['qbinfo']['qbwebuiusername'],
                        password=yamlinfo['qbinfo']['qbwebuipassword'])
    except:
        logger.warning(f'Qbittorrent登录失败')
    logger.info('正在登录Qbittorrent')
    try:
        client.auth_log_in()
    except:
        logger.warning(f"Qbittorrent信息错误，登录失败，\n当前设置的Qbittorent地址为{yamlinfo['qbinfo']['qburl']},用户名{yamlinfo['qbinfo']['qbwebuiusername']}，密码{yamlinfo['qbinfo']['qbwebuipassword']}，请检查")
    logger.info('成功登录Qbittorrent')
    for i in range(2, row):
        download = ws["F" + str(i)].value
        url_list.append(download)
        row += 1
    for url in url_list:
        passkey = ws["I" + str(counter + 1)].value
        r = requests.get(url,params={"passkey": passkey})
        if r.status_code == 200:
            content_disposition = r.headers.get("Content-Disposition")
            if content_disposition:
                file_name = r.headers["Content-Disposition"].split(";")[-1].split("=")[-1].strip('"')
                file_name = urllib.parse.unquote(file_name)
                # 拼接完整的文件路径
                file_full_path = file_path + file_name
                with open(file_full_path, "wb") as f:
                    f.write(r.content)
                print(f"{file_name}种子文件已成功保存到本地")
                res = client.torrents_add(urls=url, is_skip_checking=False, is_paused=True)
                if res == "Ok.":
                    print(f"{file_name}添加Qbittorent成功")
                elif "fail" in res.lower():
                    print(f"{file_name}添加Qbittorent失败")
                elif "Torrent is already in the download list" in res:
                    print(f"{file_name}在Qbittorent中已存在")
                counter += 1
            else:
                print("无法获取文件名,相关信息已记录在日志中，请查看record文件夹中的torrent_download.log")
                logging.error(f"无法获取文件名，下载失败：{url}")
        else:
            print(f"下载失败：{url}")
            continue
    new_count = len([name for name in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, name))])
    logger.info(f'下载完成，本次共下载了{counter}个种子，实际下载成功了{new_count - old_count}个种子')







