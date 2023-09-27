import re
import datetime
from loguru import logger

def mkyaml(counter,filename,name,small_descr,tags,team,type,audio,codec,medium,douban,imdb,country,date,standard,tmdb_id,torrent,yamlinfo):
    #亚洲国家
    east_asia = ["中国大陆", "蒙古", "朝鲜", "韩国", "日本", "香港", "台湾", "澳门","中国" ] #仅作判定使用，无任何地缘政治因素
    southeast_asia = ["菲律宾", "越南", "老挝", "柬埔寨", "缅甸", "泰国", "马来西亚", "文莱", "新加坡", "印度尼西亚", "东帝汶"]
    south_asia = ["尼泊尔", "不丹", "孟加拉国", "印度", "巴基斯坦", "斯里兰卡","马尔代夫"]
    central_asia = ["哈萨克斯坦","吉尔吉斯斯坦","塔吉克斯坦","乌兹别克斯坦","土库曼斯坦"]
    west_asia = ["阿富汗", "伊拉克", "伊朗", "叙利亚", "约旦", "黎巴嫩", "以色列", "巴勒斯坦", "沙特阿拉伯", "巴林", "卡塔尔", "科威特", "阿拉伯联合酋长国", "阿联酋", "阿曼", "也门", "格鲁吉亚", "亚美尼亚", "阿塞拜疆", "土耳其", "塞浦路斯"]
    asia = set(east_asia + southeast_asia + south_asia + central_asia + west_asia)
    #欧美国家
    eu = ["澳大利亚", "芬兰", "瑞典", "挪威", "冰岛", "丹麦", "爱沙尼亚", "拉脱维亚", "立陶宛", "白俄罗斯", "俄罗斯", "乌克兰", "摩尔多瓦", "波兰", "捷克", "斯洛伐克", "匈牙利", "德国", "奥地利", "英国", "爱尔兰", "荷兰", "比利时", "卢森堡", "法国", "摩纳哥", "西班牙", "葡萄牙", "意大利", "梵蒂冈", "圣马力诺", "马耳他", "希腊", "阿尔巴尼亚", "保加利亚", "罗马尼亚", "加拿大", "美国", "墨西哥", "危地马拉", "伯利兹", "萨尔瓦多", "洪都拉斯", "尼加拉瓜", "哥斯达黎加", "巴拿马", "哥伦比亚", "委内瑞拉", "圭亚那", "苏里南", "厄瓜多尔", "秘鲁", "玻利维亚", "巴西", "智利", "阿根廷","乌拉圭","巴拉圭","古巴","海地","多米尼加共和国","牙买加","巴哈马","安提瓜和巴布达","圣基茨和尼维斯","多米尼克","圣卢西亚","圣文森特和格林纳丁斯","格林纳达","巴巴多斯"]
    #站点特判
    #碟粉非亚洲资源与动漫.年份大于五年
    current_year = datetime.date.today().year # 获取当前年份
    keep_year = abs(current_year - int(date))
    if country in asia and not "anime" in type and keep_year > 4:
        discfan = '0'
        print(f"当前资源产地为{country},类型为{type},上映时间{keep_year}年\n符合碟粉发种要求")
    else:
        discfan = 'null'
        print(f"当前资源产地为{country},类型为{type},上映时间{keep_year}年\n不符合碟粉发种要求")
    #ilolicon动漫
    if not type == 'anime':
        ilolicon = 'null'
    else:
        ilolicon = '0'
    #白兔4K
    if not '2160' in standard or not '4k' in standard:
        hares = 'null'
    else:
        hares = '0'
    #freefarm大陆资源
    if not '大陆' in country:
        freefarm = '0'
    else:
        freefarm = 'null'
    #tccf纪录片
    if type == 'doc':
        tccf = "0"
    else:
        tccf = 'null'
    #猫H264/X264
    if "H264" in codec.upper():
        pter= "null"
    else:
        pter = '0'
    site=""
    site += f"    audience: null\n"
    site += f"    btschool: null\n"
    site += f"    carpt: 0\n"
    site += f"    cyanbug: 0\n"
    site += f"    dajiao: 0\n"
    site += f"    discfan: {discfan}\n"
    site += f"    dragonhd: 0\n"
    site += f"    freefarm: {freefarm}\n"
    site += f"    gtk: 0\n"
    site += f"    haidan: 0\n"
    site += f"    hares: {hares}\n"
    site += f"    hdarea: 0\n"
    site += f"    hddolby: 0\n"
    site += f"    hdfans: 0\n"
    site += f"    hdhome: 0\n"
    site += f"    hdmayi: 0\n"
    site += f"    hdpost: null\n"
    site += f"    hdpt: 0\n"
    site += f"    hdsky: null\n"
    site += f"    hdtime: 0\n"
    site += f"    hdu: 0\n"
    site += f"    hdvideo: 0\n"
    site += f"    hdzone: 0\n"
    site += f"    hhclub: null\n"
    site += f"    hitpt: 0\n"
    site += f"    hudbt: null\n"
    site += f"    icc: 0\n"
    site += f"    itzmx: null\n"
    site += f"    joyhd: 0\n"
    site += f"    kufei: 0\n"
    site += f"    mangguo: null\n"
    site += f"    mteam: null\n"
    site += f"    nanyang: 0\n"
    site += f"    okpt: 0\n"
    site += f"    oshen: 0\n"
    site += f"    piggo: 0\n"
    site += f"    ptcafe: 0\n"
    site += f"    ptchina: 0\n"
    site += f"    pter: {pter}\n"
    site += f"    pthome: 0\n"
    site += f"    ptlsp: 0\n"
    site += f"    ptsbao: null\n"
    site += f"    pttime: 0\n"
    site += f"    redleaves: 0\n"
    site += f"    rousi: 0\n"
    site += f"    soulvoice: 0\n"
    site += f"    ssd: null\n"
    site += f"    tccf: {tccf}\n"
    site += f"    ubits: 0\n"
    site += f"    wintersakura: 0\n"
    site += f"    ydy: 0\n"
    site += f"    yiptba: 0\n"
    site += f"    wuerpt: 0\n"
    site += f"    zhuque: 0\n"
    site += f"    zmpt: 0\n"

    # 确定中文名
    cnname = ""
    cnname = filename.split(".")  # 以空格为分隔符分割字符串
    cnname = cnname[0]  # 取第一个元素作为中文名
    cnname = cnname[0:len(cnname)]  # 取整个字符串作为中文名（这一步其实可以省略）
    cnname = cnname.replace(":", " ")
    cnname = cnname.replace("：", " ")
    cnname = cnname.replace("’", " ")
    cnname = cnname.replace("”", " ")
    print(cnname)

    # 确定英文名
    enname=""
    if "2019" in name:
        en1 = name.split("2019")[0]
        enname = en1.replace(".", " ")
    elif "2020" in name:
        en1 = name.split("2020")[0]
        enname = en1.replace(".", " ")
    elif "19" in name:
        en1 = name.split("19")[0]
        enname = en1.replace(".", " ")
    elif "20" in name:
        en1 = name.split("20")[0]
        enname = en1.replace(".", " ")
    enname = enname.replace("'", " ")
    enname = enname.replace(":", " ")
    print(enname)

    #获取path序列
    au = f"{yamlinfo['basic']['workpath']}text.yaml"
    f = open(au, 'r',encoding='utf-8') # 以只读模式打开文件
    lines = f.readlines() # 读取所有行并存储在列表中
    f.close() # 关闭文件

    pattern = r'path\d+' # 定义正则表达式模式

    index = -1 # 初始化索引为-1，表示没有找到
    for i in range(len(lines)): # 遍历列表中的每个元素的索引
        if re.search(pattern, lines[i]): # 如果当前行包含"path(n)"
            index = i # 更新索引为当前值
    if index != -1: # 如果索引不等于-1，表示找到了
        line = lines[index] # 获取最后一个带有"path"的行的值
        match = re.search(r'\d+', line) # 使用正则表达式查找其中的数字
        if match: # 如果找到了数字
            pathnum = int(match.group()) + 1 # 提取数字并转换为整数
            print(f"已找到最大的path序列为{int(match.group())},正在将当前path序列设置为{pathnum}")
        else: # 如果没有找到数字
            pathnum = "1" # 将pathnum设为1
            print("未找到path序列，已将pathnum设为1")
    else: # 如果索引等于-1，表示没有找到
        pathnum = "1" # 将pathnum设为1
        print("未找到path序列，已将pathnum设为1")


    # 确认来源
    if "UHD" in name.upper() and "BLU" in name.upper() and "DIY" in name.upper():
        source = "UHD BLURAY DIY"
    elif "UHD" in name.upper() and "BLU" in name.upper():
        source = "UHD BLURAY"
    elif "BLURAY" in name.upper():
        source = "BLURAY"
    elif "UHD" in name.upper() and "TV" in name.upper() and "DIY" in name.upper():
        source = "UHD TV DIY"
    elif "UHD" in name.upper() and "TV" in name.upper():
        source = "UHD TV"
    elif "UHD" in name.upper():
        source = "UHD"
    elif "HDTV" in name.upper():
        source = "HDTV"
    elif "WEB" in name.upper():
        source = "WEBDL"
    elif "DVD" in name.upper():
        source = "DVD"
    elif "CD" in name.upper():
        source = "CD"
    elif "ENCODE" in name.upper():
        source = "ENCODE"
    else:
        source = "OTHER"

    #确认编码
    if "x265" in name and "10bit" in name:
        codec="x265 10bit"
    elif "x265" in name:
        codec="x265"
    elif "H265" in name and "10bit" in name and "HDR" in name:
        codec="H265 10bit HDR"
    elif "H265" in name and "10bit" in name:
        codec="H265 10bit"
    elif "H265" in name:
        codec="H265"
    elif "H264" in name:
        codec="H264"
    elif "AVC" in name:
        codec = "AVC"
    elif "x264" in name:
        codec = "x264"
    elif "HEVC" in name:
        codec = "HEVC"
    else:
        codec = input(f"无法确认视频格式，请手动输入,文件标题{name}")

    #确认音频
    if "DTS-HD" in name.upper() and "MA" in name.upper() and "1.0" in name.upper():
        audio = "DTS-HD MA 1.0"
    elif "DTS-HD" in name.upper() and "MA" in name.upper() and "2.0" in name.upper():
        audio = "DTS-HD MA 2.0"
    elif "DTS-HD" in name.upper() and "MA" in name.upper() and "5.1" in name.upper():
        audio = "DTS-HD MA 5.1"
    elif "DTS-HD" in name.upper() and "MA" in name.upper() and "7.1" in name.upper():
        audio = "DTS-HD MA 7.1"
    elif "TRUE" in name.upper() and "AutoTransferMachineOS" in name.upper() and "7.1" in name.upper():
        audio = "TrueHD AutoTransferMachineos 7.1"
    elif "TRUE" in name.upper() and "AutoTransferMachineOS" in name.upper():
        audio = "TrueHD AutoTransferMachineos"
    elif "TRUE" in name.upper() and "5.1" in name.upper():
        audio = "TrueHD 5.1"
    elif "TRUE" in name.upper():
        audio = "TrueHD"
    elif "AAC" in name.upper():
        audio = "AAC"
    elif "AC3" in name.upper():
        audio = "AC3"
    elif "AC3" in name.upper():
        audio = "AC3"
    elif "DDP" in name.upper() and "AutoTransferMachineOS" in name.upper() and "5.1" in name.upper():
        audio = "DDP5.1 AutoTransferMachineos"
    elif "DDP" in name.upper() and "5.1" in name.upper():
        audio = "DDP5.1"
    elif "DDP" in name.upper() and "2.0" in name.upper():
        audio = "DDP2.0"
    elif "DDP" in name.upper():
        audio = "DDP"
    elif "DD" in name.upper() and "2.0" in name.upper():
        audio = "DD2.0"
    elif "DD" in name.upper():
        audio = "DD"
    elif "FLAC" in name.upper():
        audio = "FLAC"
    else:
        audio = input(f"无法确认音频格式，请手动输入,文件标题{name}")

    text = ""
    text += f"  path{pathnum}:\n"
    text += f"    downloadpath: /download\n"
    text += f"    enable: 1\n"
    text += f"    collection: 1\n"
    text += f"    path: /home/media/{filename}\n"
    text += f"    uploadname: \"{name}\"\n"
    text += f"    filename: \"{torrent}\"\n"
    text += f"    chinesename: \"{cnname}\"\n"
    text += f"    englishname: \"{enname}\"\n"
    text += f"    small_descr: \"{small_descr}\"\n"
    text += f"    tags: {tags}\n"
    text += f"    sub: {team}\n"
    text += f"    type: {type}\n"
    text += f'    contenthead: \'[quote][b][color=#d98a91][size=3][font=Arial Black]转自[/size][size=5]YingWEB[/size][size=3]，感谢原作者发布[/color][/size][/font][/b][/quote]\'\n'
    text += f"    audio_format: {audio}\n"
    text += f"    video_format: {codec}\n"
    text += f"    medium: {medium}\n"
    text += f"    source: {source}\n"
    text += f"    doubanurl: {douban}\n"
    text += f"    screenshot: null\n"
    text += f"    from_url: null\n"
    text += f"    imdb_url: {imdb}\n"
    text += f"    tmdb_id: {tmdb_id}\n"
    text += f"{site}"
    logger.info(text)
    with open("au", "a+", encoding="utf-8") as f:
        f.write(text)