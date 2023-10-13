import time
from requests.cookies import cookiejar_from_dict
from loguru import logger
import sys
import get_shadowflow


start_time = time.time()
def cookies_raw2jar(raw_cookies):
    cookie_dict = {}
    for cookie in raw_cookies.split(";"):
        key, value = cookie.split("=", 1)
        cookie_dict[key] = value
    return cookiejar_from_dict(cookie_dict)

def get_torrent(yamlinfo):
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
    get_shadowflow(siteurl,sitecookie,sitepasskey)







