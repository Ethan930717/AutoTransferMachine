import re
import cloudscraper
from bs4 import BeautifulSoup
import openpyxl
import time
from requests.cookies import cookiejar_from_dict
from loguru import logger
import sys
import fileinput
import json

start_time = time.time()
def cookies_raw2jar(raw_cookies):
    cookie_dict = {}
    for cookie in raw_cookies.split(";"):
        key, value = cookie.split("=", 1)
        cookie_dict[key] = value
    return cookiejar_from_dict(cookie_dict)

def get_torrent(yamlinfo):
    choosesite = input(f"请选择你要下载种子的网站\n1.影")
    if choosesite == "1":
        sitename = "shadowflow"
        logger.info('即将从影站下载种子')
    else:
        logger.info('未能识别当前选择的站点，退出脚本')
        sys.exit(0)
    siteurl = yamlinfo['site info'][sitename]['url']
    sitecookie = yamlinfo['site info'][sitename]['cookie']
    sitepasskey = yamlinfo['site info'][sitename]['passkey']

    scraper = cloudscraper.create_scraper()
    wb = openpyxl.Workbook()
    ws = wb.active
    row = 2
    ws.title = f"{sitename}_torrents"
    pagenum = input('请输入本次需要爬取几页种子（默认只爬取前十页）')
    try:
        pagenum = int(pagenum)
        if pagenum > 0:  # 如果输入是正整数
            print(f"您选择了爬取{pagenum}页种子")
        else:
            print("您输入的数字不合理，请重新输入！")
    except ValueError:
        pagenum = 10
        print(f"您没有输入数字，将默认爬取{pagenum}页种子")
    outtag = input(
        f"请选择需要排除的资源关键字，可多选，无格式要求（默认排除禁转、限转资源）\n例：排除有国语粤语标签的动漫和综艺资源，则输入CD12\n A.电影 B.剧集 C.综艺 D.动漫 E.纪录片 F.MV\n 1.国语 2.粤语 3.中字 4.DIY 5.完结 6.分集 7.杜比视界 8.HDR")
    tags = []
    tags.append("禁转")
    tags.append("限转")
    if "a" in outtag.lower():
        tags.append("电影")
    if "b" in outtag.lower():
        tags.append("剧集")
    if "c" in outtag.lower():
        tags.append("综艺")
    if "d" in outtag.lower():
        tags.append("动漫")
    if "e" in outtag.lower():
        tags.append("纪录片")
    if "f" in outtag.lower():
        tags.append("MV")
    if "1" in outtag:
        tags.append("国语")
    if "2" in outtag:
        tags.append("粤语")
    if "3" in outtag:
        tags.append("中字")
    if "4" in outtag:
        tags.append("DIY")
    if "5" in outtag:
        tags.append("完结")
    if "6" in outtag:
        tags.append("分集")
    if "7" in outtag:
        tags.append("杜比视界")
    if "8" in outtag:
        tags.append("HDR")
    tags_str = " ".join(tags)
    logger.info(f"选择完毕，本次将为您排除{tags_str}的资源，爬种即将开始")
    for page in range(pagenum):
        torrent_url= f"{siteurl}torrents.php?page={page}"
        r = scraper.get(torrent_url, cookies=cookies_raw2jar(sitecookie),timeout=30)
        soup = BeautifulSoup(r.content, "html.parser")
        if r.status_code == 200:
            # 查找id为torrents的表格元素
            table = soup.find("table", class_="torrents")
            if table:
                trs = table.find_all("tr")[1:]
                ws["A1"] = "标题"
                ws["B1"] = "体积"
                ws["C1"] = "做种人数"
                ws["D1"] = "发布时间"
                ws["E1"] = "种子ID"
                ws["F1"] = "下载链接"
                for tr in trs:
                    if any(x in tr.text for x in tags):
                        print(f"不符合筛选条件，跳过")
                        continue
                    try:
                        embedded = tr.find("td", class_="embedded")
                        a = embedded.find("a", href=lambda x: "details" in x)
                        b = a["href"]
                        title = a["title"]
                        details = f"{siteurl}{b}"
                        pattern = "id=(\d+)&hit"
                        torrent_id= re.search(pattern, details)
                        if torrent_id:
                            print(torrent_id.group(1))
                        else:
                            print("未识别到种子ID")
                        download = details.replace("details", "download")
                        download = download.replace("hit=1", f"passkey={sitepasskey}")
                        seeders = tr.find_all("td")[-4].text
                        size = tr.find_all("td")[-5].text
                        uploadtime = tr.find_all("td")[-6].text
                        ws["A" + str(row)] = title
                        ws["B" + str(row)] = size
                        ws["C" + str(row)] = seeders
                        ws["D" + str(row)] = uploadtime
                        ws["E" + str(row)] = details
                         #ws["E" + str(row)] = torrent_id.group(1)
                        ws["F" + str(row)] = download
                        row += 1  # 行号加一
                        print(title,size,seeders,uploadtime,details)
                    except IndexError:
                        print("啥也没找到")
                        continue
            else:
                print("没东西了，停")
                break
        else:
            print("没东西了，停")
            continue
    wb.save(f"{sitename}_torrents.csv")
    total_rows = row - 1
    total_pages = page + 1
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"爬取结束，本次共读取到{total_rows}个种子,耗时{execution_time}，请选择接下来的任务\n 1.批量打印种子链接 2.批量打印下载链接 3.结束ATM")
    running = True
    while running:
        choice = input("请输入您的选择：")
        if choice == "1":
            print("以下是所有的种子链接：")
            for i in range(2, row):
                details = ws["E" + str(i)].value
                print(details)
        elif choice == "2":
            print("以下是所有的下载链接：")
            for i in range(2, row):
                download = ws["F" + str(i)].value
                print(download)
        elif choice == "3":
            print("感谢您使用ATM，再见！")
            sys.exit(0)  # 结束脚本
        else:
            print("您输入的选项不正确，请重新输入！")
        continue  # 跳过当前循环，回到输入框重新输入
    #获取path序列
    forsure = input(f"是否需要将Yaml模板中的torrent_file路径替换成本次生成的CSV文件路径\nY.是，替换路径\nN.否，不需要替换\n默认不替换")
    if forsure == "Y":
        au = f"{yamlinfo['basic']['workpath']}au.yaml"
        with fileinput.input(au, inplace=True) as f:
            pattern = r"\s*:\s*torrent_list\s*"
            replace = f"  torrent_list: {yamlinfo['basic']['screenshot_path']}/{sitename}_torrents.csv"
            for line in f:
                print(re.sub(pattern, replace, line), end='')
    else:
        logger.info("未选择替换路径，即将结束本次任务")
        sys.exit()