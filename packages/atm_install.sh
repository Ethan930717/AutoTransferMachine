#!/usr/bin/env bash
#安装python
echo "请指定一个存放目录以存放配置文件,如/home/program"
valid=false
while [ $valid = false ]
do
read dir
if [ -d $dir ]
then
valid=true
cd $dir
pwd
else
echo "输入地址有误，请重新输入！"
fi
done
cd $dir
mkdir atm
echo "创建atm文件夹成功"
cd atm
mkdir torrent_path record_path screenshot_path
echo "创建功能文件夹成功"
cat > au.yaml << EOF
basic:
  picture_num: 6   #默认自动截图的张数，不设置就是3
  workpath: /home/atm/     #au.yaml所在文件夹的地址
  doubancookie: #豆瓣的cookie
  new_folder: 0   #不用动
  check: 0   #不用动basic:
  picture_num: 6   #默认自动截图的张数，不设置就是3
  workpath: /home/atm/     #au.yaml所在文件夹的地址
  doubancookie: #豆瓣的cookie
  new_folder: 0   #不用动
  check: 0   #不用动
  record_path: /home/atm/record_path   
  screenshot_path: /home/atm/screenshot_path   #这三个是上面那个地址里面的三个子文件夹，跟au.yaml同级
  torrent_path: /home/atm/torrent_path
  torrent_list: /home/atm/record_path/shadowflow_torrents.xlsx  
  #这个是存放种子目录的xlsx表格，使用拉种模式后会自动生成表格，可以选择让脚本自动写入这个地址
  serverchan_api: SCT149255TZvd5PvM******* #server酱api，发种结束后可以push推送通知
  tmdb_api: #tmdbapi

qbinfo:
  qburl: 192.168.5.1:8080  #QB地址
  qbwebuiusername: admin   #用户名
  qbwebuipassword: admin    #密码
  start: 1  #选1则进种自动开始，选0进种暂停，默认跳校验
image hosting:
  seq:#这边可以调整图床优先级顺序
    1: smms
    2: pter
    3: freeimage
    4: dahuimg
  pter:
    cookie: KEEP_LOGIN_GOAUTH=vrksE%3Aecd5c7992a32ff3***********  #cookie直接F12从控制台复制抓取即可
    url: https://s3.pterclub.com
  dahuimg: #大胡图床还没做好，占个坑
    cookie: 
    url: https://img.dahu.fun/
  smms:
    apikey: 
  freeimage:
    cookie: 
    url: https://freeimage.host/
#下面几个已经取消适配了，但是自动调整yaml时还是会添加，后续会删除
  picgo:
    url: https://www.picgo.net/api/1/upload
  emp:
    url: https://jerking.empornium.ph
  chd:
    url: https://shewang.net/

site info:  #这里添加站点信息
  shadowflow:  #转出不转进的站点也需要添加进去，要抓cookie跟passkey
    passkey: 4e1fb7c4e*******
    url: https://shadowflow.org/
    enable: 0  #0就是不启用，转种的时候会自动跳过， 1就是启用
    uplver: 0  #0是不匿名发种，1是匿名
    cookie: *******
  ilolicon:
    url: https://share.ilolicon.com/
    enable: 1
    uplver: 0
    passkey: 
    cookie: 
  hdpost:  #hdpost适配不上，写出来，希望有大佬帮忙
    url: https://pt.hdpost.top/
    enable: 1
    uplver: 0
    cookie:
  piggo:
    url: https://piggo.me/
    enable: 1
    uplver: 0
    cookie: 

#以下是转种的资源信息，了解为主，测试阶段可以手动添加，后续脚本适配会自动生成
path info:
  path1:
    downloadpath: /download #这里是QB内部的下载地址
    enable: 1 #这里选择本种是否启动，选0则会跳过这个种
    collection: 1 #这里默认1即可，是打包发布的意思
    path: /home/media/黑鹰坠落.Black.Hawk.Down.2001.1080p.AMZN.WEB-DL.H264.DDP5.1-YingWEB #写的是资源在机器上的文件夹地址
    uploadname: Black Hawk Down 2001 1080p AMZN WEB-DL H264 DDP5.1-YingWEB #这条是主标题，会适配自动生成，也可以手写
    filename: '[Shadow].黑鹰坠落.Black.Hawk.Down.2001.1080p.AMZN.WEB-DL.H264.DDP5.1-YingWEB.torrent' 
   这里是种子文件名，所有资源的种子都要放在torrent_file文件夹里，建议直接从源站下载好，种子名字要跟资源名字相匹配
    chinesename: 黑鹰坠落     #资源中文名，用于抓豆瓣链接
    englishname: 'Black Hawk Down '  #同上，这些都会适配自动生成
    small_descr: '黑鹰坠落/黑鹰15小时/黑鹰计划/黑鹰降落 | 类型:动作 主演:乔什·哈奈特/伊万·麦克格雷格/汤姆·塞兹摩尔 [英语|内封中字]'       #副标题，也是从源站抓取自动生成
    tags: 官方 中字    #标签，同上
    sub: YingWEB    #制作组，从主标题抓取，自动生成
    type: movie   #类型，同上
    contenthead: #这里写简介头的内容，也就是感谢发布的位置
        contenttail:  #这里写简介尾的内容，适用性较少
    audio_format: DDP5.1   #音频
    video_format: H264     #视频
    medium: WEB-DL   #媒介
    source: WEB-DL   #来源
    doubanurl: https://movie.douban.com/subject/1291824/ #不写豆瓣链接则会自动抓取
    screenshot: null #如果需要自选截图，则这边直接复制图片链接即可,长度随意，注意要把basic_num数量改为0，否则默认还是会自动截图
    from_url: https://mikanani.me/
    imdb_url: null
    carpt: 0
EOF
echo "创建yaml配置模板成功，创建启动指令文件"
cd /usr/local/bin/
cat > atm << EOF
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from AutoTransferMachine.main import main
if _name_ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
EOF
chmod a+x /usr/local/bin/atm
echo "创建成功，尝试第一次启动ATM"
atm -h








