import re
import cloudscraper
from bs4 import BeautifulSoup
import openpyxl
import time
from requests.cookies import cookiejar_from_dict
from loguru import logger
import sys
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
    siteurl = audata['site info'][sitename]['url']
    sitecookie = audata['site info'][sitename]['cookie']
    sitepasskey = audata['site info'][sitename]['passkey']

    scraper = cloudscraper.create_scraper()
    wb = openpyxl.Workbook()
    ws = wb.active
    row = 2
    ws.title = f"{sitename}_torrents"
    for page in range(999):
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
                        if "禁转" in tr.text or "分集" in tr.text : # 这里可以排除不想爬的种子标签
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
                            ws["E" + str(row)] = torrent_id.group(1)
                            ws["F" + str(row)] = download
                            row += 1  # 行号加一

                        except IndexError:
                            print("啥也没找到")
                            continue
                        print(title,size,seeders,uploadtime,details)
                else:
                    print("没东西了，停")
                    break
            else:
                print("没东西了，停")
                continue
    wb.save(f"{sitename}_torrents.xlsx")
    total_rows = row - 1
    total_pages = page + 1
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"爬取结束，本次共读取到{total_rows}个种子,耗时{execution_time}，请选择接下来的任务\n 1.批量打印种子链接 2.批量打印下载链接 3.结束ATM")
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