import re
import os
import lxml
import cloudscraper
from bs4 import BeautifulSoup
from requests.cookies import cookiejar_from_dict
import time
from loguru import logger
import sys
import shutil
import yaml
import csv
import requests
from utils.getinfo.torrent_download import download_torrent
from utils.getinfo.makeyaml import mkyaml
import urllib


def cookies_raw2jar(raw_cookies):
    cookie_dict = {}
    for cookie in raw_cookies.split(";"):
        key, value = cookie.split("=", 1)
        cookie_dict[key] = value
    return cookiejar_from_dict(cookie_dict)

def shadowflow_download(sitename, siteurl, sitecookie, sitepasskey, yamlinfo):
    row = 0
    scraper = cloudscraper.create_scraper()
    csv_filename = f"{sitename}_torrents.csv"
    file = open(csv_filename, mode='w', newline='', encoding='utf-8-sig')
    writer = csv.writer(file)
    writer.writerow(["标题", "体积", "做种人数", "发布时间", "详情链接", "下载链接", "站点", "cookie", "passkey"])
    try:
        pagenum = int(input('请输入本次需要爬取几页种子: '))
        if pagenum > 0:  # 如果输入是正整数
            print(f"您选择了爬取{pagenum}页种子")
    except ValueError:
        print('输入错误，请输入一个整数。')
    while True:

        outtag = input(
            f"请选择需要排除的资源关键字，可多选，无格式要求（默认排除禁转、限转资源，注意区分大小写) \n例：排除有国语粤语标签的动漫和综艺资源，则输入CD12 \n做种人数(seed)，体积(size)筛选请使用前后比较符，如0<seed<5则为排除做种人数小于5人的种子，10<size<100则表示排除体积在10GB-100GB之间的种子，可与关键字一同筛选）\n A.电影 B.剧集 C.综艺 D.动漫 E.纪录片 F.MV\n gy.国语 yy.粤语 zz.中字 diy.DIY wj.完结 fj.分集 db.杜比视界 hdr.HDR\n请输入排除项:")
        tags = []
        tags.append("禁转")
        tags.append("限转")
        if "A" in outtag:
            tags.append("电影")
        if "B" in outtag:
            tags.append("剧集")
        if "C" in outtag:
            tags.append("综艺")
        if "D" in outtag:
            tags.append("动漫")
        if "E" in outtag:
            tags.append("纪录片")
        if "F" in outtag:
            tags.append("MV")
        if "gy" in outtag:
            tags.append("国语")
        if "yy" in outtag:
            tags.append("粤语")
        if "zz" in outtag:
            tags.append("中字")
        if "diy" in outtag:
            tags.append("DIY")
        if "wj" in outtag:
            tags.append("完结")
        if "fj" in outtag:
            tags.append("分集")
        if "db" in outtag:
            tags.append("杜比视界")
        if "hdr" in outtag:
            tags.append("HDR")
        tags_str = " ".join(tags)
        # 解析输入，查找是否包含seed筛选条件
        seed_filter = None
        seedprint = ""
        if 'seed' in outtag:
            match = re.search(r'(\d+)\s*<\s*seed\s*<\s*(\d+)', outtag)
            if match:
                seed_min = int(match.group(1))
                seed_max = int(match.group(2))
                seed_filter = lambda x: seed_min <= int(x) < seed_max
                seedprint = f"做种人数在{seed_min}到{seed_max}之间,"

        # 解析输入，查找是否包含size筛选条件
        size_filter = None
        sizeprint = ""
        if 'size' in outtag:
            match = re.search(r'(\d+)\s*<\s*size\s*<\s*(\d+)', outtag)
            if match:
                size_min = int(match.group(1))
                size_max = int(match.group(2))
                size_filter = lambda x: size_min <= int(x) < size_max
                sizeprint = f"体积在{size_min}GB到{size_max}GB之间"
        download_ensure = input(f"选择完毕，本次将为您排除{tags_str},{seedprint}{sizeprint}的资源\n确认：Y \n重选： N \n")
        if download_ensure.lower() == "y":
            break
        elif download_ensure.lower() == "n":
            continue
        else:
            print("输入有误，请输入Y或者N")
    start_time = time.time()
    for page in range(pagenum):
        torrent_url = f"{siteurl}torrents.php?page={page}"
        r = scraper.get(torrent_url, cookies=cookies_raw2jar(sitecookie), timeout=30)
        soup = BeautifulSoup(r.content, "html.parser")
        if r.status_code == 200:
            # 查找id为torrents的表格元素
            table = soup.find("table", class_="torrents")
            if table:
                trs = table.find_all("tr")[1:]
                for tr in trs:
                    if any(x in tr.text for x in tags):
                        print(f"不符合筛选条件，跳过")
                        continue
                    else:
                        td_list = tr.find_all("td")
                        if len(td_list) >= 4:
                            seeders = td_list[-4].text
                        else:
                            continue
                        size = tr.find_all("td")[-5].text
                        size_pattern = re.search(r'(\d+\.\d+|\d+)', size)
                        size = float(size_pattern.group(1)) / 1024 if 'MB' in size else float(size_pattern.group(1))
                        # 将MB单位的体积转换为GB单位
                        if (seed_filter is None or seed_filter(seeders)) and (size_filter is None or size_filter(size)):
                            try:
                                embedded = tr.find("td", class_="embedded")
                                a = embedded.find("a", href=lambda x: "details" in x)
                                b = a["href"]
                                title = a["title"]
                                details = f"{siteurl}{b}"
                                pattern = "id=(\d+)&hit"
                                torrent_id = re.search(pattern, details)
                                if torrent_id:
                                    pass
                                else:
                                    print("未识别到种子ID")
                                download = details.replace("details", "download")
                                download = download.replace("hit=1", f"passkey={sitepasskey}")
                                seeders = tr.find_all("td")[-4].text
                                size = tr.find_all("td")[-5].text
                                uploadtime = tr.find_all("td")[-6].text
                                writer.writerow([title, size, seeders, uploadtime, details, download, sitename, sitecookie,sitepasskey])
                                logger.info(f'{title}获取成功')
                                row += 1
                            except IndexError:
                                continue
                        else:
                            print(f"不符合筛选条件，跳过")
            else:
                print("没东西了，停")
                break
        else:
            print("没东西了，停")
            continue

    file.close()
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"爬取结束，本次共读取到{row}个种子,耗时{execution_time}，请选择接下来的任务\n 1.批量打印种子链接 2.批量打印下载链接 3.跳过")
    # 移动文件到指定目录
    if os.path.exists(csv_filename):
        os.makedirs(yamlinfo['basic']['record_path'], exist_ok=True)
        shutil.move(csv_filename, os.path.join(yamlinfo['basic']['record_path'], csv_filename))
    else:
        print(f"文件 {csv_filename} 不存在!")

    # 打开CSV文件并读取数据
    csv_filepath = os.path.join(yamlinfo['basic']['record_path'], csv_filename)
    details_list = []
    download_list = []

    with open(csv_filepath, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            details_list.append(row[4])  # 假设详情在第5列，根据实际情况进行调整
            download_list.append(row[5])  # 假设下载URL在第6列，根据实际情况进行调整

    # 提示用户选择并打印相应的信息
    choice = input("请输入您的选择：")
    while True:
        if choice == "1":
            print("以下是所有的种子链接：")
            for detail in details_list:
                print(detail)
            break
        elif choice == "2":
            print("以下是所有的下载链接：")
            for download in download_list:
                print(download)
            break
        elif choice == "3":
            print("好的")
            break
        else:
            print("选择错误，请重新选择")
            choice = input("请输入您的选择：")
    #获取path序列
    while True:
        forsure = input(f"本次数据已保存在{yamlinfo['basic']['record_path']}/{sitename}_torrents.csv\n是否需要将Yaml模板中的torrent_file路径替换成本次生成的数据文件路径\nY.是，替换路径\nN.否，不需要替换\n默认不替换")
        if forsure.upper() == 'Y':
            au = f"{yamlinfo['basic']['workpath']}au.yaml"
            logger.info(f"检测到模板路径为{au}")
            with open(au, "r") as f:
                yamlinfo = yaml.load(f, Loader=yaml.FullLoader)
                yamlinfo["basic"]["torrent_list"] = f"{yamlinfo['basic']['record_path']}/{sitename}_torrents.csv"
                with open(au, "w") as f:
                    yaml.dump(yamlinfo, f)
            logger.info(f"修改完成，当前yaml模板的torrent_list为{yamlinfo['basic']['torrent_list']}")
            while True:
                dlsure = input(
                    f'是否需要将本次抓取到的资源种子下载到本地（下载路径为torrent_path，请确认配置文件中已正确配置该项\nY.是，下载\nN，否，不下载')
                if dlsure.upper() == "Y":
                    logger.info("开始下载")
                    return download_torrent(yamlinfo)
                elif dlsure.upper() == "N":
                    logger.info("未选择下载种子，即将结束本次任务")
                    sys.exit()
                else:
                    logger.info("选择错误，请重新选择")
                    continue
        elif forsure.upper() == 'N':
            logger.info('已选择不替换路径')
            while True:
                dlsure = input(f'是否需要将本次抓取到的资源种子下载到本地（选是则同步将种子上传到QB，默认添加后为暂停状态）\nY.是，下载\nN，否，不下载')
                if dlsure.upper() == "Y":
                    logger.info("开始下载")
                    return download_torrent(yamlinfo)
                elif dlsure.upper() == "N":
                    logger.info("未选择下载种子，即将结束本次任务")
                    sys.exit()
                else:
                    logger.info("选择错误，请重新选择")
                    continue
        else:
            logger.info("选择错误，请重新选择")
            continue


def shadowflow_trans(yamlinfo,csv_filepath):
    au = f"{yamlinfo['basic']['workpath']}au.yaml"
    with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        all_data = [row for row in reader]
        url_list = [row['详情链接'] for row in all_data]
        first_data = all_data[1]
        sitename = first_data['站点']
        cookie = first_data['cookie']
    writemode = input(f"请选择模板转换方式\nY.在原有的pathinfo下自动续写\nN.覆盖原有的pathinfo，从path1开始生成（默认自动续写）")
    if writemode.lower() == "n":
        logger.info('当前为覆盖模式')
        with open(au, "r", encoding="utf-8") as f:
            lines = f.readlines()
        above_path_info = True
        new_lines = []
        for line in lines:
            if "path info" in line:
                above_path_info = False  # 发现 "path info" 行，将标志设为 False
            if above_path_info:
                new_lines.append(line)
        with open(au, "w", encoding="utf-8") as f:
            for new_line in new_lines:
                f.write(new_line)
    else:
        logger.info('当前为续写模式')
    print(csv_filepath)
    tmdb_api = yamlinfo['basic']['tmdb_api']
    scraper = cloudscraper.create_scraper()
    counter = 1
    for url in url_list:
        result = urllib.parse.urlparse(url)
        siteurl = urllib.parse.urlunparse((result.scheme, result.netloc, '', '', '', ''))
        print(f"当前域名 {siteurl},匹配站点{sitename}")
        r = scraper.post(url, cookies=cookies_raw2jar(cookie), timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")
        tree = lxml.etree.HTML(r.text)
        print(f"当前检索链接 {url}")

    #主标题
        xpath_name = "//*[@id='top']/text()"
        try:
            name = tree.xpath(xpath_name)[0]
            name = name.rstrip()
            getteam = name.split("-")
            # 取列表的最后一个元素，即最后一个"-"后面的内容
            team = getteam[-1]
        except IndexError:
            name = input(f"无法读取主标题名，请手动输入,种子地址{url}\n请在此输入正确的主标题名：")
        print(f"成功记录主标题名 {name}")

    # 种子名称
        filename=""
        try:
            links = soup.find_all("a", class_="index")
            for link in links:
                href = link.get("href")
                if "download" in href:
                    torrent = link.text
                    filename=torrent.replace(".torrent","")
                    filename=filename.replace("[Shadow].","")
        except IndexError:
            filename= input(f"无法读取种子名称，请手动输入,种子地址{url}\n请在此输入正确的种子名称：")
        print(f"成功读取文件名称 {filename}")

        #副标题
        try:
            elements = soup.find_all("td", class_="rowfollow", valign="top", align="left")[0]
            texts_sdescr = [element.get_text() for element in elements]
            for small_descr in texts_sdescr:
               print(f"成功读取副标题名 {small_descr}")
        except IndexError:
            small_descr = input(f"无法读取副标题名，请手动输入,种子地址{url}\n请在此输入正确的副标题名：")


        #产地&年份
        kdescr = soup.find(id="kdescr")
        lines = kdescr.text.split("\n")
        country = ''
        try:
            for line in lines:
                if "◎产　　地　" in line:
                    country = line.split("◎产　　地　")[1]
            print(f"读取产地成功 {country}")
        except IndexError:
            country= input(f"无法确认产地，请手动输入,文件标题{name}\n请在此输入正确的产地（国家）：")


        madeyear=''
        try:
            match = re.search("◎年　　份　(\d+)", kdescr.text)
            if match:
                madeyear = match.group(1)
            else:
                year_match = re.search(r"\b(19\d{2}|20\d{2})\b", name)
                if year_match:
                    madeyear = year_match.group(0)
                    print(f"从文件名中提取年份成功 {madeyear}")
                else:
                    madeyear = input(f"无法确认年份，请手动输入,文件标题{name}\n请在此输入正确年份：")
        except IndexError:
            madeyear = input(f"无法确认年份，请手动输入,文件标题{name}\n请在此输入正确年份：")

        #标签
        try:
            elements = soup.find_all("td", class_="rowfollow", valign="top", align="left")[1]
            texts_tags = [element.get_text() for element in elements]
            tags = " ".join(texts_tags)
            print(f"读取标签成功 {tags}")
            if "mv" in tags.lower() or "体育" in tags or "音轨" in tags or "sport" in tags.lower() :
                print("当前尚未适配转载该类型资源，即将跳过本资源")
                continue
        except IndexError:
            tags = input(f"无法确认标签，请手动输入,资源链接{url}\n请在此输入正确的标签：")

        #确认完结
        if "complete" in name.lower() and "完结" in tags:
            complete = 1
        elif "complete" in name.lower() and not "完结" in tags:
            choice = input(f'标题包含Complete，但资源未勾选完结标签，请手动确认该资源是否完结\n输入1代表完结，输入0代表未完结: ')
            if choice == '1':
                complete = 1
            elif choice == '0':
                complete = 0
            else:
                print("无效的输入，请重新输入")
        elif not "complete" in name.lower() and "完结" in tags:
            choice = input(f'资源已勾选完结标签，但标题不包含Complete，请手动确认该资源是否完结\n输入1代表完结，输入0代表未完结: ')
            if choice == '1':
                complete = 1
                name = input(f"请在主标题中手动加入Complete,添加位置在季数之后，如 S01 Complete\n当前主标题{name}")
            elif choice == '0':
                complete = 0
            else:
                print("无效的输入，请重新输入")
        else:
            complete = 0

        #基本信息
        try:
            elements = soup.find_all("td", class_="rowfollow", valign="top", align="left")[2]
            texts_info = [element.get_text() for element in elements]
            info = " ".join(texts_info)
            print("获取基本信息成功")
            infolist = info.split()
            size = " ".join(infolist[1:3])
            type = infolist[4]
            medium = infolist[6]
            codec = infolist[8]
            audio = infolist[10]
            standard = infolist[12]
            print(f"资源体积 {size}")
            print(f"类型 {type}")
            if "电影" in type:
                type = "movie"
            elif "剧集" in type:
                type = "tvseries"
            elif "综艺" in type:
                type = "tvshow"
            elif "纪录" in type:
                type = "doc"
            elif "动画" in type:
                type = "anime"
            elif "音轨" in type:
                type = "music"
                print("检测到类型为音轨，当前尚未适配转载该类型资源，即将跳过本资源")
                continue
            elif "MV" in type:
                type = "mv"
                print("检测到类型为MV，当前尚未适配转载该类型资源，即将跳过本资源")
                continue
            elif "体育" in type:
                type = "sport"
                print("检测到类型为体育，当前尚未适配转载该类型资源，即将跳过本资源")
                continue
            else:
                type = "other"
                print("未检测到当前资源类型，即将跳过本资源")
                continue

            print(f"媒介 {medium}")
            print(f"编码 {codec}")
            print(f"音频编码 {audio}")
            print(f"清晰度 {standard}")
            print(f"制作组 {team}")
        except IndexError:
            print("无法获取基本信息")

    # 豆瓣
        douban = None
        try:
            dblinks = soup.find_all("a", href=lambda x: x and "douban" in x)
            douban = [(link.get("href"), link.get_text()) for link in dblinks]
            for douban in dblinks:
                douban = douban.get("href")
                print(f"成功获取豆瓣链接 {douban}")
        except IndexError:
            print("无法获取豆瓣链接")

        #IMDB
        imdb = ""
        tmdb_id = ""
        try:
            imdblinks = soup.find_all("a", href=lambda x: x and "imdb" in x)
            if imdblinks:
                imdb = [(link.get("href"), link.get_text()) for link in imdblinks]
                for imdb in imdblinks:
                    imdb = imdb.get("href")
                    print(f"成功获取IMDB链接 {imdb}")
                    imdb_split=imdb.split('/')
                    imdb_id=imdb_split[4]
                    print(f"正在通过IMDBID '{imdb_id}' 获取TMDBID")
                    tmdb_url = "https://api.themoviedb.org/3/find/"+imdb_id+"?api_key="+tmdb_api+"&external_source=imdb_id&include_adult=true&language=zh-CN"
                    print(tmdb_url)
                    try:
                        tmdb_res = requests.get(tmdb_url)
                        if tmdb_res.status_code == 200:
                            data = tmdb_res.json()
                            if data["movie_results"]:
                                tmdb_id = data["movie_results"][0]["id"]
                                tmdb_title = data["movie_results"][0]["title"]
                                print(f"TMDBID获取成功 {tmdb_id} ")
                                print(f"中文标题 {tmdb_title} ")
                            elif data["tv_results"]:
                                tmdb_id = data["tv_results"][0]["id"]
                                tmdb_title = data["tv_results"][0]["name"]
                                print(f"TMDBID获取成功 {tmdb_id} ")
                                print(f"中文标题 {tmdb_title} ")
                            elif data["tv_episode_results"]:
                                tmdb_id = data["tv_episode_results"][0]["id"]
                                tmdb_title = data["tv_episode_results"][0]["name"]
                                print(f"TMDBID获取成功 {tmdb_id} ")
                                print(f"中文标题 {tmdb_title} ")
                            else:
                                print("未成功获取TMDBID，尝试使用影片名称搜索")
                                if type == "movie":
                                    print("")
                                else:
                                    print("")
                        else:
                            print(f"TMDB请求失败 {tmdb_res.status_code}.")
                    except IndexError:
                        tmdb_id = ""
                        tmdb_title = ""
                        print("无法连接到tmdb")
                else:
                    imdb = ""
                    print("该资源暂无imdb链接")
        except Exception as e:
            print("无法获取IMDB链接")
        counter += 1
        logger.info(f"第{counter}个资源读取完成")
        mkyaml(yamlinfo,counter,filename,name,small_descr,tags,team,type,audio,codec,medium,douban,imdb,country,madeyear,standard,tmdb_id,torrent)
